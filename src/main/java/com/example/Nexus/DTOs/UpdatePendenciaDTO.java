package com.example.Nexus.DTOs;

import lombok.Data;

@Data
public class UpdatePendenciaDTO {

    private String equipamento;
    private String situacao;
    private String status;
    private String prioridade;

    private Integer prazoResposta;
    private String observacoes;
    private String versao;
}
