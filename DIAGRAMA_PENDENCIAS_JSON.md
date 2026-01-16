# Diagrama da Estrutura dos JSONs de Pendências

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ARQUIVO: {numero}.json                          │
│                    Localização: PENDENCIAS/{status}/                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          OBJETO PRINCIPAL                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌───────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  CAMPOS BASE  │      │   OBJETO CLIENTE │      │  STATUS/SITUAÇÃO  │
├───────────────┤      ├──────────────────┤      ├──────────────────┤
│ numero        │      │ razao_social      │      │ situacao         │
│ data_criacao  │      │ telefone          │      │ status           │
│ data_atualiz. │      │ cnpj              │      │ prioridade       │
│ vendedor      │      │ cidade            │      │ prazo_resposta   │
│ setor         │      │ contato           │      │ origem           │
│ equipamento   │      │ email             │      │ observacoes      │
│               │      │ inscricao_estad.  │      │                  │
│               │      │ endereco           │      │                  │
└───────────────┘      └──────────────────┘      └──────────────────┘
        │
        │
        ├─────────────────────────────────────────────────────────────┐
        │                                                             │
        ▼                                                             ▼
┌──────────────────┐                                      ┌──────────────────┐
│  ARRAY HISTÓRICO  │                                      │  ARRAY PROPOSTAS  │
│  historico[]     │                                      │  propostas_vincul.│
├──────────────────┤                                      ├──────────────────┤
│  ┌────────────┐  │                                      │  ┌────────────┐  │
│  │ data       │  │                                      │  │ codigo     │  │
│  │ status_ant.│  │                                      │  │ data       │  │
│  │ status_novo│  │                                      │  │ arquivo    │  │
│  │ usuario    │  │                                      │  └────────────┘  │
│  └────────────┘  │                                      │  ┌────────────┐  │
│  ┌────────────┐  │                                      │  │ codigo     │  │
│  │ ...        │  │                                      │  │ ...        │  │
│  └────────────┘  │                                      │  └────────────┘  │
└──────────────────┘                                      └──────────────────┘
        │
        │
        ├─────────────────────────────────────────────────────────────┐
        │                                                             │
        ▼                                                             ▼
┌──────────────────┐                                      ┌──────────────────┐
│  ARRAY ANEXOS    │                                      │  ARRAY TAGS       │
│  anexos[]        │                                      │  tags[]           │
├──────────────────┤                                      ├──────────────────┤
│  (preparado para │                                      │  (preparado para │
│   futuras impl.) │                                      │   futuras impl.) │
└──────────────────┘                                      └──────────────────┘
        │
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        OBJETO METADATA                                  │
├─────────────────────────────────────────────────────────────────────────┤
│ versao                  │ "1.0"                                        │
│ ultima_modificacao      │ "2024-01-01T10:30:00.123456"                │
│ modificado_por          │ "Thalita Costa"                              │
│                                                                         │
│ (Usado para detectar conflitos de edição simultânea)                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Diagrama Detalhado por Seção

### 1. CAMPOS BASE
```
┌─────────────────────────────────────────────┐
│ numero              │ "2401010001"          │
│ data_criacao        │ "2024-01-01T10:30..." │
│ data_atualizacao    │ "2024-01-01T10:30..." │
│ vendedor            │ "Thalita Costa"       │
│ setor               │ "COMERCIAL GUINDASTES"│
│ equipamento         │ "Guindaste OLC 10T"   │
└─────────────────────────────────────────────┘
```

### 2. OBJETO CLIENTE
```
┌─────────────────────────────────────────────┐
│ cliente: {                                  │
│   razao_social:      "Empresa XYZ Ltda"     │
│   telefone:         "(11) 99999-9999"      │
│   cnpj:               "12.345.678/0001-90"  │
│   cidade:             "São Paulo"          │
│   contato:            "João Silva"         │
│   email:              "contato@empresa.com" │
│   inscricao_estadual: "123.456.789.012"     │
│   endereco:           "Rua Exemplo, 123"   │
│ }                                           │
└─────────────────────────────────────────────┘
```

