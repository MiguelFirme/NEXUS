import { useState, useEffect, useMemo } from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import MenuItem from "@mui/material/MenuItem";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import InputAdornment from "@mui/material/InputAdornment";
import Popover from "@mui/material/Popover";
import Typography from "@mui/material/Typography";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";
import EditRounded from "@mui/icons-material/EditRounded";
import CalendarMonthRounded from "@mui/icons-material/CalendarMonthRounded";
import { Calendar } from "react-date-range";
import { ptBR } from "date-fns/locale";
import { updatePendencia, deletePendencia, getErrorMessage } from "../services/api";
import type { Pendencia } from "../types";

type Props = {
  open: boolean;
  onClose: () => void;
  pendencia: Pendencia | null;
  onSaved?: () => void;
  /** Nível do usuário logado (para habilitar exclusão apenas para nível >= 3) */
  currentUserLevel?: number;
  /** Chamado quando a pendência for excluída com sucesso */
  onDeleted?: () => void;
};

const SITUACOES = ["Aberta", "Em Andamento", "Finalizada"];

export default function EditPendenciaModal({
  open,
  onClose,
  pendencia,
  onSaved,
  currentUserLevel,
  onDeleted,
}: Props) {
  const [equipamento, setEquipamento] = useState("");
  const [observacoes, setObservacoes] = useState("");
  const [situacao, setSituacao] = useState("");
  const [prazoDias, setPrazoDias] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [calendarAnchor, setCalendarAnchor] = useState<HTMLElement | null>(null);
  const [prazoData, setPrazoData] = useState<Date | null>(null);

  const dataCriacaoDate = useMemo(() => {
    if (!pendencia?.dataCriacao) return null;
    const d = new Date(pendencia.dataCriacao);
    return new Date(d.getFullYear(), d.getMonth(), d.getDate());
  }, [pendencia?.dataCriacao]);

  useEffect(() => {
    if (pendencia) {
      setEquipamento(pendencia.equipamento ?? pendencia.titulo ?? "");
      setObservacoes(pendencia.observacoes ?? pendencia.descricao ?? "");
      setSituacao(pendencia.situacao ?? pendencia.status ?? "Aberta");
      setPrazoDias(pendencia.prazoResposta != null ? String(pendencia.prazoResposta) : "");
      setError(null);
      const dc = pendencia.dataCriacao ? new Date(pendencia.dataCriacao) : new Date();
      const days = pendencia.prazoResposta ?? 0;
      const limit = new Date(dc.getFullYear(), dc.getMonth(), dc.getDate());
      limit.setDate(limit.getDate() + days);
      setPrazoData(limit);
    }
  }, [pendencia, open]);

  const openCalendar = (e: React.MouseEvent<HTMLElement>) => {
    setCalendarAnchor(e.currentTarget);
  };

  const handleSave = async () => {
    if (!pendencia) return;
    setError(null);
    setLoading(true);
    try {
      const prazo = prazoDias.trim() === "" ? undefined : parseInt(prazoDias, 10);
      if (prazo !== undefined && (Number.isNaN(prazo) || prazo < 0)) {
        setError("Prazo deve ser um número de dias válido (≥ 0).");
        setLoading(false);
        return;
      }
      await updatePendencia(pendencia.id, {
        equipamento: equipamento || undefined,
        observacoes: observacoes || undefined,
        situacao: situacao || undefined,
        ...(typeof prazo === "number" && prazo >= 0 && { prazoResposta: prazo }),
      });
      onSaved?.();
      onClose();
    } catch (err: unknown) {
      setError(getErrorMessage(err) || "Erro ao salvar");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!pendencia) return;
    if (!confirm("Tem certeza que deseja excluir esta pendência? Esta ação não pode ser desfeita.")) {
      return;
    }
    setError(null);
    setLoading(true);
    try {
      await deletePendencia(pendencia.id);
      onDeleted?.();
      onClose();
    } catch (err: unknown) {
      setError(getErrorMessage(err) || "Erro ao excluir pendência");
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
          select
          fullWidth
          label="Situação"
          value={situacao}
          onChange={(e) => setSituacao(e.target.value)}
          disabled={loading}
          sx={{ mb: 2 }}
        >
          {SITUACOES.map((s) => (
            <MenuItem key={s} value={s}>{s}</MenuItem>
          ))}
        </TextField>
        <TextField
          fullWidth
          type="number"
          inputProps={{ min: 0, step: 1 }}
          label="Prazo (dias)"
          placeholder="Ex: 5"
          value={prazoDias}
          onChange={(e) => setPrazoDias(e.target.value)}
          disabled={loading}
          helperText="Deixe vazio para não alterar o prazo. Use o calendário para escolher o dia do prazo."
          sx={{ mb: 2 }}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  aria-label="Abrir calendário para selecionar data do prazo"
                  onClick={openCalendar}
                  disabled={loading || !pendencia?.dataCriacao}
                  edge="end"
                  size="small"
                >
                  <CalendarMonthRounded />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
        <Popover
          open={Boolean(calendarAnchor)}
          anchorEl={calendarAnchor}
          onClose={() => setCalendarAnchor(null)}
          anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
          transformOrigin={{ vertical: "top", horizontal: "right" }}
          slotProps={{ paper: { sx: { borderRadius: 2, overflow: "hidden", mt: 1 } } }}
        >
          <Calendar
            locale={ptBR}
            date={prazoData ?? dataCriacaoDate ?? new Date()}
            minDate={dataCriacaoDate ?? undefined}
            onChange={(date: Date) => {
              setPrazoData(date);
              if (!dataCriacaoDate) return;
              const selected = new Date(date.getFullYear(), date.getMonth(), date.getDate());
              const diffMs = selected.getTime() - dataCriacaoDate.getTime();
              const diffDays = Math.max(0, Math.round(diffMs / (24 * 60 * 60 * 1000)));
              setPrazoDias(String(diffDays));
              setCalendarAnchor(null);
            }}
          />
        </Popover>
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
      <DialogActions sx={{ px: 3, py: 2, gap: 1, justifyContent: "space-between" }}>
        <Box sx={{ display: "flex", gap: 1 }}>
          {currentUserLevel != null && currentUserLevel >= 3 && (
            <Button
              color="error"
              variant="outlined"
              onClick={handleDelete}
              disabled={loading}
            >
              Excluir pendência
            </Button>
          )}
        </Box>
        <Box sx={{ display: "flex", gap: 1 }}>
          <Button onClick={onClose} disabled={loading}>
            Cancelar
          </Button>
          <Button
            onClick={handleSave}
            variant="contained"
            disabled={loading}
            startIcon={loading ? <CircularProgress size={18} color="inherit" /> : undefined}
          >
            {loading ? "Salvando…" : "Salvar"}
          </Button>
        </Box>
      </DialogActions>
    </Dialog>
  );
}
