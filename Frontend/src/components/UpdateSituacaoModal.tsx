import { useState, useEffect } from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import MenuItem from "@mui/material/MenuItem";
import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";
import AddTaskRounded from "@mui/icons-material/AddTaskRounded";
import { updatePendencia, getErrorMessage } from "../services/api";
import type { Pendencia } from "../types";

const SITUACOES = ["Aberta", "Em Andamento", "Finalizada"];

type Props = {
  open: boolean;
  onClose: () => void;
  pendencia: Pendencia | null;
  onSaved?: () => void;
};

export default function UpdateSituacaoModal({ open, onClose, pendencia, onSaved }: Props) {
  const [situacao, setSituacao] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (pendencia) {
      setSituacao(pendencia.situacao ?? pendencia.status ?? "Aberta");
      setError(null);
    }
  }, [pendencia, open]);

  const handleSave = async () => {
    if (!pendencia) return;
    setError(null);
    setLoading(true);
    try {
      await updatePendencia(pendencia.id, { situacao: situacao || undefined });
      onSaved?.();
      onClose();
    } catch (err: unknown) {
      setError(getErrorMessage(err) || "Erro ao atualizar");
    } finally {
      setLoading(false);
    }
  };

  if (!pendencia) return null;

  return (
    <Dialog
      open={open}
      onClose={loading ? undefined : onClose}
      fullWidth
      maxWidth="xs"
      PaperProps={{
        sx: { borderRadius: 2, boxShadow: "0 8px 32px rgba(0,0,0,0.12)" },
      }}
    >
      <DialogTitle sx={{ display: "flex", alignItems: "center", gap: 1.5, fontWeight: 600 }}>
        <Box
          sx={{
            width: 40,
            height: 40,
            borderRadius: 1.5,
            bgcolor: "primary.main",
            color: "white",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <AddTaskRounded />
        </Box>
        Atualizar situação
      </DialogTitle>
      <DialogContent dividers sx={{ pt: 2 }}>
        {error && (
          <Alert severity="error" onClose={() => setError(null)} sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        <TextField
          select
          fullWidth
          label="Situação"
          value={situacao}
          onChange={(e) => setSituacao(e.target.value)}
          disabled={loading}
        >
          {SITUACOES.map((s) => (
            <MenuItem key={s} value={s}>{s}</MenuItem>
          ))}
        </TextField>
      </DialogContent>
      <DialogActions sx={{ px: 3, py: 2, gap: 1 }}>
        <Button onClick={onClose} disabled={loading}>
          Cancelar
        </Button>
        <Button onClick={handleSave} variant="contained" disabled={loading} startIcon={loading ? <CircularProgress size={18} color="inherit" /> : undefined}>
          {loading ? "Salvando…" : "Salvar"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
