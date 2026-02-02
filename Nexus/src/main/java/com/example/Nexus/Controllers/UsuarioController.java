package com.example.Nexus.Controllers;

import com.example.Nexus.DTOs.UsuarioDTO;
import com.example.Nexus.Services.UsuarioService;
import com.example.Nexus.config.CurrentUser;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/usuarios")
public class UsuarioController {

    private final UsuarioService usuarioService;

    public UsuarioController(UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
    }

    @GetMapping
    public List<UsuarioDTO> listarTodos() {
        return usuarioService.listarTodos();
    }

    @GetMapping("/{id}")
    public UsuarioDTO porId(@PathVariable Integer id) {
        return usuarioService.buscarPorId(id);
    }

    /** Atualiza o nível de um usuário (somente nível 4 pode alterar). */
    @PatchMapping("/{id}/nivel")
    public UsuarioDTO atualizarNivel(@PathVariable Integer id, @RequestBody Map<String, Integer> body, Authentication authentication) {
        CurrentUser current = (CurrentUser) authentication.getPrincipal();
        // verificar se usuário atual é nível 4
        UsuarioDTO atual = usuarioService.buscarPorId(current.getId());
        if (atual.getNivelUsuario() == null || atual.getNivelUsuario() != 4) {
            throw new RuntimeException("Acesso negado");
        }
        Integer novo = body.get("nivel");
        if (novo == null) throw new RuntimeException("Nível inválido");
        return usuarioService.atualizarNivel(id, novo);
    }

    /** Atualiza a senha de um usuário (somente nível 4 pode alterar). */
    @PatchMapping("/{id}/senha")
    public ResponseEntity<?> atualizarSenha(@PathVariable Integer id, @RequestBody Map<String, String> body, Authentication authentication) {
        CurrentUser current = (CurrentUser) authentication.getPrincipal();
        UsuarioDTO atual = usuarioService.buscarPorId(current.getId());
        if (atual.getNivelUsuario() == null || atual.getNivelUsuario() != 4) {
            return ResponseEntity.status(403).body(Map.of("message", "Acesso negado"));
        }
        String nova = body.get("novaSenha");
        if (nova == null || nova.isBlank()) return ResponseEntity.badRequest().body(Map.of("message", "Nova senha obrigatória"));
        usuarioService.atualizarSenha(id, nova);
        return ResponseEntity.ok(Map.of("message", "Senha atualizada"));
    }

    @GetMapping("/setor/{idSetor}")
    public List<UsuarioDTO> porSetor(@PathVariable Integer idSetor) {
        return usuarioService.buscarPorSetor(idSetor);
    }

    @GetMapping("/nivel/{nivel}")
    public List<UsuarioDTO> porNivel(@PathVariable Integer nivel) {
        return usuarioService.buscarPorNivel(nivel);
    }

    @GetMapping("/email/{email}")
    public UsuarioDTO porEmail(@PathVariable String email) {
        return usuarioService.buscarPorEmail(email)
                .orElseThrow(() -> new RuntimeException("Usuário não encontrado"));
    }
}
