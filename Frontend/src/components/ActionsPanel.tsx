import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import RefreshRounded from "@mui/icons-material/RefreshRounded";
import EditRounded from "@mui/icons-material/EditRounded";
import SwapHorizRounded from "@mui/icons-material/SwapHorizRounded";
import AddTaskRounded from "@mui/icons-material/AddTaskRounded";
import AddRounded from "@mui/icons-material/AddRounded";
import DeleteOutline from "@mui/icons-material/DeleteOutline";
import type { Pendencia } from "../types";

type Props = {
  onNew?: () => void;
  onRefresh?: () => void;
  onEdit?: (p: Pendencia) => void;
  onUpdateSituacao?: (p: Pendencia) => void;
  onTransferir?: (p: Pendencia) => void;
  onDelete?: (p: Pendencia) => void;
  selected?: Pendencia | null;
  canCreate?: boolean;
  canDelete?: boolean;
};

export default function ActionsPanel({
  onNew,
  onRefresh,
  onEdit,
  onUpdateSituacao,
  onTransferir,
  onDelete,
  selected,
  canCreate,
  canDelete,
}: Props) {
  return (
    <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5} flexWrap="wrap" useFlexGap>
      <Button variant="outlined" size="small" startIcon={<RefreshRounded />} onClick={() => onRefresh?.()}>
        Atualizar
      </Button>
      <Button
        variant="outlined"
        size="small"
        startIcon={<EditRounded />}
        disabled={!selected}
        onClick={() => selected && onEdit?.(selected)}
      >
        Editar
      </Button>
      <Button
        variant="outlined"
        size="small"
        startIcon={<AddTaskRounded />}
        disabled={!selected}
        onClick={() => selected && onUpdateSituacao?.(selected)}
      >
        Atualizar situação
      </Button>
      <Button
        variant="outlined"
        size="small"
        startIcon={<SwapHorizRounded />}
        disabled={!selected}
        onClick={() => selected && onTransferir?.(selected)}
      >
        Transferir
      </Button>
      <Box sx={{ flex: 1 }} />
      <Button
        variant="outlined"
        size="small"
        color="error"
        startIcon={<DeleteOutline />}
        disabled={!selected || !canDelete}
        onClick={() => selected && onDelete?.(selected)}
      >
        Remover
      </Button>
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
