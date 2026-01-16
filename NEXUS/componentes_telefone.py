# -*- coding: utf-8 -*-
"""
Componentes reutilizáveis da interface para campo de Telefone do Cliente

Este módulo padroniza a exibição do campo de telefone com detecção automática:
- Campo de entrada de telefone
- UF detectada automaticamente
- Vendedor detectado automaticamente
- Indicadores visuais

Uso:
    frame, widgets = criar_bloco_telefone_cliente(parent, telefone_atual='', larguras=None)
    frame.pack(...)
"""

import tkinter as tk
from tkinter import ttk


def criar_bloco_telefone_cliente(parent, telefone_atual='', larguras=None, auto_detect=True):
    """Cria e retorna um frame com campo de telefone e detecção automática.

    Args:
        parent: container pai (tk/ttk Frame)
        telefone_atual (str): telefone atual para pré-preencher
        larguras (dict): dict com larguras dos campos {'telefone': 20, 'vendedor': 15}

    Returns:
        tuple: (frame, widgets_dict)
            - frame: ttk.LabelFrame com todo o componente
            - widgets_dict: dict com {'entry_telefone', 'combo_uf', 'combo_vendedor', 'uf_indicator', 'vendedor_indicator'}
    """
    # Configurações padrão de largura
    larguras = larguras or {
        'telefone': 25,
        'vendedor': 15
    }
    
    # Frame principal
    frame_telefone = ttk.LabelFrame(parent, text=" 📞 Telefone do Cliente ", padding="15")
    
    # Container central para telefone
    telefone_container = ttk.Frame(frame_telefone)
    telefone_container.pack(anchor='center')
    
    # Campo de entrada do telefone
    entry_telefone = ttk.Entry(telefone_container, width=larguras['telefone'], font=('Arial', 11))
    entry_telefone.pack(side='left')
    if telefone_atual:
        entry_telefone.insert(0, telefone_atual)
    
    # Container para UF e Vendedor (dentro da mesma seção de telefone)
    auto_container = ttk.Frame(frame_telefone)
    auto_container.pack(anchor='center', pady=(20, 0))
    
    # UF (lado esquerdo)
    uf_frame = ttk.Frame(auto_container)
    uf_frame.pack(side='left', padx=(0, 20))
    
    ttk.Label(uf_frame, text="UF:", font=('Arial', 10, 'bold')).pack(side='left', padx=(0, 10))
    combo_uf = ttk.Combobox(uf_frame, state='readonly', width=3, font=('Arial', 10))
    combo_uf['values'] = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    combo_uf.pack(side='left')
    
    # Indicador visual para UF
    uf_indicator = ttk.Label(uf_frame, text="⚪", font=('Arial', 12))
    uf_indicator.pack(side='left', padx=(5, 0))
    
    # Vendedor (lado direito)
    vendedor_frame = ttk.Frame(auto_container)
    vendedor_frame.pack(side='left')
    
    ttk.Label(vendedor_frame, text="Vendedor:", font=('Arial', 10, 'bold')).pack(side='left', padx=(0, 10))
    combo_vendedor = ttk.Combobox(vendedor_frame, state='readonly', width=larguras['vendedor'], font=('Arial', 10))
    
    # Carregar vendedores da planilha DADOS_VENDEDORES.csv
    try:
        from mapeamento_usuarios import obter_lista_usuarios
        vendedores_planilha = obter_lista_usuarios()
        combo_vendedor['values'] = vendedores_planilha
    except Exception as e:
        print(f"⚠️ Erro ao carregar vendedores da planilha: {e}")
        # Fallback para lista fixa
        # Se não conseguir carregar, usar lista vazia (sistema requer CSV)
        combo_vendedor['values'] = []
    
    combo_vendedor.pack(side='left')
    
    # Indicador visual para Vendedor
    vendedor_indicator = ttk.Label(vendedor_frame, text="⚪", font=('Arial', 12))
    vendedor_indicator.pack(side='left', padx=(5, 0))
    
    # Função de detecção automática
    def detectar_vendedor_auto(event=None):
        """Detecta vendedor automaticamente baseado no telefone"""
        telefone = entry_telefone.get().strip()
        
        if not telefone:
            # Resetar indicadores quando não há telefone
            uf_indicator.config(text="⚪", foreground='gray')
            vendedor_indicator.config(text="⚪", foreground='gray')
            combo_uf.set('')
            combo_vendedor.set('')
            return
        
        try:
            from mapeamento_usuarios import detectar_usuario_por_telefone
            info = detectar_usuario_por_telefone(telefone)
            
            if info:
                # Setor detectado (compatibilidade - pode não ter UF mais)
                if 'uf' in info and info['uf'] in combo_uf['values']:
                    combo_uf.set(info['uf'])
                    uf_indicator.config(text="🟢", foreground='green')
                elif 'setor' in info:
                    # Mostrar setor no indicador de UF (compatibilidade visual)
                    uf_indicator.config(text="🟢", foreground='green')
                
                # Usuário detectado
                usuario_nome = info.get('nome', '')
                if usuario_nome and usuario_nome in combo_vendedor['values']:
                    combo_vendedor.set(usuario_nome)
                    vendedor_indicator.config(text="🟢", foreground='green')
                else:
                    vendedor_indicator.config(text="🔴", foreground='red')
            else:
                # Nenhum dado detectado
                combo_uf.set('')
                combo_vendedor.set('')
                uf_indicator.config(text="🔴", foreground='red')
                vendedor_indicator.config(text="🔴", foreground='red')
                
        except Exception as e:
            print(f"Erro na detecção: {e}")
            combo_uf.set('')
            combo_vendedor.set('')
            uf_indicator.config(text="🔴", foreground='red')
            vendedor_indicator.config(text="🔴", foreground='red')
    
    # Função de formatação do telefone
    def validar_telefone(event=None):
        valor = entry_telefone.get()
        tem_codigo_pais = False
        if valor.startswith('+55'):
            tem_codigo_pais = True
            valor = valor[3:].strip()
        elif valor.startswith('55') and len(valor) > 2 and valor[2] in ' ()':
            tem_codigo_pais = True
            valor = valor[2:].strip()
        apenas_numeros = ''.join(filter(str.isdigit, valor))
        if len(apenas_numeros) > 11:
            apenas_numeros = apenas_numeros[:11]
        if len(apenas_numeros) == 11:
            telefone_formatado = f"+55 ({apenas_numeros[:2]}) {apenas_numeros[2]} {apenas_numeros[3:7]}-{apenas_numeros[7:]}"
        elif len(apenas_numeros) == 10:
            telefone_formatado = f"+55 ({apenas_numeros[:2]}) {apenas_numeros[2:6]}-{apenas_numeros[6:]}"
        elif len(apenas_numeros) >= 8:
            if len(apenas_numeros) >= 10:
                telefone_formatado = f"+55 ({apenas_numeros[:2]}) {apenas_numeros[2:6]}-{apenas_numeros[6:]}"
            else:
                telefone_formatado = f"+55 ({apenas_numeros[:2]}) {apenas_numeros[2:]}"
        else:
            telefone_formatado = apenas_numeros
        if telefone_formatado != entry_telefone.get():
            entry_telefone.delete(0, tk.END)
            entry_telefone.insert(0, telefone_formatado)
        
        # Chamar detecção após formatação
        detectar_vendedor_auto()
    
    # Vincular eventos (opcionais)
    if auto_detect:
        entry_telefone.bind('<KeyRelease>', detectar_vendedor_auto)  # Detecção em tempo real
        entry_telefone.bind('<FocusOut>', validar_telefone)  # Formatação completa
        # Detectar automaticamente ao carregar se há telefone
        if telefone_atual:
            detectar_vendedor_auto()
    
    # Retornar frame e widgets para uso externo
    widgets = {
        'entry_telefone': entry_telefone,
        'combo_uf': combo_uf,
        'combo_vendedor': combo_vendedor,
        'uf_indicator': uf_indicator,
        'vendedor_indicator': vendedor_indicator,
        'detectar_vendedor_auto': detectar_vendedor_auto,
        'validar_telefone': validar_telefone
    }
    
    return frame_telefone, widgets


def inicializar_telefone_com_dados(widgets, cliente_data, vendedor_atual='', auto_detect=True):
    """Inicializa os campos de telefone com dados existentes.
    
    Args:
        widgets: dict retornado por criar_bloco_telefone_cliente
        cliente_data: dict com dados do cliente
        vendedor_atual: vendedor atual da pendência
    """
    # Inicializar telefone
    telefone_atual = cliente_data.get('telefone', '')
    if telefone_atual:
        widgets['entry_telefone'].delete(0, tk.END)
        widgets['entry_telefone'].insert(0, telefone_atual)
    
    # Inicializar UF
    uf_atual = cliente_data.get('uf', '')
    if uf_atual and uf_atual in widgets['combo_uf']['values']:
        widgets['combo_uf'].set(uf_atual)
    
    # Inicializar vendedor
    if vendedor_atual and vendedor_atual in widgets['combo_vendedor']['values']:
        widgets['combo_vendedor'].set(vendedor_atual)
    
    # Detectar automaticamente se há telefone (opcional)
    if auto_detect and telefone_atual:
        widgets['detectar_vendedor_auto']()
