package com.example.Nexus.Entities;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import lombok.Data;

@Data
@Entity
@Table(name = "setores", schema="nexus")
public class Setor {

    @Id
    @Column(name = "id_setor")
    private Integer id;

    private String nome_setor;
}

