import { useState, useEffect, useMemo } from "react";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";
import Table from "@mui/material/Table";
import TableHead from "@mui/material/TableHead";
import TableBody from "@mui/material/TableBody";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import type { Pendencia } from "../types";
import {
  uploadAnexo,
  getAnexos,
  deleteAnexo,
  getSetores,
  getUsuarios,
  aceitarTransferencia,
  devolverTransferencia,
  getErrorMessage,
} from "../services/api";
import Link from "@mui/material/Link";
import UploadFileRounded from "@mui/icons-material/UploadFileRounded";
import PrintRounded from "@mui/icons-material/PrintRounded";
import EditRounded from "@mui/icons-material/EditRounded";
import SwapHorizRounded from "@mui/icons-material/SwapHorizRounded";
import { useAuth } from "../contexts/AuthContext";

type AnexoItem = {
  filename: string;
  url: string;
  originalName: string;
  ext: string;
  uploadedAt?: Date;
  sizeMB?: number;
  usuario?: string;
};

type Props = {
  pendencia: Pendencia | null;
  onAtribuir?: () => void;
  onSaved?: () => void;
  onEdit?: () => void;
  onTransferirProximaEtapa?: () => void;
};

function StatusChip({ situacao }: { situacao?: string }) {
  if (!situacao) return null;
  const map: Record<string, "default" | "warning" | "info" | "success"> = {
    Aberta: "warning",
    "Em Andamento": "info",
    Finalizada: "success",
  };
  const color = map[situacao] ?? "default";
  return <Chip label={situacao} size="small" color={color} sx={{ fontWeight: 600 }} />;
}

function PrioridadeChip({ prioridade }: { prioridade?: string }) {
  if (!prioridade) return null;
  const map: Record<string, "default" | "success" | "warning" | "error"> = {
    Baixa: "success",
    Média: "warning",
    Alta: "error",
  };
  const color = map[prioridade] ?? "default";
  return <Chip label={prioridade} size="small" color={color} sx={{ fontWeight: 600 }} />;
}

function DetailRow({ label, value }: { label: string; value?: string | number | null }) {
  if (value == null || value === "") return null;
  return (
    <Box sx={{ display: "flex", gap: 1, mb: 1, flexWrap: "wrap" }}>
      <Typography variant="body2" color="text.secondary" sx={{ minWidth: 140 }}>
        {label}:
      </Typography>
      <Typography variant="body2">{value}</Typography>
    </Box>
  );
}

const HISTORICO_LABELS: Record<string, string> = {
  data: "Data",
  dataAlteracao: "Data da alteração",
  usuario: "Usuário",
  autor: "Autor",
  descricao: "Descrição",
  mensagem: "Mensagem",
  acao: "Ação",
  situacao: "Situação",
  situacaoAnterior: "Situação anterior",
  observacao: "Observação",
  observacoes: "Observações",
  idSetor: "Setor",
  idSetorAnterior: "Setor anterior",
  idUsuario: "Usuário",
  idUsuarioAnterior: "Usuário anterior",
  status: "Status",
  statusAnterior: "Status anterior",
};

function formatHistoricoKey(key: string): string {
  return HISTORICO_LABELS[key] ?? key.replace(/([A-Z])/g, " $1").replace(/^./, (s) => s.toUpperCase());
}

