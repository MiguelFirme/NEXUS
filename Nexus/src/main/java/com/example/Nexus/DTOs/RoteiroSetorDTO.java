package com.example.Nexus.DTOs;

import lombok.Data;

@Data
public class RoteiroSetorDTO {
    private Integer id;
    private Integer roteiroId;
    private Integer idSetor;
    private Integer ordem;
    private String nomeSetor; // Para facilitar no frontend
}
