import { useState } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import MenuItem from "@mui/material/MenuItem";
import Button from "@mui/material/Button";
import FilterListRounded from "@mui/icons-material/FilterListRounded";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";

type Props = {
  onApply?: (filters?: unknown) => void;
};

export default function Filters({ onApply }: Props) {
  const [periodStart, setPeriodStart] = useState<string>("");
  const [periodEnd, setPeriodEnd] = useState<string>("");
  const [status, setStatus] = useState<string>("Todas");
  const [prioridade, setPrioridade] = useState<string>("Todas");
  const [statusExcept, setStatusExcept] = useState<boolean>(false);
  const [prioridadeExcept, setPrioridadeExcept] = useState<boolean>(false);

  const apply = () => {
    onApply?.({ periodStart, periodEnd, status, statusExcept, prioridade, prioridadeExcept });
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
        label="Período início"
        type="date"
        size="small"
        value={periodStart}
        onChange={(e) => setPeriodStart(e.target.value)}
        InputLabelProps={{ shrink: true }}
        sx={{ minWidth: 160 }}
      />
      <TextField
        label="Período fim"
        type="date"
        size="small"
        value={periodEnd}
        onChange={(e) => setPeriodEnd(e.target.value)}
        InputLabelProps={{ shrink: true }}
        sx={{ minWidth: 160 }}
      />
      <TextField
        select
        label="Status"
        size="small"
        value={status}
        onChange={(e) => setStatus(e.target.value)}
        sx={{ minWidth: 180 }}
      >
        <MenuItem value="Todas">Todas</MenuItem>
        <MenuItem value="Aberta">Aberta</MenuItem>
        <MenuItem value="Em Andamento">Em Andamento</MenuItem>
        <MenuItem value="Finalizada">Finalizada</MenuItem>
      </TextField>
      <FormControlLabel
        control={<Checkbox size="small" checked={statusExcept} onChange={(e) => setStatusExcept(e.target.checked)} />}
        label="Exceto"
        sx={{ ml: 0 }}
      />
      <TextField
        select
        label="Prioridade"
        size="small"
        value={prioridade}
        onChange={(e) => setPrioridade(e.target.value)}
        sx={{ minWidth: 180 }}
      >
        <MenuItem value="Todas">Todas</MenuItem>
        <MenuItem value="Alta">Alta</MenuItem>
        <MenuItem value="Média">Média</MenuItem>
        <MenuItem value="Baixa">Baixa</MenuItem>
      </TextField>
      <FormControlLabel
        control={<Checkbox size="small" checked={prioridadeExcept} onChange={(e) => setPrioridadeExcept(e.target.checked)} />}
        label="Exceto"
        sx={{ ml: 0 }}
      />

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