### 3. STATUS E SITUAÇÃO
```
┌─────────────────────────────────────────────┐
│ situacao:        "Novo contato"             │
│                  │                           │
│                  ├─ "Proposta enviada"       │
│                  ├─ "Retorno pendente"       │
│                  ├─ "Em negociação"          │
│                  ├─ "Proposta aprovada"      │
│                  ├─ "Entrada pendente"       │
│                  ├─ "Venda Concluída"        │
│                  └─ "Venda Perdida"          │
│                                             │
│ status:          "Ativa"                    │
│                  │                           │
│                  ├─ "Arquivada"              │
│                  ├─ "Cancelada"              │
│                  ├─ "Concluída"              │
│                  └─ "Em Atraso"              │
│                                             │
│ prioridade:      "normal" / "alta" / "baixa" │
│ prazo_resposta:  ""                          │
│ origem:          "manual"                    │
│ observacoes:     "Texto livre..."           │
└─────────────────────────────────────────────┘
```

### 4. ARRAY HISTÓRICO
```
historico: [
  ┌─────────────────────────────────────────────┐
  │ {                                            │
  │   data:            "2024-01-01T10:30:00..." │
  │   status_anterior: ""                       │
  │   status_novo:     "Pendência registrada..."│
  │   usuario:         "Thalita Costa"          │
  │ }                                            │
  └─────────────────────────────────────────────┘
  ┌─────────────────────────────────────────────┐
  │ {                                            │
  │   data:            "2024-01-02T14:20:00..."  │
  │   status_anterior: "Novo contato"           │
  │   status_novo:     "Proposta enviada"       │
  │   usuario:         "Thalita Costa"          │
  }                                            │
  └─────────────────────────────────────────────┘
  ┌─────────────────────────────────────────────┐
  │ {                                            │
  │   data:            "2024-01-03T09:15:00..."  │
  │   status_anterior: "Ativa"                  │
  │   status_novo:     "Status: Ativa → Arquivada"│
  │   usuario:         "Sistema"                │
  }                                            │
  └─────────────────────────────────────────────┘
]
```

### 5. ARRAY PROPOSTAS VINCULADAS
```
propostas_vinculadas: [
  ┌─────────────────────────────────────────────┐
  │ {                                            │
  │   codigo:  "PROP-2024-001"                  │
  │   data:    "2024-01-02T14:20:00..."         │
  │   arquivo: "PROP-2024-001.pdf"              │
  }                                            │
  └─────────────────────────────────────────────┘
  ┌─────────────────────────────────────────────┐
  │ {                                            │
  │   codigo:  "PROP-2024-002"                   │
  │   data:    "2024-01-05T11:30:00..."         │
  │   arquivo: "PROP-2024-002.pdf"              │
  }                                            │
  └─────────────────────────────────────────────┘
]
```

### 6. METADATA
```
metadata: {
  ┌─────────────────────────────────────────────┐
  │ versao:              "1.0"                  │
  │ ultima_modificacao:  "2024-01-01T10:30..."  │
  │ modificado_por:     "Thalita Costa"         │
  │                                             │
  │ [Usado para detectar conflitos de edição]  │
  └─────────────────────────────────────────────┘
}
```

---

## Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────┐
│                    CRIAÇÃO DE PENDÊNCIA                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  Preenche campos obrigatórios:       │
        │  - cliente (razao_social, telefone)  │
        │  - equipamento                       │
        │  - observacoes (opcional)            │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  Sistema gera automaticamente:       │
        │  - numero (sequencial)                │
        │  - data_criacao / data_atualizacao    │
        │  - vendedor (distribuição por setor)  │
        │  - setor                              │
        │  - situacao: "Novo contato"          │
        │  - status: "Ativa"                   │
        │  - historico[0] (criação)            │
        │  - metadata                           │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  Salva em:                            │
        │  PENDENCIAS/ATIVAS/{numero}.json      │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  OPERAÇÕES POSTERIORES:               │
        │  - Atualizar situação                 │
        │  - Editar observações                 │
        │  - Transferir entre usuários          │
        │  - Mover entre pastas (status)         │
        │  - Vincular propostas                 │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  Cada operação adiciona entrada    │
        │  no historico[] e atualiza:          │
        │  - data_atualizacao                   │
        │  - metadata.ultima_modificacao       │
        │  - metadata.modificado_por            │
        └───────────────────────────────────────┘
