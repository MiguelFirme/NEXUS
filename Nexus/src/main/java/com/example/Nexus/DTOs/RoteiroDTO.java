package com.example.Nexus.DTOs;

import lombok.Data;
import java.time.LocalDateTime;
import java.util.List;

@Data
public class RoteiroDTO {
    private Integer id;
    private String nome;
    private String descricao;
    private Boolean ativo;
    private LocalDateTime dataCriacao;
    /** Passos na ordem: SETOR (idSetor, nomeSetor) ou USUARIO (idUsuario, nomeUsuario). */
    private List<PassoRoteiroExibicaoDTO> passos;
}
