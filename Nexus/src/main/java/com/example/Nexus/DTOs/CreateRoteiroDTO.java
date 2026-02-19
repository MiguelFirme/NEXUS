package com.example.Nexus.DTOs;

import lombok.Data;
import java.util.List;

@Data
public class CreateRoteiroDTO {
    private String nome;
    private String descricao;
    private Boolean ativo;
    /** Passos na ordem: cada passo é SETOR (idSetor) ou USUARIO (idUsuario). */
    private List<PassoRoteiroDTO> passos;
}