function formatHistoricoValue(
  value: unknown,
  key: string,
  setoresMap?: Map<number, string>,
  usuariosMap?: Map<number, string>
): string {
  if (value == null) return "—";
  
  // Formata IDs de setor e usuário com nomes
  if (key === "idSetor" || key === "idSetorAnterior") {
    if (typeof value === "number" && setoresMap?.has(value)) {
      return `${setoresMap.get(value)} (Setor #${value})`;
    }
    return typeof value === "number" ? `Setor #${value}` : String(value);
  }
  
  if (key === "idUsuario" || key === "idUsuarioAnterior") {
    if (typeof value === "number" && usuariosMap?.has(value)) {
      return `${usuariosMap.get(value)} (Usuário #${value})`;
    }
    return typeof value === "number" ? `Usuário #${value}` : String(value);
  }
  
  if (typeof value === "string" && /^\d{4}-\d{2}-\d{2}/.test(value)) {
    try {
      return new Date(value).toLocaleString("pt-BR");
    } catch {
      return value;
    }
  }
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function HistoricoEntry({ 
  item, 
  index,
  setoresMap,
  usuariosMap 
}: { 
  item: unknown; 
  index: number;
  setoresMap?: Map<number, string>;
  usuariosMap?: Map<number, string>;
}) {
  if (item == null) return null;
  if (typeof item !== "object") {
    return (
      <Box
        sx={{
          display: "flex",
          alignItems: "flex-start",
          gap: 1.5,
          mb: 2,
        }}
      >
        <Box
          sx={{
            width: 10,
            height: 10,
            borderRadius: "50%",
            bgcolor: "primary.main",
            mt: 0.8,
            flexShrink: 0,
          }}
        />
        <Paper variant="outlined" sx={{ p: 1.5, flex: 1, bgcolor: "background.paper" }}>
          <Typography variant="body2">{String(item)}</Typography>
        </Paper>
      </Box>
    );
  }
  const entries = Object.entries(item as Record<string, unknown>).filter(([, v]) => v != null && v !== "");
  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "flex-start",
        gap: 1.5,
        mb: 2,
      }}
    >
      <Box
        sx={{
          width: 10,
          height: 10,
          borderRadius: "50%",
          bgcolor: "primary.main",
          mt: 0.8,
          flexShrink: 0,
        }}
      />
      <Paper variant="outlined" sx={{ p: 1.5, flex: 1, bgcolor: "background.paper" }}>
        {entries.length === 0 ? (
          <Typography variant="body2" color="text.secondary">
            Entrada #{index + 1}
          </Typography>
        ) : (
          <Box sx={{ display: "flex", flexDirection: "column", gap: 0.75 }}>
            {entries.map(([key, value]) => (
              <Box key={key} sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
                <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600, minWidth: 120 }}>
                  {formatHistoricoKey(key)}:
                </Typography>
                <Typography variant="body2">{formatHistoricoValue(value, key, setoresMap, usuariosMap)}</Typography>
              </Box>
            ))}
          </Box>
        )}
      </Paper>
    </Box>
  );
}

function HistoricoContent({ 
  historico,
  setoresMap,
  usuariosMap 
}: { 
  historico?: unknown;
  setoresMap?: Map<number, string>;
  usuariosMap?: Map<number, string>;
}) {
  if (historico == null) {
    return (
      <Box sx={{ textAlign: "center", py: 3 }}>
        <Typography variant="body2" color="text.secondary">
          Nenhum histórico registrado para esta pendência.
        </Typography>
      </Box>
    );
  }
  if (Array.isArray(historico)) {
    return (
      <Box
        sx={{
          borderLeft: "2px solid",
          borderColor: "divider",
          pl: 2,
          ml: 0.5,
        }}
      >
        {historico.map((item, i) => (
          <HistoricoEntry key={i} item={item} index={i} setoresMap={setoresMap} usuariosMap={usuariosMap} />
        ))}
      </Box>
    );
  }
  if (typeof historico === "object") {
    const entries = Object.entries(historico as Record<string, unknown>).filter(([, v]) => v != null && v !== "");
    if (entries.length === 0) {
      return (
        <Typography variant="body2" color="text.secondary">
          Nenhum dado no histórico.
        </Typography>
      );
    }
    return (
      <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
        {entries.map(([key, value]) => (
          <Box key={key} sx={{ display: "flex", gap: 1, flexWrap: "wrap", alignItems: "baseline" }}>
            <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600, minWidth: 140 }}>
              {formatHistoricoKey(key)}:
            </Typography>
            <Typography variant="body2">{formatHistoricoValue(value, key, setoresMap, usuariosMap)}</Typography>
          </Box>
        ))}
      </Box>
    );
  }
  return <Typography variant="body2">{String(historico)}</Typography>;
}

