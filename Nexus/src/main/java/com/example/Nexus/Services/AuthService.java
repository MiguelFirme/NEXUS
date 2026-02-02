package com.example.Nexus.Services;

import com.example.Nexus.DTOs.UsuarioDTO;
import com.example.Nexus.Entities.Usuario;
import com.example.Nexus.Repositories.UsuarioRepository;
import com.example.Nexus.config.JwtService;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final UsuarioRepository usuarioRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    public AuthService(UsuarioRepository usuarioRepository, PasswordEncoder passwordEncoder, JwtService jwtService) {
        this.usuarioRepository = usuarioRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
    }

    /**
     * Login: valida nome de usuário e senha, retorna token JWT e dados do usuário (sem senha).
     */
    public LoginResult login(String nomeUsuario, String senha) {
        Usuario usuario = usuarioRepository.findByNomeUsuario(nomeUsuario)
                .orElseThrow(() -> new RuntimeException("Usuário ou senha inválidos."));
        if (usuario.getSenha() == null || usuario.getSenha().isBlank()) {
            throw new RuntimeException("Senha ainda não definida. Use \"Definir senha\" para criar sua senha.");
        }
        if (!passwordEncoder.matches(senha, usuario.getSenha())) {
            throw new RuntimeException("Usuário ou senha inválidos.");
        }
        String token = jwtService.generateToken(usuario.getId(), usuario.getEmailUsuario(), usuario.getIdSetor());
        UsuarioDTO dto = toDTO(usuario);
        return new LoginResult(token, dto);
    }

    /**
     * Define a primeira senha para um usuário que ainda não tem (senha nula).
     * Após definir, retorna token (login automático).
     */
    public LoginResult definirSenha(String nomeUsuario, String novaSenha) {
        Usuario usuario = usuarioRepository.findByNomeUsuario(nomeUsuario)
                .orElseThrow(() -> new RuntimeException("Usuário não encontrado."));
        if (usuario.getSenha() != null && !usuario.getSenha().isBlank()) {
            throw new RuntimeException("Este usuário já possui senha. Use o login normal.");
        }
        usuario.setSenha(passwordEncoder.encode(novaSenha));
        usuarioRepository.save(usuario);
        String token = jwtService.generateToken(usuario.getId(), usuario.getEmailUsuario(), usuario.getIdSetor());
        UsuarioDTO dto = toDTO(usuario);
        return new LoginResult(token, dto);
    }

    public static record LoginResult(String token, UsuarioDTO usuario) {}

    private UsuarioDTO toDTO(Usuario u) {
        UsuarioDTO dto = new UsuarioDTO();
        dto.setId(u.getId());
        dto.setNomeUsuario(u.getNomeUsuario());
        dto.setEmailUsuario(u.getEmailUsuario());
        dto.setIdSetor(u.getIdSetor());
        dto.setCargoUsuario(u.getCargoUsuario());
        dto.setNivelUsuario(u.getNivelUsuario());
        return dto;
    }
}
