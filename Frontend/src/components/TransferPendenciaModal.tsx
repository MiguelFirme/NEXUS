import { useEffect, useState } from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Radio from "@mui/material/Radio";
import TextField from "@mui/material/TextField";
import MenuItem from "@mui/material/MenuItem";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { getSetores, getUsuarios, transferirPendencia, getRoteiro, type RoteiroDTO } from "../services/api";
import type { Pendencia } from "../types";

type Props = {
  open: boolean;
  onClose: () => void;
  pendencia: Pendencia | null;
  onSaved?: () => void;
  /** Modo inicial (padrão: transferir por setor) */
  initialMode?: "setor" | "usuario";
  /** Se informado, fixa o setor (usado no fluxo de \"Atribuir\" dentro de um setor) */
  fixedSetorId?: number | null;
};

export default function TransferPendenciaModal({
  open,
  onClose,
  pendencia,
  onSaved,
  initialMode = "setor",
  fixedSetorId = null,
}: Props) {
  const [mode, setMode] = useState<"setor" | "usuario">(initialMode);
  const [setores, setSetores] = useState<{ id: number; nome_setor?: string }[]>([]);
  const [usuarios, setUsuarios] = useState<{ id: number; nomeUsuario?: string; idSetor?: number }[]>([]);
  const [setorId, setSetorId] = useState<number | "">("");
  const [usuarioId, setUsuarioId] = useState<number | "">("");
  const [loading, setLoading] = useState(false);
  const [roteiro, setRoteiro] = useState<RoteiroDTO | null>(null);
  const [setoresValidos, setSetoresValidos] = useState<number[]>([]);
  const [proximoPassoUsuario, setProximoPassoUsuario] = useState<number | null>(null);

  useEffect(() => {
    if (!open) return;
    
    // Carrega listas apenas quando o modal abre
    getSetores()
      .then(setSetores)
      .catch(() => setSetores([]));
    getUsuarios()
      .then(setUsuarios)
      .catch(() => setUsuarios([]));

    // Carrega roteiro se a pendência estiver em um
    if (pendencia?.idRoteiro) {
      getRoteiro(pendencia.idRoteiro)
        .then((r) => {
          setRoteiro(r);
          const passos = (r.passos ?? []).slice().sort((a, b) => a.ordem - b.ordem);
          let setoresValidosNext: number[] = [];
          let proximoUsuario: number | null = null;
          // Se a pendência está atribuída a um usuário, estamos no passo desse usuário (não no setor dele)
          const indicePorUsuario =
            pendencia.idUsuario != null
              ? passos.findIndex((p) => p.tipo === "USUARIO" && p.idUsuario === pendencia.idUsuario)
              : -1;
          const indicePorSetor =
            pendencia.idSetor != null
              ? passos.findIndex((p) => p.tipo === "SETOR" && p.idSetor === pendencia.idSetor)
              : -1;
          const indiceAtual = indicePorUsuario >= 0 ? indicePorUsuario : indicePorSetor;
          if (indiceAtual >= 0 && indiceAtual < passos.length - 1) {
            const proximo = passos[indiceAtual + 1];
            if (proximo.tipo === "SETOR" && proximo.idSetor != null) {
              setoresValidosNext = [proximo.idSetor];
            } else if (proximo.tipo === "USUARIO" && proximo.idUsuario != null) {
              proximoUsuario = proximo.idUsuario;
            }
          }
          setSetoresValidos(setoresValidosNext);
          setProximoPassoUsuario(proximoUsuario);
        })
        .catch(() => {
          setRoteiro(null);
          setSetoresValidos([]);
          setProximoPassoUsuario(null);
        });
    } else {
      setRoteiro(null);
      setSetoresValidos([]);
      setProximoPassoUsuario(null);
    }

    const baseSetor = fixedSetorId ?? pendencia?.idSetor ?? null;
    if (fixedSetorId != null && !pendencia?.idRoteiro) {
      setMode("usuario");
    } else if (pendencia?.idRoteiro) {
      setMode(initialMode);
    } else {
      setMode(initialMode);
    }
    setSetorId(baseSetor ?? "");
    setUsuarioId(pendencia?.idUsuario ?? "");
  }, [open, pendencia, initialMode, fixedSetorId]);

  useEffect(() => {
    if (!open || !pendencia?.idRoteiro || !roteiro) return;
    if (proximoPassoUsuario != null) {
      setMode("usuario");
      setUsuarioId(proximoPassoUsuario);
    } else if (setoresValidos.length > 0) {
      setMode("setor");
      setSetorId(setoresValidos[0]);
    }
  }, [open, pendencia?.idRoteiro, roteiro, proximoPassoUsuario, setoresValidos.length]);

  const handleConfirm = async () => {
    if (!pendencia) return;
    try {
      setLoading(true);

      if (mode === "setor") {
        if (!setorId || setorId === "") return;
        await transferirPendencia(pendencia.id, {
          idSetor: setorId as number,
          // Convenção: 0 remove atribuição de usuário, deixando a pendência \"no setor\"
          idUsuario: 0,
        });
      } else {
        if (!usuarioId || usuarioId === "") return;
        const user = usuarios.find((u) => u.id === usuarioId);
        await transferirPendencia(pendencia.id, {
          idUsuario: usuarioId as number,
          // Garante que o setor acompanhe o usuário, se informado
          idSetor: (user?.idSetor ?? (setorId || pendencia.idSetor)) as number,
        });
      }

      onSaved?.();
      onClose();
    } finally {
      setLoading(false);
    }
  };

  // Filtra setores: se há roteiro, mostra apenas os válidos; se há setor fixo, apenas esse
  const effectiveSetores = (() => {
    let filtered = setores;
    
    if (fixedSetorId != null) {
      filtered = filtered.filter((s) => s.id === fixedSetorId);
    } else if (roteiro && setoresValidos.length > 0) {
      // Se há roteiro, mostra apenas os setores válidos (próximo na sequência)
      filtered = filtered.filter((s) => setoresValidos.includes(s.id));
    }
    
    return filtered;
  })();

  const effectiveUsuarios = (() => {
    if (roteiro && proximoPassoUsuario != null) {
      return usuarios.filter((u) => u.id === proximoPassoUsuario);
    }
    if (fixedSetorId != null) {
      return usuarios.filter((u) => u.idSetor === fixedSetorId);
    }
    return usuarios;
  })();

  const canConfirm =
    pendencia &&
    ((mode === "setor" && setorId !== "" && setorId != null) ||
      (mode === "usuario" && usuarioId !== "" && usuarioId != null));

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{fixedSetorId != null ? "Atribuir pendência" : "Transferir pendência"}</DialogTitle>
      <DialogContent>
        {!pendencia ? (
          <Typography variant="body2" color="text.secondary">
            Nenhuma pendência selecionada.
          </Typography>
        ) : (
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}>
            {roteiro && (
              <Typography variant="body2" color="info.main" sx={{ mb: 1, p: 1, bgcolor: "info.light", borderRadius: 1 }}>
                ℹ️ Esta pendência está no roteiro "<strong>{roteiro.nome}</strong>". Siga a sequência do roteiro (próximo passo: setor ou usuário).
              </Typography>
            )}
            {fixedSetorId == null && !roteiro ? (
              <>
                <Typography variant="body2" color="text.secondary">
                  Escolha se deseja transferir a pendência para um <strong>setor</strong> (todos do setor verão e poderão
                  atribuir) ou diretamente para um <strong>usuário específico</strong>.
                </Typography>

                <FormControl component="fieldset">
                  <FormLabel component="legend">Destino</FormLabel>
                  <RadioGroup
                    row
                    value={mode}
                    onChange={(e) => setMode(e.target.value as "setor" | "usuario")}
                  >
                    <FormControlLabel value="setor" control={<Radio />} label="Setor" />
                    <FormControlLabel value="usuario" control={<Radio />} label="Usuário específico" />
                  </RadioGroup>
                </FormControl>
              </>
            ) : fixedSetorId != null && !roteiro ? (
              <Typography variant="body2" color="text.secondary">
                Atribua esta pendência a um <strong>usuário</strong> do setor selecionado.
              </Typography>
            ) : roteiro ? (
              <Typography variant="body2" color="text.secondary">
                {proximoPassoUsuario != null
                  ? <>Transfira esta pendência para o <strong>próximo passo</strong>: usuário indicado na sequência do roteiro.</>
                  : <>Transfira esta pendência para o <strong>próximo setor</strong> na sequência do roteiro.</>}
              </Typography>
            ) : null}

            {mode === "setor" && (
              <>
                {roteiro && setoresValidos.length === 0 && proximoPassoUsuario == null && (
                  <Typography variant="body2" color="warning.main" sx={{ mb: 1 }}>
                    ⚠️ Esta pendência está no último passo do roteiro "{roteiro.nome}". Não há próximo passo para transferir.
                  </Typography>
                )}
                <TextField
                  select
                  label="Setor"
                  size="small"
                  value={setorId}
                  onChange={(e) => setSetorId(e.target.value === "" ? "" : Number(e.target.value))}
                  fullWidth
                  disabled={fixedSetorId != null || (roteiro && setoresValidos.length === 0)}
                  helperText={roteiro && setoresValidos.length === 0 ? "Não há mais setores disponíveis neste roteiro" : undefined}
                >
                  {effectiveSetores.map((s) => (
                    <MenuItem key={s.id} value={s.id}>
                      {s.nome_setor ?? `Setor #${s.id}`}
                    </MenuItem>
                  ))}
                </TextField>
              </>
            )}

            {mode === "usuario" && !roteiro && (
              <TextField
                select
                label="Usuário"
                size="small"
                value={usuarioId}
                onChange={(e) => setUsuarioId(e.target.value === "" ? "" : Number(e.target.value))}
                fullWidth
              >
                {effectiveUsuarios.map((u) => (
                  <MenuItem key={u.id} value={u.id}>
                    {u.nomeUsuario ?? `Usuário #${u.id}`}{" "}
                    {u.idSetor != null ? ` (Setor ${u.idSetor})` : ""}
                  </MenuItem>
                ))}
              </TextField>
            )}
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={loading}>
          Cancelar
        </Button>
        <Button
          onClick={handleConfirm}
          variant="contained"
          disabled={!canConfirm || loading || !pendencia}
        >
          Confirmar
        </Button>
      </DialogActions>
    </Dialog>
  );
}

