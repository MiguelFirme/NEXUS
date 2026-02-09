import { useState, useMemo } from "react";
import Table from "@mui/material/Table";
import TableHead from "@mui/material/TableHead";
import TableBody from "@mui/material/TableBody";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableSortLabel from "@mui/material/TableSortLabel";
import Chip from "@mui/material/Chip";
import type { Pendencia } from "../types";

type Props = {
  pendencias: Pendencia[];
  onSelect?: (p: Pendencia) => void;
};

function StatusChip({ situacao }: { situacao?: string }) {
  if (!situacao) return <span>—</span>;
  const map: Record<string, "default" | "warning" | "info" | "success"> = {
    Aberta: "warning",
    "Em Andamento": "info",
    Finalizada: "success",
  };
  const color = map[situacao] ?? "default";
  return (
    <Chip
      label={situacao}
      size="small"
      color={color}
      sx={{ fontWeight: 600, fontSize: "0.75rem" }}
    />
  );
}

function PrioridadeChip({ prioridade }: { prioridade?: string }) {
  if (!prioridade) return <span>—</span>;
  const map: Record<string, "default" | "success" | "warning" | "error"> = {
    Baixa: "success",
    Média: "warning",
    Alta: "error",
  };
  const color = map[prioridade] ?? "default";
  return (
    <Chip
      label={prioridade}
      size="small"
      color={color}
      sx={{ fontWeight: 600, fontSize: "0.75rem" }}
    />
  );
}

function AtrasadaChip({ atrasada }: { atrasada?: boolean }) {
  if (!atrasada) return <span>—</span>;
  return (
    <Chip
      label="Atrasada"
      size="small"
      color="error"
      variant="filled"
      sx={{ fontWeight: 600, fontSize: "0.75rem" }}
    />
  );
}

type SortField = "titulo" | "data" | "dataFinal" | "hora" | "situacao" | "prioridade" | "atrasada";
type SortDirection = "asc" | "desc";

export default function PendenciasList({ pendencias, onSelect }: Props) {
  const [sortField, setSortField] = useState<SortField | null>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  const sortedPendencias = useMemo(() => {
    if (!sortField) return pendencias;

    return [...pendencias].sort((a, b) => {
      let aValue: any;
      let bValue: any;

      switch (sortField) {
        case "titulo":
          aValue = a.titulo?.toLowerCase() || "";
          bValue = b.titulo?.toLowerCase() || "";
          break;
        case "data":
          aValue = a.data ? new Date(a.data).getTime() : 0;
          bValue = b.data ? new Date(b.data).getTime() : 0;
          break;
        case "dataFinal":
          aValue = a.dataCriacao && a.prazoResposta
            ? new Date(a.dataCriacao).getTime() + (a.prazoResposta * 24 * 60 * 60 * 1000)
            : 0;
          bValue = b.dataCriacao && b.prazoResposta
            ? new Date(b.dataCriacao).getTime() + (b.prazoResposta * 24 * 60 * 60 * 1000)
            : 0;
          break;
        case "hora":
          aValue = a.hora || "";
          bValue = b.hora || "";
          break;
        case "situacao":
          aValue = a.situacao || "";
          bValue = b.situacao || "";
          break;
        case "prioridade":
          const prioridadeOrder: Record<string, number> = { Alta: 0, Média: 1, Baixa: 2 };
          aValue = prioridadeOrder[a.prioridade || ""] ?? 3;
          bValue = prioridadeOrder[b.prioridade || ""] ?? 3;
          break;
        case "atrasada":
          aValue = a.atrasada ? 1 : 0;
          bValue = b.atrasada ? 1 : 0;
          break;
        default:
          return 0;
      }

      if (aValue < bValue) return sortDirection === "asc" ? -1 : 1;
      if (aValue > bValue) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }, [pendencias, sortField, sortDirection]);

  const SortableHeader = ({ 
    field, 
    label 
  }: { 
    field: SortField; 
    label: string;
  }) => (
    <TableCell
      sx={{
        fontWeight: 700,
        bgcolor: "grey.50",
        color: "text.secondary",
        fontSize: "0.8rem",
        cursor: "pointer",
        userSelect: "none",
        "&:hover": { bgcolor: "grey.100" },
      }}
      onClick={() => handleSort(field)}
    >
      <TableSortLabel
        active={sortField === field}
        direction={sortField === field ? sortDirection : "asc"}
      >
        {label}
      </TableSortLabel>
    </TableCell>
  );

  return (
    <TableContainer sx={{ borderRadius: 2, overflow: "hidden", border: "1px solid", borderColor: "divider" }}>
      <Table size="small" stickyHeader>
        <TableHead>
          <TableRow>
            <SortableHeader field="titulo" label="Pendência" />
            <SortableHeader field="data" label="Data" />
            <SortableHeader field="dataFinal" label="Data final" />
            <SortableHeader field="hora" label="Hora" />
            <SortableHeader field="situacao" label="Situação" />
            <SortableHeader field="prioridade" label="Prioridade" />
            <SortableHeader field="atrasada" label="Status" />
          </TableRow>
        </TableHead>
        <TableBody>
          {sortedPendencias.length === 0 ? (
            <TableRow>
              <TableCell colSpan={7} align="center" sx={{ py: 4, color: "text.secondary" }}>
                Nenhuma pendência encontrada
              </TableCell>
            </TableRow>
          ) : (
            sortedPendencias.map((p) => (
              <TableRow
                key={p.id}
                hover
                onClick={() => onSelect?.(p)}
                sx={{
                  cursor: "pointer",
                  "&:hover": { bgcolor: "action.hover" },
                  bgcolor: p.atrasada ? "rgba(244, 67, 54, 0.08)" : "transparent",
                }}
              >
                <TableCell sx={{ fontWeight: 500 }}>{p.titulo}</TableCell>
                <TableCell sx={{ color: "text.secondary" }}>
                  {p.data ? new Date(p.data).toLocaleDateString("pt-BR") : "—"}
                </TableCell>
                <TableCell sx={{ color: "text.secondary" }}>
                  {p.dataCriacao && p.prazoResposta != null ? (() => {
                    try {
                      const d = new Date(p.dataCriacao);
                      d.setDate(d.getDate() + (p.prazoResposta ?? 0));
                      return d.toLocaleDateString("pt-BR");
                    } catch {
                      return "—";
                    }
                  })() : "—"}
                </TableCell>
                <TableCell sx={{ color: "text.secondary" }}>{p.hora ?? "—"}</TableCell>
                <TableCell>
                  <StatusChip situacao={p.situacao} />
                </TableCell>
                <TableCell>
                  <PrioridadeChip prioridade={p.prioridade} />
                </TableCell>
                <TableCell>
                  <AtrasadaChip atrasada={p.atrasada} />
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
