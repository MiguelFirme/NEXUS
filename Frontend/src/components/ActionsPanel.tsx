import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import RefreshRounded from "@mui/icons-material/RefreshRounded";
import AddRounded from "@mui/icons-material/AddRounded";
import PrintRounded from "@mui/icons-material/PrintRounded";

type Props = {
  onNew?: () => void;
  onRefresh?: () => void;
  onPrintRelatorio?: () => void;
  canCreate?: boolean;
};

export default function ActionsPanel({
  onNew,
  onRefresh,
  onPrintRelatorio,
  canCreate,
}: Props) {
  return (
    <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5} flexWrap="wrap" useFlexGap>
      <Button variant="outlined" size="small" startIcon={<RefreshRounded />} onClick={() => onRefresh?.()}>
        Atualizar
      </Button>
      <Button
        variant="outlined"
        size="small"
        startIcon={<PrintRounded />}
        onClick={() => onPrintRelatorio?.()}
      >
        Imprimir relatório
      </Button>
      <Box sx={{ flex: 1 }} />
      {canCreate ? (
        <Button
          variant="contained"
          startIcon={<AddRounded />}
          onClick={() => onNew?.()}
          fullWidth
          sx={{ minWidth: 180 }}
        >
          Nova pendência
        </Button>
      ) : null}
    </Stack>
  );
}
