# Subir o NEXUS com Docker (Docker Desktop)

## 1. Pré-requisitos

- **Docker Desktop** instalado e em execução.

## 2. Arquivo `.env` (opcional)

Na **raiz do projeto** (pasta onde está o `docker-compose.yml`), você pode criar um arquivo **`.env`** para customizar senha do banco, portas etc.

Use o arquivo **`env.example.txt`** como modelo: abra-o, copie o conteúdo e salve como **`.env`** na raiz.

**Se não criar o `.env`**, o Compose usa os valores padrão (usuário/senha `postgres`, banco `nexus`, portas 5432, 8080, 3000).

```env
POSTGRES_DB=nexus
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_PORT=5432
BACKEND_PORT=8080
FRONTEND_PORT=3000
VITE_API_URL=http://localhost:8080
```

Ajuste a senha (`POSTGRES_PASSWORD`) se quiser. As portas podem ficar assim para uso local.

## 3. Subir os containers

Abra um terminal na **raiz do projeto** e execute:

```bash
docker compose up -d
```

- Na primeira vez ele vai **construir** as imagens do backend e do frontend e **baixar** a do Postgres (pode levar alguns minutos).
- `-d` = roda em segundo plano.

## 4. Acessar a aplicação

- **Interface (frontend):** [http://localhost:3000](http://localhost:3000)
- **API (backend):** [http://localhost:8080](http://localhost:8080)

**Login padrão** (se usou o script de dados iniciais do banco):

- Usuário: **admin**
- Senha: **admin123**

## 5. Parar e remover

```bash
docker compose down
```

Para apagar também os dados do banco (volumes):

```bash
docker compose down -v
```

## 6. Reconstruir após mudanças no código

```bash
docker compose up -d --build
```

## 7. Ver logs

```bash
docker compose logs -f
```

---

Resumo: criar o `.env` (a partir do `env.example.txt`), rodar `docker compose up -d` e acessar **http://localhost:3000**.
