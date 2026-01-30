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

    public PendenciaController(PendenciaService pendenciaService) {
        this.pendenciaService = pendenciaService;
    }

    /**
     * Lista pendências conforme o usuário logado: por setor (se tiver) ou por usuário.
     */
    @GetMapping
    public List<PendenciaDTO> listarTodas(Authentication authentication) {
        CurrentUser user = (CurrentUser) authentication.getPrincipal();
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


}
