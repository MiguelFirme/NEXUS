package com.example.Nexus.Entities;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "roteiro_setores", schema = "nexus")
public class RoteiroSetor {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "roteiro_id", nullable = false)
    private Integer roteiroId;

    @Column(name = "id_setor", nullable = false)
    private Integer idSetor;

    @Column(name = "ordem", nullable = false)
    private Integer ordem; // Ordem na sequência do roteiro (1, 2, 3, ...)

    // Relacionamento com Roteiro (opcional, para facilitar queries)
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "roteiro_id", insertable = false, updatable = false)
    private Roteiro roteiro;
}
