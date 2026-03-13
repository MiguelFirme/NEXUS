import { useState, useEffect, useRef } from "react";
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
import Popover from "@mui/material/Popover";
import BusinessRounded from "@mui/icons-material/BusinessRounded";
import PersonRounded from "@mui/icons-material/PersonRounded";
import BoltRounded from "@mui/icons-material/BoltRounded";
import CalendarMonthRounded from "@mui/icons-material/CalendarMonthRounded";
import AssignmentRounded from "@mui/icons-material/AssignmentRounded";
import CheckCircleRounded from "@mui/icons-material/CheckCircleRounded";
import CancelRounded from "@mui/icons-material/CancelRounded";
import { createPendencia, getErrorMessage, getSetores, getUsuarios, getRoteirosAtivos, type RoteiroDTO } from "../services/api";
import { Calendar } from "react-date-range";
import { ptBR } from "date-fns/locale";

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
  const [roteiros, setRoteiros] = useState<RoteiroDTO[]>([]);
  const [idSetor, setIdSetor] = useState<number | "">("");
  const [idUsuario, setIdUsuario] = useState<number | "">("");
  const [idRoteiro, setIdRoteiro] = useState<number | "">("");
  const [prioridade, setPrioridade] = useState("Média");
  const [prazoDias, setPrazoDias] = useState("");
  const [prazoData, setPrazoData] = useState<Date | null>(null);
  const [observacoes, setObservacoes] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const prazoAnchorRef = useRef<HTMLDivElement | null>(null);
  const [prazoCalendarOpen, setPrazoCalendarOpen] = useState(false);

  useEffect(() => {
    if (open) {
      getSetores().then(setSetores).catch(() => setSetores([]));
      getUsuarios().then(setUsuarios).catch(() => setUsuarios([]));
      getRoteirosAtivos().then(setRoteiros).catch(() => setRoteiros([]));
    }
  }, [open]);

  useEffect(() => {
    if (!open) return;

    if (prioridade === "Baixa") {
      setPrazoDias("14");
    } else if (prioridade === "Média") {
      setPrazoDias("7");
    } else if (prioridade === "Alta") {
      setPrazoDias("3");
    }
  }, [open, prioridade]);

  const handleCreate = async () => {
    setError(null);
    setLoading(true);
    try {
      // Número é gerado no backend em ordem crescente (1, 2, 3, ...)
      await createPendencia({
        situacao: "Aberta",
        idSetor: idSetor === "" ? undefined : Number(idSetor),
        idUsuario: idUsuario === "" ? undefined : Number(idUsuario),
        idRoteiro: idRoteiro === "" ? undefined : Number(idRoteiro),
        prioridade: prioridade || undefined,
        prazoResposta: prazoDias === "" ? undefined : parseInt(prazoDias, 10),
        observacoes: observacoes?.trim() || undefined,
      });
      setIdSetor("");
      setIdUsuario("");
      setIdRoteiro("");
      setPrioridade("Média");
      setPrazoDias("");
      setPrazoData(null);
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

        <TextField
          select
          fullWidth
          label="Roteiro (opcional)"
          value={idRoteiro}
          onChange={(e) => setIdRoteiro(e.target.value === "" ? "" : Number(e.target.value))}
          disabled={loading}
          sx={{ mb: 2 }}
          helperText="Selecione um roteiro para que a pendência siga uma sequência de setores"
        >
          <MenuItem value="">Nenhum</MenuItem>
          {roteiros.map((r) => (
            <MenuItem key={r.id} value={r.id}>
              {r.nome} {r.passos && r.passos.length > 0 && `(${r.passos.length} passos)`}
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

        <Box ref={prazoAnchorRef} sx={{ mb: 2 }}>
          <TextField
            fullWidth
            label="Prazo para Resolução (dias)"
            type="number"
            inputProps={{ min: 0 }}
            value={prazoDias}
            onChange={(e) => setPrazoDias(e.target.value)}
            disabled={loading}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <CalendarMonthRounded
                    sx={{ color: "action.active", fontSize: 20, cursor: "pointer" }}
                    onClick={() => !loading && setPrazoCalendarOpen(true)}
                  />
                </InputAdornment>
              ),
            }}
          />
          <Popover
            open={prazoCalendarOpen}
            onClose={() => setPrazoCalendarOpen(false)}
            anchorEl={prazoAnchorRef.current}
            anchorOrigin={{ vertical: "bottom", horizontal: "left" }}
          >
            <Calendar
              locale={ptBR}
              date={prazoData ?? new Date()}
              onChange={(date: Date) => {
                setPrazoData(date);
                const today = new Date();
                const startOfToday = new Date(today.getFullYear(), today.getMonth(), today.getDate());
                const startOfSelected = new Date(date.getFullYear(), date.getMonth(), date.getDate());
                const diffMs = startOfSelected.getTime() - startOfToday.getTime();
                const diffDays = Math.max(0, Math.ceil(diffMs / (1000 * 60 * 60 * 24)));
                setPrazoDias(diffDays.toString());
              }}
            />
          </Popover>
        </Box>

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
