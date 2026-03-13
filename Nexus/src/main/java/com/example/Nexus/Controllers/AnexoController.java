package com.example.Nexus.Controllers;

import com.example.Nexus.Services.AnexoService;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.net.MalformedURLException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;

@RestController
public class AnexoController {

    private final AnexoService anexoService;

    public AnexoController(AnexoService anexoService) {
        this.anexoService = anexoService;
    }

    /**
     * Insere um anexo na pendência.
     * Requer autenticação.
     */
    @PostMapping("/pendencias/{id}/anexos")
    public ResponseEntity<?> upload(@PathVariable Integer id, @RequestParam("file") MultipartFile file) {
        if (file == null || file.isEmpty()) {
            return ResponseEntity.badRequest().body(Map.of("message", "Arquivo não enviado"));
        }
        try {
            String filename = anexoService.saveAttachment(id, file);
            String url = "/anexos/" + filename;
            return ResponseEntity.ok(Map.of("filename", filename, "url", url));
        } catch (IOException e) {
            return ResponseEntity.status(500).body(Map.of("message", "Falha ao salvar arquivo"));
        }
    }

    /**
     * Lista os anexos da pendência.
     * Requer autenticação.
     */
    @GetMapping("/pendencias/{id}/anexos")
    public ResponseEntity<?> list(@PathVariable Integer id) {
        try {
            List<String> list = anexoService.listAttachments(id);
            List<Map<String, String>> body = list.stream()
                    .map(n -> Map.<String, String>of("filename", n, "url", "/anexos/" + n))
                    .toList();
            return ResponseEntity.ok(body);
        } catch (IOException e) {
            return ResponseEntity.status(500).body(Map.of("message", "Falha ao listar anexos"));
        }
    }

    /**
     * Remove um anexo pelo nome do arquivo (query param para evitar problemas de encoding no path).
     * Requer autenticação.
     */
    @DeleteMapping(value = "/pendencias/{id}/anexos", params = "filename")
    public ResponseEntity<?> delete(@PathVariable Integer id, @RequestParam("filename") String filename) {
        if (filename == null || filename.isBlank()) {
            return ResponseEntity.badRequest().body(Map.of("message", "Nome do arquivo é obrigatório"));
        }
        try {
            boolean removed = anexoService.deleteAttachment(id, filename.trim());
            if (!removed) {
                return ResponseEntity.status(404).body(Map.of("message", "Anexo não encontrado"));
            }
            return ResponseEntity.noContent().build();
        } catch (IOException e) {
            return ResponseEntity.status(500).body(Map.of("message", "Falha ao remover anexo"));
        }
    }

    /**
     * Download do arquivo (acesso público para links diretos).
     */
    @GetMapping("/anexos/{filename:.+}")
    public ResponseEntity<?> serve(@PathVariable String filename) {
        try {
            Resource res = anexoService.loadAsResource(filename);
            if (res == null) return ResponseEntity.notFound().build();
            Path p = Path.of(res.getURI());
            String contentType = Files.probeContentType(p);
            return ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, "inline; filename=\"" + filename + "\"")
                    .contentType(contentType != null ? MediaType.parseMediaType(contentType) : MediaType.APPLICATION_OCTET_STREAM)
                    .body(res);
        } catch (MalformedURLException e) {
            return ResponseEntity.notFound().build();
        } catch (IOException e) {
            return ResponseEntity.status(500).body(Map.of("message", "Erro ao ler arquivo"));
        }
    }
}
