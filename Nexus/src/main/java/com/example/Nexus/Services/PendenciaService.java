package com.example.Nexus.Services;

import com.example.Nexus.DTOs.CreatePendenciaDTO;
import com.example.Nexus.DTOs.PatchPendenciaDTO;
import com.example.Nexus.DTOs.UpdatePendenciaDTO;
import com.example.Nexus.DTOs.PendenciaDTO;
import com.example.Nexus.Entities.Pendencia;
import com.example.Nexus.Repositories.PendenciaRepository;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class PendenciaService {

    private final PendenciaRepository pendenciaRepository;
    private final ObjectMapper objectMapper;
    private final RoteiroService roteiroService;

    public PendenciaService(
            PendenciaRepository pendenciaRepository, 
            ObjectMapper objectMapper,
            RoteiroService roteiroService) {
        this.pendenciaRepository = pendenciaRepository;
        this.objectMapper = objectMapper;
        this.roteiroService = roteiroService;
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

    /**
     * Lista pendências visíveis para o usuário:
     * - Se a pendência tiver um usuário atribuído (idUsuario != null), apenas esse usuário vê.
     * - Se não tiver usuário atribuído (idUsuario == null) mas tiver setor, todos do setor veem.
     */
    public List<PendenciaDTO> listarParaUsuario(Integer idUsuario, Integer idSetor) {
        List<Pendencia> todas = pendenciaRepository.findAll();

        return todas.stream()
                .filter(p -> {
                    // Se tem usuário atribuído, só ele enxerga
                    if (p.getIdUsuario() != null) {
                        return p.getIdUsuario().equals(idUsuario);
                    }
                    // Senão, visibilidade por setor (se tiver setor e usuário tiver setor)
                    if (p.getIdSetor() != null && idSetor != null) {
                        return p.getIdSetor().equals(idSetor);
                    }
                    // Caso sem setor definido: opcionalmente podemos torná-la visível só ao criador/usuario
                    return false;
                })
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    /* =========================
       CREATE
       ========================= */

    public PendenciaDTO criar(CreatePendenciaDTO dto) {
        Pendencia p = new Pendencia();

        // Coluna "numero" é NOT NULL no banco: usa valor do DTO ou gera um padrão
        String numero = dto.getNumero();
        if (numero == null || numero.isBlank()) {
            // Gera número aleatório de 6 dígitos
            int randomNum = (int) (Math.random() * 900000) + 100000; // 100000 a 999999
            numero = String.valueOf(randomNum);
        }
        p.setNumero(numero);
        p.setEquipamento(dto.getEquipamento());
        // Toda pendência criada inicia com situação "Aberta"
        String situacao = dto.getSituacao();
        if (situacao == null || situacao.isBlank()) {
            situacao = "Aberta";
        }
        p.setSituacao(situacao);
        p.setStatus(dto.getStatus());
        p.setPrioridade(dto.getPrioridade());
        p.setPrazoResposta(dto.getPrazoResposta());
        p.setOrigem(dto.getOrigem());
        p.setObservacoes(dto.getObservacoes());
        p.setVersao(dto.getVersao());

        p.setIdUsuario(dto.getIdUsuario());
        p.setIdSetor(dto.getIdSetor());
        p.setIdRoteiro(dto.getIdRoteiro());

        // JSONB
        p.setCliente(dto.getCliente());
        p.setPropostasVinculadas(dto.getPropostasVinculadas());
        p.setHistorico(dto.getHistorico());

        p.setDataCriacao(LocalDateTime.now());
        p.setUltimaModificacao(LocalDateTime.now());

        // Inicializa histórico com registro de criação
        JsonNode historicoCriacao = criarEntradaHistorico(
                "Criação",
                null,
                p.getSituacao(),
                null,
                p.getStatus(),
                null,
                p.getIdUsuario(),
                null,
                p.getIdSetor(),
                p.getObservacoes()
        );
        p.setHistorico(historicoCriacao);

        Pendencia salva = pendenciaRepository.save(p);
        return toDTO(salva);
    }

    /* =========================
       UPDATE
       ========================= */

    public PendenciaDTO atualizar(Integer id, UpdatePendenciaDTO dto) {
        Pendencia p = pendenciaRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Pendência não encontrada"));

        String situacaoAnterior = p.getSituacao();
        String statusAnterior = p.getStatus();

        p.setEquipamento(dto.getEquipamento());
        p.setSituacao(dto.getSituacao());
        p.setStatus(dto.getStatus());
        p.setPrioridade(dto.getPrioridade());
        p.setPrazoResposta(dto.getPrazoResposta());
        p.setObservacoes(dto.getObservacoes());
        p.setVersao(dto.getVersao());

        p.setUltimaModificacao(LocalDateTime.now());

        String acao = determinarAcao(
                situacaoAnterior,
                p.getSituacao(),
                statusAnterior,
                p.getStatus(),
                p.getIdUsuario(),
                p.getIdUsuario(),
                p.getIdSetor(),
                p.getIdSetor()
        );
        String descricao = montarDescricaoHistorico(
                situacaoAnterior,
                p.getSituacao(),
                statusAnterior,
                p.getStatus(),
                p.getIdUsuario(),
                p.getIdUsuario(),
                p.getIdSetor(),
                p.getIdSetor()
        );

        // Registra alteração completa
        JsonNode historicoAtualizado = adicionarEntradaHistorico(
                p.getHistorico(),
                acao,
                situacaoAnterior,
                p.getSituacao(),
                statusAnterior,
                p.getStatus(),
                null,
                p.getIdUsuario(),
                null,
                p.getIdSetor(),
                dto.getObservacoes(),
                descricao
        );
        p.setHistorico(historicoAtualizado);

        return toDTO(pendenciaRepository.save(p));
    }

    public PendenciaDTO patch(Integer id, PatchPendenciaDTO dto) {
        Pendencia p = pendenciaRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Pendência não encontrada"));

        // Valores "antes" para o histórico
        String situacaoAnterior = p.getSituacao();
        String statusAnterior = p.getStatus();
        Integer idUsuarioAntes = p.getIdUsuario();
        Integer idSetorAntes = p.getIdSetor();

        if (dto.getEquipamento() != null) p.setEquipamento(dto.getEquipamento());
        if (dto.getSituacao() != null) p.setSituacao(dto.getSituacao());
        if (dto.getStatus() != null) p.setStatus(dto.getStatus());
        if (dto.getPrioridade() != null) p.setPrioridade(dto.getPrioridade());
        if (dto.getPrazoResposta() != null) p.setPrazoResposta(dto.getPrazoResposta());
        if (dto.getObservacoes() != null) p.setObservacoes(dto.getObservacoes());
        if (dto.getVersao() != null) p.setVersao(dto.getVersao());

        // Validação de roteiro antes de transferir setor
        if (dto.getIdSetor() != null && !dto.getIdSetor().equals(idSetorAntes)) {
            // Se a pendência está em um roteiro, valida se o setor destino é válido
            if (p.getIdRoteiro() != null) {
                boolean setorValido = roteiroService.isSetorValidoParaTransferencia(
                        p.getIdRoteiro(), 
                        idSetorAntes, 
                        dto.getIdSetor()
                );
                if (!setorValido) {
                    throw new RuntimeException(
                        "Não é possível transferir para este setor. A pendência está em um roteiro e deve seguir a sequência definida."
                    );
                }
            }
            p.setIdSetor(dto.getIdSetor());
        }
        if (dto.getIdUsuario() != null) {
            // Convenção: idUsuario == 0 → remover atribuição (setar null)
            if (dto.getIdUsuario() == 0) {
                p.setIdUsuario(null);
            } else {
                p.setIdUsuario(dto.getIdUsuario());
            }
        }
        if (dto.getIdRoteiro() != null) {
            p.setIdRoteiro(dto.getIdRoteiro());
        }

        // JSONB
        if (dto.getCliente() != null) p.setCliente(dto.getCliente());
        if (dto.getPropostasVinculadas() != null) p.setPropostasVinculadas(dto.getPropostasVinculadas());

        p.setUltimaModificacao(LocalDateTime.now());

        // Monta descrição da alteração (campos relevantes)
        String observacaoHistorico = dto.getObservacoes();

        String acao = determinarAcao(
                situacaoAnterior,
                p.getSituacao(),
                statusAnterior,
                p.getStatus(),
                idUsuarioAntes,
                p.getIdUsuario(),
                idSetorAntes,
                p.getIdSetor()
        );
        String descricao = montarDescricaoHistorico(
                situacaoAnterior,
                p.getSituacao(),
                statusAnterior,
                p.getStatus(),
                idUsuarioAntes,
                p.getIdUsuario(),
                idSetorAntes,
                p.getIdSetor()
        );

        JsonNode historicoAtualizado = adicionarEntradaHistorico(
                p.getHistorico(),
                acao,
                situacaoAnterior,
                p.getSituacao(),
                statusAnterior,
                p.getStatus(),
                idUsuarioAntes,
                p.getIdUsuario(),
                idSetorAntes,
                p.getIdSetor(),
                observacaoHistorico,
                descricao
        );
        p.setHistorico(historicoAtualizado);

        return toDTO(pendenciaRepository.save(p));
    }

    /* =========================
       DELETE
       ========================= */

    public void delete(Integer id) {
        if (!pendenciaRepository.existsById(id)) {
            throw new RuntimeException("Pendência não encontrada");
        }
        pendenciaRepository.deleteById(id);
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
        dto.setIdRoteiro(p.getIdRoteiro());
        dto.setHistorico(p.getHistorico());

        return dto;
    }

    /**
     * Cria uma nova estrutura de histórico (array JSON) com uma única entrada.
     */
    private JsonNode criarEntradaHistorico(
            String acao,
            String situacaoAnterior,
            String situacao,
            String statusAnterior,
            String status,
            Integer idUsuarioAntes,
            Integer idUsuarioDepois,
            Integer idSetorAntes,
            Integer idSetorDepois,
            String observacoes
    ) {
        ArrayNode array = objectMapper.createArrayNode();
        array.add(criarObjetoHistorico(
                acao,
                situacaoAnterior,
                situacao,
                statusAnterior,
                status,
                idUsuarioAntes,
                idUsuarioDepois,
                idSetorAntes,
                idSetorDepois,
                observacoes,
                null
        ));
        return array;
    }

    /**
     * Adiciona uma entrada de histórico a um JSON existente (que pode ser null, objeto único ou array).
     */
    private JsonNode adicionarEntradaHistorico(
            JsonNode historicoExistente,
            String acao,
            String situacaoAnterior,
            String situacao,
            String statusAnterior,
            String status,
            Integer idUsuarioAntes,
            Integer idUsuarioDepois,
            Integer idSetorAntes,
            Integer idSetorDepois,
            String observacoes,
            String descricao
    ) {
        ArrayNode array;

        if (historicoExistente == null || historicoExistente.isNull()) {
            array = objectMapper.createArrayNode();
        } else if (historicoExistente.isArray()) {
            array = (ArrayNode) historicoExistente;
        } else {
            // Se o histórico anterior era um único objeto, converte para array
            array = objectMapper.createArrayNode();
            array.add(historicoExistente);
        }

        array.add(criarObjetoHistorico(
                acao,
                situacaoAnterior,
                situacao,
                statusAnterior,
                status,
                idUsuarioAntes,
                idUsuarioDepois,
                idSetorAntes,
                idSetorDepois,
                observacoes,
                descricao
        ));

        return array;
    }

    /**
     * Cria o objeto JSON de uma entrada de histórico.
     */
    private ObjectNode criarObjetoHistorico(
            String acao,
            String situacaoAnterior,
            String situacao,
            String statusAnterior,
            String status,
            Integer idUsuarioAntes,
            Integer idUsuarioDepois,
            Integer idSetorAntes,
            Integer idSetorDepois,
            String observacoes,
            String descricao
    ) {
        ObjectNode node = objectMapper.createObjectNode();
        node.put("dataAlteracao", LocalDateTime.now().toString());
        node.put("acao", acao);

        if (situacaoAnterior != null) node.put("situacaoAnterior", situacaoAnterior);
        if (situacao != null) node.put("situacao", situacao);

        if (statusAnterior != null) node.put("statusAnterior", statusAnterior);
        if (status != null) node.put("status", status);

        if (idUsuarioAntes != null) node.put("idUsuarioAnterior", idUsuarioAntes);
        if (idUsuarioDepois != null) node.put("idUsuario", idUsuarioDepois);

        if (idSetorAntes != null) node.put("idSetorAnterior", idSetorAntes);
        if (idSetorDepois != null) node.put("idSetor", idSetorDepois);

        if (observacoes != null && !observacoes.isBlank()) {
            node.put("observacoes", observacoes);
        }

        if (descricao != null && !descricao.isBlank()) {
            node.put("descricao", descricao);
        }

        return node;
    }

    private String determinarAcao(
            String situacaoAntes,
            String situacaoDepois,
            String statusAntes,
            String statusDepois,
            Integer idUsuarioAntes,
            Integer idUsuarioDepois,
            Integer idSetorAntes,
            Integer idSetorDepois
    ) {
        boolean mudouSetor = (idSetorAntes == null && idSetorDepois != null)
                || (idSetorAntes != null && !idSetorAntes.equals(idSetorDepois));
        boolean mudouUsuario = (idUsuarioAntes == null && idUsuarioDepois != null)
                || (idUsuarioAntes != null && !idUsuarioAntes.equals(idUsuarioDepois));
        boolean mudouSituacao = (situacaoAntes == null && situacaoDepois != null)
                || (situacaoAntes != null && !situacaoAntes.equals(situacaoDepois));
        boolean mudouStatus = (statusAntes == null && statusDepois != null)
                || (statusAntes != null && !statusAntes.equals(statusDepois));

        // Prioridade: ações mais “específicas” primeiro
        if (mudouSetor && mudouUsuario) return "Transferência";
        if (mudouSetor) return "Transferência de setor";
        if (mudouUsuario) {
            if (idUsuarioDepois == null) return "Desatribuição";
            if (idUsuarioAntes == null) return "Atribuição";
            return "Reatribuição";
        }
        if (mudouSituacao) return "Mudança de situação";
        if (mudouStatus) return "Mudança de status";

        return "Edição";
    }

    private String montarDescricaoHistorico(
            String situacaoAntes,
            String situacaoDepois,
            String statusAntes,
            String statusDepois,
            Integer idUsuarioAntes,
            Integer idUsuarioDepois,
            Integer idSetorAntes,
            Integer idSetorDepois
    ) {
        StringBuilder sb = new StringBuilder();

        if ((idSetorAntes == null && idSetorDepois != null) || (idSetorAntes != null && !idSetorAntes.equals(idSetorDepois))) {
            sb.append("Setor: ").append(idSetorAntes == null ? "—" : idSetorAntes)
                    .append(" → ").append(idSetorDepois == null ? "—" : idSetorDepois).append(". ");
        }
        if ((idUsuarioAntes == null && idUsuarioDepois != null) || (idUsuarioAntes != null && !idUsuarioAntes.equals(idUsuarioDepois))) {
            sb.append("Usuário: ").append(idUsuarioAntes == null ? "—" : idUsuarioAntes)
                    .append(" → ").append(idUsuarioDepois == null ? "—" : idUsuarioDepois).append(". ");
        }
        if ((situacaoAntes == null && situacaoDepois != null) || (situacaoAntes != null && !situacaoAntes.equals(situacaoDepois))) {
            sb.append("Situação: ").append(situacaoAntes == null ? "—" : situacaoAntes)
                    .append(" → ").append(situacaoDepois == null ? "—" : situacaoDepois).append(". ");
        }
        if ((statusAntes == null && statusDepois != null) || (statusAntes != null && !statusAntes.equals(statusDepois))) {
            sb.append("Status: ").append(statusAntes == null ? "—" : statusAntes)
                    .append(" → ").append(statusDepois == null ? "—" : statusDepois).append(". ");
        }

        String s = sb.toString().trim();
        // remove ponto final sobrando
        if (s.endsWith(".")) s = s.substring(0, s.length() - 1);
        return s;
    }
}
