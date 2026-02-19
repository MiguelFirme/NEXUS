import { useState } from "react";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import { getEstatisticasPendencias, type EstatisticasPendencias } from "../services/api";

export default function Estatisticas() {
  const [dataInicial, setDataInicial] = useState<string>("");
  const [dataFinal, setDataFinal] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState<EstatisticasPendencias | null>(null);

  const handleAplicar = async () => {
    setLoading(true);
    try {
      const res = await getEstatisticasPendencias({
        dataInicial: dataInicial || undefined,
        dataFinal: dataFinal || undefined,
      });
      setStats(res);
    } catch {
      setStats(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h6" fontWeight={600} color="text.primary" sx={{ mb: 2 }}>
        Filtros
      </Typography>
      <Paper sx={{ p: 2, mb: 3, borderRadius: 2 }}>
        <Box sx={{ display: "flex", gap: 2, alignItems: "center", flexWrap: "wrap" }}>
          <TextField
            label="Data inicial"
            type="date"
            size="small"
            value={dataInicial}
            onChange={(e) => setDataInicial(e.target.value)}
            InputLabelProps={{ shrink: true }}
            sx={{ minWidth: 160 }}
          />
          <TextField
            label="Data final"
            type="date"
            size="small"
            value={dataFinal}
            onChange={(e) => setDataFinal(e.target.value)}
            InputLabelProps={{ shrink: true }}
            sx={{ minWidth: 160 }}
          />
          <Button variant="contained" onClick={handleAplicar} disabled={loading}>
            {loading ? "Carregando…" : "Aplicar"}
          </Button>
        </Box>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          Deixe as datas em branco para considerar todas as pendências.
        </Typography>
      </Paper>

      {stats && (
        <Grid container spacing={3}>
          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <Paper sx={{ p: 2.5, borderRadius: 2, textAlign: "center" }}>
              <Typography variant="overline" color="text.secondary">
                Total criadas
              </Typography>
              <Typography variant="h4" fontWeight={700} color="primary.main">
                {stats.totalCriadas}
              </Typography>
            </Paper>
          </Grid>
          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <Paper sx={{ p: 2.5, borderRadius: 2, textAlign: "center" }}>
              <Typography variant="overline" color="text.secondary">
                Em atraso
              </Typography>
              <Typography
                variant="h4"
                fontWeight={700}
                sx={{ color: stats.quantidadeAtraso > 0 ? "error.main" : "text.primary" }}
              >
                {stats.quantidadeAtraso}
              </Typography>
            </Paper>
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <Paper sx={{ p: 2.5, borderRadius: 2 }}>
              <Typography variant="subtitle2" fontWeight={600} sx={{ mb: 1.5 }}>
                Por status
              </Typography>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Status</TableCell>
                      <TableCell align="right">Quantidade</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {stats.porStatus.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={2} align="center" color="text.secondary">
                          —
                        </TableCell>
                      </TableRow>
                    ) : (
                      stats.porStatus.map((row) => (
                        <TableRow key={row.valor}>
                          <TableCell>{row.valor}</TableCell>
                          <TableCell align="right">{row.quantidade}</TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </Paper>
          </Grid>
          <Grid size={{ xs: 12, md: 4 }}>
            <Paper sx={{ p: 2.5, borderRadius: 2 }}>
              <Typography variant="subtitle2" fontWeight={600} sx={{ mb: 1.5 }}>
                Por situação
              </Typography>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Situação</TableCell>
                      <TableCell align="right">Quantidade</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {stats.porSituacao.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={2} align="center" color="text.secondary">
                          —
                        </TableCell>
                      </TableRow>
                    ) : (
                      stats.porSituacao.map((row) => (
                        <TableRow key={row.valor}>
                          <TableCell>{row.valor}</TableCell>
                          <TableCell align="right">{row.quantidade}</TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </Paper>
          </Grid>
          <Grid size={{ xs: 12, md: 4 }}>
            <Paper sx={{ p: 2.5, borderRadius: 2 }}>
              <Typography variant="subtitle2" fontWeight={600} sx={{ mb: 1.5 }}>
                Por prioridade
              </Typography>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Prioridade</TableCell>
                      <TableCell align="right">Quantidade</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {stats.porPrioridade.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={2} align="center" color="text.secondary">
                          —
                        </TableCell>
                      </TableRow>
                    ) : (
                      stats.porPrioridade.map((row) => (
                        <TableRow key={row.valor}>
                          <TableCell>{row.valor}</TableCell>
                          <TableCell align="right">{row.quantidade}</TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </Paper>
          </Grid>
        </Grid>
      )}

      {!stats && !loading && (
        <Typography variant="body2" color="text.secondary">
          Use os filtros e clique em &quot;Aplicar&quot; para carregar as estatísticas.
        </Typography>
      )}
    </Box>
  );
}
