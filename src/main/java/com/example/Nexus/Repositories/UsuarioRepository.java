package com.example.Nexus.Repositories;

import com.example.Nexus.Entities.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface UsuarioRepository extends JpaRepository<Usuario, Integer> {

    Optional<Usuario> findByEmailUsuario(String emailUsuario);

    List<Usuario> findByIdSetor(Integer idSetor);

    List<Usuario> findByNivelUsuario(Integer nivelUsuario);
}
