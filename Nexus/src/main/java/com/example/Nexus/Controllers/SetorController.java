package com.example.Nexus.Controllers;

import com.example.Nexus.Entities.Setor;
import com.example.Nexus.Repositories.SetorRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/setores")
public class SetorController {

    private final SetorRepository setorRepository;

    public SetorController(SetorRepository setorRepository) {
        this.setorRepository = setorRepository;
    }

    @GetMapping
    public List<Setor> listarTodos() {
        return setorRepository.findAll();
    }
}