```

---

## Relação Status ↔ Pasta

```
┌─────────────────────────────────────────────────────────────┐
│                    MAPEAMENTO STATUS → PASTA                 │
└─────────────────────────────────────────────────────────────┘

    status: "Ativa"      ──────►  PENDENCIAS/ATIVAS/
    status: "Arquivada"  ──────►  PENDENCIAS/ARQUIVADAS/
    status: "Cancelada"  ──────►  PENDENCIAS/CANCELADAS/
    status: "Concluída"  ──────►  PENDENCIAS/CONCLUÍDAS/
    status: "Em Atraso"  ──────►  PENDENCIAS/EM ATRASO/

    ⚠️ IMPORTANTE: O campo "status" no JSON deve sempre
       corresponder à pasta onde o arquivo está armazenado!
```

---

## Tipos de Dados

```
┌─────────────────────────────────────────────────────────────┐
│                      TIPOS DE DADOS                          │
└─────────────────────────────────────────────────────────────┘

STRING:
  - numero, vendedor, setor, equipamento
  - situacao, status, prioridade, origem
  - cliente.* (todos os campos)
  - historico[].status_anterior, status_novo, usuario
  - propostas_vinculadas[].codigo, arquivo
  - metadata.versao, modificado_por

ISO DATETIME (string):
  - data_criacao, data_atualizacao
  - historico[].data
  - propostas_vinculadas[].data
  - metadata.ultima_modificacao

ARRAY:
  - historico[] (objetos)
  - propostas_vinculadas[] (objetos)
  - anexos[] (vazio, preparado)
  - tags[] (vazio, preparado)

OBJETO:
  - cliente {}
  - metadata {}
```

---

## Exemplo Completo Visual

```
{
  "numero": "2401010001"
  │
  ├─ "data_criacao": "2024-01-01T10:30:00.123456"
  ├─ "data_atualizacao": "2024-01-01T10:30:00.123456"
  ├─ "vendedor": "Thalita Costa"
  ├─ "setor": "COMERCIAL GUINDASTES"
  ├─ "equipamento": "Guindaste OLC 10T"
  │
  ├─ "cliente": {
  │     ├─ "razao_social": "Empresa XYZ Ltda"
  │     ├─ "telefone": "(11) 99999-9999"
  │     ├─ "cnpj": "12.345.678/0001-90"
  │     ├─ "cidade": "São Paulo"
  │     ├─ "contato": "João Silva"
  │     ├─ "email": "contato@empresa.com"
  │     ├─ "inscricao_estadual": "123.456.789.012"
  │     └─ "endereco": "Rua Exemplo, 123"
  │   }
  │
  ├─ "situacao": "Novo contato"
  ├─ "status": "Ativa"
  ├─ "prioridade": "normal"
  ├─ "prazo_resposta": ""
  ├─ "origem": "manual"
  ├─ "observacoes": "Cliente interessado em aluguel"
  │
  ├─ "historico": [
  │     {
  │       ├─ "data": "2024-01-01T10:30:00.123456"
  │       ├─ "status_anterior": ""
  │       ├─ "status_novo": "Pendência registrada..."
  │       └─ "usuario": "Thalita Costa"
  │     }
  │   ]
  │
  ├─ "propostas_vinculadas": [
  │     {
  │       ├─ "codigo": "PROP-2024-001"
  │       ├─ "data": "2024-01-02T14:20:00.123456"
  │       └─ "arquivo": "PROP-2024-001.pdf"
  │     }
  │   ]
  │
  ├─ "anexos": []
  ├─ "tags": []
  │
  └─ "metadata": {
        ├─ "versao": "1.0"
        ├─ "ultima_modificacao": "2024-01-01T10:30:00.123456"
        └─ "modificado_por": "Thalita Costa"
      }
}
```
