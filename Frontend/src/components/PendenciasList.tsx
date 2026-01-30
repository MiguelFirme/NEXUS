import Table from "@mui/material/Table";
import TableHead from "@mui/material/TableHead";
import TableBody from "@mui/material/TableBody";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
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

export default function PendenciasList({ pendencias, onSelect }: Props) {
  return (
    <TableContainer sx={{ borderRadius: 2, overflow: "hidden", border: "1px solid", borderColor: "divider" }}>
      <Table size="small" stickyHeader>
        <TableHead>
          <TableRow>
            <TableCell sx={{ fontWeight: 700, bgcolor: "grey.50", color: "text.secondary", fontSize: "0.8rem" }}>
              Pendência
            </TableCell>
            <TableCell sx={{ fontWeight: 700, bgcolor: "grey.50", color: "text.secondary", fontSize: "0.8rem" }}>
              Data
            </TableCell>
            <TableCell sx={{ fontWeight: 700, bgcolor: "grey.50", color: "text.secondary", fontSize: "0.8rem" }}>
              Hora
            </TableCell>
            <TableCell sx={{ fontWeight: 700, bgcolor: "grey.50", color: "text.secondary", fontSize: "0.8rem" }}>
              Situação
            </TableCell>
            <TableCell sx={{ fontWeight: 700, bgcolor: "grey.50", color: "text.secondary", fontSize: "0.8rem" }}>
              Prioridade
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {pendencias.length === 0 ? (
            <TableRow>
              <TableCell colSpan={5} align="center" sx={{ py: 4, color: "text.secondary" }}>
                Nenhuma pendência encontrada
              </TableCell>
            </TableRow>
          ) : (
            pendencias.map((p) => (
              <TableRow
                key={p.id}
                hover
                onClick={() => onSelect?.(p)}
                sx={{
                  cursor: "pointer",
                  "&:hover": { bgcolor: "action.hover" },
                }}
              >
                <TableCell sx={{ fontWeight: 500 }}>{p.titulo}</TableCell>
                <TableCell sx={{ color: "text.secondary" }}>
                  {p.data ? new Date(p.data).toLocaleDateString("pt-BR") : "—"}
                </TableCell>
                <TableCell sx={{ color: "text.secondary" }}>{p.hora ?? "—"}</TableCell>
                <TableCell>
                  <StatusChip situacao={p.situacao} />
                </TableCell>
                <TableCell>
                  <PrioridadeChip prioridade={p.prioridade} />
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
