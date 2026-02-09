package com.example.Nexus.Repositories;

import com.example.Nexus.Entities.RoteiroSetor;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RoteiroSetorRepository extends JpaRepository<RoteiroSetor, Integer> {
    List<RoteiroSetor> findByRoteiroIdOrderByOrdem(Integer roteiroId);
    void deleteByRoteiroId(Integer roteiroId);
}
