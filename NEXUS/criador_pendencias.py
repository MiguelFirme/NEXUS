# -*- coding: utf-8 -*-
"""
Criador de Pendências
Interface para criar novas pendências manualmente
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class CriadorPendencias:
    """Classe responsável pela criação de novas pendências"""
    
    def __init__(self, master, vendedor_detectado, callback_atualizacao=None, larguras=None):
        """
        Inicializa o criador de pendências
        
        Args:
            master: Widget pai (janela principal)
            vendedor_detectado: Nome do vendedor detectado automaticamente
            callback_atualizacao: Função para atualizar a lista após criação
            larguras: Dict com larguras dos campos {'telefone': 20, 'vendedor': 15, 'cliente': 30, 'cnpj': 30, 'equipamento': 30}
        """
        self.master = master
        self.vendedor_detectado = vendedor_detectado
        self.callback_atualizacao = callback_atualizacao
        
        # Configurações de largura dos campos
        self.larguras = larguras or {
            'telefone': 20,
            'vendedor': 10,
            'cliente': 30,
            'cnpj': 30,
            'equipamento': 30
        }
    
    def abrir_janela_criacao(self):
        """Abre a janela para criar uma nova pendência manualmente"""
        # Criar janela de nova pendência
        janela_pend = tk.Toplevel(self.master)
        janela_pend.title("Nova Pendência")
        janela_pend.geometry("450x600")
        janela_pend.resizable(False, False)
        
        # Centralizar janela
        janela_pend.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() - 500) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - 500) // 2
        janela_pend.geometry(f"+{x}+{y}")
        
        main_frame = ttk.Frame(janela_pend, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # ===== CONTAINER: SETOR RESPONSÁVEL =====
        frame_setor = ttk.LabelFrame(main_frame, text=" 🏢 Setor Responsável ", padding="12")
        frame_setor.pack(fill='x', pady=(0, 12))
        
        combo_setor = ttk.Combobox(frame_setor, state='readonly', width=35)
        try:
            from mapeamento_usuarios import obter_lista_setores
            setores = obter_lista_setores()
            combo_setor['values'] = setores
        except Exception as e:
            print(f"Erro ao carregar setores: {e}")
            combo_setor['values'] = ['COMERCIAL GUINDASTES']
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
                    # Não selecionar automaticamente - deixar vazio
                except Exception as e:
                    print(f"Erro ao carregar usuários do setor: {e}")
                    combo_usuario['values'] = []
            else:
                combo_usuario['values'] = []
        
        combo_setor.bind('<<ComboboxSelected>>', atualizar_usuarios_por_setor)
        # Iniciar vazio - não selecionar automaticamente
        
        # ===== CONTAINER: PRIORIDADE =====
        frame_prioridade = ttk.LabelFrame(main_frame, text=" ⚡ Prioridade ", padding="12")
        frame_prioridade.pack(fill='x', pady=(0, 12))
        
        combo_prioridade = ttk.Combobox(frame_prioridade, state='readonly', width=35)
        combo_prioridade['values'] = ['Baixa', 'Média', 'Alta']
        combo_prioridade.set('Média')  # Valor padrão
        combo_prioridade.pack(pady=5)
        
        # ===== CONTAINER: PRAZO PARA RESOLUÇÃO =====
        frame_prazo = ttk.LabelFrame(main_frame, text=" 📅 Prazo para Resolução (dias) ", padding="12")
        frame_prazo.pack(fill='x', pady=(0, 12))
        
        prazo_var = tk.StringVar()
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

        # ===== CONTAINER 2.5: OBSERVAÇÕES =====
        frame_observacoes = ttk.LabelFrame(main_frame, text=" 📝 Observações ", padding="15")
        frame_observacoes.pack(fill='x', pady=(0, 15))
        
        text_observacoes = tk.Text(frame_observacoes, height=4, font=('Arial', 10), wrap='word')
        text_observacoes.pack(fill='x', pady=(0, 5))
        # Navegação: Prazo → Observações
        
        # Vincular Enter para executar o botão Registrar
        def on_enter_observacoes(event):
            # Sempre executa a validação completa
            try:
                confirmar_pendencia()
            except Exception as e:
                # Em caso de erro inesperado, mostra mensagem
                messagebox.showerror("Erro", f"Erro inesperado: {e}")
            return 'break'  # Previne quebra de linha
        
        text_observacoes.bind('<Return>', on_enter_observacoes)
        
        # Vincular Shift+Enter para pular linha (comportamento padrão)
        text_observacoes.bind('<Shift-Return>', lambda e: None)
        
        # Navegação: Prazo → Observações → Registrar
        entry_prazo.bind('<Return>', lambda e: text_observacoes.focus())
        
        def confirmar_pendencia():
            setor_selecionado = combo_setor.get()
            usuario_selecionado = combo_usuario.get()
            prioridade_selecionada = combo_prioridade.get()
            prazo_dias = prazo_var.get().strip()
            observacoes = text_observacoes.get('1.0', tk.END).strip()
            
            # Validações
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
            
            # Criar pendência
            from gerenciador_pendencias_json import GerenciadorPendenciasJSON
            ger_pend = GerenciadorPendenciasJSON()
            
            resultado = ger_pend.criar_pendencia(
                cliente='',  # Removido
                telefone='',  # Removido
                equipamento='',  # Removido
                cnpj='',  # Removido
                vendedor_manual=usuario_selecionado,
                setor_manual=setor_selecionado,
                observacoes=observacoes if observacoes else '',
                inscricao='',  # Removido
                endereco='',  # Removido
                prioridade=prioridade_mapeada,
                prazo_resposta=prazo_resposta
            )
            
            if resultado:
                numero = resultado['numero']
                # Suportar tanto 'usuario' (canônico) quanto 'vendedor' (compatibilidade)
                usuario = resultado.get('usuario') or resultado.get('vendedor', '')
                setor = resultado['setor']
                
                msg = f"✅ Pendência registrada e ativada!\n\n"
                msg += f"Número: {numero}\n"
                msg += f"Setor: {setor}\n"
                msg += f"Usuário: {usuario}\n"
                msg += f"Prioridade: {prioridade_selecionada}"
                if prazo_resposta:
                    msg += f"\nPrazo: {prazo_resposta} dias"
                
                messagebox.showinfo("Sucesso", msg)
                janela_pend.destroy()
                
                # Executar callback de atualização se fornecido (informando o número criado)
                if self.callback_atualizacao:
                    self.callback_atualizacao(numero)
                
                return True
            else:
                messagebox.showerror("Erro", "Erro ao criar pendência.\nTente novamente.")
                return False
        
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        # Configurar estilos dos botões
        style = ttk.Style()
        style.configure('Green.TButton', foreground='#25D366', background='#25D366', font=('Arial', 9, 'bold'))
        style.configure('Red.TButton', foreground='#FF4444', background='#FF4444', font=('Arial', 9, 'bold'))
        
        ttk.Button(btn_frame, text="✓  Registrar", command=confirmar_pendencia, 
                  width=18, style='Green.TButton').pack(side='left', padx=6)
        ttk.Button(btn_frame, text="✗  Cancelar", command=janela_pend.destroy, 
                  width=18, style='Red.TButton').pack(side='left', padx=6)
        
        # Focar no campo de setor
        combo_setor.focus()
        
        return janela_pend
    
    def _validar_cpf(self, cpf):
        """Valida CPF usando o algoritmo oficial"""
        # Remover caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, cpf))
        
        # Verificar se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verificar se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Calcular primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        # Calcular segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        # Verificar se os dígitos verificadores estão corretos
        return cpf[9] == str(digito1) and cpf[10] == str(digito2)
    
    def _validar_cnpj(self, cnpj):
        """Valida CNPJ usando o algoritmo oficial"""
        # Remover caracteres não numéricos
        cnpj = ''.join(filter(str.isdigit, cnpj))
        
        # Verificar se tem 14 dígitos
        if len(cnpj) != 14:
            return False
        
        # Verificar se todos os dígitos são iguais
        if cnpj == cnpj[0] * 14:
            return False
        
        # Calcular primeiro dígito verificador
        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        # Calcular segundo dígito verificador
        pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        # Verificar se os dígitos verificadores estão corretos
        return cnpj[12] == str(digito1) and cnpj[13] == str(digito2)
