package com.example.Nexus.DTOs;

import com.fasterxml.jackson.databind.JsonNode;
import lombok.Data;

import java.time.LocalDateTime;

@Data
public class PendenciaDTO {

    private Integer id;
    private String numero;

    private LocalDateTime dataCriacao;
    private LocalDateTime ultimaModificacao;

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
    
    /** Status da transferência: PENDENTE, ACEITA, DEVOLVIDA, ou null */
    private String statusTransferencia;

    /** Histórico da pendência (JSONB). */
    private JsonNode historico;
}
