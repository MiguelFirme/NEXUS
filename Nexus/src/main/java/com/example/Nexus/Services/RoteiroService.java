package com.example.Nexus.Services;

import com.example.Nexus.DTOs.CreateRoteiroDTO;
import com.example.Nexus.DTOs.RoteiroDTO;
import com.example.Nexus.DTOs.RoteiroSetorDTO;
import com.example.Nexus.Entities.Roteiro;
import com.example.Nexus.Entities.RoteiroSetor;
import com.example.Nexus.Entities.Setor;
import com.example.Nexus.Repositories.RoteiroRepository;
import com.example.Nexus.Repositories.RoteiroSetorRepository;
import com.example.Nexus.Repositories.SetorRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class RoteiroService {

    private final RoteiroRepository roteiroRepository;
    private final RoteiroSetorRepository roteiroSetorRepository;
    private final SetorRepository setorRepository;

    public RoteiroService(
            RoteiroRepository roteiroRepository,
            RoteiroSetorRepository roteiroSetorRepository,
            SetorRepository setorRepository) {
        this.roteiroRepository = roteiroRepository;
        this.roteiroSetorRepository = roteiroSetorRepository;
        this.setorRepository = setorRepository;
    }

    public List<RoteiroDTO> listarTodos() {
        return roteiroRepository.findAll().stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    public List<RoteiroDTO> listarAtivos() {
        return roteiroRepository.findByAtivoTrue().stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    public RoteiroDTO buscarPorId(Integer id) {
        Roteiro roteiro = roteiroRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Roteiro não encontrado"));
        return toDTO(roteiro);
    }

    @Transactional
    public RoteiroDTO criar(CreateRoteiroDTO dto) {
        Roteiro roteiro = new Roteiro();
        roteiro.setNome(dto.getNome());
        roteiro.setDescricao(dto.getDescricao());
        roteiro.setAtivo(dto.getAtivo() != null ? dto.getAtivo() : true);
        
        roteiro = roteiroRepository.save(roteiro);

        // Salva os setores na ordem especificada
        if (dto.getSetores() != null && !dto.getSetores().isEmpty()) {
            for (var setorOrdem : dto.getSetores()) {
                RoteiroSetor roteiroSetor = new RoteiroSetor();
                roteiroSetor.setRoteiroId(roteiro.getId());
                roteiroSetor.setIdSetor(setorOrdem.getIdSetor());
                roteiroSetor.setOrdem(setorOrdem.getOrdem());
                roteiroSetorRepository.save(roteiroSetor);
            }
        }

        return toDTO(roteiro);
    }

    @Transactional
    public RoteiroDTO atualizar(Integer id, CreateRoteiroDTO dto) {
        Roteiro roteiro = roteiroRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Roteiro não encontrado"));

        roteiro.setNome(dto.getNome());
        roteiro.setDescricao(dto.getDescricao());
        if (dto.getAtivo() != null) {
            roteiro.setAtivo(dto.getAtivo());
        }

        roteiro = roteiroRepository.save(roteiro);

        // Remove setores antigos e adiciona os novos
        roteiroSetorRepository.deleteByRoteiroId(id);
        if (dto.getSetores() != null && !dto.getSetores().isEmpty()) {
            for (var setorOrdem : dto.getSetores()) {
                RoteiroSetor roteiroSetor = new RoteiroSetor();
                roteiroSetor.setRoteiroId(roteiro.getId());
                roteiroSetor.setIdSetor(setorOrdem.getIdSetor());
                roteiroSetor.setOrdem(setorOrdem.getOrdem());
                roteiroSetorRepository.save(roteiroSetor);
            }
        }

        return toDTO(roteiro);
    }

    @Transactional
    public void deletar(Integer id) {
        if (!roteiroRepository.existsById(id)) {
            throw new RuntimeException("Roteiro não encontrado");
        }
        roteiroSetorRepository.deleteByRoteiroId(id);
        roteiroRepository.deleteById(id);
    }

    /**
     * Retorna o próximo setor válido no roteiro, baseado no setor atual.
     * Retorna null se não houver próximo setor ou se a pendência não estiver em um roteiro.
     */
    public Integer getProximoSetorValido(Integer roteiroId, Integer setorAtual) {
        if (roteiroId == null) {
            return null;
        }

        List<RoteiroSetor> setores = roteiroSetorRepository.findByRoteiroIdOrderByOrdem(roteiroId);
        if (setores.isEmpty()) {
            return null;
        }

        // Encontra o índice do setor atual
        int indiceAtual = -1;
        for (int i = 0; i < setores.size(); i++) {
            if (setores.get(i).getIdSetor().equals(setorAtual)) {
                indiceAtual = i;
                break;
            }
        }

        // Se não encontrou o setor atual ou é o último, retorna null
        if (indiceAtual == -1 || indiceAtual >= setores.size() - 1) {
            return null;
        }

        // Retorna o próximo setor na sequência
        return setores.get(indiceAtual + 1).getIdSetor();
    }

    /**
     * Verifica se um setor é válido para transferência no roteiro.
     * Retorna true se o setor é o próximo na sequência do roteiro.
     */
    public boolean isSetorValidoParaTransferencia(Integer roteiroId, Integer setorAtual, Integer setorDestino) {
        if (roteiroId == null) {
            return true; // Sem roteiro, qualquer setor é válido
        }

        Integer proximoSetor = getProximoSetorValido(roteiroId, setorAtual);
        return proximoSetor != null && proximoSetor.equals(setorDestino);
    }

    /**
     * Retorna todos os setores válidos do roteiro (apenas o próximo na sequência).
     */
    public List<Integer> getSetoresValidos(Integer roteiroId, Integer setorAtual) {
        Integer proximoSetor = getProximoSetorValido(roteiroId, setorAtual);
        if (proximoSetor == null) {
            return List.of();
        }
        return List.of(proximoSetor);
    }

    private RoteiroDTO toDTO(Roteiro roteiro) {
        RoteiroDTO dto = new RoteiroDTO();
        dto.setId(roteiro.getId());
        dto.setNome(roteiro.getNome());
        dto.setDescricao(roteiro.getDescricao());
        dto.setAtivo(roteiro.getAtivo());
        dto.setDataCriacao(roteiro.getDataCriacao());

        // Carrega os setores do roteiro
        List<RoteiroSetor> setores = roteiroSetorRepository.findByRoteiroIdOrderByOrdem(roteiro.getId());
        dto.setSetores(setores.stream().map(rs -> {
            RoteiroSetorDTO rsDto = new RoteiroSetorDTO();
            rsDto.setId(rs.getId());
            rsDto.setRoteiroId(rs.getRoteiroId());
            rsDto.setIdSetor(rs.getIdSetor());
            rsDto.setOrdem(rs.getOrdem());
            
            // Busca o nome do setor
            setorRepository.findById(rs.getIdSetor()).ifPresent(setor -> {
                rsDto.setNomeSetor(setor.getNome_setor());
            });
            
            return rsDto;
        }).collect(Collectors.toList()));

        return dto;
    }
}
