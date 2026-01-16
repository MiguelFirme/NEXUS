# -*- coding: utf-8 -*-
"""
Monitor de Mudanças em Tempo Real
Sistema de Propostas Comerciais - Olivo Guindastes

Monitora mudanças nos arquivos JSON de pendências e notifica a interface
para atualização automática sem necessidade de clicar em botão.
"""

import os
import time
from pathlib import Path
from datetime import datetime
import hashlib


class MonitorMudancas:
    """Monitora mudanças em arquivos/pastas para sincronização multi-usuário"""
    
    def __init__(self, pasta_registros, monitorar_arquivadas=True):
        """
        Inicializa o monitor (OTIMIZADO)
        
        Args:
            pasta_registros: Path da pasta REGISTROS
            monitorar_arquivadas: Se True, também monitora a pasta ARQUIVADAS.
                                  Se False, foca apenas em ATIVAS (mais leve).
        """
        self.pasta_registros = Path(pasta_registros)
        self.monitorar_arquivadas = bool(monitorar_arquivadas)
        self.cache_estados = {}
        self.ultima_verificacao = None
        # Cache de contagem de arquivos (mais rápido que hash completo)
        self._cache_contagem = {}
        self._cache_ultima_modificacao = {}
    
    def _calcular_hash_pasta(self, pasta):
        """
        Calcula hash baseado em arquivos da pasta (OTIMIZADO)
        Usa contagem + timestamp mais recente ao invés de processar todos os arquivos
        
        Returns:
            str: Hash MD5 representando estado da pasta
        """
        if not pasta.exists():
            return ""
        
        try:
            # OTIMIZAÇÃO: Usar contagem + timestamp mais recente (muito mais rápido)
            arquivos = list(pasta.glob("*.json"))
            contagem = len(arquivos)
            
            if contagem == 0:
                return "0"
            
            # Pegar apenas o timestamp de modificação mais recente (não precisa de todos)
            timestamp_mais_recente = 0
            for arq in arquivos[:100]:  # Limitar a 100 para performance (suficiente para detectar mudanças)
                try:
                    stat = arq.stat()
                    if stat.st_mtime > timestamp_mais_recente:
                        timestamp_mais_recente = stat.st_mtime
                except:
                    pass
            
            # Hash simples: contagem + timestamp mais recente
            info = f"{contagem}:{timestamp_mais_recente}"
            return hashlib.md5(info.encode()).hexdigest()
        except Exception:
            # Fallback para método antigo se houver erro
            return ""
    
    def verificar_mudancas(self):
        """
        Verifica se houve mudanças desde última verificação
        
        Returns:
            dict: {
                'ativas': bool,
                'arquivadas': bool,
                'fechadas': bool,
                'qualquer_mudanca': bool
            }
        """
        mudancas = {
            'ativas': False,
            'arquivadas': False,
            'qualquer_mudanca': False
        }
        
        # Sempre monitora ATIVAS. ARQUIVADAS só quando habilitado para
        # deixar o refresh mais leve na maior parte do tempo.
        pastas = {
            'ativas': self.pasta_registros / "ATIVAS",
        }
        if self.monitorar_arquivadas:
            pastas['arquivadas'] = self.pasta_registros / "ARQUIVADAS"
        
        for nome, pasta in pastas.items():
            hash_atual = self._calcular_hash_pasta(pasta)
            hash_anterior = self.cache_estados.get(nome)
            
            if hash_anterior is None:
                # Primeira verificação - apenas armazenar
                self.cache_estados[nome] = hash_atual
            elif hash_atual != hash_anterior:
                # Houve mudança!
                mudancas[nome] = True
                mudancas['qualquer_mudanca'] = True
                self.cache_estados[nome] = hash_atual
        
        self.ultima_verificacao = datetime.now()
        return mudancas
    
    def resetar_cache(self):
        """Reseta o cache (força nova leitura na próxima verificação)"""
        self.cache_estados.clear()
    
    def definir_monitorar_arquivadas(self, valor: bool):
        """Ativa/desativa monitoramento da pasta ARQUIVADAS.
        
        Ao alterar, o cache é resetado para evitar inconsistências.
        """
        self.monitorar_arquivadas = bool(valor)
        self.resetar_cache()
    
    def obter_estatisticas_pastas(self):
        """
        Obtém contagem de arquivos por pasta
        
        Returns:
            dict: Contagem por pasta
        """
        stats = {}
        
        pastas = {
            'ativas': self.pasta_registros / "ATIVAS",
        }
        if self.monitorar_arquivadas:
            pastas['arquivadas'] = self.pasta_registros / "ARQUIVADAS"
        
        for nome, pasta in pastas.items():
            if pasta.exists():
                arquivos = list(pasta.glob("*.json"))
                stats[nome] = len(arquivos)
            else:
                stats[nome] = 0
        
        stats['total'] = sum(stats.values())
        return stats


class SistemaNotificacoes:
    """Sistema de notificações para mudanças em tempo real"""
    
    def __init__(self):
        self.callbacks = []
        self.historico_mudancas = []
    
    def registrar_callback(self, callback):
        """
        Registra função para ser chamada quando houver mudança
        
        Args:
            callback: Função a ser chamada (sem argumentos)
        """
        if callback not in self.callbacks:
            self.callbacks.append(callback)
    
    def remover_callback(self, callback):
        """Remove callback registrado"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def notificar_mudanca(self, tipo_mudanca='geral', dados=None):
        """
        Notifica todos os callbacks registrados
        
        Args:
            tipo_mudanca: Tipo de mudança ('criacao', 'atualizacao', 'exclusao', 'geral')
            dados: Dados adicionais sobre a mudança
        """
        # Registrar no histórico
        self.historico_mudancas.append({
            'timestamp': datetime.now(),
            'tipo': tipo_mudanca,
            'dados': dados
        })
        
        # Limitar histórico a últimas 100 mudanças
        if len(self.historico_mudancas) > 100:
            self.historico_mudancas = self.historico_mudancas[-100:]
        
        # Chamar todos os callbacks
        for callback in self.callbacks:
            try:
                callback()
            except Exception as e:
                print(f"⚠️ Erro em callback: {e}")
    
    def obter_historico_recente(self, limite=10):
        """Retorna histórico recente de mudanças"""
        return self.historico_mudancas[-limite:]


# Instância global do sistema de notificações
sistema_notificacoes = SistemaNotificacoes()

