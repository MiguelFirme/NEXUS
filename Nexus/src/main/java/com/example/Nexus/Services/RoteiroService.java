package com.example.Nexus.Services;

import com.example.Nexus.DTOs.CreateRoteiroDTO;
import com.example.Nexus.DTOs.PassoRoteiroDTO;
import com.example.Nexus.DTOs.PassoRoteiroExibicaoDTO;
import com.example.Nexus.DTOs.RoteiroDTO;
import com.example.Nexus.Entities.Roteiro;
import com.example.Nexus.Entities.RoteiroPasso;
import com.example.Nexus.Entities.Setor;
import com.example.Nexus.Entities.Usuario;
import com.example.Nexus.Repositories.RoteiroPassoRepository;
import com.example.Nexus.Repositories.RoteiroRepository;
import com.example.Nexus.Repositories.SetorRepository;
import com.example.Nexus.Repositories.UsuarioRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class RoteiroService {

    private final RoteiroRepository roteiroRepository;
    private final RoteiroPassoRepository roteiroPassoRepository;
    private final SetorRepository setorRepository;
    private final UsuarioRepository usuarioRepository;

    public RoteiroService(
            RoteiroRepository roteiroRepository,
            RoteiroPassoRepository roteiroPassoRepository,
            SetorRepository setorRepository,
            UsuarioRepository usuarioRepository) {
        this.roteiroRepository = roteiroRepository;
        this.roteiroPassoRepository = roteiroPassoRepository;
        this.setorRepository = setorRepository;
        this.usuarioRepository = usuarioRepository;
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

        if (dto.getPassos() != null && !dto.getPassos().isEmpty()) {
            for (PassoRoteiroDTO passo : dto.getPassos()) {
                if (passo.getTipo() == null) continue;
                RoteiroPasso rp = new RoteiroPasso();
                rp.setRoteiroId(roteiro.getId());
                rp.setOrdem(passo.getOrdem() != null ? passo.getOrdem() : 0);
                rp.setTipo(passo.getTipo());
                if ("SETOR".equalsIgnoreCase(passo.getTipo()) && passo.getIdSetor() != null) {
                    rp.setIdSetor(passo.getIdSetor());
                    rp.setIdUsuario(null);
                } else if ("USUARIO".equalsIgnoreCase(passo.getTipo()) && passo.getIdUsuario() != null) {
                    rp.setIdUsuario(passo.getIdUsuario());
                    rp.setIdSetor(null);
                } else {
                    continue;
                }
                roteiroPassoRepository.save(rp);
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

        roteiroPassoRepository.deleteByRoteiroId(id);
        if (dto.getPassos() != null && !dto.getPassos().isEmpty()) {
            for (PassoRoteiroDTO passo : dto.getPassos()) {
                if (passo.getTipo() == null) continue;
                RoteiroPasso rp = new RoteiroPasso();
                rp.setRoteiroId(roteiro.getId());
                rp.setOrdem(passo.getOrdem() != null ? passo.getOrdem() : 0);
                rp.setTipo(passo.getTipo());
                if ("SETOR".equalsIgnoreCase(passo.getTipo()) && passo.getIdSetor() != null) {
                    rp.setIdSetor(passo.getIdSetor());
                    rp.setIdUsuario(null);
                } else if ("USUARIO".equalsIgnoreCase(passo.getTipo()) && passo.getIdUsuario() != null) {
                    rp.setIdUsuario(passo.getIdUsuario());
                    rp.setIdSetor(null);
                } else {
                    continue;
                }
                roteiroPassoRepository.save(rp);
            }
        }

        return toDTO(roteiro);
    }

    @Transactional
    public void deletar(Integer id) {
        if (!roteiroRepository.existsById(id)) {
            throw new RuntimeException("Roteiro não encontrado");
        }
        roteiroPassoRepository.deleteByRoteiroId(id);
        roteiroRepository.deleteById(id);
    }

    /**
     * Retorna o próximo passo (setor ou usuário) para transferência.
     * Útil quando o próximo passo é um usuário.
     */
    public ProximoPasso getProximoPasso(Integer roteiroId, Integer setorAtual, Integer usuarioAtual) {
        if (roteiroId == null) return null;

        List<RoteiroPasso> passos = roteiroPassoRepository.findByRoteiroIdOrderByOrdem(roteiroId);
        int indiceAtual = -1;
        for (int i = 0; i < passos.size(); i++) {
            RoteiroPasso p = passos.get(i);
            if ("SETOR".equals(p.getTipo()) && setorAtual != null && setorAtual.equals(p.getIdSetor())) {
                indiceAtual = i;
                break;
            }
            if ("USUARIO".equals(p.getTipo()) && usuarioAtual != null && usuarioAtual.equals(p.getIdUsuario())) {
                indiceAtual = i;
                break;
            }
        }
        if (indiceAtual == -1 || indiceAtual >= passos.size() - 1) return null;

        RoteiroPasso proximo = passos.get(indiceAtual + 1);
        ProximoPasso pp = new ProximoPasso();
        pp.tipo = proximo.getTipo();
        pp.idSetor = proximo.getIdSetor();
        pp.idUsuario = proximo.getIdUsuario();
        return pp;
    }

    public static class ProximoPasso {
        public String tipo;
        public Integer idSetor;
        public Integer idUsuario;
    }

    /**
     * Próximo setor válido considerando que a posição atual pode ser um passo de usuário.
     * Quando a pendência está atribuída a um usuário, considera que estamos no passo desse usuário.
     */
    public Integer getProximoSetorValido(Integer roteiroId, Integer setorAtual, Integer usuarioAtual) {
        if (roteiroId == null) return null;
        List<RoteiroPasso> passos = roteiroPassoRepository.findByRoteiroIdOrderByOrdem(roteiroId);
        int indiceAtual = -1;
        if (usuarioAtual != null) {
            for (int i = 0; i < passos.size(); i++) {
                RoteiroPasso p = passos.get(i);
                if ("USUARIO".equals(p.getTipo()) && usuarioAtual.equals(p.getIdUsuario())) {
                    indiceAtual = i;
                    break;
                }
            }
        }
        if (indiceAtual == -1 && setorAtual != null) {
            for (int i = 0; i < passos.size(); i++) {
                RoteiroPasso p = passos.get(i);
                if ("SETOR".equals(p.getTipo()) && setorAtual.equals(p.getIdSetor())) {
                    indiceAtual = i;
                    break;
                }
            }
        }
        if (indiceAtual == -1) return null;
        for (int i = indiceAtual + 1; i < passos.size(); i++) {
            RoteiroPasso p = passos.get(i);
            if ("SETOR".equals(p.getTipo())) return p.getIdSetor();
        }
        return null;
    }

    public boolean isSetorValidoParaTransferencia(Integer roteiroId, Integer setorAtual, Integer setorDestino) {
        if (roteiroId == null) return true;
        Integer proximoSetor = getProximoSetorValido(roteiroId, setorAtual, null);
        return proximoSetor != null && proximoSetor.equals(setorDestino);
    }

    /**
     * Valida transferência para setor quando a posição atual pode ser um passo de usuário
     * (pendência atribuída a um usuário que aceitou a transferência).
     */
    public boolean isSetorValidoParaTransferencia(Integer roteiroId, Integer setorAtual, Integer usuarioAtual, Integer setorDestino) {
        if (roteiroId == null) return true;
        Integer proximoSetor = getProximoSetorValido(roteiroId, setorAtual, usuarioAtual);
        return proximoSetor != null && proximoSetor.equals(setorDestino);
    }

    /**
     * Verifica se transferir para o usuário é o próximo passo válido no roteiro.
     */
    public boolean isUsuarioValidoParaTransferencia(Integer roteiroId, Integer setorAtual, Integer usuarioAtual, Integer idUsuarioDestino) {
        if (roteiroId == null) return true;
        ProximoPasso pp = getProximoPasso(roteiroId, setorAtual, usuarioAtual);
        return pp != null && "USUARIO".equals(pp.tipo) && idUsuarioDestino != null && idUsuarioDestino.equals(pp.idUsuario);
    }

    public List<Integer> getSetoresValidos(Integer roteiroId, Integer setorAtual) {
        Integer proximoSetor = getProximoSetorValido(roteiroId, setorAtual, null);
        if (proximoSetor == null) return List.of();
        return List.of(proximoSetor);
    }

    private RoteiroDTO toDTO(Roteiro roteiro) {
        RoteiroDTO dto = new RoteiroDTO();
        dto.setId(roteiro.getId());
        dto.setNome(roteiro.getNome());
        dto.setDescricao(roteiro.getDescricao());
        dto.setAtivo(roteiro.getAtivo());
        dto.setDataCriacao(roteiro.getDataCriacao());

        List<RoteiroPasso> passos = roteiroPassoRepository.findByRoteiroIdOrderByOrdem(roteiro.getId());
        dto.setPassos(passos.stream().map(p -> {
            PassoRoteiroExibicaoDTO pdto = new PassoRoteiroExibicaoDTO();
            pdto.setId(p.getId());
            pdto.setOrdem(p.getOrdem());
            pdto.setTipo(p.getTipo());
            pdto.setIdSetor(p.getIdSetor());
            pdto.setIdUsuario(p.getIdUsuario());
            if (p.getIdSetor() != null) {
                setorRepository.findById(p.getIdSetor()).ifPresent(s -> pdto.setNomeSetor(s.getNome_setor()));
            }
            if (p.getIdUsuario() != null) {
                usuarioRepository.findById(p.getIdUsuario()).ifPresent(u -> pdto.setNomeUsuario(u.getNomeUsuario()));
            }
            return pdto;
        }).collect(Collectors.toList()));

        return dto;
    }
}
