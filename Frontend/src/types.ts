/** Resposta do backend (PendenciaDTO) */
export type PendenciaDTO = {
  id: number;
  numero?: string;
  dataCriacao?: string; // ISO
  ultimaModificacao?: string; // ISO
  equipamento?: string;
  situacao?: string;
  status?: string;
  prioridade?: string;
  prazoResposta?: number;
  origem?: string;
  observacoes?: string;
  versao?: string;
  idUsuario?: number;
  idSetor?: number;
  historico?: unknown;
};

/** Payload para criar pendência (CreatePendenciaDTO) */
export type CreatePendenciaPayload = {
  numero?: string;
  equipamento?: string;
  situacao?: string;
  status?: string;
  prioridade?: string;
  prazoResposta?: number;
  origem?: string;
  observacoes?: string;
  versao?: string;
  idUsuario?: number;
  idSetor?: number;
};

/** Payload para PATCH (PatchPendenciaDTO) */
export type PatchPendenciaPayload = Partial<{
  equipamento: string;
  situacao: string;
  status: string;
  prioridade: string;
  prazoResposta: number;
  observacoes: string;
  versao: string;
}>;

/** Tipo usado na UI: mapeado do DTO para exibição */
export type Pendencia = PendenciaDTO & {
  /** Título para lista/detalhes: numero || equipamento || "Pendência" */
  titulo?: string;
  /** Descrição: observacoes */
  descricao?: string;
  /** Data para exibição: dataCriacao */
  data?: string;
  /** Hora extraída de dataCriacao (opcional) */
  hora?: string;
  /** Flag indicando se está atrasada (prazo vencido) */
  atrasada?: boolean;
};
