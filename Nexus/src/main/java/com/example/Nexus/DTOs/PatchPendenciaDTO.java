package com.example.Nexus.DTOs;

import com.fasterxml.jackson.databind.JsonNode;
import lombok.Data;

@Data
public class PatchPendenciaDTO {

    private String equipamento;
    private String situacao;
    private String status;
    private String prioridade;
    private Integer prazoResposta;
    private String observacoes;
    private String versao;

    /**
     * Transferência / atribuição:
     * - idSetor: setor responsável pela pendência
     * - idUsuario: usuário responsável. Quando enviado como 0 (zero), será interpretado como "remover atribuição"
     *   e o campo idUsuario será definido como null na entidade.
     *
     * Ambos são opcionais no PATCH.
     */
    private Integer idSetor;
    private Integer idUsuario;

    // JSONB
    private JsonNode cliente;
    private JsonNode propostasVinculadas;
    private JsonNode historico;
}
