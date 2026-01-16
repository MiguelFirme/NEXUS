# -*- coding: utf-8 -*-
"""
Configuração de Caminhos
Centraliza todos os caminhos para a pasta local do projeto
"""

import os
from pathlib import Path


class ConfiguracaoRede:
    """Configuração centralizada de caminhos"""
    
    # PASTA PRINCIPAL (pasta local do projeto)
    # Obtém o diretório pai do diretório NEXUS (raiz do projeto)
    _BASE_DIR = Path(__file__).parent.parent
    PASTA_GERENCIAMENTO = _BASE_DIR / "GERENCIAMENTO"
    
    # PASTA DE PENDENCIAS JSON (Pendências individuais)
    PASTA_REGISTROS_JSON = PASTA_GERENCIAMENTO / "PENDENCIAS"
    
    # ARQUIVOS CENTRALIZADOS (na pasta GERENCIAMENTO)
    ARQUIVO_REGISTRO = PASTA_GERENCIAMENTO / "AUDITORIA.csv"
    ARQUIVO_PENDENCIAS = PASTA_GERENCIAMENTO / "PENDENCIAS.csv"  # Legacy (não usado mais)
    ARQUIVO_USUARIOS = PASTA_GERENCIAMENTO / "DADOS_LOGIN.csv"
    
    # ARQUIVO DE CONFIGURAÇÃO (na pasta NEXUS)
    ARQUIVO_SITUACOES = Path(__file__).parent / "valores_situacao.txt"
    ARQUIVO_CAMPOS_JSON = Path(__file__).parent / "mapeamento_campos.json"
    
    @classmethod
    def inicializar_estrutura(cls):
        """
        Cria a estrutura de pastas necessária
        
        Returns:
            bool: True se sucesso
        """
        try:
            # Criar pasta de gerenciamento
            cls.PASTA_GERENCIAMENTO.mkdir(exist_ok=True)
            
            # Criar pasta de pendências JSON
            cls.PASTA_REGISTROS_JSON.mkdir(exist_ok=True)
            # Criar todas as subpastas de status
            (cls.PASTA_REGISTROS_JSON / "ATIVAS").mkdir(exist_ok=True)
            (cls.PASTA_REGISTROS_JSON / "ARQUIVADAS").mkdir(exist_ok=True)
            (cls.PASTA_REGISTROS_JSON / "CANCELADAS").mkdir(exist_ok=True)
            (cls.PASTA_REGISTROS_JSON / "CONCLUÍDAS").mkdir(exist_ok=True)
            (cls.PASTA_REGISTROS_JSON / "EM ATRASO").mkdir(exist_ok=True)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar estrutura: {e}")
            return False
    
    @classmethod
    def verificar_acesso(cls):
        """
        Verifica se tem acesso às pastas
        
        Returns:
            dict: Status de acesso
        """
        status = {
            'pasta_gerenciamento': cls.PASTA_GERENCIAMENTO.exists(),
            'pasta_registros': cls.PASTA_REGISTROS_JSON.exists(),
            'acesso_completo': False
        }
        
        status['acesso_completo'] = all([
            status['pasta_gerenciamento'],
            status['pasta_registros']
        ])
        
        return status
    
    @classmethod
    def obter_valores_situacao(cls):
        """
        Carrega os valores de situação do arquivo centralizado
        
        Returns:
            list: Lista de valores de situação (sem 'Todas')
        """
        try:
            if not cls.ARQUIVO_SITUACOES.exists():
                # Valores padrão se arquivo não existir
                return ['Novo contato', 'Proposta enviada', 'Retorno pendente', 
                        'Em negociação', 'Proposta aprovada', 'Entrada pendente', 
                        'Venda Concluída', 'Venda Perdida']
            
            with open(cls.ARQUIVO_SITUACOES, 'r', encoding='utf-8') as f:
                valores = [linha.strip() for linha in f if linha.strip()]
            
            # Se arquivo estiver vazio, retornar valores padrão
            if not valores:
                return ['Novo contato', 'Proposta enviada', 'Retorno pendente', 
                        'Em negociação', 'Proposta aprovada', 'Entrada pendente', 
                        'Venda Concluída', 'Venda Perdida']
            
            return valores
            
        except Exception as e:
            print(f"⚠️ Erro ao carregar valores de situação: {e}")
            # Retornar valores padrão em caso de erro
            return ['Novo contato', 'Proposta enviada', 'Retorno pendente', 
                    'Em negociação', 'Proposta aprovada', 'Entrada pendente', 
                    'Venda Concluída', 'Venda Perdida']
    
    @classmethod
    def obter_mapeamento_campos(cls):
        """
        Retorna o mapeamento centralizado de campos do JSON de pendências
        
        Returns:
            dict: Mapeamento de campos canônicos
        """
        # Mapeamento padrão (campos canônicos)
        mapeamento_padrao = {
            # Campos principais
            'usuario': 'usuario',  # Nome do usuário responsável (antigo: vendedor)
            'nome_usuario': 'nome_usuario',  # Nome completo do usuário
            'setor': 'setor',  # Setor responsável
            'situacao': 'situacao',  # Situação comercial
            'status': 'status',  # Status operacional
            'numero': 'numero',  # Número da pendência
            'data_criacao': 'data_criacao',
            'data_atualizacao': 'data_atualizacao',
            'prioridade': 'prioridade',
            'prazo_resposta': 'prazo_resposta',
            'observacoes': 'observacoes',
            'origem': 'origem',
            'equipamento': 'equipamento',
            'cliente': 'cliente',
            'historico': 'historico',
            'propostas_vinculadas': 'propostas_vinculadas',
            'anexos': 'anexos',
            'tags': 'tags',
            'metadata': 'metadata',
        }
        
        # Tentar carregar de arquivo JSON se existir
        try:
            if cls.ARQUIVO_CAMPOS_JSON.exists():
                import json
                with open(cls.ARQUIVO_CAMPOS_JSON, 'r', encoding='utf-8') as f:
                    mapeamento_customizado = json.load(f)
                    # Mesclar com padrão (customizado tem prioridade)
                    mapeamento_padrao.update(mapeamento_customizado)
        except Exception as e:
            print(f"⚠️ Erro ao carregar mapeamento de campos: {e}")
        
        return mapeamento_padrao
    
    @classmethod
    def obter_campo_canonico(cls, campo):
        """
        Retorna o nome canônico de um campo
        
        Args:
            campo: Nome do campo (pode ser antigo ou novo)
            
        Returns:
            str: Nome canônico do campo
        """
        mapeamento = cls.obter_mapeamento_campos()
        
        # Mapeamento de compatibilidade (campos antigos → canônicos)
        compatibilidade = {
            'vendedor': 'usuario',
            'vendedor_nome': 'usuario',
            'nome_vendedor': 'usuario',
        }
        
        # Se está no mapeamento de compatibilidade, retornar canônico
        if campo in compatibilidade:
            return compatibilidade[campo]
        
        # Se está no mapeamento, retornar o valor
        if campo in mapeamento:
            return mapeamento[campo]
        
        # Caso contrário, retornar o próprio campo
        return campo
    

