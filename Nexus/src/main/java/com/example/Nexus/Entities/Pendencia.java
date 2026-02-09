package com.example.Nexus.Entities;

import com.fasterxml.jackson.databind.JsonNode;
import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "pendencias", schema = "nexus")
public class Pendencia {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String numero;

    private LocalDateTime dataCriacao;
    private LocalDateTime dataAtualizacao;

    private String equipamento;
    private String situacao;
    private String status;
    private String prioridade;

    private Integer prazoResposta;
    private String origem;
    private String observacoes;
    private String versao;

    private LocalDateTime ultimaModificacao;
    private String modificadoPor;

    private Integer idUsuario;
    private Integer idSetor;
    private Integer idRoteiro; // Roteiro que a pendência deve seguir

    // 🔽 JSONB CORRETO
    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private JsonNode cliente;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private JsonNode propostasVinculadas;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private JsonNode historico;
}
