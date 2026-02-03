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
import { getSetores, getUsuarios, transferirPendencia } from "../services/api";
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

  useEffect(() => {
    if (!open) return;
    // Carrega listas apenas quando o modal abre
    getSetores()
      .then(setSetores)
      .catch(() => setSetores([]));
    getUsuarios()
      .then(setUsuarios)
      .catch(() => setUsuarios([]));

    // Define estado inicial
    setMode(initialMode);
    const baseSetor = fixedSetorId ?? pendencia?.idSetor ?? null;
    setSetorId(baseSetor ?? "");
    setUsuarioId(pendencia?.idUsuario ?? "");
  }, [open, pendencia, initialMode, fixedSetorId]);

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

  const effectiveSetores =
    fixedSetorId != null ? setores.filter((s) => s.id === fixedSetorId) : setores;

  const canConfirm =
    pendencia &&
    ((mode === "setor" && setorId !== "" && setorId != null) ||
      (mode === "usuario" && usuarioId !== "" && usuarioId != null));

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Transferir pendência</DialogTitle>
      <DialogContent>
        {!pendencia ? (
          <Typography variant="body2" color="text.secondary">
            Nenhuma pendência selecionada.
          </Typography>
        ) : (
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}>
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
                {usuarios.map((u) => (
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

