package com.example.Nexus.DTOs;

import lombok.Data;

@Data
public class PassoRoteiroExibicaoDTO {
    private Integer id;
    private Integer ordem;
    private String tipo; // "SETOR" ou "USUARIO"
    private Integer idSetor;
    private String nomeSetor;
    private Integer idUsuario;
    private String nomeUsuario;
}
