package com.example.Nexus.Services;

import com.example.Nexus.DTOs.CreatePendenciaDTO;
import com.example.Nexus.DTOs.PatchPendenciaDTO;
import com.example.Nexus.DTOs.UpdatePendenciaDTO;
import com.example.Nexus.DTOs.PendenciaDTO;
import com.example.Nexus.Entities.Pendencia;
import com.example.Nexus.Repositories.PendenciaRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class PendenciaService {

    private final PendenciaRepository pendenciaRepository;

    public PendenciaService(PendenciaRepository pendenciaRepository) {
        this.pendenciaRepository = pendenciaRepository;
    }

    /* =========================
       LISTAGENS
       ========================= */

    public List<PendenciaDTO> listarTodas() {
        return pendenciaRepository.findAll()
                .stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    public List<PendenciaDTO> listarPorUsuario(Integer idUsuario) {
        return pendenciaRepository.findByIdUsuario(idUsuario)
                .stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    public List<PendenciaDTO> listarPorSetor(Integer idSetor) {
        return pendenciaRepository.findByIdSetor(idSetor)
                .stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    /* =========================
       CREATE
       ========================= */

    public PendenciaDTO criar(CreatePendenciaDTO dto) {
        Pendencia p = new Pendencia();

        p.setNumero(dto.getNumero());
        p.setEquipamento(dto.getEquipamento());
        p.setSituacao(dto.getSituacao());
        p.setStatus(dto.getStatus());
        p.setPrioridade(dto.getPrioridade());
        p.setPrazoResposta(dto.getPrazoResposta());
        p.setOrigem(dto.getOrigem());
        p.setObservacoes(dto.getObservacoes());
        p.setVersao(dto.getVersao());

        p.setIdUsuario(dto.getIdUsuario());
        p.setIdSetor(dto.getIdSetor());

        // JSONB
        p.setCliente(dto.getCliente());
        p.setPropostasVinculadas(dto.getPropostasVinculadas());
        p.setHistorico(dto.getHistorico());

        p.setDataCriacao(LocalDateTime.now());
        p.setUltimaModificacao(LocalDateTime.now());

        Pendencia salva = pendenciaRepository.save(p);
        return toDTO(salva);
    }

    /* =========================
       UPDATE
       ========================= */

    public PendenciaDTO atualizar(Integer id, UpdatePendenciaDTO dto) {
        Pendencia p = pendenciaRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Pendência não encontrada"));

        p.setEquipamento(dto.getEquipamento());
        p.setSituacao(dto.getSituacao());
        p.setStatus(dto.getStatus());
        p.setPrioridade(dto.getPrioridade());
        p.setPrazoResposta(dto.getPrazoResposta());
        p.setObservacoes(dto.getObservacoes());
        p.setVersao(dto.getVersao());

        p.setUltimaModificacao(LocalDateTime.now());

        return toDTO(pendenciaRepository.save(p));
    }

    public PendenciaDTO patch(Integer id, PatchPendenciaDTO dto) {
        Pendencia p = pendenciaRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Pendência não encontrada"));

        if (dto.getEquipamento() != null) p.setEquipamento(dto.getEquipamento());
        if (dto.getSituacao() != null) p.setSituacao(dto.getSituacao());
        if (dto.getStatus() != null) p.setStatus(dto.getStatus());
        if (dto.getPrioridade() != null) p.setPrioridade(dto.getPrioridade());
        if (dto.getPrazoResposta() != null) p.setPrazoResposta(dto.getPrazoResposta());
        if (dto.getObservacoes() != null) p.setObservacoes(dto.getObservacoes());
        if (dto.getVersao() != null) p.setVersao(dto.getVersao());

        // JSONB
        if (dto.getCliente() != null) p.setCliente(dto.getCliente());
        if (dto.getPropostasVinculadas() != null) p.setPropostasVinculadas(dto.getPropostasVinculadas());
        if (dto.getHistorico() != null) p.setHistorico(dto.getHistorico());

        p.setUltimaModificacao(LocalDateTime.now());

        return toDTO(pendenciaRepository.save(p));
    }

    /* =========================
       MAPPER
       ========================= */

    private PendenciaDTO toDTO(Pendencia p) {
        PendenciaDTO dto = new PendenciaDTO();

        dto.setId(p.getId());
        dto.setNumero(p.getNumero());
        dto.setDataCriacao(p.getDataCriacao());
        dto.setUltimaModificacao(p.getUltimaModificacao());
        dto.setEquipamento(p.getEquipamento());
        dto.setSituacao(p.getSituacao());
        dto.setStatus(p.getStatus());
        dto.setPrioridade(p.getPrioridade());
        dto.setPrazoResposta(p.getPrazoResposta());
        dto.setOrigem(p.getOrigem());
        dto.setObservacoes(p.getObservacoes());
        dto.setVersao(p.getVersao());
        dto.setIdUsuario(p.getIdUsuario());
        dto.setIdSetor(p.getIdSetor());

        return dto;
    }
}
