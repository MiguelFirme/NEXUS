package com.example.Nexus.Repositories;

import com.example.Nexus.Entities.Pendencia;
import org.springframework.data.jpa.repository.JpaRepository;

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
}
