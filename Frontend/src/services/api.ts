import axios from "axios";
import type { PendenciaDTO, Pendencia, CreatePendenciaPayload, PatchPendenciaPayload } from "../types";

const baseURL = import.meta.env.VITE_API_URL ?? "http://localhost:8080";

/** Extrai mensagem legível de erro (axios ou outro). */
export function getErrorMessage(err: unknown): string {
  if (axios.isAxiosError(err) && err.response?.data != null) {
    const d = err.response.data;
    if (typeof d === "string") return d;
    if (typeof d === "object" && d !== null && "message" in d && typeof (d as { message: unknown }).message === "string")
      return (d as { message: string }).message;
    return "Erro na requisição";
  }
  return err instanceof Error ? err.message : "Erro desconhecido";
}

const api = axios.create({
  baseURL,
  timeout: 10000,
  headers: { "Content-Type": "application/json" },
});

// Nome usado no AuthContext para persistir token
const STORAGE_TOKEN = "nexus_token";

// Adiciona Authorization automaticamente quando houver token no localStorage
api.interceptors.request.use((config) => {
  try {
    const token = localStorage.getItem(STORAGE_TOKEN);
    if (token && config.headers) {
      (config.headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
    }
  } catch {
    // ignore (e.g. SSR or privacy settings)
  }
  return config;
});

// Interceptor de resposta para normalizar erros e limpar token em 401
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (axios.isAxiosError(err) && err.response?.status === 401) {
      try {
        localStorage.removeItem(STORAGE_TOKEN);
        localStorage.removeItem("nexus_usuario");
      } catch {}
    }
    return Promise.reject(err);
  }
);

/** Converte PendenciaDTO do backend para o formato usado na UI */
function toPendencia(dto: PendenciaDTO): Pendencia {
  const data = dto.dataCriacao ?? "";
  const dateOnly = data.slice(0, 10);
  const timePart = data.slice(11, 16); // HH:mm
  return {
    ...dto,
    titulo: dto.numero ?? dto.equipamento ?? "Pendência",
    descricao: dto.observacoes,
    data: dateOnly,
    hora: timePart || undefined,
    situacao: dto.situacao ?? dto.status,
  };
}

export async function getPendencias(usuarioId?: number): Promise<Pendencia[]> {
  const params = usuarioId != null ? { params: { usuarioId } } : {};
  const res = await api.get<PendenciaDTO[]>("/pendencias", params);
  return (res.data ?? []).map(toPendencia);
}

export async function createPendencia(payload: CreatePendenciaPayload): Promise<PendenciaDTO> {
  const res = await api.post<PendenciaDTO>("/pendencias", payload);
  return res.data;
}

export async function deletePendencia(id: number): Promise<void> {
  await api.delete(`/pendencias/${id}`);
}

export async function updatePendencia(id: number, payload: PatchPendenciaPayload): Promise<PendenciaDTO> {
  const res = await api.patch<PendenciaDTO>(`/pendencias/${id}`, payload);
  return res.data;
}

/** Transferência / atribuição de pendência (atalho para PATCH com idSetor/idUsuario) */
export async function transferirPendencia(
  id: number,
  payload: Pick<PatchPendenciaPayload, "idSetor" | "idUsuario">
): Promise<PendenciaDTO> {
  const res = await api.patch<PendenciaDTO>(`/pendencias/${id}`, payload);
  return res.data;
}

/** Anexos: upload and list */
export async function uploadAnexo(pendenciaId: number, file: File): Promise<{ filename: string; url: string }> {
  const fd = new FormData();
  fd.append("file", file);
  const res = await api.post(`/pendencias/${pendenciaId}/anexos`, fd, { headers: { "Content-Type": "multipart/form-data" } });
  const d = res.data as { filename: string; url: string };
  const u = d.url && (d.url as string).startsWith("http") ? d.url : `${baseURL}${d.url}`;
  return { filename: d.filename, url: u };
}

export async function getAnexos(pendenciaId: number): Promise<{ filename: string; url: string }[]> {
  const res = await api.get<{ filename: string; url: string }[]>(`/pendencias/${pendenciaId}/anexos`);
  const list = res.data ?? [];
  return list.map((d) => ({ filename: d.filename, url: d.url && d.url.startsWith("http") ? d.url : `${baseURL}${d.url}` }));
}

/** Lista de usuários (GET /usuarios) */
export async function getUsuarios(): Promise<{ id: number; nomeUsuario?: string; emailUsuario?: string; idSetor?: number; nivelUsuario?: number }[]> {
  const res = await api.get<{ id: number; nomeUsuario?: string; emailUsuario?: string; idSetor?: number; nivelUsuario?: number }[]>("/usuarios");
  return res.data ?? [];
}

/** Lista de setores (GET /setores) */
export async function getSetores(): Promise<{ id: number; nome_setor?: string }[]> {
  const res = await api.get<{ id: number; nome_setor?: string }[]>("/setores");
  return res.data ?? [];
}

/** Autenticação (usado pelo AuthContext ou diretamente) */
export async function login(nomeUsuario: string, senha: string): Promise<{ token: string; usuario: unknown }> {
  const res = await api.post("/auth/login", { nomeUsuario: nomeUsuario.trim(), senha });
  return res.data;
}

export async function definirSenha(nomeUsuario: string, novaSenha: string): Promise<{ token: string; usuario: unknown }> {
  const res = await api.post("/auth/definir-senha", { nomeUsuario: nomeUsuario.trim(), novaSenha });
  return res.data;
}

// Usuários: atualizar nível e senha (admin nivel 4)
export async function atualizarNivelUsuario(id: number, nivel: number): Promise<unknown> {
  const res = await api.patch(`/usuarios/${id}/nivel`, { nivel });
  return res.data;
}

export async function atualizarSenhaUsuario(id: number, novaSenha: string): Promise<unknown> {
  const res = await api.patch(`/usuarios/${id}/senha`, { novaSenha });
  return res.data;
}

export async function criarUsuario(payload: any): Promise<any> {
  const res = await api.post("/usuarios", payload);
  return res.data;
}
