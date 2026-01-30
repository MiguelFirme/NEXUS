package com.example.Nexus.Controllers;

import com.example.Nexus.DTOs.UsuarioDTO;
import com.example.Nexus.Services.UsuarioService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

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
