# Estrutura dos Arquivos JSON de Pendências

## Visão Geral
Cada pendência é armazenada como um arquivo JSON individual na pasta `GERENCIAMENTO/PENDENCIAS/`, organizada em subpastas por status:
- `ATIVAS/`
- `ARQUIVADAS/`
- `CANCELADAS/`
- `CONCLUÍDAS/`
- `EM ATRASO/`

O nome do arquivo segue o padrão: `{numero_pendencia}.json` (ex: `2401010001.json`)

---

## Estrutura Completa do JSON

```json
{
  "numero": "2401010001",
  "data_criacao": "2024-01-01T10:30:00.123456",
  "data_atualizacao": "2024-01-01T10:30:00.123456",
  "vendedor": "Thalita Costa",
  "setor": "COMERCIAL GUINDASTES",
  "cliente": {
    "razao_social": "Empresa XYZ Ltda",
    "telefone": "(11) 99999-9999",
    "cnpj": "12.345.678/0001-90",
    "cidade": "São Paulo",
    "contato": "João Silva",
    "email": "contato@empresa.com",
    "inscricao_estadual": "123.456.789.012",
    "endereco": "Rua Exemplo, 123"
  },
  "equipamento": "Guindaste OLC 10T",
  "situacao": "Novo contato",
  "status": "Ativa",
  "prioridade": "normal",
  "prazo_resposta": "",
  "origem": "manual",
  "observacoes": "Cliente interessado em aluguel de guindaste",
  "historico": [
    {
      "data": "2024-01-01T10:30:00.123456",
      "status_anterior": "",
      "status_novo": "Pendência registrada no setor COMERCIAL GUINDASTES.",
      "usuario": "Thalita Costa"
    }
  ],
  "propostas_vinculadas": [
    {
      "codigo": "PROP-2024-001",
      "data": "2024-01-02T14:20:00.123456",
      "arquivo": "PROP-2024-001.pdf"
    }
  ],
  "anexos": [],
  "tags": [],
  "metadata": {
    "versao": "1.0",
    "ultima_modificacao": "2024-01-01T10:30:00.123456",
    "modificado_por": "Thalita Costa"
  }
}
```

---

## Descrição Detalhada dos Campos

### Campos Principais

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `numero` | string | Número único da pendência (formato: AAMMDDSSSS) | `"2401010001"` |
| `data_criacao` | string (ISO) | Data/hora de criação em formato ISO 8601 | `"2024-01-01T10:30:00.123456"` |
| `data_atualizacao` | string (ISO) | Data/hora da última atualização | `"2024-01-01T10:30:00.123456"` |
| `vendedor` | string | Nome do usuário responsável pela pendência | `"Thalita Costa"` |
| `setor` | string | Setor ao qual a pendência foi atribuída | `"COMERCIAL GUINDASTES"` |

### Objeto `cliente`

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `razao_social` | string | Razão social da empresa cliente | `"Empresa XYZ Ltda"` |
| `telefone` | string | Telefone de contato | `"(11) 99999-9999"` |
| `cnpj` | string | CNPJ da empresa | `"12.345.678/0001-90"` |
| `cidade` | string | Cidade do cliente | `"São Paulo"` |
| `contato` | string | Nome do contato na empresa | `"João Silva"` |
| `email` | string | E-mail de contato | `"contato@empresa.com"` |
| `inscricao_estadual` | string | Inscrição estadual | `"123.456.789.012"` |
| `endereco` | string | Endereço completo | `"Rua Exemplo, 123"` |

### Campos de Status e Situação

| Campo | Tipo | Descrição | Valores Possíveis |
|-------|------|-----------|-------------------|
| `situacao` | string | **Pipeline comercial** (situação no funil de vendas) | `"Novo contato"`, `"Proposta enviada"`, `"Retorno pendente"`, `"Em negociação"`, `"Proposta aprovada"`, `"Entrada pendente"`, `"Venda Concluída"`, `"Venda Perdida"` |
| `status` | string | **Estado operacional** (onde está fisicamente) | `"Ativa"`, `"Arquivada"`, `"Cancelada"`, `"Concluída"`, `"Em Atraso"` |

