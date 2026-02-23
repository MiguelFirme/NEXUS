package com.example.Nexus.Repositories;

import com.example.Nexus.Entities.Pendencia;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.time.LocalDateTime;
import java.util.List;

public interface PendenciaRepository extends JpaRepository<Pendencia, Integer> {

    List<Pendencia> findByStatus(String status);

    List<Pendencia> findBySituacao(String situacao);

    List<Pendencia> findByIdUsuario(Integer idUsuario);

    List<Pendencia> findByIdSetor(Integer idSetor);

    List<Pendencia> findByDataCriacaoBetween(
            LocalDateTime inicio,
            LocalDateTime fim
    );

    /**
     * Maior valor numérico da coluna numero (apenas registros em que numero é numérico).
     * Usado para gerar o próximo número em ordem crescente (max + 1).
     */
    @Query(value = "SELECT COALESCE(MAX(CAST(TRIM(numero) AS INTEGER)), 0) FROM nexus.pendencias WHERE numero IS NOT NULL AND TRIM(numero) <> '' AND TRIM(numero) ~ '^[0-9]+$'", nativeQuery = true)
    Integer findMaxNumeroAsInteger();
}
