import { useEffect, useState } from "react";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Filters from "./components/Filters";
import PendenciasList from "./components/PendenciasList";
import PendenciaDetails from "./components/PendenciaDetails";
import ActionsPanel from "./components/ActionsPanel";
import NewPendenciaModal from "./components/NewPendenciaModal";
import EditPendenciaModal from "./components/EditPendenciaModal";
import UpdateSituacaoModal from "./components/UpdateSituacaoModal";
import TransferPendenciaModal from "./components/TransferPendenciaModal";
import { getPendencias, deletePendencia } from "./services/api";
import type { Pendencia } from "./types";
import Login from "./components/Login";
import { useAuth } from "./contexts/AuthContext";

export default function App() {
  const { token, isReady, usuario } = useAuth();
  const [pendenciasRaw, setPendenciasRaw] = useState<Pendencia[]>([]);
  const [pendencias, setPendencias] = useState<Pendencia[]>([]);
  const [selected, setSelected] = useState<Pendencia | null>(null);
  const [openNew, setOpenNew] = useState(false);
  const [openEdit, setOpenEdit] = useState(false);
  const [openSituacao, setOpenSituacao] = useState(false);
  const [openTransfer, setOpenTransfer] = useState(false);
  const [transferConfig, setTransferConfig] = useState<{ mode: "transfer" | "atribuir"; fixedSetorId: number | null }>({
    mode: "transfer",
    fixedSetorId: null,
  });
  const [snackbar, setSnackbar] = useState<{ message: string; severity: "success" | "error" | "info" } | null>(null);
  const [filtroUsuarioId, setFiltroUsuarioId] = useState<number | undefined>(undefined);

  const fetch = async (usuarioId?: number) => {
    try {
      const data = await getPendencias(usuarioId);
      setPendenciasRaw(data);
      setPendencias(processPendencias(data));
    } catch (err) {
      console.error("Erro ao buscar pendências (verifique se o backend está rodando em " + (import.meta.env.VITE_API_URL ?? "http://localhost:8080") + ")", err);
      setPendenciasRaw([]);
      setPendencias([]);
    }
  };

  const applyFilters = async (filters?: { periodStart?: string; periodEnd?: string; status?: string; prioridade?: string; usuarioId?: number }) => {
    // Se o filtro de usuário mudou, precisa buscar novamente da API
    const novoUsuarioId = filters?.usuarioId;
    if (novoUsuarioId !== filtroUsuarioId) {
      setFiltroUsuarioId(novoUsuarioId);
      // Busca pendências do usuário selecionado (ou todas se undefined)
      await fetch(novoUsuarioId);
      // Continua aplicando os outros filtros locais abaixo
    }

    if (!filters) {
      setPendencias(processPendencias(pendenciasRaw));
      return;
    }

    let filtered = [...pendenciasRaw];

    // Filtrar por período
    if (filters.periodStart) {
      filtered = filtered.filter((p) => p.data >= filters.periodStart!);
    }
    if (filters.periodEnd) {
      filtered = filtered.filter((p) => p.data <= filters.periodEnd!);
    }

    // Filtrar por status/situação
    // Suporta flag "exceto": se filters.statusExcept for true, remove pendências com a situação selecionada
    const statusExcept = (filters as any).statusExcept === true;
    if (filters.status && filters.status !== "Todas") {
      if (statusExcept) {
        filtered = filtered.filter((p) => p.situacao !== filters.status);
      } else {
        filtered = filtered.filter((p) => p.situacao === filters.status);
      }
    }

    // Filtrar por prioridade
    const prioridadeExcept = (filters as any).prioridadeExcept === true;
    if (filters.prioridade && filters.prioridade !== "Todas") {
      if (prioridadeExcept) {
        filtered = filtered.filter((p) => p.prioridade !== filters.prioridade);
      } else {
        filtered = filtered.filter((p) => p.prioridade === filters.prioridade);
      }
    }

    setPendencias(processPendencias(filtered));
  };

  const processPendencias = (list: Pendencia[]): Pendencia[] => {
    return list
      .map((p) => ({
        ...p,
        atrasada: isAtrasada(p),
      }))
      .sort((a, b) => {
        // Ordenar por atraso primeiro (atrasadas no topo)
        if (a.atrasada && !b.atrasada) return -1;
        if (!a.atrasada && b.atrasada) return 1;

        // Depois por prioridade: Alta > Média > Baixa
        const prioridadeOrder: { [key: string]: number } = { Alta: 0, Média: 1, Baixa: 2 };
        const aPrio = prioridadeOrder[a.prioridade || ""] ?? 3;
        const bPrio = prioridadeOrder[b.prioridade || ""] ?? 3;
        return aPrio - bPrio;
      });
  };

  const isAtrasada = (p: Pendencia): boolean => {
    if (!p.dataCriacao || !p.prazoResposta) return false;

    const dataCriacao = new Date(p.dataCriacao);
    const dataLimite = new Date(dataCriacao);
    dataLimite.setDate(dataLimite.getDate() + p.prazoResposta);

    return new Date() > dataLimite;
  };

  useEffect(() => {
    // apenas busca pendências quando o auth estiver pronto e houver token
    if (!isReady) return;
    if (!token) return;
    fetch();
  }, [isReady, token]);

  if (isReady && !token) {
    return <Login />;
  }

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
          <Filters 
            onApply={applyFilters} 
            showUsuarioFilter={!!usuario && (usuario.nivelUsuario ?? 0) >= 4}
          />
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
                  onRefresh={() => fetch(filtroUsuarioId)}
                  onEdit={() => setOpenEdit(true)}
                  onUpdateSituacao={() => setOpenSituacao(true)}
                  onTransferir={() => {
                    setTransferConfig({ mode: "transfer", fixedSetorId: null });
                    setOpenTransfer(true);
                  }}
                  selected={selected}
                    canCreate={!!usuario && (usuario.nivelUsuario ?? 0) > 2}
                    canDelete={!!usuario && (usuario.nivelUsuario ?? 0) >= 3}
                    onDelete={async (p) => {
                      if (!p) return;
                      try {
                        await deletePendencia(p.id);
                        setSelected(null);
                        await fetch();
                        showSnackbar("Pendência removida.", "success");
                      } catch (e:any) {
                        console.error(e);
                        showSnackbar(e?.message ?? "Falha ao remover pendência.", "error");
                      }
                    }}
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
              <PendenciaDetails
                pendencia={selected}
                onAtribuir={() => {
                  if (!selected) return;
                  setTransferConfig({ mode: "atribuir", fixedSetorId: selected.idSetor ?? null });
                  setOpenTransfer(true);
                }}
              />
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

      <TransferPendenciaModal
        open={openTransfer}
        onClose={() => setOpenTransfer(false)}
        pendencia={selected}
        initialMode={transferConfig.mode === "atribuir" ? "usuario" : "setor"}
        fixedSetorId={transferConfig.mode === "atribuir" ? transferConfig.fixedSetorId : null}
        onSaved={() => {
          fetch();
          showSnackbar("Pendência transferida.", "success");
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
      <Footer />
    </Box>
  );
}

