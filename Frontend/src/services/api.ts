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

export async function getPendencias(): Promise<Pendencia[]> {
  const res = await api.get<PendenciaDTO[]>("/pendencias");
  return (res.data ?? []).map(toPendencia);
}

export async function createPendencia(payload: CreatePendenciaPayload): Promise<PendenciaDTO> {
  const res = await api.post<PendenciaDTO>("/pendencias", payload);
  return res.data;
}

export async function updatePendencia(id: number, payload: PatchPendenciaPayload): Promise<PendenciaDTO> {
  const res = await api.patch<PendenciaDTO>(`/pendencias/${id}`, payload);
  return res.data;
}

/** Lista de usuários (GET /usuarios) */
export async function getUsuarios(): Promise<{ id: number; nomeUsuario?: string }[]> {
  const res = await api.get<{ id: number; nomeUsuario?: string }[]>("/usuarios");
  return res.data ?? [];
}

/** Lista de setores (GET /setores) */
export async function getSetores(): Promise<{ id: number; nome_setor?: string }[]> {
  const res = await api.get<{ id: number; nome_setor?: string }[]>("/setores");
  return res.data ?? [];
}
