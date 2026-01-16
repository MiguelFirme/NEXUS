# -*- coding: utf-8 -*-
"""
Módulo de Gerenciadores de Negócio
"""

from .gerenciador_pendencias_json import GerenciadorPendenciasJSON
# RastreadorPropostas removido - funcionalidade de rastreamento de propostas foi descontinuada
# GerenciadorPrecos removido - funcionalidade de busca de preços no Excel foi descontinuada

__all__ = ['GerenciadorPendenciasJSON']

