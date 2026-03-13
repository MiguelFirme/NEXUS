import { useState, useEffect, useRef } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import MenuItem from "@mui/material/MenuItem";
import Button from "@mui/material/Button";
import FilterListRounded from "@mui/icons-material/FilterListRounded";
import Popover from "@mui/material/Popover";
import dayjs from "dayjs";
import { DateRange, Range, RangeKeyDict } from "react-date-range";
import { ptBR } from "date-fns/locale";
import "react-date-range/dist/styles.css";
import "react-date-range/dist/theme/default.css";
import { getUsuarios } from "../services/api";

export type FiltersPayload = {
  periodStart?: string;
  periodEnd?: string;
  status?: string;
  prioridade?: string;
  usuarioId?: number;
  numeroPesquisa?: string;
};

type Props = {
  onApply?: (filters?: FiltersPayload) => void | Promise<void>;
  /** Se true, mostra o filtro de usuário (apenas para nível 4+) */
  showUsuarioFilter?: boolean;
};

export default function Filters({ onApply, showUsuarioFilter = false }: Props) {
  const [periodRange, setPeriodRange] = useState<Range>({
    startDate: null,
    endDate: null,
    key: "selection",
  });
  const [periodLabel, setPeriodLabel] = useState<string>("");
  const [periodOpen, setPeriodOpen] = useState(false);
  const periodAnchorRef = useRef<HTMLDivElement | null>(null);
  const [status, setStatus] = useState<string>("Todas");
  const [prioridade, setPrioridade] = useState<string>("Todas");
  const [usuarioId, setUsuarioId] = useState<number | "">("");
  const [numeroPesquisa, setNumeroPesquisa] = useState<string>("");
  const [usuarios, setUsuarios] = useState<{ id: number; nomeUsuario?: string }[]>([]);

  useEffect(() => {
    if (showUsuarioFilter) {
      getUsuarios()
        .then(setUsuarios)
        .catch(() => setUsuarios([]));
    }
  }, [showUsuarioFilter]);

  const apply = () => {
    const start = periodRange.startDate;
    const end = periodRange.endDate;
    const periodStart = start ? dayjs(start).format("YYYY-MM-DD") : undefined;
    const periodEnd = end ? dayjs(end).format("YYYY-MM-DD") : undefined;

    onApply?.({
      periodStart,
      periodEnd,
      status,
      prioridade,
      usuarioId: usuarioId === "" ? undefined : usuarioId,
      numeroPesquisa: numeroPesquisa.trim() || undefined,
    });
  };

  return (
    <Box
      sx={{
        display: "flex",
        gap: 2,
        alignItems: "center",
        flexWrap: "wrap",
      }}
    >
      <TextField
        label="Número da pendência"
        placeholder="Ex: 430952"
        size="small"
        value={numeroPesquisa}
        onChange={(e) => setNumeroPesquisa(e.target.value)}
        sx={{ minWidth: 160 }}
      />
      <Box ref={periodAnchorRef}>
        <TextField
          label="Por período"
          size="small"
          value={periodLabel}
          onClick={() => setPeriodOpen(true)}
          sx={{ minWidth: 260 }}
          InputProps={{ readOnly: true }}
          placeholder="Selecione o período"
        />
      </Box>
      <Popover
        open={periodOpen}
        onClose={() => setPeriodOpen(false)}
        anchorEl={periodAnchorRef.current}
        anchorOrigin={{ vertical: "bottom", horizontal: "left" }}
      >
        <DateRange
          ranges={[periodRange]}
          locale={ptBR}
          weekdayDisplayFormat="EEEEE"
          onChange={(item: RangeKeyDict) => {
            const selection = item.selection;
            setPeriodRange(selection);

            const start = selection.startDate;
            const end = selection.endDate;

            if (start && end) {
              const startLabel = dayjs(start).format("DD/MM/YYYY");
              const endLabel = dayjs(end).format("DD/MM/YYYY");
              setPeriodLabel(`${startLabel} - ${endLabel}`);
            } else if (start) {
              const startLabel = dayjs(start).format("DD/MM/YYYY");
              setPeriodLabel(startLabel);
            } else {
              setPeriodLabel("");
            }
          }}
          moveRangeOnFirstSelection={false}
          rangeColors={["#1976d2"]}
        />
      </Popover>
      <TextField
        select
        label="Por status"
        size="small"
        value={status}
        onChange={(e) => setStatus(e.target.value)}
        sx={{ minWidth: 220 }}
      >
        <MenuItem value="Todas">Todos os status</MenuItem>
        <MenuItem value="Aberta">Aberta</MenuItem>
        <MenuItem value="Em Andamento">Em Andamento</MenuItem>
        <MenuItem value="Finalizada">Finalizada</MenuItem>
      </TextField>
      <TextField
        select
        label="Por prioridade"
        size="small"
        value={prioridade}
        onChange={(e) => setPrioridade(e.target.value)}
        sx={{ minWidth: 220 }}
      >
        <MenuItem value="Todas">Todas as prioridades</MenuItem>
        <MenuItem value="Alta">Alta</MenuItem>
        <MenuItem value="Média">Média</MenuItem>
        <MenuItem value="Baixa">Baixa</MenuItem>
      </TextField>

      {showUsuarioFilter && (
        <TextField
          select
          label="Por usuário"
          size="small"
          value={usuarioId}
          onChange={(e) => setUsuarioId(e.target.value === "" ? "" : Number(e.target.value))}
          sx={{ minWidth: 220 }}
        >
          <MenuItem value="">Todos os usuários</MenuItem>
          {usuarios.map((u) => (
            <MenuItem key={u.id} value={u.id}>
              {u.nomeUsuario ?? `Usuário #${u.id}`}
            </MenuItem>
          ))}
        </TextField>
      )}

      <Box sx={{ flex: 1 }} />

      <Button
        variant="contained"
        onClick={apply}
        startIcon={<FilterListRounded />}
        sx={{ px: 2.5 }}
      >
        Aplicar filtros
      </Button>
    </Box>
  );
}