export default function PendenciaDetails({ pendencia, onAtribuir, onSaved, onEdit, onTransferirProximaEtapa }: Props) {
  const [tab, setTab] = useState(0);
  const [anexos, setAnexos] = useState<AnexoItem[]>([]);
  const [setores, setSetores] = useState<{ id: number; nome_setor?: string }[]>([]);
  const [usuarios, setUsuarios] = useState<{ id: number; nomeUsuario?: string }[]>([]);
  const [loadingAcao, setLoadingAcao] = useState(false);
  const [uploadingAnexo, setUploadingAnexo] = useState(false);
  const [removingFilename, setRemovingFilename] = useState<string | null>(null);
  const { usuario } = useAuth();

  const carregarAnexos = async (pendenciaId: number) => {
    try {
      const raw = await getAnexos(pendenciaId);
      const enriched = await Promise.all(
        raw.map(async (d) => {
          const parts = d.filename.split("_");
          let uploadedAt: Date | undefined;
          let originalName = d.filename;
          if (parts.length >= 3) {
            const ts = Number(parts[1]);
            if (!Number.isNaN(ts)) {
              uploadedAt = new Date(ts);
            }
            originalName = parts.slice(2).join("_");
          }
          const dot = originalName.lastIndexOf(".");
          const ext = dot > -1 ? originalName.slice(dot + 1) : "";

          let sizeMB: number | undefined;
          try {
            const res = await fetch(d.url, { method: "HEAD" });
            const len = res.headers.get("content-length");
            if (len) {
              const bytes = Number(len);
              if (!Number.isNaN(bytes)) {
                sizeMB = bytes / (1024 * 1024);
              }
            }
          } catch {
            // ignora erro ao obter tamanho
          }

          return {
            filename: d.filename,
            url: d.url,
            originalName,
            ext,
            uploadedAt,
            sizeMB,
          } as AnexoItem;
        })
      );

      enriched.sort((a, b) => {
        const ta = a.uploadedAt?.getTime() ?? 0;
        const tb = b.uploadedAt?.getTime() ?? 0;
        return ta - tb;
      });

      setAnexos(enriched);
    } catch {
      setAnexos([]);
    }
  };

  // Cria mapas para busca rápida de nomes por ID
  const setoresMap = useMemo(() => {
    const map = new Map<number, string>();
    setores.forEach(s => {
      if (s.id && s.nome_setor) {
        map.set(s.id, s.nome_setor);
      }
    });
    return map;
  }, [setores]);

  const usuariosMap = useMemo(() => {
    const map = new Map<number, string>();
    usuarios.forEach(u => {
      if (u.id && u.nomeUsuario) {
        map.set(u.id, u.nomeUsuario);
      }
    });
    return map;
  }, [usuarios]);

  useEffect(() => {
    if (!pendencia) return;
    carregarAnexos(pendencia.id);
    getSetores().then(setSetores).catch(() => setSetores([]));
    getUsuarios().then(setUsuarios).catch(() => setUsuarios([]));
  }, [pendencia]);

  if (!pendencia) {
    return (
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: 280,
          textAlign: "center",
          color: "text.secondary",
          px: 2,
        }}
      >
        <Typography variant="body2">
          Selecione uma pendência na lista para ver os detalhes.
        </Typography>
      </Box>
    );
  }

  return (
    <Box className="pendencia-print-page" sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
      {/* Layout normal (telas) */}
      <Box className="screen-only" sx={{ display: "flex", flexDirection: "column", flex: 1, minHeight: 0 }}>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1, flexWrap: "wrap", mb: 1.5 }}>
          <Typography variant="h6" fontWeight={700} color="text.primary">
            Pendência {pendencia.numero ?? pendencia.id}
          </Typography>
          <StatusChip situacao={pendencia.situacao} />
          <PrioridadeChip prioridade={pendencia.prioridade} />
        </Box>

        <Box sx={{ mb: 2 }}>
          <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
            <Button
              className="no-print"
              variant="outlined"
              size="small"
              startIcon={<PrintRounded />}
              onClick={() => {
                const originalTitle = document.title;
                document.title = `Pendência ${pendencia.numero ?? pendencia.id}`;
                window.print();
                setTimeout(() => {
                  document.title = originalTitle;
                }, 500);
              }}
            >
              Imprimir
            </Button>
            <Button
              variant="outlined"
              size="small"
              startIcon={<EditRounded />}
              onClick={() => onEdit?.()}
            >
              Editar
            </Button>
            <Button
              variant="outlined"
              size="small"
              startIcon={<SwapHorizRounded />}
              onClick={() => onTransferirProximaEtapa?.()}
            >
              Próxima etapa
            </Button>
          </Box>
        </Box>

        <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ minHeight: 40, mb: 1 }}>
          <Tab label="Detalhes" id="pendencia-tab-0" aria-controls="pendencia-panel-0" />
          <Tab label="Histórico" id="pendencia-tab-1" aria-controls="pendencia-panel-1" />
        </Tabs>

        {tab === 0 && (
          <Box id="pendencia-panel-0" role="tabpanel" sx={{ flex: 1, minHeight: 0, overflow: "auto" }}>
            <DetailRow label="Número" value={pendencia.numero} />
            <DetailRow label="Equipamento" value={pendencia.equipamento} />
            <DetailRow label="Situação" value={pendencia.situacao} />
            <DetailRow label="Status" value={pendencia.status} />
            <DetailRow label="Prioridade" value={pendencia.prioridade} />
            <DetailRow label="Prazo (dias)" value={pendencia.prazoResposta} />
            <DetailRow label="Origem" value={pendencia.origem} />
            <DetailRow label="Versão" value={pendencia.versao} />
            {(pendencia.idUsuario != null || pendencia.idSetor != null) && (
              <Box sx={{ display: "flex", alignItems: "center", gap: 1, flexWrap: "wrap", mb: 1 }}>
                <DetailRow
                  label="Usuário / Setor"
                  value={[
                    pendencia.idUsuario != null 
                      ? (usuariosMap.get(pendencia.idUsuario) 
                          ? `${usuariosMap.get(pendencia.idUsuario)} (Usuário #${pendencia.idUsuario})`
                          : `Usuário #${pendencia.idUsuario}`)
                      : null,
                    pendencia.idSetor != null 
                      ? (setoresMap.get(pendencia.idSetor)
                          ? `${setoresMap.get(pendencia.idSetor)} (Setor #${pendencia.idSetor})`
                          : `Setor #${pendencia.idSetor}`)
                      : null,
                  ]
                    .filter(Boolean)
                    .join(" · ")}
                />
                {/* Botão "Atribuir" quando a pendência está apenas no setor */}
                {usuario &&
                  pendencia.idSetor != null &&
                  pendencia.idUsuario == null &&
                  usuario.idSetor === pendencia.idSetor &&
                  pendencia.statusTransferencia !== "PENDENTE" &&
                  onAtribuir && (
                    <Button
                      size="small"
                      variant="outlined"
                      onClick={onAtribuir}
                    >
                      Atribuir
                    </Button>
                  )}
                {/* Botões de Aceitar/Devolver quando a transferência está pendente */}
                {usuario &&
                  pendencia.statusTransferencia === "PENDENTE" &&
                  ((pendencia.idUsuario != null && pendencia.idUsuario === usuario.id) ||
                    (pendencia.idSetor != null && pendencia.idUsuario == null && usuario.idSetor === pendencia.idSetor)) && (
                    <Box sx={{ display: "flex", gap: 1 }}>
                      <Button
                        size="small"
                        variant="contained"
                        color="success"
                        disabled={loadingAcao}
                        onClick={async () => {
                          if (!pendencia) return;
                          try {
                            setLoadingAcao(true);
                            await aceitarTransferencia(pendencia.id);
                            onSaved?.();
                          } catch (e: any) {
                            alert(e?.message ?? "Erro ao aceitar transferência");
                          } finally {
                            setLoadingAcao(false);
                          }
                        }}
                      >
                        Aceitar
                      </Button>
                      <Button
                        size="small"
                        variant="outlined"
                        color="error"
                        disabled={loadingAcao}
                        onClick={async () => {
                          if (!pendencia) return;
                          if (!confirm("Tem certeza que deseja devolver esta transferência?")) return;
                          try {
                            setLoadingAcao(true);
                            await devolverTransferencia(pendencia.id);
                            onSaved?.();
                          } catch (e: any) {
                            alert(e?.message ?? "Erro ao devolver transferência");
                          } finally {
                            setLoadingAcao(false);
                          }
                        }}
                      >
                        Devolver
                      </Button>
                    </Box>
                  )}
              </Box>
            )}

            {pendencia.descricao && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 0.5 }}>
                  Observações
                </Typography>
                <Paper variant="outlined" sx={{ p: 1.5, bgcolor: "grey.50" }}>
                  <Typography variant="body2" sx={{ whiteSpace: "pre-wrap" }}>
                    {pendencia.descricao}
                  </Typography>
                </Paper>
              </Box>
            )}

            <Box
              sx={{
                mt: 2,
                pt: 2,
                borderTop: "1px solid",
                borderColor: "divider",
                display: "flex",
                flexWrap: "wrap",
                gap: 1.5,
                fontSize: "0.8rem",
                color: "text.secondary",
              }}
            >
              {pendencia.dataCriacao && (
                <span>Data criação: {new Date(pendencia.dataCriacao).toLocaleString("pt-BR")}</span>
              )}
              {pendencia.ultimaModificacao && (
                <span>Última modificação: {new Date(pendencia.ultimaModificacao).toLocaleString("pt-BR")}</span>
              )}
            </Box>

            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
                Anexos
              </Typography>
              {anexos.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  Nenhum anexo
                </Typography>
              ) : (
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Nº</TableCell>
                      <TableCell>Nome do arquivo</TableCell>
                      <TableCell>Tipo</TableCell>
                      <TableCell>Tamanho</TableCell>
                      <TableCell>Usuário</TableCell>
                      <TableCell>Remover</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {anexos.map((a, index) => (
                      <TableRow key={a.filename}>
                        <TableCell>{index + 1}</TableCell>
                        <TableCell>
                          <Link href={a.url} target="_blank" rel="noreferrer">
                            {a.originalName || a.filename}
                          </Link>
                        </TableCell>
                        <TableCell>{a.ext ? a.ext.toUpperCase() : "—"}</TableCell>
                        <TableCell>
                          {a.sizeMB != null ? `${a.sizeMB.toFixed(2)} MB` : "—"}
                        </TableCell>
                        <TableCell>{a.usuario ?? "—"}</TableCell>
                        <TableCell>
                          <Button
                            size="small"
                            color="error"
                            variant="text"
                            disabled={removingFilename === a.filename}
                            onClick={async () => {
                              if (!pendencia) return;
                              if (!confirm("Tem certeza que deseja remover este anexo?")) return;
                              try {
                                setRemovingFilename(a.filename);
                                await deleteAnexo(pendencia.id, a.filename);
                                await carregarAnexos(pendencia.id);
                              } catch (err: unknown) {
                                const msg = getErrorMessage(err);
                                alert(msg || "Falha ao remover anexo");
                              } finally {
                                setRemovingFilename(null);
                              }
                            }}
                          >
                            Remover
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}

              <Box sx={{ mt: 1, display: "flex", gap: 1, alignItems: "center" }}>
                <input
                  id="anexo-input"
                  type="file"
                  style={{ display: "none" }}
                  onChange={async (e) => {
                    if (!pendencia) return;
                    const selected = e.target.files?.[0] ?? null;
                    if (!selected) return;
                    try {
                      setUploadingAnexo(true);
                      await uploadAnexo(pendencia.id, selected);
                      await carregarAnexos(pendencia.id);
                    } catch (err: unknown) {
                      const msg = getErrorMessage(err);
                      alert(msg || "Falha no upload do anexo");
                    } finally {
                      setUploadingAnexo(false);
                      e.target.value = "";
                    }
                  }}
                />
                <label htmlFor="anexo-input">
                  <Button
                    component="span"
                    variant="outlined"
                    size="small"
                    startIcon={<UploadFileRounded />}
                    disabled={uploadingAnexo}
                  >
                    Anexar
                  </Button>
                </label>
                {uploadingAnexo && (
                  <Typography variant="caption" color="text.secondary">
                    Enviando anexo...
                  </Typography>
                )}
              </Box>
            </Box>
          </Box>
        )}

        {tab === 1 && (
          <Box id="pendencia-panel-1" role="tabpanel" sx={{ flex: 1, minHeight: 0, overflow: "auto" }}>
            <Paper variant="outlined" sx={{ p: 2, bgcolor: "grey.50" }}>
              <HistoricoContent historico={pendencia.historico} setoresMap={setoresMap} usuariosMap={usuariosMap} />
            </Paper>
          </Box>
        )}
      </Box>

      {/* Layout específico para impressão (detalhes + histórico sempre juntos) */}
      <Box className="print-only">
        <Box sx={{ mb: 2 }}>
          <Typography variant="h5" fontWeight={700}>
            Pendência {pendencia.numero ?? pendencia.id}
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            {pendencia.titulo}
          </Typography>
          <Box sx={{ mt: 1 }}>
            <StatusChip situacao={pendencia.situacao} />
          </Box>
        </Box>

        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
            Detalhes
          </Typography>
          <DetailRow label="Número" value={pendencia.numero} />
          <DetailRow label="Equipamento" value={pendencia.equipamento} />
          <DetailRow label="Situação" value={pendencia.situacao} />
          <DetailRow label="Status" value={pendencia.status} />
          <DetailRow label="Prioridade" value={pendencia.prioridade} />
          <DetailRow label="Prazo (dias)" value={pendencia.prazoResposta} />
          <DetailRow label="Origem" value={pendencia.origem} />
          <DetailRow label="Versão" value={pendencia.versao} />
          {(pendencia.idUsuario != null || pendencia.idSetor != null) && (
            <DetailRow
              label="Usuário / Setor"
              value={[
                pendencia.idUsuario != null 
                  ? (usuariosMap.get(pendencia.idUsuario) 
                      ? `${usuariosMap.get(pendencia.idUsuario)} (Usuário #${pendencia.idUsuario})`
                      : `Usuário #${pendencia.idUsuario}`)
                  : null,
                pendencia.idSetor != null 
                  ? (setoresMap.get(pendencia.idSetor)
                      ? `${setoresMap.get(pendencia.idSetor)} (Setor #${pendencia.idSetor})`
                      : `Setor #${pendencia.idSetor}`)
                  : null,
              ]
                .filter(Boolean)
                .join(" · ")}
            />
          )}
        </Box>

        {pendencia.descricao && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 0.5 }}>
              Observações
            </Typography>
            <Paper variant="outlined" sx={{ p: 1.5 }}>
              <Typography variant="body2" sx={{ whiteSpace: "pre-wrap" }}>
                {pendencia.descricao}
              </Typography>
            </Paper>
          </Box>
        )}

        <Box
          sx={{
            mt: 1,
            pt: 1,
            borderTop: "1px solid",
            borderColor: "divider",
            display: "flex",
            flexWrap: "wrap",
            gap: 1.5,
            fontSize: "0.8rem",
            color: "text.secondary",
          }}
        >
          {pendencia.dataCriacao && (
            <span>Data criação: {new Date(pendencia.dataCriacao).toLocaleString("pt-BR")}</span>
          )}
          {pendencia.ultimaModificacao && (
            <span>Última modificação: {new Date(pendencia.ultimaModificacao).toLocaleString("pt-BR")}</span>
          )}
        </Box>

        <Box sx={{ mt: 2 }}>
          <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
            Anexos
          </Typography>
          {anexos.length === 0 ? (
            <Typography variant="body2" color="text.secondary">
              Nenhum anexo
            </Typography>
          ) : (
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Nº</TableCell>
                  <TableCell>Nome do arquivo</TableCell>
                  <TableCell>Tipo</TableCell>
                  <TableCell>Tamanho</TableCell>
                  <TableCell>Usuário</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {anexos.map((a, index) => (
                  <TableRow key={a.filename}>
                    <TableCell>{index + 1}</TableCell>
                    <TableCell>{a.originalName || a.filename}</TableCell>
                    <TableCell>{a.ext ? a.ext.toUpperCase() : "—"}</TableCell>
                    <TableCell>
                      {a.sizeMB != null ? `${a.sizeMB.toFixed(2)} MB` : "—"}
                    </TableCell>
                    <TableCell>{a.usuario ?? "—"}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </Box>

        <Box sx={{ mt: 3 }}>
          <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
            Histórico
          </Typography>
          <HistoricoContent historico={pendencia.historico} setoresMap={setoresMap} usuariosMap={usuariosMap} />
        </Box>
      </Box>
    </Box>
  );
}
