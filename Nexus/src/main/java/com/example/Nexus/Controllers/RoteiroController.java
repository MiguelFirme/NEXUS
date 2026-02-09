package com.example.Nexus.Controllers;

import com.example.Nexus.DTOs.CreateRoteiroDTO;
import com.example.Nexus.DTOs.RoteiroDTO;
import com.example.Nexus.Services.RoteiroService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/roteiros")
public class RoteiroController {

    private final RoteiroService roteiroService;

    public RoteiroController(RoteiroService roteiroService) {
        this.roteiroService = roteiroService;
    }

    @GetMapping
    public List<RoteiroDTO> listarTodos() {
        return roteiroService.listarTodos();
    }

    @GetMapping("/ativos")
    public List<RoteiroDTO> listarAtivos() {
        return roteiroService.listarAtivos();
    }

    @GetMapping("/{id}")
    public RoteiroDTO buscarPorId(@PathVariable Integer id) {
        return roteiroService.buscarPorId(id);
    }

    @PostMapping
    public RoteiroDTO criar(@RequestBody CreateRoteiroDTO dto) {
        return roteiroService.criar(dto);
    }

    @PutMapping("/{id}")
    public RoteiroDTO atualizar(@PathVariable Integer id, @RequestBody CreateRoteiroDTO dto) {
        return roteiroService.atualizar(id, dto);
    }

    @DeleteMapping("/{id}")
    public void deletar(@PathVariable Integer id) {
        roteiroService.deletar(id);
    }
}
