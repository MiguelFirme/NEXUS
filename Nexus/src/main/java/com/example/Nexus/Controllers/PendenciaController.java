package com.example.Nexus.Controllers;

import com.example.Nexus.DTOs.CreatePendenciaDTO;
import com.example.Nexus.DTOs.PatchPendenciaDTO;
import com.example.Nexus.DTOs.UpdatePendenciaDTO;
import com.example.Nexus.DTOs.PendenciaDTO;
import com.example.Nexus.Entities.Pendencia;
import com.example.Nexus.Services.PendenciaService;
import com.example.Nexus.config.CurrentUser;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/pendencias")
public class PendenciaController {

    private final PendenciaService pendenciaService;
    private final com.example.Nexus.Services.UsuarioService usuarioService;

    public PendenciaController(PendenciaService pendenciaService, com.example.Nexus.Services.UsuarioService usuarioService) {
        this.pendenciaService = pendenciaService;
        this.usuarioService = usuarioService;
    }

    /**
     * Lista pendências conforme o usuário logado: por setor (se tiver) ou por usuário.
     * Usuários nível 4+ podem usar o parâmetro ?usuarioId= para ver pendências de outro usuário.
     */
    @GetMapping
    public List<PendenciaDTO> listarTodas(
            Authentication authentication,
            @RequestParam(required = false) Integer usuarioId
    ) {
        CurrentUser user = (CurrentUser) authentication.getPrincipal();
        
        // Se usuário nível 4+ especificou um usuarioId, lista pendências daquele usuário
        if (usuarioId != null) {
            var atual = usuarioService.buscarPorId(user.getId());
            if (atual.getNivelUsuario() != null && atual.getNivelUsuario() >= 4) {
                return pendenciaService.listarPorUsuario(usuarioId);
            }
        }
        
        // Comportamento padrão: lista pendências do próprio usuário/setor
        return pendenciaService.listarParaUsuario(user.getId(), user.getIdSetor());
    }

    @GetMapping("/usuario/{idUsuario}")
    public List<PendenciaDTO> porUsuario(@PathVariable Integer idUsuario) {
        return pendenciaService.listarPorUsuario(idUsuario);
    }

    @GetMapping("/setor/{idSetor}")
    public List<PendenciaDTO> porSetor(@PathVariable Integer idSetor) {
        return pendenciaService.listarPorSetor(idSetor);
    }

    @PostMapping
    public PendenciaDTO criar(@RequestBody CreatePendenciaDTO dto) {
        return pendenciaService.criar(dto);
    }

    @PutMapping("/{id}")
    public PendenciaDTO atualizar(
            @PathVariable Integer id,
            @RequestBody UpdatePendenciaDTO dto
    ) {
        return pendenciaService.atualizar(id, dto);
    }

    @PatchMapping("/{id}")
    public PendenciaDTO patch(
            @PathVariable Integer id,
            @RequestBody PatchPendenciaDTO dto
    ) {
        return pendenciaService.patch(id, dto);
    }

    /** Remove uma pendência (somente usuários nível >= 3) */
    @DeleteMapping("/{id}")
    public java.util.Map<String, String> delete(@PathVariable Integer id, org.springframework.security.core.Authentication authentication) {
        com.example.Nexus.config.CurrentUser current = (com.example.Nexus.config.CurrentUser) authentication.getPrincipal();
        var atual = usuarioService.buscarPorId(current.getId());
        if (atual.getNivelUsuario() == null || atual.getNivelUsuario() < 3) {
            throw new RuntimeException("Acesso negado");
        }
        pendenciaService.delete(id);
        return java.util.Map.of("message", "Pendência removida");
    }

    /**
     * Aceita uma transferência pendente.
     * Apenas o usuário/setor que recebeu a transferência pode aceitar.
     */
    @PostMapping("/{id}/aceitar-transferencia")
    public PendenciaDTO aceitarTransferencia(
            @PathVariable Integer id,
            Authentication authentication
    ) {
        CurrentUser user = (CurrentUser) authentication.getPrincipal();
        
        // Validação: verifica se o usuário atual pode aceitar (deve ser o destinatário)
        PendenciaDTO pendenciaAntes = pendenciaService.buscarPorId(id);
        
        // Se há usuário específico atribuído, apenas esse usuário pode aceitar
        if (pendenciaAntes.getIdUsuario() != null) {
            if (!pendenciaAntes.getIdUsuario().equals(user.getId())) {
                throw new RuntimeException("Você não tem permissão para aceitar esta transferência");
            }
        } else if (pendenciaAntes.getIdSetor() != null) {
            // Se não há usuário específico mas há setor, qualquer usuário do setor pode aceitar
            if (user.getIdSetor() == null || !pendenciaAntes.getIdSetor().equals(user.getIdSetor())) {
                throw new RuntimeException("Você não tem permissão para aceitar esta transferência");
            }
        } else {
            throw new RuntimeException("Esta pendência não foi transferida para nenhum setor ou usuário");
        }
        
        return pendenciaService.aceitarTransferencia(id);
    }

    /**
     * Devolve uma transferência pendente.
     * Apenas o usuário/setor que recebeu a transferência pode devolver.
     */
    @PostMapping("/{id}/devolver-transferencia")
    public PendenciaDTO devolverTransferencia(
            @PathVariable Integer id,
            Authentication authentication
    ) {
        CurrentUser user = (CurrentUser) authentication.getPrincipal();
        
        // Validação: verifica se o usuário atual pode devolver (deve ser o destinatário)
        PendenciaDTO pendenciaAntes = pendenciaService.buscarPorId(id);
        
        // Se há usuário específico atribuído, apenas esse usuário pode devolver
        if (pendenciaAntes.getIdUsuario() != null) {
            if (!pendenciaAntes.getIdUsuario().equals(user.getId())) {
                throw new RuntimeException("Você não tem permissão para devolver esta transferência");
            }
        } else if (pendenciaAntes.getIdSetor() != null) {
            // Se não há usuário específico mas há setor, qualquer usuário do setor pode devolver
            if (user.getIdSetor() == null || !pendenciaAntes.getIdSetor().equals(user.getIdSetor())) {
                throw new RuntimeException("Você não tem permissão para devolver esta transferência");
            }
        } else {
            throw new RuntimeException("Esta pendência não foi transferida para nenhum setor ou usuário");
        }
        
        return pendenciaService.devolverTransferencia(id);
    }

}
