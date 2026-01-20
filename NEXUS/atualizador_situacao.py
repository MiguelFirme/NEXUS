# -*- coding: utf-8 -*-
"""
Atualizador de Situação de Pendências
Responsável por alterar o status/situação de uma pendência selecionada
"""

import tkinter as tk
from tkinter import ttk, messagebox
from NEXUS.gerenciador_pendencias_json import GerenciadorPendenciasJSON
from datetime import datetime

class AtualizadorSituacao:
    """Classe responsável pela atualização de situação de pendências"""

    def __init__(self, master, callback_atualizacao=None):
        """
        Inicializa o atualizador de situação

        Args:
            master: Widget pai (janela principal)
            callback_atualizacao: Função para atualizar a lista após alteração
        """
        self.master = master
        self.callback_atualizacao = callback_atualizacao

    def abrir_atualizador_situacao(self, numero_pendencia, dados_pendencia):
        """
        Abre a janela para atualizar a situação de uma pendência
        
        Args:
            numero_pendencia: Número da pendência a ser atualizada
            dados_pendencia: Dados completos da pendência
        """
        try:
            # Criar janela
            janela_situacao = tk.Toplevel(self.master)
            janela_situacao.title(f"Atualizar Situação - Pendência {numero_pendencia}")
            janela_situacao.geometry("300x220")
            janela_situacao.resizable(False, False)
            
            # Centralizar janela na tela
            janela_situacao.update_idletasks()
            width = janela_situacao.winfo_width()
            height = janela_situacao.winfo_height()
            x = (janela_situacao.winfo_screenwidth() // 2) - (width // 2)
            y = (janela_situacao.winfo_screenheight() // 2) - (height // 2)
            janela_situacao.geometry(f"{width}x{height}+{x}+{y}")
            
            # Centralizar janela
            janela_situacao.transient(self.master)
            janela_situacao.grab_set()
            
            # Frame principal
            main_frame = ttk.Frame(janela_situacao, padding="20")
            main_frame.pack(fill='both', expand=True, padx=5, pady=5)
            
            # Situação atual
            situacao_frame = ttk.LabelFrame(main_frame, text=" 📊 Situação ", padding="15")
            situacao_frame.pack(fill='x', pady=(0, 20))
            
            situacao_atual = dados_pendencia.get('situacao', 'Novo contato')
            ttk.Label(situacao_frame, text=f"Pendência N° {numero_pendencia}", font=('Arial', 10, 'bold')).pack(pady=(0, 5))
            
            # Dropdown para situação (com situação atual pré-selecionada)
            combo_situacao = ttk.Combobox(situacao_frame, state='readonly', width=20)
            # Carregar situações do arquivo centralizado
            try:
                from config_rede import ConfiguracaoRede
                situacoes_comerciais = ConfiguracaoRede.obter_valores_situacao()
            except Exception as e:
                print(f"Erro ao carregar situações: {e}")
                # Fallback
                situacoes_comerciais = ['Novo contato', 'Proposta enviada', 'Retorno pendente', 
                                        'Em negociação', 'Proposta aprovada', 'Entrada pendente', 
                                        'Venda Concluída', 'Venda Perdida']
            combo_situacao['values'] = situacoes_comerciais
            # Pré-selecionar situação atual se estiver na lista
            if situacao_atual in situacoes_comerciais:
                combo_situacao.set(situacao_atual)
            else:
                # Se situação atual não estiver na lista, usar 'Novo contato' como padrão
                combo_situacao.set('Novo contato')
            
            # Centralizar texto no dropdown
            combo_situacao.configure(justify='center')
            combo_situacao.pack(pady=5)
            
            # Função para confirmar atualização
            def confirmar_atualizacao():
                nova_situacao = combo_situacao.get()
                
                if not nova_situacao:
                    messagebox.showwarning("Aviso", "Selecione uma nova situação.")
                    combo_situacao.focus()
                    return
                
                if nova_situacao == situacao_atual:
                    messagebox.showinfo("Informação", "A nova situação é igual à atual.")
                    return
                
                # Salvar alteração via gerenciador central
                try:
                    # Suportar tanto 'usuario' (canônico) quanto 'vendedor' (compatibilidade)
                    usuario = (dados_pendencia.get('usuario') or dados_pendencia.get('vendedor') or '').strip() or 'Sistema'
                    ger_pend = GerenciadorPendenciasJSON()
                    sucesso = ger_pend.atualizar_status(numero_pendencia, nova_situacao, '', usuario)
                    if sucesso:
                        messagebox.showinfo("Sucesso", f"Situação alterada com sucesso!\n\n{numero_pendencia}: {situacao_atual} → {nova_situacao}")
                        janela_situacao.destroy()
                        
                        # Chamar callback de atualização se fornecido
                        if self.callback_atualizacao:
                            self.callback_atualizacao()
                    else:
                        messagebox.showerror("Erro", "Erro ao atualizar situação da pendência.")
                        
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro inesperado: {e}")
            
            # Botão Salvar (dentro do mesmo container)
            ttk.Button(situacao_frame, text="💾 Salvar alteração", 
                      command=confirmar_atualizacao, 
                      style='Accent.TButton', width=20).pack(pady=(15, 5))
            
        except ImportError as e:
            messagebox.showerror("Erro", f"Erro ao importar deletar_pendencia_dialog módulos necessários: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado ao abrir atualizador: {e}")


def atualizar_situacao(numero_pendencia: str, nova_situacao: str, observacao: str = '', usuario: str = 'Sistema') -> bool:
    """API central para atualizar a situação de uma pendência.
    Encaminha para GerenciadorPendenciasJSON.atualizar_status para manter o padrão de histórico.
    """
    if not (nova_situacao and nova_situacao.strip()):
        return False
    try:
        ger = GerenciadorPendenciasJSON()
        return ger.atualizar_status(numero_pendencia, nova_situacao.strip(), observacao or '', usuario or 'Sistema')
    except Exception:
        return False
