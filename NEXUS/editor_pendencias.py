# -*- coding: utf-8 -*-
"""
Editor de Pendências
Sistema de Propostas Comerciais - Olivo Guindastes

Módulo responsável pela interface de edição de pendências
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class EditorPendencias:
    """Classe responsável pela edição de pendências"""
    
    def __init__(self, parent_window, vendedor_detectado=None):
        self.parent_window = parent_window
        self.vendedor_detectado = vendedor_detectado
    
    def abrir_editor_pendencia(self, numero_pendencia, callback_atualizacao=None):
        """
        Abre a janela de edição de pendência
        
        Args:
            numero_pendencia (str): Número da pendência a ser editada
            callback_atualizacao (function): Função para ser chamada após atualização
        """
        try:
            from gerenciador_pendencias_json import GerenciadorPendenciasJSON
            ger = GerenciadorPendenciasJSON()
            
            pendencia = ger.ler_pendencia(numero_pendencia)
            if not pendencia:
                messagebox.showerror("Erro", "Pendência não encontrada")
                return
            
            # Criar janela principal
            janela_edit = tk.Toplevel(self.parent_window)
            janela_edit.title(f"Editar Pendência {numero_pendencia}")
            janela_edit.geometry("450x600")
            janela_edit.resizable(False, False)
            
            # Centralizar
            janela_edit.update_idletasks()
            x = self.parent_window.winfo_x() + (self.parent_window.winfo_width() - 600) // 2
            y = self.parent_window.winfo_y() + (self.parent_window.winfo_height() - 700) // 2
            janela_edit.geometry(f"+{x}+{y}")
            
            # Frame principal com scroll
            main_frame = ttk.Frame(janela_edit, padding="20")
            main_frame.pack(fill='both', expand=True)
            
            # ===== CONTAINER: SETOR RESPONSÁVEL =====
            frame_setor = ttk.LabelFrame(main_frame, text=" 🏢 Setor Responsável ", padding="12")
            frame_setor.pack(fill='x', pady=(0, 12))
            
            combo_setor = ttk.Combobox(frame_setor, state='readonly', width=35)
            try:
                from mapeamento_usuarios import obter_lista_setores
                setores = obter_lista_setores()
                combo_setor['values'] = setores
                # Pré-selecionar setor atual da pendência
                setor_atual = pendencia.get('setor', '')
                if setor_atual and setor_atual in setores:
                    combo_setor.set(setor_atual)
            except Exception as e:
                print(f"Erro ao carregar setores: {e}")
                combo_setor['values'] = []
            combo_setor.pack(pady=5)
            
            # ===== CONTAINER: USUÁRIO RESPONSÁVEL =====
            frame_usuario = ttk.LabelFrame(main_frame, text=" 👤 Usuário Responsável ", padding="12")
            frame_usuario.pack(fill='x', pady=(0, 12))
            
            combo_usuario = ttk.Combobox(frame_usuario, state='readonly', width=35)
            combo_usuario.pack(pady=5)
            
            # Função para atualizar usuários quando setor mudar
            def atualizar_usuarios_por_setor(event=None):
                setor_selecionado = combo_setor.get()
                if setor_selecionado:
                    try:
                        from mapeamento_usuarios import obter_usuarios_por_setor, obter_usuario_por_codigo
                        codigos_usuarios = obter_usuarios_por_setor(setor_selecionado)
                        nomes_usuarios = []
                        for codigo in codigos_usuarios:
                            usuario = obter_usuario_por_codigo(codigo)
                            if usuario:
                                nomes_usuarios.append(usuario['nome'])
                        combo_usuario['values'] = nomes_usuarios
                        # Pré-selecionar usuário atual da pendência (suportar tanto 'usuario' quanto 'vendedor')
                        usuario_atual = pendencia.get('usuario') or pendencia.get('vendedor', '')
                        if usuario_atual and usuario_atual in nomes_usuarios:
                            combo_usuario.set(usuario_atual)
                    except Exception as e:
                        print(f"Erro ao carregar usuários do setor: {e}")
                        combo_usuario['values'] = []
                else:
                    combo_usuario['values'] = []
            
            combo_setor.bind('<<ComboboxSelected>>', atualizar_usuarios_por_setor)
            # Carregar usuários do setor atual
            atualizar_usuarios_por_setor()
            
            # ===== CONTAINER: PRIORIDADE =====
            frame_prioridade = ttk.LabelFrame(main_frame, text=" ⚡ Prioridade ", padding="12")
            frame_prioridade.pack(fill='x', pady=(0, 12))
            
            combo_prioridade = ttk.Combobox(frame_prioridade, state='readonly', width=35)
            combo_prioridade['values'] = ['Baixa', 'Média', 'Alta']
            # Pré-selecionar prioridade atual
            prioridade_atual = pendencia.get('prioridade', 'normal')
            mapeamento_prioridade = {
                'baixa': 'Baixa',
                'normal': 'Média',
                'media': 'Média',
                'alta': 'Alta'
            }
            prioridade_display = mapeamento_prioridade.get(prioridade_atual.lower(), 'Média')
            combo_prioridade.set(prioridade_display)
            combo_prioridade.pack(pady=5)
            
            # ===== CONTAINER: PRAZO PARA RESOLUÇÃO =====
            frame_prazo = ttk.LabelFrame(main_frame, text=" 📅 Prazo para Resolução (dias) ", padding="12")
            frame_prazo.pack(fill='x', pady=(0, 12))
            
            prazo_var = tk.StringVar()
            prazo_atual = pendencia.get('prazo_resposta', '')
            if prazo_atual:
                prazo_var.set(prazo_atual)
            entry_prazo = ttk.Entry(frame_prazo, textvariable=prazo_var, width=35, justify='center')
            entry_prazo.pack(pady=5)
            
            # Validar: apenas números
            def validar_prazo(event=None):
                valor = prazo_var.get()
                valor_filtrado = ''.join(ch for ch in valor if ch.isdigit())
                if valor != valor_filtrado:
                    prazo_var.set(valor_filtrado)
            entry_prazo.bind('<KeyRelease>', validar_prazo)
            
            # Navegação com ENTER
            combo_setor.bind('<Return>', lambda e: combo_usuario.focus())
            combo_usuario.bind('<Return>', lambda e: combo_prioridade.focus())
            combo_prioridade.bind('<Return>', lambda e: entry_prazo.focus())
            entry_prazo.bind('<Return>', lambda e: text_observacoes.focus())
            
            # ===== CONTAINER: OBSERVAÇÕES =====
            frame_observacoes = ttk.LabelFrame(main_frame, text=" 📝 Observações ", padding="15")
            frame_observacoes.pack(fill='x', pady=(0, 15))
            
            # Calcular altura dinâmica baseada no conteúdo existente
            observacoes = pendencia.get('observacoes', '')
            if observacoes:
                linhas = observacoes.count('\n') + 1
                altura = max(4, min(linhas + 1, 10))  # Mínimo 4, máximo 10 linhas
            else:
                altura = 4  # Altura padrão para campo vazio
            
            text_observacoes = tk.Text(frame_observacoes, height=altura, font=('Arial', 10), wrap='word')
            text_observacoes.pack(fill='x', pady=(0, 5))
         
            # Carregar observação existente
            if observacoes:
                text_observacoes.insert('1.0', observacoes)
            
            # Vincular Enter nas observações para executar o botão Salvar
            def on_enter_observacoes(event):
                # Sempre executa a validação completa
                try:
                    salvar_todas_alteracoes()
                except Exception as e:
                    # Em caso de erro inesperado, mostra mensagem
                    messagebox.showerror("Erro", f"Erro inesperado: {e}")
                return 'break'  # Previne quebra de linha
            
            text_observacoes.bind('<Return>', on_enter_observacoes)
            text_observacoes.bind('<Shift-Return>', lambda e: None)  # Shift+Enter para nova linha
            
            # ===== FUNÇÕES DE SALVAMENTO =====
            def salvar_todas_alteracoes():
                """Salva todas as alterações feitas na interface"""
                try:
                    # Validações
                    setor_selecionado = combo_setor.get()
                    usuario_selecionado = combo_usuario.get()
                    prioridade_selecionada = combo_prioridade.get()
                    prazo_dias = prazo_var.get().strip()
                    
                    if not setor_selecionado:
                        messagebox.showwarning("Aviso", "Selecione o setor responsável!")
                        combo_setor.focus()
                        return
                    
                    if not usuario_selecionado:
                        messagebox.showwarning("Aviso", "Selecione o usuário responsável!")
                        combo_usuario.focus()
                        return
                    
                    if not prioridade_selecionada:
                        messagebox.showwarning("Aviso", "Selecione a prioridade!")
                        combo_prioridade.focus()
                        return
                    
                    # Validar prazo (opcional, mas se preenchido deve ser número válido)
                    prazo_resposta = ''
                    if prazo_dias:
                        try:
                            prazo_int = int(prazo_dias)
                            if prazo_int < 1:
                                messagebox.showwarning("Aviso", "O prazo deve ser maior que zero!")
                                entry_prazo.focus()
                                return
                            prazo_resposta = str(prazo_int)
                        except ValueError:
                            messagebox.showwarning("Aviso", "O prazo deve ser um número válido!")
                            entry_prazo.focus()
                            return
                    
                    # Mapear prioridade para formato do sistema (normal, alta, baixa)
                    prioridade_mapeada = prioridade_selecionada.lower()
                    if prioridade_mapeada == 'média':
                        prioridade_mapeada = 'normal'
                    
                    # Verificar se houve alterações
                    setor_atual = pendencia.get('setor', '')
                    # Suportar tanto 'usuario' (canônico) quanto 'vendedor' (compatibilidade)
                    usuario_atual = pendencia.get('usuario') or pendencia.get('vendedor', '')
                    prioridade_atual = pendencia.get('prioridade', 'normal')
                    prazo_atual = pendencia.get('prazo_resposta', '')
                    
                    setor_alterado = setor_selecionado != setor_atual
                    usuario_alterado = usuario_selecionado != usuario_atual
                    prioridade_alterada = prioridade_mapeada != prioridade_atual
                    prazo_alterado = prazo_resposta != prazo_atual
                    
                    # Preparar atualizações
                    atualizacoes = {}
                    
                    if setor_alterado:
                        atualizacoes['setor'] = setor_selecionado
                    
                    if usuario_alterado:
                        atualizacoes['usuario'] = usuario_selecionado  # Campo canônico (antigo: vendedor)
                    
                    if prioridade_alterada:
                        atualizacoes['prioridade'] = prioridade_mapeada
                    
                    if prazo_alterado:
                        atualizacoes['prazo_resposta'] = prazo_resposta
                    
                    # Atualizar observações
                    obs_texto = text_observacoes.get('1.0', 'end-1c').strip()
                    obs_atual = pendencia.get('observacoes', '')
                    obs_alterada = obs_texto != obs_atual
                    
                    usuario = self.vendedor_detectado['nome'] if self.vendedor_detectado else 'Sistema'
                    
                    # Aplicar atualizações
                    if atualizacoes:
                        resultado = ger.atualizar_pendencia(
                            numero=numero_pendencia,
                            atualizacoes=atualizacoes,
                            usuario=usuario
                        )
                        
                        if not resultado.get('sucesso'):
                            messagebox.showerror("Erro", f"Erro ao atualizar: {resultado.get('mensagem', 'Erro desconhecido')}")
                            return
                    
                    # Atualizar observações se alteradas
                    if obs_alterada:
                        ger.atualizar_observacoes(numero_pendencia, obs_texto, usuario)
                    
                    # Verificar se houve alguma alteração
                    if not atualizacoes and not obs_alterada:
                        messagebox.showinfo("Informação", "Nenhuma alteração foi feita.")
                        return
                    
                    # Mensagem de sucesso
                    mensagem = "✅ Pendência atualizada com sucesso!\n\n"
                    if setor_alterado:
                        mensagem += f"• Setor: {setor_atual} → {setor_selecionado}\n"
                    if usuario_alterado:
                        mensagem += f"• Usuário: {usuario_atual} → {usuario_selecionado}\n"
                    if prioridade_alterada:
                        mensagem += f"• Prioridade: {prioridade_atual} → {prioridade_selecionada}\n"
                    if prazo_alterado:
                        mensagem += f"• Prazo: {prazo_atual or '(nenhum)'} → {prazo_resposta or '(nenhum)'}\n"
                    if obs_alterada:
                        mensagem += "• Observações atualizadas\n"
                    
                    messagebox.showinfo("Sucesso", mensagem)
                    janela_edit.destroy()
                    
                    # Chamar callback de atualização se fornecido
                    if callback_atualizacao:
                        callback_atualizacao()
                        
                except ValueError as e:
                    messagebox.showerror("Erro", f"Valor inválido: {e}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro inesperado: {e}")
                    import traceback
                    traceback.print_exc()
            
            # Botões
            btn_frame = ttk.Frame(janela_edit)
            btn_frame.pack(fill='x', padx=10, pady=15)
            
            # Botão de arquivar (canto inferior esquerdo)
            def arquivar_pendencia():
                """Arquiva a pendência"""
                if messagebox.askyesno("Confirmar", f"Arquivar pendência {numero_pendencia}?"):
                    try:
                        from gerenciador_pendencias_json import GerenciadorPendenciasJSON
                        ger_pend = GerenciadorPendenciasJSON()
                        
                        resultado = ger_pend.arquivar_pendencia(numero_pendencia, "Venda Perdida via editor")
                        
                        if resultado:
                            messagebox.showinfo("Sucesso", f"Pendência {numero_pendencia} arquivada com sucesso!")
                            janela_edit.destroy()
                            
                            # Chamar callback de atualização se fornecido
                            if callback_atualizacao:
                                callback_atualizacao()
                        else:
                            messagebox.showerror("Erro", "Erro ao arquivar pendência")
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao arquivar: {e}")
            
            # Botão Cancelar (esquerda)
            ttk.Button(btn_frame, text="✗ Cancelar", 
                      command=janela_edit.destroy, width=15).pack(side='left', padx=5)
            
            # Espaçador para centralizar o botão de salvar
            ttk.Frame(btn_frame).pack(side='left', expand=True)
            
            # Botão Salvar (centro)
            ttk.Button(btn_frame, text="💾 Salvar alterações", 
                      command=salvar_todas_alteracoes, 
                      style='Accent.TButton', width=18).pack(side='left', padx=5)
            
            # Espaçador para empurrar o botão de arquivar para a direita
            ttk.Frame(btn_frame).pack(side='left', expand=True)
            
            # Botão Arquivar (direita)
            ttk.Button(btn_frame, text="📦 Arquivar", 
                      command=arquivar_pendencia, 
                      width=12).pack(side='right', padx=5)
            
        except ImportError as e:
            messagebox.showerror("Erro", f"Erro ao importar módulos necessários: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado ao abrir editor: {e}")
