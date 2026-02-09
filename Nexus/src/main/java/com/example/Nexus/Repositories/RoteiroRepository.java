package com.example.Nexus.Repositories;

import com.example.Nexus.Entities.Roteiro;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RoteiroRepository extends JpaRepository<Roteiro, Integer> {
    List<Roteiro> findByAtivoTrue();
}
