# -*- coding: utf-8 -*-
"""
Componentes reutilizáveis da interface para exibir Dados do Cliente

Este módulo padroniza a exibição dos dados do cliente (somente 4 campos):
- Razão Social
- CPF/CNPJ
- Inscrição
- Endereço

Uso:
    frame = criar_bloco_dados_cliente(parent, cliente_data)
    frame.pack(...)
"""

import tkinter as tk
from tkinter import ttk


def criar_bloco_dados_cliente(parent, cliente_data):
    """Cria e retorna um frame com os 4 campos padronizados de Dados do Cliente.

    Args:
        parent: container pai (tk/ttk Frame)
        cliente_data (dict): dicionário com chaves esperadas: razao_social, cnpj, inscricao_estadual, endereco, cidade

    Returns:
        ttk.Frame: frame já preenchido com labels e valores
    """
    dados_frame = ttk.LabelFrame(parent, text=" 👤 Dados do Cliente ", padding="8")

    info_grid = ttk.Frame(dados_frame)
    info_grid.pack(fill='x', expand=True)

    # Configurar colunas
    info_grid.columnconfigure(0, weight=0, minsize=110)  # Labels
    info_grid.columnconfigure(1, weight=1, minsize=180)  # Valores

    # Razão Social
    ttk.Label(info_grid, text="Razão Social:", font=('Arial', 8, 'bold'), width=14).grid(row=0, column=0, sticky='w', pady=2)
    razao_social = (cliente_data.get('razao_social', '') or '-').strip()
    if not razao_social:
        razao_social = '-'
    ttk.Label(info_grid, text=razao_social, font=('Arial', 8)).grid(row=0, column=1, sticky='w', padx=5, pady=2)

    # CPF/CNPJ
    ttk.Label(info_grid, text="CPF/CNPJ:", font=('Arial', 8, 'bold'), width=14).grid(row=1, column=0, sticky='w', pady=2)
    cnpj = (cliente_data.get('cnpj', '') or '-').strip() or '-'
    ttk.Label(info_grid, text=cnpj, font=('Arial', 8)).grid(row=1, column=1, sticky='w', padx=5, pady=2)

    # Inscrição
    ttk.Label(info_grid, text="Inscrição:", font=('Arial', 8, 'bold'), width=14).grid(row=2, column=0, sticky='w', pady=2)
    inscr = (cliente_data.get('inscricao_estadual', '') or '-').strip() or '-'
    ttk.Label(info_grid, text=inscr, font=('Arial', 8)).grid(row=2, column=1, sticky='w', padx=5, pady=2)

    # Endereço (tentar endereco, senão cidade)
    ttk.Label(info_grid, text="Endereço:", font=('Arial', 8, 'bold'), width=14).grid(row=3, column=0, sticky='w', pady=2)
    endereco = (cliente_data.get('endereco', '') or '').strip()
    if not endereco:
        endereco = (cliente_data.get('cidade', '') or '').strip()
    endereco = endereco if endereco else '-'
    ttk.Label(info_grid, text=endereco, font=('Arial', 8)).grid(row=3, column=1, sticky='w', padx=5, pady=2)

    return dados_frame


