# Docker - Nexus

## Uso rápido

Na raiz do projeto:

```bash
docker compose up -d --build
```

- **Frontend:** http://localhost:3000  
- **Backend (API):** http://localhost:8080  
- **PostgreSQL:** localhost:5432 (banco `Nexus_DB`)

## Variáveis de ambiente (opcional)

Crie um arquivo `.env` na raiz do projeto se quiser alterar:

- `POSTGRES_PASSWORD` – senha do PostgreSQL (padrão: 2696)
- `VITE_API_URL` – URL da API usada pelo frontend no browser (padrão: http://localhost:8080). Só afeta o build da imagem do frontend.

## Usuário inicial

Após o primeiro `up`, o banco é inicializado com:

- **Setores:** ENGENHARIA, COMERCIAL, DESENVOLVIMENTO, PCP, CUSTOS  
- **Usuário admin:** nome `admin`, senha `admin123` (nível 4)

## Volumes

- `postgres_data` – dados do PostgreSQL  
- `nexus_uploads` – anexos enviados pelo backend  

## Scripts de init do banco

Os arquivos em `docker/db/` rodam na primeira subida do container do Postgres (em ordem alfabética):

- `01-nexus-schema.sql` – schema e tabelas
- `02-nexus-data.sql` – setores e usuário admin

As migrations Flyway (V1, V2) rodam quando o backend sobe e adicionam colunas se necessário.
