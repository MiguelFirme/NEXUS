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

type PassoDestino = {
  tipo: "SETOR" | "USUARIO";
  idSetor?: number;
  idUsuario?: number;
  label: string;
  ordem?: number;
};

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
  const [nextStep, setNextStep] = useState<PassoDestino | null>(null);
  const [previousSteps, setPreviousSteps] = useState<PassoDestino[]>([]);
  const [selectedPassoAnterior, setSelectedPassoAnterior] = useState<PassoDestino | null>(null);
  const [setoresValidos, setSetoresValidos] = useState<number[]>([]);
  const [usuariosValidosRoteiro, setUsuariosValidosRoteiro] = useState<number[]>([]);
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
          const indicePorUsuario =
            pendencia.idUsuario != null
              ? passos.findIndex((p) => p.tipo === "USUARIO" && p.idUsuario === pendencia.idUsuario)
              : -1;
          const indicePorSetor =
            pendencia.idSetor != null
              ? passos.findIndex((p) => p.tipo === "SETOR" && p.idSetor === pendencia.idSetor)
              : -1;
          const indiceAtual = indicePorUsuario >= 0 ? indicePorUsuario : indicePorSetor;
          const setoresNext: number[] = [];
          const usuariosNext: number[] = [];
          let proximoUsuario: number | null = null;
          let next: PassoDestino | null = null;
          const anteriores: PassoDestino[] = [];
          if (indiceAtual >= 0) {
            for (let i = 0; i < passos.length; i++) {
              if (i === indiceAtual) continue;
              if (i > indiceAtual + 1) break;
              const p = passos[i];
              const label = p.tipo === "SETOR" ? (p.nomeSetor ?? `Setor #${p.idSetor}`) : (p.nomeUsuario ?? `Usuário #${p.idUsuario}`);
              const passo: PassoDestino = {
                tipo: p.tipo,
                idSetor: p.idSetor ?? undefined,
                idUsuario: p.idUsuario ?? undefined,
                label: `Passo ${p.ordem} - ${label}`,
                ordem: p.ordem,
              };
              if (i < indiceAtual) anteriores.push(passo);
              else if (i === indiceAtual + 1) next = passo;
              if (p.tipo === "SETOR" && p.idSetor != null) setoresNext.push(p.idSetor);
              if (p.tipo === "USUARIO" && p.idUsuario != null) {
                usuariosNext.push(p.idUsuario);
                if (i === indiceAtual + 1) proximoUsuario = p.idUsuario;
              }
            }
          }
          setNextStep(next);
          setPreviousSteps(anteriores);
          setSelectedPassoAnterior(anteriores.length > 0 ? anteriores[0] : null);
          setSetoresValidos(setoresNext);
          setUsuariosValidosRoteiro(usuariosNext);
          setProximoPassoUsuario(proximoUsuario);
        })
        .catch(() => {
          setRoteiro(null);
          setNextStep(null);
          setPreviousSteps([]);
          setSetoresValidos([]);
          setUsuariosValidosRoteiro([]);
          setProximoPassoUsuario(null);
        });
    } else {
      setRoteiro(null);
      setNextStep(null);
      setPreviousSteps([]);
      setSetoresValidos([]);
      setUsuariosValidosRoteiro([]);
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
    if (proximoPassoUsuario != null && usuariosValidosRoteiro.length > 0) {
      setMode("usuario");
      setUsuarioId(proximoPassoUsuario);
    } else if (setoresValidos.length > 0) {
      setMode("setor");
      setSetorId(setoresValidos[0]);
    } else if (usuariosValidosRoteiro.length > 0) {
      setMode("usuario");
      setUsuarioId(usuariosValidosRoteiro[0]);
    }
  }, [open, pendencia?.idRoteiro, roteiro, proximoPassoUsuario, setoresValidos.length, usuariosValidosRoteiro.length]);

  const transferirParaPasso = async (passo: PassoDestino) => {
    if (!pendencia) return;
    if (passo.tipo === "SETOR" && passo.idSetor != null) {
      await transferirPendencia(pendencia.id, { idSetor: passo.idSetor, idUsuario: 0 });
    } else if (passo.tipo === "USUARIO" && passo.idUsuario != null) {
      const user = usuarios.find((u) => u.id === passo.idUsuario);
      await transferirPendencia(pendencia.id, {
        idUsuario: passo.idUsuario,
        idSetor: (user?.idSetor ?? pendencia.idSetor) as number,
      });
    }
  };

  const handleProximo = async () => {
    if (!pendencia || !nextStep) return;
    try {
      setLoading(true);
      await transferirParaPasso(nextStep);
      onSaved?.();
      onClose();
    } finally {
      setLoading(false);
    }
  };

  const handleAnterior = async () => {
    if (!pendencia || !selectedPassoAnterior) return;
    try {
      setLoading(true);
      await transferirParaPasso(selectedPassoAnterior);
      onSaved?.();
      onClose();
    } finally {
      setLoading(false);
    }
  };

  const handleConfirm = async () => {
    if (!pendencia) return;
    try {
      setLoading(true);

      if (mode === "setor") {
        if (!setorId || setorId === "") return;
        await transferirPendencia(pendencia.id, {
          idSetor: setorId as number,
          idUsuario: 0,
        });
      } else {
        if (!usuarioId || usuarioId === "") return;
        const user = usuarios.find((u) => u.id === usuarioId);
        await transferirPendencia(pendencia.id, {
          idUsuario: usuarioId as number,
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
    if (roteiro && usuariosValidosRoteiro.length > 0) {
      return usuarios.filter((u) => usuariosValidosRoteiro.includes(u.id));
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
                ℹ️ Esta pendência está no roteiro "<strong>{roteiro.nome}</strong>". Use <strong>Próximo</strong> para avançar ou <strong>Anterior</strong> para voltar a um passo já percorrido.
              </Typography>
            )}

            {roteiro ? (
              <Box sx={{ display: "flex", flexDirection: "column", gap: 2.5 }}>
                {nextStep ? (
                  <Box sx={{ p: 1.5, bgcolor: "action.hover", borderRadius: 1 }}>
                    <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 0.5 }}>
                      Próximo passo
                    </Typography>
                    <Typography variant="body1" fontWeight={500} sx={{ mb: 1 }}>
                      {nextStep.label.replace(/^Passo \d+ - /, "")}
                    </Typography>
                    <Button variant="contained" onClick={handleProximo} disabled={loading} fullWidth>
                      Próximo
                    </Button>
                  </Box>
                ) : (
                  roteiro && previousSteps.length === 0 && (
                    <Typography variant="body2" color="text.secondary">
                      Esta pendência está no último passo do roteiro. Não há próximo passo.
                    </Typography>
                  )
                )}
                {previousSteps.length > 0 && (
                  <Box sx={{ p: 1.5, bgcolor: "grey.100", borderRadius: 1 }}>
                    <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
                      Voltar para passo anterior
                    </Typography>
                    <TextField
                      select
                      size="small"
                      value={selectedPassoAnterior?.label ?? ""}
                      onChange={(e) => {
                        const p = previousSteps.find((x) => x.label === e.target.value);
                        setSelectedPassoAnterior(p ?? null);
                      }}
                      fullWidth
                      sx={{ mb: 1 }}
                    >
                      {previousSteps.map((p) => (
                        <MenuItem key={p.label} value={p.label}>
                          {p.label}
                        </MenuItem>
                      ))}
                    </TextField>
                    <Button variant="outlined" onClick={handleAnterior} disabled={loading || !selectedPassoAnterior} fullWidth>
                      Anterior
                    </Button>
                  </Box>
                )}
              </Box>
            ) : (
              <>
                {fixedSetorId == null ? (
                  <>
                    <Typography variant="body2" color="text.secondary">
                      Escolha se deseja transferir para um <strong>setor</strong> ou para um <strong>usuário específico</strong>.
                    </Typography>
                    <FormControl component="fieldset">
                      <FormLabel component="legend">Destino</FormLabel>
                      <RadioGroup row value={mode} onChange={(e) => setMode(e.target.value as "setor" | "usuario")}>
                        <FormControlLabel value="setor" control={<Radio />} label="Setor" />
                        <FormControlLabel value="usuario" control={<Radio />} label="Usuário específico" />
                      </RadioGroup>
                    </FormControl>
                  </>
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    Atribua esta pendência a um <strong>usuário</strong> do setor selecionado.
                  </Typography>
                )}
                {mode === "setor" && (
                  <TextField
                    select
                    label="Setor"
                    size="small"
                    value={setorId}
                    onChange={(e) => setSetorId(e.target.value === "" ? "" : Number(e.target.value))}
                    fullWidth
                    disabled={fixedSetorId != null}
                  >
                    {effectiveSetores.map((s) => (
                      <MenuItem key={s.id} value={s.id}>
                        {s.nome_setor ?? `Setor #${s.id}`}
                      </MenuItem>
                    ))}
                  </TextField>
                )}
                {mode === "usuario" && (
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
                        {u.nomeUsuario ?? `Usuário #${u.id}`}
                        {u.idSetor != null ? ` (Setor ${u.idSetor})` : ""}
                      </MenuItem>
                    ))}
                  </TextField>
                )}
              </>
            )}
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={loading}>
          Cancelar
        </Button>
        {!roteiro && (
          <Button
            onClick={handleConfirm}
            variant="contained"
            disabled={!canConfirm || loading || !pendencia}
          >
            Confirmar
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
}

