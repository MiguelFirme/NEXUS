package com.example.Nexus.Services;

import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.net.MalformedURLException;
import java.nio.file.*;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class AnexoService {

    private final Path baseDir;

    public AnexoService() throws IOException {
        this.baseDir = Paths.get("uploads").toAbsolutePath().normalize();
        if (!Files.exists(this.baseDir)) {
            Files.createDirectories(this.baseDir);
        }
    }

    public String saveAttachment(Integer pendenciaId, MultipartFile file) throws IOException {
        String original = Path.of(file.getOriginalFilename() == null ? "file" : file.getOriginalFilename()).getFileName().toString();
        String safe = original.replaceAll("[^a-zA-Z0-9._-]", "_");
        String filename = String.format("%d_%d_%s", pendenciaId, System.currentTimeMillis(), safe);
        Path target = baseDir.resolve(filename);
        try (var in = file.getInputStream()) {
            Files.copy(in, target, StandardCopyOption.REPLACE_EXISTING);
        }
        return filename;
    }

    public List<String> listAttachments(Integer pendenciaId) throws IOException {
        String prefix = pendenciaId + "_";
        try {
            return Files.list(baseDir)
                    .filter(p -> p.getFileName().toString().startsWith(prefix))
                    .map(p -> p.getFileName().toString())
                    .collect(Collectors.toList());
        } catch (NoSuchFileException e) {
            return new ArrayList<>();
        }
    }

    public Resource loadAsResource(String filename) throws MalformedURLException {
        Path file = baseDir.resolve(filename).normalize();
        UrlResource resource = new UrlResource(file.toUri());
        if (resource.exists() && resource.isReadable()) {
            return resource;
        }
        return null;
    }
}
