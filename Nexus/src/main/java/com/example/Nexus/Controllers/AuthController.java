package com.example.Nexus.Controllers;

import com.example.Nexus.Services.AuthService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody Map<String, String> body) {
        String nomeUsuario = body.get("nomeUsuario");
        String senha = body.get("senha");
        if (nomeUsuario == null || nomeUsuario.isBlank() || senha == null || senha.isBlank()) {
            return ResponseEntity.badRequest().body(Map.of("message", "Nome de usuário e senha são obrigatórios."));
        }
        try {
            AuthService.LoginResult result = authService.login(nomeUsuario.trim(), senha);
            return ResponseEntity.ok(Map.of(
                    "token", result.token(),
                    "usuario", result.usuario()
            ));
        } catch (RuntimeException e) {
            return ResponseEntity.status(401).body(Map.of("message", e.getMessage()));
        }
    }

    /**
     * Define a primeira senha (quando o usuário ainda não tem senha no banco).
     */
    @PostMapping("/definir-senha")
    public ResponseEntity<?> definirSenha(@RequestBody Map<String, String> body) {
        String nomeUsuario = body.get("nomeUsuario");
        String novaSenha = body.get("novaSenha");
        if (nomeUsuario == null || nomeUsuario.isBlank() || novaSenha == null || novaSenha.isBlank()) {
            return ResponseEntity.badRequest().body(Map.of("message", "Nome de usuário e nova senha são obrigatórios."));
        }
        try {
            AuthService.LoginResult result = authService.definirSenha(nomeUsuario.trim(), novaSenha);
            return ResponseEntity.ok(Map.of(
                    "token", result.token(),
                    "usuario", result.usuario()
            ));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(Map.of("message", e.getMessage()));
        }
    }
}
