package com.example.Nexus.DTOs;

import lombok.Data;

import java.util.List;

@Data
public class EstatisticasPendenciasDTO {

    /** Total de pendências criadas no período (ou todas se sem filtro). */
    private long totalCriadas;

    /** Quantidade de pendências em atraso (prazo vencido). */
    private long quantidadeAtraso;

    /** Contagem por status (ex.: Aberta, Fechada). Chave = status, valor = quantidade. */
    private List<ContagemDTO> porStatus;

    /** Contagem por situação. */
    private List<ContagemDTO> porSituacao;

    /** Contagem por prioridade (Alta, Média, Baixa). */
    private List<ContagemDTO> porPrioridade;

    @Data
    public static class ContagemDTO {
        private String valor;   // ex: "Aberta", "Alta"
        private long quantidade;
    }
}
