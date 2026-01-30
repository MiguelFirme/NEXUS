import { useState, useEffect } from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import MenuItem from "@mui/material/MenuItem";
import InputAdornment from "@mui/material/InputAdornment";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import ToggleButton from "@mui/material/ToggleButton";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";
import BusinessRounded from "@mui/icons-material/BusinessRounded";
import PersonRounded from "@mui/icons-material/PersonRounded";
import BoltRounded from "@mui/icons-material/BoltRounded";
import CalendarMonthRounded from "@mui/icons-material/CalendarMonthRounded";
import AssignmentRounded from "@mui/icons-material/AssignmentRounded";
import CheckCircleRounded from "@mui/icons-material/CheckCircleRounded";
import CancelRounded from "@mui/icons-material/CancelRounded";
import { createPendencia, getErrorMessage, getSetores, getUsuarios } from "../services/api";

const PRIORIDADES = [
  { value: "Baixa", label: "Baixa" },
  { value: "Média", label: "Média" },
  { value: "Alta", label: "Alta" },
];

type Props = {
  open: boolean;
  onClose: () => void;
  onCreated?: () => void;
};

export default function NewPendenciaModal({ open, onClose, onCreated }: Props) {
  const [setores, setSetores] = useState<{ id: number; nome_setor?: string }[]>([]);
  const [usuarios, setUsuarios] = useState<{ id: number; nomeUsuario?: string }[]>([]);
  const [idSetor, setIdSetor] = useState<number | "">("");
  const [idUsuario, setIdUsuario] = useState<number | "">("");
  const [prioridade, setPrioridade] = useState("Média");
  const [prazoDias, setPrazoDias] = useState("");
  const [observacoes, setObservacoes] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (open) {
      getSetores().then(setSetores).catch(() => setSetores([]));
      getUsuarios().then(setUsuarios).catch(() => setUsuarios([]));
    }
  }, [open]);

  const handleCreate = async () => {
    setError(null);
    setLoading(true);
    try {
      const numero = `PEN-${Date.now()}`;
      await createPendencia({
        numero,
        situacao: "Aberta",
        idSetor: idSetor === "" ? undefined : Number(idSetor),
        idUsuario: idUsuario === "" ? undefined : Number(idUsuario),
        prioridade: prioridade || undefined,
        prazoResposta: prazoDias === "" ? undefined : parseInt(prazoDias, 10),
        observacoes: observacoes?.trim() || undefined,
      });
      setIdSetor("");
      setIdUsuario("");
      setPrioridade("Média");
      setPrazoDias("");
      setObservacoes("");
      onCreated?.();
      onClose();
    } catch (err: unknown) {
      setError(getErrorMessage(err) || "Erro ao criar pendência");
    } finally {
      setLoading(false);
    }
  };

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
      <DialogTitle sx={{ fontWeight: 600, display: "flex", alignItems: "center", gap: 1 }}>
        Nova Pendência
      </DialogTitle>
      <DialogContent dividers sx={{ pt: 2, bgcolor: "grey.50" }}>
        {error && (
          <Alert severity="error" onClose={() => setError(null)} sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <TextField
          select
          fullWidth
          label="Setor Responsável"
          value={idSetor}
          onChange={(e) => setIdSetor(e.target.value === "" ? "" : Number(e.target.value))}
          disabled={loading}
          sx={{ mb: 2 }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <BusinessRounded sx={{ color: "action.active", fontSize: 20 }} />
              </InputAdornment>
            ),
          }}
        >
          <MenuItem value="">Nenhum</MenuItem>
          {setores.map((s) => (
            <MenuItem key={s.id} value={s.id}>
              {s.nome_setor ?? `Setor ${s.id}`}
            </MenuItem>
          ))}
        </TextField>

        <TextField
          select
          fullWidth
          label="Usuário Responsável"
          value={idUsuario}
          onChange={(e) => setIdUsuario(e.target.value === "" ? "" : Number(e.target.value))}
          disabled={loading}
          sx={{ mb: 2 }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <PersonRounded sx={{ color: "action.active", fontSize: 20 }} />
              </InputAdornment>
            ),
          }}
        >
          <MenuItem value="">Nenhum</MenuItem>
          {usuarios.map((u) => (
            <MenuItem key={u.id} value={u.id}>
              {u.nomeUsuario ?? `Usuário ${u.id}`}
            </MenuItem>
          ))}
        </TextField>

        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1, display: "flex", alignItems: "center", gap: 0.5 }}>
            <BoltRounded sx={{ fontSize: 18 }} />
            Prioridade
          </Typography>
          <ToggleButtonGroup
            value={prioridade}
            exclusive
            onChange={(_, v) => v != null && setPrioridade(v)}
            disabled={loading}
            fullWidth
            size="small"
            sx={{ flexWrap: "wrap" }}
          >
            {PRIORIDADES.map((p) => (
              <ToggleButton key={p.value} value={p.value} sx={{ flex: 1, minWidth: 80 }}>
                {p.label}
              </ToggleButton>
            ))}
          </ToggleButtonGroup>
        </Box>

        <TextField
          fullWidth
          label="Prazo para Resolução (dias)"
          type="number"
          inputProps={{ min: 0 }}
          value={prazoDias}
          onChange={(e) => setPrazoDias(e.target.value)}
          disabled={loading}
          sx={{ mb: 2 }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <CalendarMonthRounded sx={{ color: "action.active", fontSize: 20 }} />
              </InputAdornment>
            ),
          }}
        />

        <TextField
          fullWidth
          label="Observações"
          multiline
          rows={4}
          value={observacoes}
          onChange={(e) => setObservacoes(e.target.value)}
          disabled={loading}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start" sx={{ alignSelf: "flex-start", mt: 1 }}>
                <AssignmentRounded sx={{ color: "action.active", fontSize: 20 }} />
              </InputAdornment>
            ),
          }}
        />
      </DialogContent>
      <DialogActions sx={{ px: 3, py: 2, gap: 1 }}>
        <Button
          onClick={onClose}
          disabled={loading}
          startIcon={<CancelRounded />}
          sx={{ bgcolor: "error.main", color: "white", "&:hover": { bgcolor: "error.dark" } }}
        >
          Cancelar
        </Button>
        <Button
          onClick={handleCreate}
          variant="contained"
          disabled={loading}
          startIcon={loading ? <CircularProgress size={18} color="inherit" /> : <CheckCircleRounded />}
          sx={{ bgcolor: "success.main", "&:hover": { bgcolor: "success.dark" } }}
        >
          {loading ? "Registrando…" : "Registrar"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
