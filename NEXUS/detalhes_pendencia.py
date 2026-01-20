"""Renderização do painel direito de detalhes de pendências.

Este módulo contém a função pública 'renderizar_painel_detalhes' que recebe a
instância da interface principal (InterfacePrincipalAbas) e o número da pendência,
e monta o conteúdo do painel direito dentro de 'interface.detail_frame'.
"""

import tkinter as tk
from tkinter import ttk


def renderizar_painel_detalhes(interface, numero_pendencia):
    """Monta o painel de detalhes para a pendência informada.

    Args:
        interface: instância de InterfacePrincipalAbas
        numero_pendencia: str número da pendência ativa
    """
    # Limpar painel de detalhes
    for widget in interface.detail_frame.winfo_children():
        widget.destroy()

    # Função para aplicar scroll a novos widgets
    def _aplicar_scroll_novos_widgets():
        def _bind_scroll_to_new_widget(widget):
            widget.bind("<Enter>", lambda e: interface.root.bind_all("<MouseWheel>", interface._on_mousewheel_detalhes))
            widget.bind("<Leave>", lambda e: interface.root.unbind_all("<MouseWheel>"))
            for child in widget.winfo_children():
                _bind_scroll_to_new_widget(child)
        _bind_scroll_to_new_widget(interface.detail_frame)

    try:
        # Carregar dados completos do JSON
        from NEXUS.gerenciador_pendencias_json import GerenciadorPendenciasJSON
        ger = GerenciadorPendenciasJSON()
        pendencia = ger.ler_pendencia(numero_pendencia)

        if not pendencia:
            ttk.Label(interface.detail_frame, text="❌ Pendência não encontrada", foreground='red').pack(pady=20)
            return

        # ===== CABEÇALHO =====
        header_frame = ttk.Frame(interface.detail_frame)
        header_frame.pack(fill='x', pady=(0, 15))

        # Título com cor baseada no tempo
        data_criacao_iso = pendencia.get('data_criacao', '')
        data_atualizacao_iso = pendencia.get('data_atualizacao', '')
        cor_tempo = interface._obter_cor_tempo_atualizacao(data_criacao_iso, data_atualizacao_iso)

        ttk.Label(header_frame, text=f"#{numero_pendencia}", font=('Arial', 24, 'bold'), foreground=cor_tempo).pack(anchor='w')

        from datetime import datetime
        if data_criacao_iso:
            try:
                dt = datetime.fromisoformat(data_criacao_iso)
                data_fmt = dt.strftime("%d/%m/%Y às %H:%M")
                ttk.Label(header_frame, text=f"Criada em: {data_fmt}", font=('Arial', 9), foreground='gray').pack(anchor='w')
            except Exception:
                pass

        ttk.Separator(interface.detail_frame, orient='horizontal').pack(fill='x', pady=10)

        # ===== INFORMAÇÕES DO CLIENTE =====
        try:
            from componentes_cliente import criar_bloco_dados_cliente
            cliente_data = pendencia.get('cliente', {})
            cliente_frame = criar_bloco_dados_cliente(interface.detail_frame, cliente_data)
            cliente_frame.pack(fill='x', pady=(0, 8))
        except Exception:
            cliente_frame = ttk.LabelFrame(interface.detail_frame, text=" 👤 Dados do Cliente ", padding="8")
            cliente_frame.pack(fill='x', pady=(0, 8))
            ttk.Label(cliente_frame, text=f"Razão Social: {pendencia.get('cliente', {}).get('razao_social', '-')}", font=('Arial', 8)).pack(anchor='w')
            ttk.Label(cliente_frame, text=f"CPF/CNPJ: {pendencia.get('cliente', {}).get('cnpj', '-')}", font=('Arial', 8)).pack(anchor='w')
            ttk.Label(cliente_frame, text=f"Inscrição: {pendencia.get('cliente', {}).get('inscricao_estadual', '-')}", font=('Arial', 8)).pack(anchor='w')
            endereco = pendencia.get('cliente', {}).get('endereco', pendencia.get('cliente', {}).get('cidade', '-'))
            ttk.Label(cliente_frame, text=f"Endereço: {endereco if endereco else '-'}", font=('Arial', 8)).pack(anchor='w')

        # Telefone do cliente (mesma formatação tabular dos demais campos)
        try:
            telefone_cli_val = pendencia.get('cliente', {}).get('telefone', '') or '-'
            if cliente_frame:
                cli_grid_tel = ttk.Frame(cliente_frame)
                cli_grid_tel.pack(fill='x', pady=(2, 0))
                cli_grid_tel.columnconfigure(0, weight=0, minsize=120)
                cli_grid_tel.columnconfigure(1, weight=1)
                ttk.Label(cli_grid_tel, text="Telefone:", font=('Arial', 8, 'bold')).grid(row=0, column=0, sticky='w')
                ttk.Label(cli_grid_tel, text=telefone_cli_val, font=('Arial', 8)).grid(row=0, column=1, sticky='w', padx=(5, 0))
        except Exception:
            pass

        # ===== INFORMAÇÕES DA PENDÊNCIA =====
        pend_frame = ttk.LabelFrame(interface.detail_frame, text=" 📋 Informações da Pendência ", padding="8")
        pend_frame.pack(fill='x', pady=(0, 8))

        pend_grid = ttk.Frame(pend_frame)
        pend_grid.pack(fill='x')
        pend_grid.columnconfigure(0, weight=0, minsize=100)
        pend_grid.columnconfigure(1, weight=1, minsize=200)

        # Equipamento de interesse
        ttk.Label(pend_grid, text="Equipamento:", font=('Arial', 8, 'bold'), width=12).grid(row=0, column=0, sticky='w', pady=1)
        ttk.Label(pend_grid, text=(pendencia.get('equipamento', '-') or '-'), font=('Arial', 8)).grid(row=0, column=1, sticky='w', padx=5, pady=1)

        # Vendedor responsável
        ttk.Label(pend_grid, text="Vendedor:", font=('Arial', 8, 'bold'), width=12).grid(row=1, column=0, sticky='w', pady=1)
        ttk.Label(pend_grid, text=pendencia.get('vendedor', '-'), font=('Arial', 8)).grid(row=1, column=1, sticky='w', padx=5, pady=1)

        ttk.Label(pend_grid, text="Situação:", font=('Arial', 8, 'bold'), width=12).grid(row=2, column=0, sticky='w', pady=1)
        status = pendencia.get('situacao', '-')
        if status in ['Venda Concluída', 'Proposta aprovada']:
            cor_status = 'green'
        elif status in ['Novo contato', 'Retorno pendente']:
            cor_status = 'orange'
        elif status in ['Em negociação', 'Proposta enviada', 'Entrada pendente']:
            cor_status = 'blue'
        elif status in ['Venda Perdida']:
            cor_status = 'red'
        else:
            cor_status = 'black'
        ttk.Label(pend_grid, text=status, foreground=cor_status, font=('Arial', 8, 'bold')).grid(row=2, column=1, sticky='w', padx=5, pady=1)

        # ===== OBSERVAÇÕES =====
        obs_frame = ttk.LabelFrame(interface.detail_frame, text=" 💬 Observações ", padding="8")
        obs_frame.pack(fill='both', expand=True, pady=(0, 8))
        observacoes = pendencia.get('observacoes', '')
        if observacoes:
            linhas = observacoes.count('\n') + 1
            altura = max(3, min(linhas + 1, 12))
            obs_text = tk.Text(obs_frame, height=altura, wrap='word', font=('Arial', 9))
            obs_text.pack(fill='both', expand=True)
            obs_text.insert('1.0', observacoes)
            obs_text.config(state='disabled')
        else:
            ttk.Label(obs_frame, text="Nenhuma observação registrada", foreground='gray', font=('Arial', 9, 'italic')).pack(pady=10)

        # ===== PROPOSTAS VINCULADAS =====
        prop_frame = ttk.LabelFrame(interface.detail_frame, text=" 📄 Propostas Vinculadas ", padding="8")
        prop_frame.pack(fill='x', pady=(0, 8))
        propostas = pendencia.get('propostas_vinculadas', [])
        if propostas:
            from datetime import datetime as _dt
            for idx, prop in enumerate(propostas, 1):
                codigo = prop.get('codigo', '')
                data_prop = prop.get('data', '')
                arquivo = prop.get('arquivo', '')
                if data_prop:
                    try:
                        dt_prop = _dt.fromisoformat(data_prop)
                        data_fmt_prop = dt_prop.strftime("%d/%m/%Y")
                    except Exception:
                        data_fmt_prop = data_prop[:10]
                else:
                    data_fmt_prop = ''
                prop_item = ttk.Frame(prop_frame)
                prop_item.pack(fill='x', pady=2)
                ttk.Label(prop_item, text=f"{idx}.", font=('Arial', 9, 'bold')).pack(side='left', padx=(0, 5))
                ttk.Label(prop_item, text=f"{codigo} - {data_fmt_prop}").pack(side='left')
                if arquivo:
                    btn_abrir = ttk.Button(prop_item, text="📂 Abrir", width=8, command=lambda a=arquivo: interface._abrir_arquivo_proposta(a))
                    btn_abrir.pack(side='right')
        else:
            ttk.Label(prop_frame, text="Nenhuma proposta vinculada", foreground='gray', font=('Arial', 9, 'italic')).pack(pady=10)

        # ===== HISTÓRICO =====
        hist_frame = ttk.LabelFrame(interface.detail_frame, text=" 📊 Histórico ", padding="8")
        hist_frame.pack(fill='x', pady=(0, 8))
        historico = pendencia.get('historico', [])
        if historico and len(historico) > 0:
            altura = max(3, min(len(historico) + 1, 8))
            hist_text = tk.Text(hist_frame, height=altura, wrap='word', font=('Arial', 9))
            hist_text.pack(fill='x')
            
            # Controlar scroll: quando o mouse está sobre o histórico, o scroll atua só nele
            def _hist_mousewheel(event):
                try:
                    hist_text.yview_scroll(-int(event.delta / 120), 'units')
                except Exception:
                    pass
                return 'break'
            hist_text.bind('<Enter>', lambda e: interface.root.unbind_all('<MouseWheel>'))
            hist_text.bind('<Leave>', lambda e: interface.root.bind_all('<MouseWheel>', interface._on_mousewheel_detalhes))
            hist_text.bind('<MouseWheel>', _hist_mousewheel)
            from datetime import datetime as _dt2
            for h in reversed(historico):
                data_h = h.get('data', '')
                status_ant = h.get('status_anterior', '')
                status_novo = h.get('status_novo', '')
                usuario_h = h.get('usuario', '') or 'Sistema'
                if data_h:
                    try:
                        dt_h = _dt2.fromisoformat(data_h)
                        data_fmt_h = dt_h.strftime("%d/%m %H:%M")
                    except Exception:
                        data_fmt_h = data_h[:16]
                else:
                    data_fmt_h = ''
                # Fallbacks para registros antigos sem texto
                texto_novo = (status_novo or '').strip()
                texto_ant = (status_ant or '').strip()
                if not texto_novo and texto_ant:
                    texto_novo = "Situação atualizada"
                formatos_completos = (
                    texto_novo.startswith('Situação:') or
                    texto_novo.startswith('Status:') or
                    texto_novo.startswith('Observações') or
                    texto_novo.startswith('TRANSFERIDO') or
                    texto_novo.startswith('ARQUIVADA') or
                    texto_novo.startswith('FECHADA') or
                    texto_novo.startswith('DELETADA') or
                    texto_novo.startswith('MOVIDA')
                )
                if formatos_completos:
                    hist_text.insert('end', f"[{data_fmt_h}] {texto_novo}\n")
                elif texto_ant and texto_novo:
                    hist_text.insert('end', f"[{data_fmt_h}] {texto_ant} → {texto_novo} ({usuario_h})\n")
                else:
                    # Se ambos vierem vazios, usar fallback claro
                    hist_text.insert('end', f"[{data_fmt_h}] {texto_novo or 'Situação atualizada'} ({usuario_h})\n")
            hist_text.config(state='disabled')
        else:
            ttk.Label(hist_frame, text="Nenhum registro no histórico", foreground='gray', font=('Arial', 9, 'italic')).pack(pady=5)

    except Exception as e:
        ttk.Label(interface.detail_frame, text=f"Erro ao carregar detalhes:\n{str(e)}", foreground='red').pack(pady=20)
    finally:
        _aplicar_scroll_novos_widgets()



