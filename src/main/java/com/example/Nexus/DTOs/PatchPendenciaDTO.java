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

    // JSONB
    private JsonNode cliente;
    private JsonNode propostasVinculadas;
    private JsonNode historico;
}
