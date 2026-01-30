import { useState, useEffect } from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";
import EditRounded from "@mui/icons-material/EditRounded";
import { updatePendencia, getErrorMessage } from "../services/api";
import type { Pendencia } from "../types";

type Props = {
  open: boolean;
  onClose: () => void;
  pendencia: Pendencia | null;
  onSaved?: () => void;
};

export default function EditPendenciaModal({ open, onClose, pendencia, onSaved }: Props) {
  const [equipamento, setEquipamento] = useState("");
  const [observacoes, setObservacoes] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (pendencia) {
      setEquipamento(pendencia.equipamento ?? pendencia.titulo ?? "");
      setObservacoes(pendencia.observacoes ?? pendencia.descricao ?? "");
      setError(null);
    }
  }, [pendencia, open]);

  const handleSave = async () => {
    if (!pendencia) return;
    setError(null);
    setLoading(true);
    try {
      await updatePendencia(pendencia.id, { equipamento: equipamento || undefined, observacoes: observacoes || undefined });
      onSaved?.();
      onClose();
    } catch (err: unknown) {
      setError(getErrorMessage(err) || "Erro ao salvar");
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
      maxWidth="sm"
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
          <EditRounded />
        </Box>
        Editar pendência
      </DialogTitle>
      <DialogContent dividers sx={{ pt: 2 }}>
        {error && (
          <Alert severity="error" onClose={() => setError(null)} sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        <TextField
          fullWidth
          label="Equipamento / Título"
          value={equipamento}
          onChange={(e) => setEquipamento(e.target.value)}
          disabled={loading}
          sx={{ mb: 2 }}
        />
        <TextField
          fullWidth
          label="Observações / Descrição"
          multiline
          rows={4}
          value={observacoes}
          onChange={(e) => setObservacoes(e.target.value)}
          disabled={loading}
        />
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
