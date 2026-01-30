package com.example.Nexus.config;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Representa o usuário autenticado (extraído do JWT) para uso nos controllers.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class CurrentUser {
    private Integer id;
    private String emailUsuario;
    private Integer idSetor;
}
