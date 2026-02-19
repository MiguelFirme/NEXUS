package com.example.Nexus.Repositories;

import com.example.Nexus.Entities.RoteiroPasso;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RoteiroPassoRepository extends JpaRepository<RoteiroPasso, Integer> {
    List<RoteiroPasso> findByRoteiroIdOrderByOrdem(Integer roteiroId);
    void deleteByRoteiroId(Integer roteiroId);
}
