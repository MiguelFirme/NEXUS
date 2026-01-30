package com.example.Nexus.config;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;

@Service
public class JwtService {

    @Value("${nexus.jwt.secret:nexus-secret-key-minimo-32-caracteres-para-hs256}")
    private String secret;

    @Value("${nexus.jwt.expiration-ms:86400000}")
    private long expirationMs; // 24h

    private SecretKey getSigningKey() {
        return Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
    }

    public String generateToken(Integer userId, String emailUsuario, Integer idSetor) {
        return Jwts.builder()
                .subject(String.valueOf(userId))
                .claim("email", emailUsuario)
                .claim("idSetor", idSetor != null ? idSetor : 0)
                .issuedAt(new Date())
                .expiration(new Date(System.currentTimeMillis() + expirationMs))
                .signWith(getSigningKey())
                .compact();
    }

    public Claims parseToken(String token) {
        return Jwts.parser()
                .verifyWith(getSigningKey())
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }

    public Integer getUserIdFromToken(String token) {
        return Integer.parseInt(parseToken(token).getSubject());
    }

    public String getEmailFromToken(String token) {
        return (String) parseToken(token).get("email");
    }

    public Integer getIdSetorFromToken(String token) {
        Object v = parseToken(token).get("idSetor");
        if (v == null) return null;
        int n = ((Number) v).intValue();
        return n == 0 ? null : n;
    }
}
