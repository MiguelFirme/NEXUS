package com.example.Nexus.DTOs;

import lombok.Data;

@Data
public class UsuarioDTO {

    private Integer id;
    private String nomeUsuario;
    private String telefoneUsuario;
    private String emailUsuario;
    private String computadorUsuario;
    private String cargoUsuario;
    private Integer nivelUsuario;
    private Integer idSetor;
}
