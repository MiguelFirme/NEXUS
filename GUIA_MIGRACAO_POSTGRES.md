# Guia de Migração: CSV para PostgreSQL - Projeto NEXUS

Este documento descreve as alterações necessárias para migrar o sistema NEXUS de armazenamento em arquivos CSV/JSON para um banco de dados PostgreSQL centralizado.

## 1. Preparação do Banco de Dados

1.  **Criar o Banco**: No pgAdmin ou via terminal, crie o banco de dados:
    ```sql
    CREATE DATABASE "Nexus_DB";
    ```
2.  **Restaurar Estrutura**: Execute o arquivo `estrutura.sql` que está na pasta `BANCO DE DADOS`:
    ```bash
    psql -U postgres -d "Nexus_DB" -f "BANCO DE DADOS/estrutura.sql"
    ```

## 2. Novos Arquivos Criados

Foram adicionados dois arquivos essenciais na pasta `NEXUS/`:

1.  **`database.py`**: Gerencia a conexão e o pool de conexões com o PostgreSQL.
    *   *Ação necessária*: Edite este arquivo para inserir a senha correta do seu usuário `postgres`.
2.  **`migrar_dados.py`**: Script utilitário para ler seus arquivos CSV e JSON atuais e inseri-los no banco de dados.
    *   *Como usar*: Execute `python migrar_dados.py` após configurar a conexão no `database.py`.

## 3. Modificações Necessárias no Código

Para que o sistema passe a usar o banco de dados em vez dos arquivos, as seguintes alterações devem ser feitas:

### A. `mapeamento_usuarios.py`
A função `_carregar_mapeamento_usuarios` deve ser alterada para buscar dados da tabela `nexus.usuarios` e `nexus.setores` em vez de ler o `DADOS_LOGIN.csv`.

**Exemplo de alteração:**
```python
def _carregar_mapeamento_usuarios():
    from database import Database
    query = "SELECT * FROM nexus.v_usuarios_com_setor"
    usuarios_db = Database.execute_query(query, fetch=True)
    
    for row in usuarios_db:
        codigo = row['codigo_usuario']
        USUARIOS[codigo] = {
            'nome': row['nome_usuario'],
            'setor': row['nome_setor'],
            # ... preencher demais campos
        }
```

### B. `gerenciador_pendencias_json.py`
As funções `criar_pendencia`, `ler_pendencia` e `atualizar_pendencia` devem ser refatoradas para executar comandos `INSERT`, `SELECT` e `UPDATE` na tabela `nexus.pendencias`.

### C. `iniciar.py`
A função `validar_e_carregar_dados` deve validar o usuário consultando o banco de dados pelo nome do computador (`computador_usuario`), eliminando a dependência do CSV no arranque do sistema.

## 4. Dependências
Adicione `psycopg2-binary` ao seu arquivo `requirements.txt` para permitir a conexão do Python com o PostgreSQL:
```text
psycopg2-binary>=2.9.0
```

---
**Nota**: Os arquivos `database.py` e `migrar_dados.py` já foram criados na pasta do projeto para facilitar o início do processo.
