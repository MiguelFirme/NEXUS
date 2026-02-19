package com.example.Nexus.Entities;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "roteiro_passos", schema = "nexus")
public class RoteiroPasso {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "roteiro_id", nullable = false)
    private Integer roteiroId;

    @Column(name = "ordem", nullable = false)
    private Integer ordem;

    @Column(name = "tipo", nullable = false, length = 20)
    private String tipo; // "SETOR" ou "USUARIO"

    @Column(name = "id_setor")
    private Integer idSetor;

    @Column(name = "id_usuario")
    private Integer idUsuario;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "roteiro_id", insertable = false, updatable = false)
    private Roteiro roteiro;
}
