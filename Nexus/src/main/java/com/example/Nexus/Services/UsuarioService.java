package com.example.Nexus.Services;

import com.example.Nexus.DTOs.UsuarioDTO;
import com.example.Nexus.Entities.Usuario;
import com.example.Nexus.Repositories.UsuarioRepository;
import org.springframework.stereotype.Service;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class UsuarioService {

    private final UsuarioRepository usuarioRepository;
    private final PasswordEncoder passwordEncoder;

    public UsuarioService(UsuarioRepository usuarioRepository, PasswordEncoder passwordEncoder) {
        this.usuarioRepository = usuarioRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public UsuarioDTO buscarPorId(Integer id) {
        return usuarioRepository.findById(id).map(this::toDTO).orElseThrow(() -> new RuntimeException("Usuário não encontrado."));
    }

    public UsuarioDTO atualizarNivel(Integer id, Integer novoNivel) {
        Usuario u = usuarioRepository.findById(id).orElseThrow(() -> new RuntimeException("Usuário não encontrado."));
        u.setNivelUsuario(novoNivel);
        usuarioRepository.save(u);
        return toDTO(u);
    }

    public void atualizarSenha(Integer id, String novaSenha) {
        Usuario u = usuarioRepository.findById(id).orElseThrow(() -> new RuntimeException("Usuário não encontrado."));
        u.setSenha(passwordEncoder.encode(novaSenha));
        usuarioRepository.save(u);
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

    public UsuarioDTO criar(UsuarioDTO dto) {
        Usuario u = new Usuario();
        u.setId(dto.getId());
        u.setNomeUsuario(dto.getNomeUsuario());
        u.setTelefoneUsuario(dto.getTelefoneUsuario());
        u.setEmailUsuario(dto.getEmailUsuario());
        u.setComputadorUsuario(dto.getComputadorUsuario());
        u.setCargoUsuario(dto.getCargoUsuario());
        u.setNivelUsuario(dto.getNivelUsuario() != null ? dto.getNivelUsuario() : 1);
        u.setIdSetor(dto.getIdSetor());
        // A senha inicial será nula, o usuário deve definir no primeiro acesso via /auth/definir-senha
        return toDTO(usuarioRepository.save(u));
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
