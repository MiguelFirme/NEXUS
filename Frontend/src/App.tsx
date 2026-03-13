import { useEffect, useState } from "react";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Filters from "./components/Filters";
import type { FiltersPayload } from "./components/Filters";
import PendenciasList from "./components/PendenciasList";
import PendenciaDetails from "./components/PendenciaDetails";
import ActionsPanel from "./components/ActionsPanel";
import Estatisticas from "./components/Estatisticas";
import NewPendenciaModal from "./components/NewPendenciaModal";
import EditPendenciaModal from "./components/EditPendenciaModal";
import TransferPendenciaModal from "./components/TransferPendenciaModal";
import { getPendencias, getRoteiro, transferirPendencia, getUsuarios, getSetores } from "./services/api";
import type { Pendencia } from "./types";
import Login from "./components/Login";
import { useAuth } from "./contexts/AuthContext";
import { printRelatorioPendenciasAtivas } from "./utils/printRelatorioPendenciasAtivas";

export default function App() {
  const { token, isReady, usuario } = useAuth();
  const [pendenciasRaw, setPendenciasRaw] = useState<Pendencia[]>([]);
  const [pendencias, setPendencias] = useState<Pendencia[]>([]);
  const [selected, setSelected] = useState<Pendencia | null>(null);
  const [openNew, setOpenNew] = useState(false);
  const [openEdit, setOpenEdit] = useState(false);
  const [openTransfer, setOpenTransfer] = useState(false);
  const [transferConfig, setTransferConfig] = useState<{ mode: "transfer" | "atribuir"; fixedSetorId: number | null }>({
    mode: "transfer",
    fixedSetorId: null,
  });
  const [snackbar, setSnackbar] = useState<{ message: string; severity: "success" | "error" | "info" } | null>(null);
  const [filtroUsuarioId, setFiltroUsuarioId] = useState<number | undefined>(undefined);
  const [abaPrincipal, setAbaPrincipal] = useState(0);

  const fetch = async (usuarioId?: number) => {
    try {
      const data = await getPendencias(usuarioId);
      setPendenciasRaw(data);
      setPendencias(processPendencias(data));
      return data;
    } catch (err) {
      console.error("Erro ao buscar pendências (verifique se o backend está rodando em " + (import.meta.env.VITE_API_URL ?? "http://localhost:8080") + ")", err);
      setPendenciasRaw([]);
      setPendencias([]);
      return [];
    }
  };

  const applyFilters = async (filters?: FiltersPayload) => {
    // Se o filtro de usuário mudou, precisa buscar novamente da API
    const novoUsuarioId = filters?.usuarioId;
    let dataToFilter = pendenciasRaw;
    
    if (novoUsuarioId !== filtroUsuarioId) {
      setFiltroUsuarioId(novoUsuarioId);
      // Busca pendências do usuário selecionado (ou todas se undefined)
      dataToFilter = await fetch(novoUsuarioId) ?? [];
      // Continua aplicando os outros filtros locais abaixo
    }

    if (!filters) {
      setPendencias(processPendencias(dataToFilter));
      return;
    }

    let filtered = [...dataToFilter];

    // Filtrar por número da pendência (contém o texto digitado)
    if (filters.numeroPesquisa) {
      const busca = filters.numeroPesquisa.trim().toLowerCase();
      filtered = filtered.filter((p) => (p.numero ?? "").toLowerCase().includes(busca));
    }

    // Filtrar por período
    if (filters.periodStart) {
      filtered = filtered.filter((p) => {
        // Usa dataCriacao se data não estiver disponível
        const dataParaComparar = p.data || (p.dataCriacao ? p.dataCriacao.slice(0, 10) : null);
        if (!dataParaComparar) return false; // Se não tem data, não inclui no filtro
        return dataParaComparar >= filters.periodStart!;
      });
    }
    if (filters.periodEnd) {
      filtered = filtered.filter((p) => {
        // Usa dataCriacao se data não estiver disponível
        const dataParaComparar = p.data || (p.dataCriacao ? p.dataCriacao.slice(0, 10) : null);
        if (!dataParaComparar) return false; // Se não tem data, não inclui no filtro
        return dataParaComparar <= filters.periodEnd!;
      });
    }

    // Filtrar por status/situação
    if (filters.status && filters.status !== "Todas") {
      filtered = filtered.filter((p) => p.situacao === filters.status);
    }

    // Filtrar por prioridade
    if (filters.prioridade && filters.prioridade !== "Todas") {
      filtered = filtered.filter((p) => p.prioridade === filters.prioridade);
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
    if (!isReady || !token) return;

    fetch(filtroUsuarioId);

    // Refresh automático a cada 5 segundos
    const interval = setInterval(() => {
      fetch(filtroUsuarioId);
    }, 5000);

    return () => clearInterval(interval);
  }, [isReady, token, filtroUsuarioId]);

  if (isReady && !token) {
    return <Login />;
  }

  const showSnackbar = (message: string, severity: "success" | "error" | "info") => {
    setSnackbar({ message, severity });
  };

  const handleImprimirRelatorioAtivas = async () => {
    try {
      const setores = await getSetores();
      const setoresMap = new Map<number, string>();
      setores.forEach((s) => {
        if (s.id != null && s.nome_setor) setoresMap.set(s.id, s.nome_setor);
      });
      const ativas = processPendencias(pendenciasRaw).filter((p) => p.situacao !== "Finalizada");
      printRelatorioPendenciasAtivas(ativas, usuario, setoresMap);
      showSnackbar("Relatório enviado para impressão.", "success");
    } catch (e) {
      console.error(e);
      showSnackbar("Falha ao gerar relatório.", "error");
    }
  };

  const handleTransferirProximaEtapa = async (p: Pendencia | null) => {
    if (!p) return;

    if (p.idRoteiro) {
      try {
        const roteiro = await getRoteiro(p.idRoteiro);

        const confirmado = window.confirm(
          `Esta pendência está vinculada ao roteiro "${roteiro.nome}".\n\n` +
            "Tem certeza de que deseja passar a pendência para a próxima etapa definida nesse roteiro?"
        );
        if (!confirmado) return;

        const passos = (roteiro.passos ?? []).slice().sort((a, b) => a.ordem - b.ordem);

        const indicePorUsuario =
          p.idUsuario != null
            ? passos.findIndex((passo) => passo.tipo === "USUARIO" && passo.idUsuario === p.idUsuario)
            : -1;
        const indicePorSetor =
          p.idSetor != null
            ? passos.findIndex((passo) => passo.tipo === "SETOR" && passo.idSetor === p.idSetor)
            : -1;

        const indiceAtual = indicePorUsuario >= 0 ? indicePorUsuario : indicePorSetor;
        if (indiceAtual < 0 || indiceAtual + 1 >= passos.length) {
          showSnackbar("Esta pendência já está no último passo do roteiro.", "info");
          return;
        }

        const proximoPasso = passos[indiceAtual + 1];

        if (proximoPasso.tipo === "SETOR" && proximoPasso.idSetor != null) {
          await transferirPendencia(p.id, { idSetor: proximoPasso.idSetor, idUsuario: 0 });
        } else if (proximoPasso.tipo === "USUARIO" && proximoPasso.idUsuario != null) {
          const usuarios = await getUsuarios();
          const usuarioDestino = usuarios.find((u) => u.id === proximoPasso.idUsuario);
          await transferirPendencia(p.id, {
            idUsuario: proximoPasso.idUsuario,
            idSetor: (usuarioDestino?.idSetor ?? p.idSetor) as number,
          });
        } else {
          showSnackbar("Não foi possível determinar o próximo passo do roteiro.", "error");
          return;
        }

        const atualizadas = await fetch(filtroUsuarioId);
        if (atualizadas && p) {
          const encontrada = atualizadas.find((x) => x.id === p.id);
          if (encontrada) {
            setSelected(encontrada);
          }
        }

        showSnackbar("Pendência transferida para a próxima etapa.", "success");
      } catch (e) {
        console.error(e);
        showSnackbar("Falha ao transferir para a próxima etapa.", "error");
      }
    } else {
      showSnackbar(
        "Esta pendência não está vinculada a um roteiro. Selecione manualmente o próximo passo (setor ou usuário).",
        "info"
      );
      setTransferConfig({ mode: "transfer", fixedSetorId: null });
      setOpenTransfer(true);
    }
  };

  return (
    <Box sx={{ minHeight: "100vh", pb: 4 }}>
      <Header />
      <Container maxWidth="xl" sx={{ mt: 3, px: { xs: 2, sm: 3 } }}>
        <Box sx={{ mb: 2 }}>
          <Tabs value={abaPrincipal} onChange={(_, v) => setAbaPrincipal(v)} sx={{ minHeight: 48, mb: 1 }}>
            <Tab label="Dashboard" id="aba-dashboard" />
            <Tab label="Estatísticas" id="aba-estatisticas" />
          </Tabs>
        </Box>

        {abaPrincipal === 0 && (
          <>
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
                  onPrintRelatorio={handleImprimirRelatorioAtivas}
                  canCreate={!!usuario && (usuario.nivelUsuario ?? 0) > 2}
                />
              </Box>
            </Paper>
          </Grid>

          <Grid size={{ xs: 12, md: 5 }}>
            <Paper
              sx={{
                p: 2.5,
                height: 420,
                maxHeight: 420,
                overflow: "auto",
                borderRadius: 2,
                boxShadow: "0 1px 3px rgba(0,0,0,0.06)",
              }}
            >
              <PendenciaDetails
                pendencia={selected}
                onAtribuir={() => {
                  if (!selected) return;
                  setTransferConfig({ mode: "atribuir", fixedSetorId: selected.idSetor ?? null });
                  setOpenTransfer(true);
                }}
                onSaved={async () => {
                  await fetch(filtroUsuarioId);
                  if (selected) {
                    const updated = await getPendencias(filtroUsuarioId);
                    const found = updated.find(p => p.id === selected.id);
                    if (found) setSelected(found);
                  }
                }}
                onEdit={() => setOpenEdit(true)}
                onTransferirProximaEtapa={() => selected && handleTransferirProximaEtapa(selected)}
              />
            </Paper>
          </Grid>
        </Grid>
          </>
        )}

        {abaPrincipal === 1 && (
          <Box sx={{ mb: 3 }}>
            <Typography variant="h4" fontWeight={700} color="text.primary" sx={{ letterSpacing: "-0.02em", mb: 1 }}>
              Estatísticas
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
              Quantidade de pendências criadas, por status, prioridade, situação e em atraso
            </Typography>
            <Estatisticas />
          </Box>
        )}
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
        currentUserLevel={usuario?.nivelUsuario}
        onSaved={() => {
          fetch();
          showSnackbar("Pendência atualizada.", "success");
        }}
        onDeleted={async () => {
          setOpenEdit(false);
          setSelected(null);
          await fetch(filtroUsuarioId);
          showSnackbar("Pendência excluída.", "success");
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