**Nota:** O campo `status` reflete a pasta onde o arquivo está armazenado:
- `"Ativa"` → pasta `ATIVAS/`
- `"Arquivada"` → pasta `ARQUIVADAS/`
- `"Cancelada"` → pasta `CANCELADAS/`
- `"Concluída"` → pasta `CONCLUÍDAS/`
- `"Em Atraso"` → pasta `EM ATRASO/`

### Outros Campos

| Campo | Tipo | Descrição | Valores Possíveis |
|-------|------|-----------|-------------------|
| `equipamento` | string | Equipamento relacionado à pendência | `"Guindaste OLC 10T"` |
| `prioridade` | string | Nível de prioridade | `"normal"`, `"alta"`, `"baixa"` |
| `prazo_resposta` | string | Prazo para resposta (se houver) | `""` (vazio) |
| `origem` | string | Como a pendência foi criada | `"manual"`, `"importacao"`, etc. |
| `observacoes` | string | Observações gerais sobre a pendência | Texto livre |

### Array `historico`

Registra todas as alterações importantes da pendência. Cada entrada contém:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `data` | string (ISO) | Data/hora da alteração |
| `status_anterior` | string | Valor anterior (situação/status) |
| `status_novo` | string | Novo valor ou descrição da ação |
| `usuario` | string | Nome do usuário que fez a alteração |

**Exemplos de entradas no histórico:**
- Criação: `"Pendência registrada no setor COMERCIAL GUINDASTES."`
- Mudança de situação: `"Novo contato"` → `"Proposta enviada"`
- Mudança de status: `"Status: Ativa → Arquivada"`
- Transferência: `"Transferida: Thalita Costa → Ricardo Feltrin"`
- Movimentação: `"ARQUIVADA - Movida de ATIVAS para ARQUIVADAS"`

### Array `propostas_vinculadas`

Lista de propostas comerciais vinculadas à pendência:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `codigo` | string | Código da proposta |
| `data` | string (ISO) | Data de criação/vinculação |
| `arquivo` | string | Nome do arquivo PDF da proposta |

### Array `anexos`

Lista de arquivos anexados à pendência (atualmente não utilizado, mas preparado para futuras implementações).

### Array `tags`

Tags para categorização (atualmente não utilizado, mas preparado para futuras implementações).

### Objeto `metadata`

Metadados técnicos do arquivo:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `versao` | string | Versão do formato do JSON | `"1.0"` |
| `ultima_modificacao` | string (ISO) | Timestamp da última modificação |
| `modificado_por` | string | Nome do último usuário que modificou |

**Uso:** O campo `ultima_modificacao` é usado para detectar conflitos de edição simultânea.

---

## Operações que Modificam o JSON

### 1. Criação de Pendência
- Cria estrutura completa com valores padrão
- Inicializa `historico` com entrada de criação
- Define `status` como `"Ativa"` e `situacao` como `"Novo contato"`

### 2. Atualização de Situação/Status
- Atualiza campo `situacao` ou `status`
- Adiciona entrada no `historico`
- Atualiza `data_atualizacao` e `metadata.ultima_modificacao`

### 3. Edição de Observações
- Atualiza campo `observacoes`
- Adiciona entrada no `historico`
- Atualiza timestamps

### 4. Transferência entre Usuários
- Atualiza campo `vendedor`
- Adiciona entrada no `historico` com detalhes da transferência

### 5. Movimentação entre Pastas
- Move arquivo físico entre pastas (ATIVAS → ARQUIVADAS, etc.)
- Atualiza campo `status` conforme pasta destino
- Adiciona entrada no `historico` com motivo

### 6. Vinculação de Proposta
- Adiciona entrada em `propostas_vinculadas`
- Adiciona entrada no `historico`

---

## Observações Importantes

1. **Encoding:** Todos os arquivos JSON são salvos com encoding UTF-8
2. **Formatação:** JSON é formatado com indentação de 2 espaços para legibilidade
3. **Conflitos:** O sistema detecta edições simultâneas comparando `metadata.ultima_modificacao`
4. **Nomenclatura:** O campo `vendedor` ainda existe no JSON por compatibilidade, mas o sistema agora usa `usuário` na interface
5. **Status vs Situação:** 
   - `status` = onde está (pasta física)
   - `situacao` = pipeline comercial (funil de vendas)
