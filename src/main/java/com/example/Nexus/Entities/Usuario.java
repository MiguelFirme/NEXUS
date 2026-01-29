package com.example.Nexus.Entities;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "usuarios", schema = "nexus")
public class Usuario {

    @Id
    @Column(name = "codigo_usuario")
    private Integer id;

    @Column(name = "nome_usuario")
    private String nomeUsuario;

    @Column(name = "telefone_usuario")
    private String telefoneUsuario;

    @Column(name = "email_usuario")
    private String emailUsuario;

    @Column(name = "computador_usuario")
    private String computadorUsuario;

    @Column(name = "cargo_usuario")
    private String cargoUsuario;

    @Column(name = "nivel_usuario")
    private Integer nivelUsuario;

    @Column(name = "id_setor")
    private Integer idSetor;
}
