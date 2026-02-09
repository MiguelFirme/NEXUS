package com.example.Nexus.DTOs;

import lombok.Data;
import java.util.List;

@Data
public class CreateRoteiroDTO {
    private String nome;
    private String descricao;
    private Boolean ativo;
    private List<SetorOrdemDTO> setores; // Lista de setores com suas ordens
}
