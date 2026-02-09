package com.example.Nexus.DTOs;

import com.fasterxml.jackson.databind.JsonNode;
import lombok.Data;

@Data
public class CreatePendenciaDTO {

    private String numero;
    private String equipamento;
    private String situacao;
    private String status;
    private String prioridade;

    private Integer prazoResposta;
    private String origem;
    private String observacoes;
    private String versao;

    private Integer idUsuario;
    private Integer idSetor;
    private Integer idRoteiro;

    // JSONB
    private JsonNode cliente;
    private JsonNode propostasVinculadas;
    private JsonNode historico;
}