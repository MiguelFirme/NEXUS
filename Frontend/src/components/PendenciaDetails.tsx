import { useState } from "react";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";
import type { Pendencia } from "../types";
import { uploadAnexo, getAnexos } from "../services/api";
import Link from "@mui/material/Link";
import IconButton from "@mui/material/IconButton";
import UploadFileRounded from "@mui/icons-material/UploadFileRounded";
import Image from "@mui/material/CardMedia";
import { useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";

type Props = { pendencia: Pendencia | null; onAtribuir?: () => void };

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
  idSetor: "Id Setor",
  idSetorAnterior: "Id Setor anterior",
  idUsuario: "Id Usuário",
  idUsuarioAnterior: "Id Usuário anterior",
  status: "Status",
  statusAnterior: "Status anterior",
};

function formatHistoricoKey(key: string): string {
  return HISTORICO_LABELS[key] ?? key.replace(/([A-Z])/g, " $1").replace(/^./, (s) => s.toUpperCase());
}

function formatHistoricoValue(value: unknown): string {
  if (value == null) return "—";
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

function HistoricoEntry({ item, index }: { item: unknown; index: number }) {
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
                <Typography variant="body2">{formatHistoricoValue(value)}</Typography>
              </Box>
            ))}
          </Box>
        )}
      </Paper>
    </Box>
  );
}

function HistoricoContent({ historico }: { historico?: unknown }) {
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
          <HistoricoEntry key={i} item={item} index={i} />
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
            <Typography variant="body2">{formatHistoricoValue(value)}</Typography>
          </Box>
        ))}
      </Box>
    );
  }
  return <Typography variant="body2">{String(historico)}</Typography>;
}

export default function PendenciaDetails({ pendencia, onAtribuir }: Props) {
  const [tab, setTab] = useState(0);
  const [anexos, setAnexos] = useState<{ filename: string; url: string }[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const { usuario } = useAuth();

  useEffect(() => {
    if (!pendencia) return;
    getAnexos(pendencia.id).then(setAnexos).catch(() => setAnexos([]));
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
    <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ minHeight: 40, mb: 1 }}>
        <Tab label="Detalhes" id="pendencia-tab-0" aria-controls="pendencia-panel-0" />
        <Tab label="Histórico" id="pendencia-tab-1" aria-controls="pendencia-panel-1" />
      </Tabs>

      {tab === 0 && (
        <Box id="pendencia-panel-0" role="tabpanel" sx={{ flex: 1, minHeight: 0, overflow: "auto" }}>
          <Box sx={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 1, mb: 2 }}>
            <Typography variant="h6" fontWeight={600} sx={{ flex: 1 }}>
              {pendencia.titulo}
            </Typography>
            <StatusChip situacao={pendencia.situacao} />
          </Box>

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
                  pendencia.idUsuario != null ? `Usuário #${pendencia.idUsuario}` : null,
                  pendencia.idSetor != null ? `Setor #${pendencia.idSetor}` : null,
                ]
                  .filter(Boolean)
                  .join(" · ")}
              />
              {/* Botão \"Atribuir\" quando a pendência está apenas no setor */}
              {usuario &&
                pendencia.idSetor != null &&
                pendencia.idUsuario == null &&
                usuario.idSetor === pendencia.idSetor &&
                onAtribuir && (
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={onAtribuir}
                  >
                    Atribuir
                  </Button>
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
            {pendencia.data && <span>Data criação: {new Date(pendencia.data).toLocaleString("pt-BR")}</span>}
            {pendencia.ultimaModificacao && (
              <span>Última modificação: {new Date(pendencia.ultimaModificacao).toLocaleString("pt-BR")}</span>
            )}
          </Box>

          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
              Anexos
            </Typography>
            <Box sx={{ display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap" }}>
              {anexos.length === 0 ? (
                <Typography variant="body2" color="text.secondary">Nenhum anexo</Typography>
              ) : (
                anexos.map((a) => (
                  <Box key={a.filename} sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                    <Link href={a.url} target="_blank" rel="noreferrer">{a.filename}</Link>
                  </Box>
                ))
              )}
            </Box>

            <Box sx={{ mt: 1, display: "flex", gap: 1, alignItems: "center" }}>
              <input id="anexo-input" type="file" style={{ display: "none" }} onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
              <label htmlFor="anexo-input">
                <IconButton component="span" color="primary" aria-label="Anexar">
                  <UploadFileRounded />
                </IconButton>
              </label>
              <Button variant="outlined" size="small" onClick={async () => {
                if (!file || !pendencia) return;
                try {
                  await uploadAnexo(pendencia.id, file);
                  const list = await getAnexos(pendencia.id);
                  setAnexos(list);
                  setFile(null);
                } catch (e:any) {
                  alert(e?.message ?? 'Falha no upload');
                }
              }}>
                Enviar anexo
              </Button>
            </Box>
          </Box>
        </Box>
      )}

      {tab === 1 && (
        <Box id="pendencia-panel-1" role="tabpanel" sx={{ flex: 1, minHeight: 0, overflow: "auto" }}>
          <Paper variant="outlined" sx={{ p: 2, bgcolor: "grey.50" }}>
            <HistoricoContent historico={pendencia.historico} />
          </Paper>
        </Box>
      )}
    </Box>
  );
}
