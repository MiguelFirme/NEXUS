import { useEffect, useState } from "react";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";
import Header from "./components/Header";
import Filters from "./components/Filters";
import PendenciasList from "./components/PendenciasList";
import PendenciaDetails from "./components/PendenciaDetails";
import ActionsPanel from "./components/ActionsPanel";
import NewPendenciaModal from "./components/NewPendenciaModal";
import EditPendenciaModal from "./components/EditPendenciaModal";
import UpdateSituacaoModal from "./components/UpdateSituacaoModal";
import { getPendencias } from "./services/api";
import type { Pendencia } from "./types";

export default function App() {
  const [pendencias, setPendencias] = useState<Pendencia[]>([]);
  const [selected, setSelected] = useState<Pendencia | null>(null);
  const [openNew, setOpenNew] = useState(false);
  const [openEdit, setOpenEdit] = useState(false);
  const [openSituacao, setOpenSituacao] = useState(false);
  const [snackbar, setSnackbar] = useState<{ message: string; severity: "success" | "error" | "info" } | null>(null);

  const fetch = async () => {
    try {
      const data = await getPendencias();
      setPendencias(data);
    } catch (err) {
      console.error("Erro ao buscar pendências (verifique se o backend está rodando em " + (import.meta.env.VITE_API_URL ?? "http://localhost:8080") + ")", err);
      setPendencias([]);
    }
  };

  useEffect(() => {
    fetch();
  }, []);

  const showSnackbar = (message: string, severity: "success" | "error" | "info") => {
    setSnackbar({ message, severity });
  };

  return (
    <Box sx={{ minHeight: "100vh", pb: 4 }}>
      <Header />
      <Container maxWidth="xl" sx={{ mt: 3, px: { xs: 2, sm: 3 } }}>
        <Box sx={{ mb: 3 }}>
          <Typography variant="h4" fontWeight={700} color="text.primary" sx={{ letterSpacing: "-0.02em" }}>
            Dashboard
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Acompanhe e gerencie suas pendências
          </Typography>
        </Box>

        <Paper
          sx={{
            p: 2.5,
            mb: 3,
            borderRadius: 2,
            boxShadow: "0 1px 3px rgba(0,0,0,0.06)",
          }}
        >
          <Typography variant="subtitle1" fontWeight={600} color="text.primary" sx={{ mb: 2 }}>
            Filtros
          </Typography>
          <Filters onApply={fetch} />
        </Paper>

        <Grid container spacing={3}>
          <Grid size={{ xs: 12, md: 7 }}>
            <Paper
              sx={{
                p: 2.5,
                height: "100%",
                minHeight: 420,
                display: "flex",
                flexDirection: "column",
                borderRadius: 2,
                boxShadow: "0 1px 3px rgba(0,0,0,0.06)",
              }}
            >
              <Typography variant="subtitle1" fontWeight={600} color="text.primary" sx={{ mb: 2 }}>
                Lista de pendências
              </Typography>
              <Box sx={{ flex: 1, minHeight: 0 }}>
                <PendenciasList
                  pendencias={pendencias}
                  onSelect={(p) => setSelected(p)}
                />
              </Box>
              <Box sx={{ mt: 2 }}>
                <ActionsPanel
                  onNew={() => setOpenNew(true)}
                  onRefresh={fetch}
                  onEdit={() => setOpenEdit(true)}
                  onUpdateSituacao={() => setOpenSituacao(true)}
                  onTransferir={() => showSnackbar("Transferir: funcionalidade em breve.", "info")}
                  selected={selected}
                />
              </Box>
            </Paper>
          </Grid>

          <Grid size={{ xs: 12, md: 5 }}>
            <Paper
              sx={{
                p: 2.5,
                minHeight: 420,
                borderRadius: 2,
                boxShadow: "0 1px 3px rgba(0,0,0,0.06)",
              }}
            >
              <Typography variant="subtitle1" fontWeight={600} color="text.primary" sx={{ mb: 2 }}>
                Detalhes
              </Typography>
              <PendenciaDetails pendencia={selected} />
            </Paper>
          </Grid>
        </Grid>
      </Container>

      <NewPendenciaModal
        open={openNew}
        onClose={() => setOpenNew(false)}
        onCreated={() => fetch()}
      />

      <EditPendenciaModal
        open={openEdit}
        onClose={() => setOpenEdit(false)}
        pendencia={selected}
        onSaved={() => {
          fetch();
          showSnackbar("Pendência atualizada.", "success");
        }}
      />

      <UpdateSituacaoModal
        open={openSituacao}
        onClose={() => setOpenSituacao(false)}
        pendencia={selected}
        onSaved={() => {
          fetch();
          showSnackbar("Situação atualizada.", "success");
        }}
      />

      <Snackbar
        open={!!snackbar}
        autoHideDuration={5000}
        onClose={() => setSnackbar(null)}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        {snackbar ? (
          <Alert onClose={() => setSnackbar(null)} severity={snackbar.severity} variant="filled">
            {snackbar.message}
          </Alert>
        ) : undefined}
      </Snackbar>
    </Box>
  );
}
