package com.example.Nexus.Services;

import com.example.Nexus.DTOs.UsuarioDTO;
import com.example.Nexus.Entities.Usuario;
import com.example.Nexus.Repositories.UsuarioRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class UsuarioService {

    private final UsuarioRepository usuarioRepository;

    public UsuarioService(UsuarioRepository usuarioRepository) {
        this.usuarioRepository = usuarioRepository;
    }

    public List<UsuarioDTO> listarTodos() {
        return usuarioRepository.findAll()
                .stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    public Optional<UsuarioDTO> buscarPorEmail(String email) {
        return usuarioRepository.findByEmailUsuario(email)
                .map(this::toDTO);
    }

    public List<UsuarioDTO> buscarPorSetor(Integer idSetor) {
        return usuarioRepository.findByIdSetor(idSetor)
                .stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    public List<UsuarioDTO> buscarPorNivel(Integer nivel) {
        return usuarioRepository.findByNivelUsuario(nivel)
                .stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    private UsuarioDTO toDTO(Usuario usuario) {
        UsuarioDTO dto = new UsuarioDTO();
        dto.setId(usuario.getId());
        dto.setNomeUsuario(usuario.getNomeUsuario());
        dto.setTelefoneUsuario(usuario.getTelefoneUsuario());
        dto.setEmailUsuario(usuario.getEmailUsuario());
        dto.setComputadorUsuario(usuario.getComputadorUsuario());
        dto.setCargoUsuario(usuario.getCargoUsuario());
        dto.setNivelUsuario(usuario.getNivelUsuario());
        dto.setIdSetor(usuario.getIdSetor());
        return dto;
    }
}
