# -*- coding: utf-8 -*-
"""
Configuração NEXUS - Versão PostgreSQL
Centraliza configurações do sistema
"""

from pathlib import Path

class ConfiguracaoRede:
    """Configuração centralizada (Agora focada em Banco de Dados)"""
    PASTA_REGISTROS_JSON = r"C:\Users\migue\Downloads\NEXUS_POSTGRES_FINAL\registros_json"
    # O sistema agora utiliza PostgreSQL. 
    # As configurações de conexão estão em database.py
    
    @classmethod
    def obter_valores_situacao(cls):
        """Retorna as situações padrão do sistema"""
        return ['Novo contato', 'Proposta enviada', 'Retorno pendente', 
                'Em negociação', 'Proposta aprovada', 'Entrada pendente', 
                'Venda Concluída', 'Venda Perdida']

    @classmethod
    def inicializar_estrutura(cls):
        """Não há mais necessidade de criar pastas para CSV/JSON"""
        return True
