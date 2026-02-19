package com.example.Nexus.DTOs;

import lombok.Data;

@Data
public class PassoRoteiroDTO {
    private String tipo; // "SETOR" ou "USUARIO"
    private Integer idSetor;
    private Integer idUsuario;
    private Integer ordem;
}
