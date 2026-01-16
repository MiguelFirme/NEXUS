# -*- coding: utf-8 -*-
"""
Interface Principal com Sistema de Abas
Sistema de Gestão de Pendências e Estatísticas - Olivo Guindastes
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Configurar encoding UTF-8 no Windows
if sys.platform == 'win32':
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass


class InterfacePrincipalAbas:
    """Interface principal com sistema de abas (navegação tipo browser)"""
    
    def __init__(self, root, codigo_usuario_validado=None, dados_usuario_validado=None):
        self.root = root
        self.root.title("NEXUS")

        # Configurar estilos dos botões
        self._configurar_estilos()
        
        # Configurar tamanho e centralizar na tela
        largura = 1400
        altura = 900
        
        # Obter dimensões da tela
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        
        # Calcular posição para 
        pos_x = (largura_tela - largura) // 2
        pos_y = (altura_tela - altura) // 2 - 50  # Mover 50px para cima
        
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        self.root.resizable(False, False)
        
        # Usar dados do usuário já validados (fornecidos pelo iniciar.py)
        if codigo_usuario_validado is not None and dados_usuario_validado:
            self.codigo_usuario = codigo_usuario_validado
            self.nivel_usuario = dados_usuario_validado.get('nivel', 1)
            self.usuario_detectado = {
                'nome': dados_usuario_validado.get('nome', ''),
                'setor': dados_usuario_validado.get('setor', ''),
                'cargo': dados_usuario_validado.get('cargo', ''),
                'telefone': dados_usuario_validado.get('telefone', ''),
                'email': dados_usuario_validado.get('email', ''),
                'computador': dados_usuario_validado.get('computador', '')
            }
            print(f"✓ Usuário validado: {dados_usuario_validado.get('nome')} (Código {codigo_usuario_validado}, Nível {self.nivel_usuario})")
        else:
            # Modo compatibilidade (não deveria acontecer se validação funcionou)
            self.usuario_detectado = None
            self.codigo_usuario = None
            self.nivel_usuario = None
            print("⚠️ Aviso: Dados do usuário não foram validados. Tentando detectar...")
            self._detectar_codigo_usuario()
        
        self._inicializar_sistema()
        
        # Sistema de auto-refresh (OTIMIZADO)
        self.auto_refresh_ativo = True
        self.intervalo_refresh = 10000  # 10 segundos (otimizado para melhor performance)
        self.monitor_mudancas = None
        self.timer_refresh = None
        self.ultima_atualizacao = None
        
        # Cache de pendências para evitar leituras repetidas
        self._cache_pendencias = {}
        self._cache_pendencias_timestamp = None
        self._cache_pendencias_ttl = 5  # Cache válido por 5 segundos
        
        # Controle de carregamento dinâmico por semana
        from datetime import date, timedelta
        hoje = date.today()
        # Por padrão, carregar última semana (7 dias atrás até hoje)
        self.semana_fim = hoje
        self.semana_inicio = hoje - timedelta(days=6)  # 7 dias incluindo hoje
        
        # Instância reutilizável do gerenciador de pendências (inicializada depois)
        self.ger_pendencias = None
        
        # Thresholds de tempo (minutos) para cores: excelente, bom, regular, mediano, ruim
        # Dobrados em relação ao padrão: [30, 60, 90, 120, 150] → [60, 120, 180, 240, 300]
        self.tempo_thresholds_min = [60, 120, 180, 240, 300]

        # SISTEMA DE SELEÇÃO PERSISTENTE E DEFINITIVA
        self.pendencia_ativa = None  # Número da pendência ATIVA (persiste sempre)
        self.pendencia_ativa_dados = None  # Dados completos da pendência ativa
        
        # Criar interface
        self.criar_interface()
        
        # Iniciar auto-refresh
        self._iniciar_auto_refresh()
        
        # Auto-refresh ao ganhar foco
        self.root.bind('<FocusIn>', self._on_focus_in)
    
    def _configurar_estilos(self):
        """Configura estilos personalizados para os botões"""
        # Estilos removidos - não há mais necessidade de estilos personalizados
        pass
    
    def _inicializar_sistema(self):
        """Inicializa o sistema para gestão de pendências e estatísticas"""
        # Sistema simplificado - apenas gestão de pendências e estatísticas
        # Componentes de geração de propostas foram removidos
        self.sistema_disponivel = True
        print(f"✓ Sistema inicializado.")
    
    def criar_interface(self):
        """Cria a interface principal com abas"""
        print("✓ Criando interface principal.")
        
        # Frame principal
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cabeçalho com título e informações do usuário
        self._criar_cabecalho(main_container)
        
        # Rodapé com status (CRIAR ANTES das abas para evitar erro de referência)
        self._criar_rodape(main_container)
        
        # Sistema de abas (Notebook)
        self.notebook = ttk.Notebook(main_container)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 10))
        
        # Bind para atualizar ao trocar de aba
        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)
        
        # Criar as 2 abas (ordem: Pendências, Estatísticas)
        self.criar_aba_pendencias()
        self.criar_aba_estatisticas()
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Carregar pendências automaticamente ao abrir o programa
        # Usar after() para garantir que a interface esteja completamente renderizada
        self.root.after(100, self._carregar_pendencias_inicial)
    
    def _criar_cabecalho(self, parent):
        """Cria o cabeçalho com título e informações"""
        header_frame = ttk.Frame(parent, padding="10")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Título principal
        titulo = ttk.Label(header_frame, 
                          text="📋 Sistema de Gestão de Pendências e Estatísticas.", 
                          font=('Arial', 18, 'bold'))
        titulo.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Informações do usuário (se disponíveis) - alinhado à esquerda
        if hasattr(self, 'usuario_detectado') and self.usuario_detectado:
            nome = self.usuario_detectado.get('nome', 'N/A')
            setor = self.usuario_detectado.get('setor', 'N/A')
            cargo = self.usuario_detectado.get('cargo', 'N/A')
            nivel = self.nivel_usuario if hasattr(self, 'nivel_usuario') and self.nivel_usuario else 'N/A'
            
            info_texto = f"👤 {nome}  |  🏢 {setor}  |  💼 {cargo}  |  ⭐ Nível {nivel}"
            info_usuario = ttk.Label(header_frame, 
                                   text=info_texto,
                                   font=('Arial', 11),
                                   foreground='#2C3E50')
            info_usuario.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        else:
            # Se não há dados do usuário, mostrar aviso
            aviso = ttk.Label(header_frame,
                            text="⚠️ Dados do usuário não disponíveis",
                            font=('Arial', 10),
                            foreground='orange')
            aviso.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Subtítulo
        subtitulo = ttk.Label(header_frame, 
                             text="Gestão de Pendências e Análise de Estatísticas", 
                             font=('Arial', 9), foreground='gray')
        subtitulo.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Linha separadora
        ttk.Separator(header_frame, orient='horizontal').grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        
        header_frame.columnconfigure(0, weight=1)
    
    def _criar_rodape(self, parent):
        """Cria o rodapé com status"""
        footer_frame = ttk.LabelFrame(parent, text="Status", padding="10")
        footer_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 0))
        
        # Status centralizado
        status_container = ttk.Frame(footer_frame)
        status_container.pack(anchor='center')
        
        self.status_icone = ttk.Label(status_container, text="✓", 
                                      font=('Arial', 14, 'bold'), foreground='green')
        self.status_icone.pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_label = ttk.Label(status_container, text="Sistema pronto", 
                                      font=('Arial', 10), foreground='green')
        self.status_label.pack(side=tk.LEFT)
    
    def criar_aba_estatisticas(self):
        """Cria a aba de estatísticas"""
        aba_stats = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(aba_stats, text="📊 Estatísticas")
        
        # Importar componentes de estatísticas
        from datetime import datetime
        
        # Funcionalidade de rastreamento de propostas foi removida
        self.rastreador = None
        
        # Frame de filtros
        filtros_frame = ttk.LabelFrame(aba_stats, text="Filtros", padding="10")
        filtros_frame.pack(fill='x', pady=(0, 10))
        
        # Mês/Ano
        ttk.Label(filtros_frame, text="Mês:").grid(row=0, column=0, padx=5)
        self.combo_mes = ttk.Combobox(filtros_frame, state='readonly', width=12)
        self.combo_mes.grid(row=0, column=1, padx=5)
        self.combo_mes['values'] = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        self.combo_mes.current(datetime.now().month - 1)
        
        ttk.Label(filtros_frame, text="Ano:").grid(row=0, column=2, padx=5)
        self.combo_ano = ttk.Combobox(filtros_frame, state='readonly', width=8)
        self.combo_ano.grid(row=0, column=3, padx=5)
        ano_atual = datetime.now().year
        self.combo_ano['values'] = [str(ano_atual - 1), str(ano_atual), str(ano_atual + 1)]
        self.combo_ano.current(1)
        
        # Auto-refresh - não precisa mais de botão "Atualizar"
        ttk.Label(filtros_frame, text="🔄 Auto-refresh ativo", foreground='green', 
                 font=('Arial', 9)).grid(row=0, column=4, padx=10)
        
        # Frame de conteúdo
        content_frame = ttk.Frame(aba_stats)
        content_frame.pack(fill='both', expand=True)
        
        # Coluna esquerda - Resumo
        left_frame = ttk.LabelFrame(content_frame, text="Resumo do Período", padding="15")
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        self.lbl_total_propostas = ttk.Label(left_frame, text="Total: 0 propostas", 
                                            font=('Arial', 12, 'bold'))
        self.lbl_total_propostas.pack(anchor='w', pady=5)
        
        self.lbl_valor_total = ttk.Label(left_frame, text="Valor Total: R$ 0,00", 
                                        font=('Arial', 11))
        self.lbl_valor_total.pack(anchor='w', pady=5)
        
        ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=10)
        
        ttk.Label(left_frame, text="Por Tipo de Equipamento:", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=5)
        
        # Aumentado para tela maximizada
        self.text_tipos = tk.Text(left_frame, height=25, width=40, font=('Courier', 10))
        self.text_tipos.pack(fill='both', expand=True, pady=5)
        
        # Coluna direita - Usuários
        right_frame = ttk.LabelFrame(content_frame, text="Performance por Usuário", padding="15")
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        colunas = ('Usuário', 'Propostas', 'Valor Total')
        self.tree_usuarios = ttk.Treeview(right_frame, columns=colunas, show='headings', height=30)
        
        self.tree_usuarios.heading('Usuário', text='Usuário')
        self.tree_usuarios.heading('Propostas', text='Propostas')
        self.tree_usuarios.heading('Valor Total', text='Valor Total')
        
        # Colunas maiores para tela maximizada
        self.tree_usuarios.column('Usuário', width=250)
        self.tree_usuarios.column('Propostas', width=120, anchor='center')
        self.tree_usuarios.column('Valor Total', width=180, anchor='e')
        
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscrollcommand=scrollbar.set)
        
        self.tree_usuarios.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Habilitar scroll com mouse wheel no TreeView de usuários
        def _on_mousewheel_usuarios(event):
            self.tree_usuarios.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel_usuarios(event):
            self.tree_usuarios.bind_all("<MouseWheel>", _on_mousewheel_usuarios)
        
        def _unbind_mousewheel_usuarios(event):
            self.tree_usuarios.unbind_all("<MouseWheel>")
        
        # Ativar scroll quando mouse entra no TreeView
        self.tree_usuarios.bind("<Enter>", _bind_mousewheel_usuarios)
        self.tree_usuarios.bind("<Leave>", _unbind_mousewheel_usuarios)
        
        # Botões de ação
        btn_frame = ttk.Frame(aba_stats)
        btn_frame.pack(fill='x', pady=10)
        
        ttk.Button(btn_frame, text="Exportar Relatório", command=self.exportar_relatorio).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Abrir Registro CSV", command=self.abrir_registro_csv).pack(side='left', padx=5)
        
        # Carregar dados iniciais
        self.atualizar_estatisticas()
    
    def criar_aba_pendencias(self):
        """Cria a aba de pendências"""
        aba_pendencias = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(aba_pendencias, text="📋 Gestão de Pendências")
        
        # Frame de filtros
        filtros_frame = ttk.LabelFrame(aba_pendencias, text="Filtros", padding="10")
        filtros_frame.pack(fill='x', pady=(0, 10))
        
        # Controle de período (semana) - CARREGAMENTO DINÂMICO
        ttk.Label(filtros_frame, text="Período:").grid(row=0, column=0, padx=5)
        
        # Container para navegação de semana
        semana_container = ttk.Frame(filtros_frame)
        semana_container.grid(row=0, column=1, padx=5)
        
        # Botão semana anterior
        self.btn_semana_anterior = ttk.Button(semana_container, text="◀◀",
                                              command=self._semana_anterior, width=5)
        self.btn_semana_anterior.pack(side='left', padx=2)

        # Label mostrando período atual
        self.label_periodo = ttk.Label(semana_container, text="", width=25, anchor='center')
        self.label_periodo.pack(side='left', padx=5)
        self._atualizar_label_periodo()

        # Botão próxima semana
        self.btn_semana_proxima = ttk.Button(semana_container, text="▶▶",
                                            command=self._semana_proxima, width=5)
        self.btn_semana_proxima.pack(side='left', padx=2)
        
        ttk.Label(filtros_frame, text="Status:").grid(row=0, column=2, padx=5)
        self.combo_status_pendencia = ttk.Combobox(filtros_frame, state='readonly', width=20)
        # Carregar status baseados nas pastas disponíveis
        try:
            from gerenciador_pendencias_json import GerenciadorPendenciasJSON
            pastas_status = GerenciadorPendenciasJSON.PASTAS_STATUS
            # Mapear nomes de pastas para nomes mais amigáveis
            mapeamento_status = {
                'ATIVAS': 'Ativa',
                'ARQUIVADAS': 'Arquivada',
                'CANCELADAS': 'Cancelada',
                'CONCLUÍDAS': 'Concluída',
                'EM ATRASO': 'Em Atraso'
            }
            status_list = ['Todas'] + [mapeamento_status.get(pasta, pasta) for pasta in pastas_status]
        except:
            # Fallback caso não consiga carregar
            status_list = ['Todas', 'Ativa', 'Arquivada', 'Cancelada', 'Concluída', 'Em Atraso']
        self.combo_status_pendencia['values'] = status_list
        self.combo_status_pendencia.current(0)
        self.combo_status_pendencia.grid(row=0, column=3, padx=5)
        self.combo_status_pendencia.bind('<<ComboboxSelected>>', lambda e: self.atualizar_pendencias())
        
        ttk.Label(filtros_frame, text="Situação:").grid(row=0, column=4, padx=5)
        self.combo_situacao_pendencia = ttk.Combobox(filtros_frame, state='readonly', width=20)
        # Carregar situações do arquivo centralizado
        try:
            from config_rede import ConfiguracaoRede
            situacoes_comerciais = ['Todas'] + ConfiguracaoRede.obter_valores_situacao()
        except Exception as e:
            print(f"Erro ao carregar situações: {e}")
            # Fallback
            situacoes_comerciais = ['Todas', 'Novo contato', 'Proposta enviada', 'Retorno pendente', 
                                    'Em negociação', 'Proposta aprovada', 'Entrada pendente', 
                                    'Venda Concluída', 'Venda Perdida']
        self.combo_situacao_pendencia['values'] = situacoes_comerciais
        self.combo_situacao_pendencia.current(0)
        self.combo_situacao_pendencia.grid(row=0, column=5, padx=5)
        self.combo_situacao_pendencia.bind('<<ComboboxSelected>>', lambda e: self.atualizar_pendencias())
        
        ttk.Label(filtros_frame, text="Usuário:").grid(row=0, column=6, padx=5)
        self.combo_usuario_pendencia = ttk.Combobox(filtros_frame, state='readonly', width=20)
        
        # Obter usuário ativo para filtro padrão
        usuario_ativo = self._obter_usuario_ativo()
        
        # Carregar usuários da planilha DADOS_LOGIN.csv
        try:
            from mapeamento_usuarios import obter_lista_usuarios
            usuarios_planilha = obter_lista_usuarios()
            usuarios = ['Todos'] + usuarios_planilha
        except Exception as e:
            print(f"✗ Erro ao carregar usuários da planilha: {e}")
            # Se não conseguir carregar, usar lista vazia (sistema requer CSV)
            usuarios = ['Todos']
        
        self.combo_usuario_pendencia['values'] = usuarios
        
        # Definir usuário ativo como padrão (se encontrado)
        if usuario_ativo and usuario_ativo in usuarios:
            self.combo_usuario_pendencia.current(usuarios.index(usuario_ativo))
        else:
            self.combo_usuario_pendencia.current(0)  # "Todos" como fallback
        
        self.combo_usuario_pendencia.grid(row=0, column=7, padx=5)
        self.combo_usuario_pendencia.bind('<<ComboboxSelected>>', lambda e: self.atualizar_pendencias())
        
        # Filtro de Setor
        ttk.Label(filtros_frame, text="Setor:").grid(row=0, column=8, padx=5)
        self.combo_setor_pendencia = ttk.Combobox(filtros_frame, state='readonly', width=20)
        
        # Carregar setores da planilha DADOS_LOGIN.csv
        try:
            from mapeamento_usuarios import obter_lista_setores
            setores_planilha = obter_lista_setores()
            setores = ['Todos'] + setores_planilha
        except Exception as e:
            print(f"✗ Erro ao carregar setores da planilha: {e}")
            # Se não conseguir carregar, usar lista vazia (sistema requer CSV)
            setores = ['Todos']
        
        self.combo_setor_pendencia['values'] = setores
        self.combo_setor_pendencia.current(0)  # "Todos" como padrão
        self.combo_setor_pendencia.grid(row=0, column=9, padx=5)
        self.combo_setor_pendencia.bind('<<ComboboxSelected>>', lambda e: self.atualizar_pendencias())
        
        # Checkbox para mostrar arquivadas (atualiza ao marcar/desmarcar)
        self.var_mostrar_arquivadas = tk.BooleanVar(value=False)
        ttk.Checkbutton(filtros_frame, text="Mostrar Arquivadas", 
                       variable=self.var_mostrar_arquivadas,
                       command=self.atualizar_pendencias).grid(row=0, column=10, padx=10)
        
        # ===== LAYOUT SPLIT: LISTA À ESQUERDA + DETALHES À DIREITA =====
        main_content = ttk.Frame(aba_pendencias)
        main_content.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ===== LADO ESQUERDO: LISTA DE PENDÊNCIAS =====
        left_frame = ttk.LabelFrame(main_content, text=" 📋 Pendências ", padding="10")
        left_frame.pack(side='left', fill='both', expand=False, padx=(0, 5))
        left_frame.pack_propagate(False)  # Não deixar conteúdo redimensionar
        # Lista: 700px conforme solicitado
        left_frame.configure(width=700, height=800)
        
        # Botão Nova Pendência movido para dentro do container de ações
        
        # Painel de pendência ativa removido da UI (lógica mantida nos bastidores)
        
        # Botões de ação - EMPACOTAR PRIMEIRO (no fundo)
        btn_frame_left = ttk.Frame(left_frame)
        btn_frame_left.pack(fill='x', pady=(5, 0), side='bottom')
        
        # Botões maiores para tela maximizada - REORGANIZADOS
        self.btn_editar = ttk.Button(btn_frame_left, text="📝 Editar", command=self._editar_pendencia_completa,
                  width=22)
        self.btn_editar.grid(row=0, column=0, columnspan=2, padx=3, pady=3, ipady=8, sticky='ew')
        
        self.btn_atualizar_situacao = ttk.Button(btn_frame_left, text="🔄 Atualizar situação", command=self.atualizar_situacao_pendencia,
                  style='Accent.TButton', width=22)
        self.btn_atualizar_situacao.grid(row=1, column=0, columnspan=2, 
                  padx=3, pady=3, ipady=8, sticky='ew')
        
        # Botão Transferir - ACIMA do botão Criar
        self.btn_transferir = ttk.Button(btn_frame_left, text="🔄 Transferir", command=self.transferir_pendencia,
                  width=22)
        self.btn_transferir.grid(row=2, column=0, columnspan=2, 
                  padx=3, pady=3, ipady=8, sticky='ew')
        
        # Botão Nova Pendência - ABAIXO de todos os outros
        self.btn_nova_pendencia = ttk.Button(btn_frame_left, text="➕ Nova Pendência", command=self.criar_nova_pendencia,
                  style='Accent.TButton', width=22)
        self.btn_nova_pendencia.grid(row=3, column=0, columnspan=2, 
                  padx=3, pady=(8, 3), ipady=8, sticky='ew')
        
        # Atualizar estado dos botões baseado no nível do usuário (será chamado após detectar usuário)
        
        btn_frame_left.columnconfigure(0, weight=1)
        btn_frame_left.columnconfigure(1, weight=1)
        
        # TreeView compacta - DEPOIS dos botões (preenche o espaço restante)
        tree_container = ttk.Frame(left_frame)
        tree_container.pack(fill='both', expand=True, pady=(0, 5))
        
        # NOVA IMPLEMENTAÇÃO: Sistema de seleção nativo do TreeView (mais confiável)
        colunas = ('Pendência', 'Data', 'Hora', 'Situação')
        self.tree_pendencias = ttk.Treeview(tree_container, columns=colunas, show='headings', selectmode='browse')
        
        # Variável para controlar ordenação
        self.ordenacao_coluna = None
        self.ordenacao_reversa = False
        
        # Configurar colunas com ordenação
        self.tree_pendencias.heading('Pendência', text='Pendência', command=lambda: self._ordenar_por_coluna('Pendência'))
        self.tree_pendencias.heading('Data', text='Data', command=lambda: self._ordenar_por_coluna('Data'))
        self.tree_pendencias.heading('Hora', text='Hora', command=lambda: self._ordenar_por_coluna('Hora'))
        self.tree_pendencias.heading('Situação', text='Situação', command=lambda: self._ordenar_por_coluna('Situação'))
        
        # Adicionar evento de clique com botão direito nos cabeçalhos para remover ordenação
        self.tree_pendencias.bind('<Button-3>', self._on_cabecalho_botao_direito)
        
        # Colunas para 600px de largura - TODAS CENTRALIZADAS
        self.tree_pendencias.column('Pendência', width=60, anchor='center')
        self.tree_pendencias.column('Data', width=50, anchor='center')
        self.tree_pendencias.column('Hora', width=40, anchor='center')
        self.tree_pendencias.column('Situação', width=120, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree_pendencias.yview)
        self.tree_pendencias.configure(yscrollcommand=scrollbar.set)
        
        self.tree_pendencias.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Adicionar método de ordenação
        self._adicionar_indicadores_ordenacao()
        
        # Habilitar scroll com mouse wheel no TreeView de pendências
        def _on_mousewheel_tree(event):
            self.tree_pendencias.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel_tree(event):
            self.tree_pendencias.bind_all("<MouseWheel>", _on_mousewheel_tree)
        
        def _unbind_mousewheel_tree(event):
            self.tree_pendencias.unbind_all("<MouseWheel>")
        
        # Ativar scroll quando mouse entra no TreeView
        self.tree_pendencias.bind("<Enter>", _bind_mousewheel_tree)
        self.tree_pendencias.bind("<Leave>", _unbind_mousewheel_tree)
        
        # Configurar estilo visual aprimorado para seleção
        # Linha selecionada: azul forte e destacado
        style = ttk.Style()
        style.map('Treeview',
                  background=[('selected', '#0078D7')],  # Azul Windows
                  foreground=[('selected', 'white')])
        
        # Tags para status visual removidas - apenas cores de tempo serão usadas
        
        # Tag especial para pendência ATIVA (persistente)
        self.tree_pendencias.tag_configure('ativa', background='#4A90E2', foreground='white')  # Azul destaque
        
        # Tags para cores baseadas no tempo desde última atualização (6 níveis a cada 30 minutos)
        # Usando background (cor da linha) ao invés de foreground (cor do texto)
        self.tree_pendencias.tag_configure('tempo_excelente', background='#E8F5E8')  # Verde claro - < 30 min
        self.tree_pendencias.tag_configure('tempo_bom', background='#F0F8E8')        # Verde-claro - 30-60 min
        self.tree_pendencias.tag_configure('tempo_regular', background='#FFFDE7')    # Amarelo claro - 60-90 min
        self.tree_pendencias.tag_configure('tempo_mediano', background='#FFF3E0')    # Laranja claro - 90-120 min
        self.tree_pendencias.tag_configure('tempo_ruim', background='#FFEBEE')       # Vermelho claro - 120-150 min
        self.tree_pendencias.tag_configure('tempo_pessimo', background='#FFE8E8')    # Vermelho-escuro claro - > 150 min
        
        # Evento de seleção (único sistema confiável)
        # UM CLIQUE já ativa a pendência definitivamente
        self.tree_pendencias.bind('<<TreeviewSelect>>', self._on_pendencia_clique_unico)
        
        # Bind para tecla ESC - desselecionar pendência ativa
        self.tree_pendencias.bind('<KeyPress-Escape>', self._on_esc_deselecionar)
        
        # ===== LADO DIREITO: PAINEL DE DETALHES =====
        right_frame = ttk.LabelFrame(main_content, text=" 📄 Detalhes da Pendência ", padding="10")
        right_frame.pack(side='right', fill='both', expand=False, padx=(5, 0))
        right_frame.pack_propagate(False)  # Não deixar conteúdo redimensionar
        # Detalhes: 650px de largura, altura ajustável
        right_frame.configure(width=650, height=700)
        
        # Container com scroll para detalhes
        detail_canvas = tk.Canvas(right_frame, highlightthickness=0)
        detail_scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=detail_canvas.yview)
        
        # Container intermediário para garantir que o conteúdo não seja sobreposto
        self.detail_frame = ttk.Frame(detail_canvas)
        
        self.detail_frame.bind(
            "<Configure>",
            lambda e: detail_canvas.configure(scrollregion=detail_canvas.bbox("all"))
        )
        
        detail_canvas.create_window((0, 0), window=self.detail_frame, anchor='nw')
        detail_canvas.configure(yscrollcommand=detail_scrollbar.set)
        
        # Usar pack com configuração adequada para evitar sobreposição
        detail_canvas.pack(side='left', fill='both', expand=True)
        detail_scrollbar.pack(side='right', fill='y')
        
        # Configurar o canvas para ter padding interno
        detail_canvas.bind('<Configure>', lambda e: self._on_canvas_configure(detail_canvas))
        
        # Habilitar scroll com mouse wheel no painel de detalhes
        def _on_mousewheel_detalhes(event):
            detail_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Salvar referência para uso posterior
        self._on_mousewheel_detalhes = _on_mousewheel_detalhes
        
        # Permitir scroll em qualquer lugar dentro do painel de detalhes
        def _bind_mousewheel_global(event):
            detail_canvas.bind_all("<MouseWheel>", _on_mousewheel_detalhes)
        
        def _unbind_mousewheel_global(event):
            detail_canvas.unbind_all("<MouseWheel>")
        
        # Função para aplicar scroll a todos os widgets filhos
        def _bind_scroll_to_widget(widget):
            widget.bind("<Enter>", _bind_mousewheel_global)
            widget.bind("<Leave>", _unbind_mousewheel_global)
            for child in widget.winfo_children():
                _bind_scroll_to_widget(child)
        
        # Ativar scroll quando mouse entra no painel direito (right_frame)
        right_frame.bind("<Enter>", _bind_mousewheel_global)
        right_frame.bind("<Leave>", _unbind_mousewheel_global)
        
        # Também ativar no canvas e frame interno
        detail_canvas.bind("<Enter>", _bind_mousewheel_global)
        detail_canvas.bind("<Leave>", _unbind_mousewheel_global)
    
    def _on_canvas_configure(self, canvas):
        """Ajusta a largura do frame interno para evitar sobreposição com a scrollbar"""
        try:
            # Obter largura atual do canvas
            canvas_width = canvas.winfo_width()
            
            # Subtrair largura da scrollbar (aproximadamente 17px)
            scrollbar_width = 17
            available_width = canvas_width - scrollbar_width
            
            # Configurar largura mínima
            if available_width > 0:
                canvas.itemconfig(canvas.find_all()[0], width=available_width)
        except Exception as e:
            # Ignorar erros durante a configuração inicial
            pass
    
    def _obter_cor_tempo_atualizacao(self, data_criacao_iso, data_atualizacao_iso=None):
        """
        Retorna a cor baseada no tempo desde a última atualização
        
        Args:
            data_criacao_iso: Data de criação em formato ISO
            data_atualizacao_iso: Data de última atualização em formato ISO (opcional)
            
        Returns:
            str: Cor correspondente ao tempo decorrido
        """
        try:
            from datetime import datetime, timedelta
            agora = datetime.now()
            
            # Priorizar data de atualização se disponível, senão usar data de criação
            data_referencia = data_atualizacao_iso if data_atualizacao_iso else data_criacao_iso
            
            if not data_referencia:
                return '#FF6B6B'  # Vermelho - Se não há data, considerar péssimo
            
            # Usar data de referência (atualização ou criação)
            data_ref = datetime.fromisoformat(data_referencia)
            tempo_decorrido = agora - data_ref
            minutos = tempo_decorrido.total_seconds() / 60
            
            # Thresholds configuráveis (minutos): [excelente, bom, regular, mediano, ruim]
            thresholds = getattr(self, 'tempo_thresholds_min', [30, 60, 90, 120, 150])
            t1, t2, t3, t4, t5 = thresholds
            # 6 níveis conforme thresholds
            if minutos < t1:
                return '#006400'  # Verde escuro forte - < 30 min
            elif minutos < t2:
                return '#228B22'  # Verde floresta - 30-60 min
            elif minutos < t3:
                return '#FF8C00'  # Laranja escuro - 60-90 min
            elif minutos < t4:
                return '#FF4500'  # Vermelho laranja - 90-120 min
            elif minutos < t5:
                return '#DC143C'  # Vermelho carmesim - 120-150 min
            else:
                return '#8B0000'  # Vermelho escuro - > 150 min
                
        except Exception as e:
            print(f"✗ Erro ao calcular cor de tempo: {e}")
            return '#B71C1C'  # Em caso de erro, considerar péssimo

    def _obter_tag_tempo_atualizacao(self, data_criacao_iso, data_atualizacao_iso=None):
        """
        Retorna a tag de cor baseada no tempo desde a última atualização
        
        Args:
            data_criacao_iso: Data de criação em formato ISO
            data_atualizacao_iso: Data de última atualização em formato ISO (opcional)
            
        Returns:
            str: Tag de cor correspondente ao tempo decorrido
        """
        try:
            from datetime import datetime, timedelta
            agora = datetime.now()
            
            # Priorizar data de atualização se disponível, senão usar data de criação
            data_referencia = data_atualizacao_iso if data_atualizacao_iso else data_criacao_iso
            
            if not data_referencia:
                return 'tempo_pessimo'  # Se não há data, considerar péssimo
            
            # Usar data de referência (atualização ou criação)
            data_ref = datetime.fromisoformat(data_referencia)
            tempo_decorrido = agora - data_ref
            minutos = tempo_decorrido.total_seconds() / 60
            
            # Thresholds configuráveis (minutos): [excelente, bom, regular, mediano, ruim]
            thresholds = getattr(self, 'tempo_thresholds_min', [30, 60, 90, 120, 150])
            t1, t2, t3, t4, t5 = thresholds
            # 6 níveis conforme thresholds
            if minutos < t1:
                return 'tempo_excelente'  # Verde - < 30 min
            elif minutos < t2:
                return 'tempo_bom'        # Verde-claro - 30-60 min
            elif minutos < t3:
                return 'tempo_regular'    # Amarelo - 60-90 min
            elif minutos < t4:
                return 'tempo_mediano'    # Laranja - 90-120 min
            elif minutos < t5:
                return 'tempo_ruim'       # Vermelho - 120-150 min
            else:
                return 'tempo_pessimo'    # Vermelho-escuro - > 150 min
                
        except Exception as e:
            print(f"✗ Erro ao calcular tempo de atualização: {e}")
            return 'tempo_pessimo'  # Em caso de erro, considerar péssimo
        self.detail_frame.bind("<Enter>", _bind_mousewheel_global)
        self.detail_frame.bind("<Leave>", _unbind_mousewheel_global)
        
        # Aplicar scroll a todos os widgets filhos do painel de detalhes
        _bind_scroll_to_widget(self.detail_frame)
        
        # Mensagem inicial (nenhuma seleção)
        self.label_sem_selecao = ttk.Label(
            self.detail_frame,
            text="← Selecione uma pendência à esquerda para ver os detalhes",
            font=('Arial', 11),
            foreground='gray'
        )
        self.label_sem_selecao.pack(pady=100)
        
        # Carregar pendências
        self.atualizar_pendencias()
    
    def atualizar_estatisticas(self):
        """Atualiza os dados de estatísticas"""
        try:
            # Funcionalidade de rastreamento de propostas foi removida
            # Mostrar dados vazios/zerados
            self.lbl_total_propostas.config(text="Total: 0 propostas")
            self.lbl_valor_total.config(text="Valor Total: R$ 0,00")
            
            # Limpar tipos
            self.text_tipos.delete('1.0', tk.END)
            self.text_tipos.insert(tk.END, "Funcionalidade de rastreamento de propostas foi removida.\n")
            
            # Limpar usuários
            for item in self.tree_usuarios.get_children():
                self.tree_usuarios.delete(item)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar estatísticas:\n{str(e)}")
    
    def atualizar_pendencias(self, preservar_selecao=True, preservar_ordenacao=True):
        """
        Atualiza a lista de pendências (usando sistema JSON)
        
        Args:
            preservar_selecao: Se True, tenta preservar a seleção atual após atualizar
            preservar_ordenacao: Se True, mantém a ordenação atual após atualizar
        """
        # Guardar seleção atual de forma robusta
        selecionado_anterior = None
        if preservar_selecao:
            try:
                selecao = self.tree_pendencias.selection()
                if selecao:
                    item = self.tree_pendencias.item(selecao[0])
                    if item and 'values' in item and len(item['values']) > 0:
                        selecionado_anterior = item['values'][0]  # Número da pendência
                        # Guardar em cache de instância para proteção extra
                        self._cache_selecao = selecionado_anterior
            except Exception as e:
                # Tentar usar cache anterior se houver
                if hasattr(self, '_cache_selecao'):
                    selecionado_anterior = self._cache_selecao
        
        # Guardar ordenação atual
        ordenacao_anterior = None
        reversa_anterior = None
        if preservar_ordenacao:
            ordenacao_anterior = self.ordenacao_coluna
            reversa_anterior = self.ordenacao_reversa
        
        # Limpar árvore
        for item in self.tree_pendencias.get_children():
            self.tree_pendencias.delete(item)
        
        # Carregar pendências do sistema JSON (OTIMIZADO com cache e instância reutilizável)
        try:
            from datetime import datetime, timedelta
            
            # Usar instância reutilizável ao invés de criar nova
            if not hasattr(self, 'ger_pendencias') or self.ger_pendencias is None:
                from gerenciador_pendencias_json import GerenciadorPendenciasJSON
                self.ger_pendencias = GerenciadorPendenciasJSON()
            
            ger_pend = self.ger_pendencias
            
            mostrar_arquivadas = self.var_mostrar_arquivadas.get()
            
            # Ajustar monitor de mudanças para refletir o que está sendo exibido:
            # - Se NÃO mostrar arquivadas: monitor mais leve (só ATIVAS)
            # - Se mostrar arquivadas: também monitora ARQUIVADAS
            if getattr(self, 'monitor_mudancas', None):
                try:
                    self.monitor_mudancas.definir_monitorar_arquivadas(bool(mostrar_arquivadas))
                except Exception:
                    pass
            
            # Obter filtros selecionados
            filtro_status = self.combo_status_pendencia.get()
            filtro_situacao = self.combo_situacao_pendencia.get()
            filtro_usuario = self.combo_usuario_pendencia.get()
            filtro_setor = self.combo_setor_pendencia.get()
            
            # OTIMIZAÇÃO: Verificar cache antes de ler do disco
            chave_cache = (
                filtro_status,
                filtro_situacao,
                filtro_usuario,
                filtro_setor,
                mostrar_arquivadas,
                self.semana_inicio,
                self.semana_fim
            )
            
            usar_cache = False
            if (hasattr(self, '_cache_pendencias_timestamp') and 
                self._cache_pendencias_timestamp is not None and
                chave_cache in self._cache_pendencias):
                # Verificar se cache ainda é válido (dentro do TTL)
                tempo_decorrido = (datetime.now() - self._cache_pendencias_timestamp).total_seconds()
                if tempo_decorrido < self._cache_pendencias_ttl:
                    pendencias = self._cache_pendencias[chave_cache]
                    usar_cache = True
            
            if not usar_cache:
                # Listar pendências com filtro de semana (CARREGAMENTO DINÂMICO)
                # Por padrão, carrega apenas última semana para melhor performance
                pendencias = ger_pend.listar_pendencias(
                    filtro_status=filtro_status if filtro_status != 'Todas' else None,
                    filtro_situacao=filtro_situacao if filtro_situacao != 'Todas' else None,
                    filtro_vendedor=filtro_usuario if filtro_usuario != 'Todos' else None,
                    filtro_setor=filtro_setor if filtro_setor != 'Todos' else None,
                    apenas_ativas=(not mostrar_arquivadas),
                    data_inicio=self.semana_inicio,
                    data_fim=self.semana_fim
                )
                
                # Filtrar pendências baseado no nível do usuário (apenas se houver código válido)
                try:
                    from mapeamento_usuarios import USUARIOS
                    if USUARIOS and len(USUARIOS) > 0 and self.codigo_usuario and self.codigo_usuario in USUARIOS:
                        # Aplicar filtro de permissão baseado no nível do usuário
                        pendencias_antes = len(pendencias)
                        pendencias = [p for p in pendencias if self._verificar_permissao_visualizar(p)]
                        pendencias_depois = len(pendencias)
                        if pendencias_antes > pendencias_depois:
                            print(f"✓ Filtro de permissão aplicado: {pendencias_antes} → {pendencias_depois} pendências visíveis")
                    elif not self.codigo_usuario:
                        print(f"⚠️ Código de usuário não definido. Mostrando todas as pendências (configure DADOS_LOGIN.csv).")
                        # Mostrar todas se não há usuário detectado (modo temporário)
                    elif self.codigo_usuario not in USUARIOS:
                        print(f"⚠️ Código de usuário {self.codigo_usuario} não encontrado no CSV. Mostrando todas as pendências.")
                        # Mostrar todas se código não existe (modo temporário)
                    elif not USUARIOS:
                        print(f"⚠️ Nenhum usuário carregado do CSV. Mostrando todas as pendências (configure DADOS_LOGIN.csv).")
                        # Mostrar todas se não há usuários (modo temporário)
                except Exception as e:
                    print(f"⚠️ Erro ao filtrar por permissão: {e}. Mostrando todas as pendências.")
                    # Em caso de erro, mostrar todas (modo temporário)
                
                # Atualizar permissões dos botões após carregar pendências
                self._atualizar_permissoes_botoes()
                
                # Armazenar no cache
                if not hasattr(self, '_cache_pendencias'):
                    self._cache_pendencias = {}
                self._cache_pendencias[chave_cache] = pendencias
                self._cache_pendencias_timestamp = datetime.now()
            
            # Se há ordenação ativa, ordenar os dados antes de inserir
            if preservar_ordenacao and ordenacao_anterior:
                pendencias = self._ordenar_dados_antes_insercao(pendencias, ordenacao_anterior, reversa_anterior)
            
            # Inserir pendências com efeito zebrado
            for idx, pend in enumerate(pendencias):
                # Extrair dados do JSON
                numero = pend.get('numero', '')
                
                # Data de criação formatada
                data_criacao_iso = pend.get('data_criacao', '')
                if data_criacao_iso:
                    try:
                        dt = datetime.fromisoformat(data_criacao_iso)
                        data_fmt = dt.strftime("%d/%m/%Y")
                        horario_fmt = dt.strftime("%H:%M")
                    except:
                        data_fmt = ''
                        horario_fmt = ''
                else:
                    data_fmt = ''
                    horario_fmt = ''
                
                # Situação (pipeline comercial)
                status = pend.get('situacao', '')
                
                # Determinar tags: pendência ATIVA + cor por tempo
                tags = []
                
                # Tag de cor baseada no tempo desde última atualização (PRIORIDADE)
                data_atualizacao_iso = pend.get('data_atualizacao', '')
                tempo_tag = self._obter_tag_tempo_atualizacao(data_criacao_iso, data_atualizacao_iso)
                if tempo_tag:
                    tags.append(tempo_tag)
                
                # Tag especial para pendência ATIVA (sobrescreve cor de tempo)
                if self.pendencia_ativa and numero == self.pendencia_ativa:
                    tags.append('ativa')  # Azul destaque para pendência ATIVA
                
                # Inserir item (SEM coluna de seleção com bolinhas)
                item_id = self.tree_pendencias.insert('', 'end', values=(
                    numero,
                    data_fmt,
                    horario_fmt,
                    status
                ), tags=tags)
                
                # Restaurar seleção se era este item
                if preservar_selecao and selecionado_anterior and numero == selecionado_anterior:
                    # Usar after() para garantir que a seleção aconteça após renderização
                    self.root.after(10, lambda: self._restaurar_selecao_segura(item_id))
        
            # Restaurar indicadores visuais se havia ordenação anterior
            if preservar_ordenacao and ordenacao_anterior:
                self.ordenacao_coluna = ordenacao_anterior
                self.ordenacao_reversa = reversa_anterior
                self._atualizar_indicadores_ordenacao(ordenacao_anterior)
        
        except Exception as e:
            print(f"✗ Erro ao carregar pendências: {e}")
            import traceback
            traceback.print_exc()
    
    def limpar_filtros_data(self):
        """Limpa os filtros de data"""
        self.entry_data_filtro.delete(0, tk.END)
        self._adicionar_placeholder_data()
        self.atualizar_pendencias()
    
    def _adicionar_placeholder_data(self):
        """Define o dia atual como valor padrão"""
        if not self.entry_data_filtro.get():
            from datetime import datetime
            hoje = datetime.now()
            data_hoje = hoje.strftime("%d/%m/%Y")
            self.entry_data_filtro.insert(0, data_hoje)
            self.entry_data_filtro.config(foreground='black')
    
    def _on_focus_in_data(self, event=None):
        """Quando o usuário clica no campo de data"""
        # Não precisa fazer nada especial, o campo já tem o dia atual
        pass
    
    def _dia_anterior(self):
        """Navega para o dia anterior"""
        print("✓ Navegando para dia anterior...")
        try:
            from datetime import datetime, timedelta
            
            data_atual = self.entry_data_filtro.get().strip()
            if not data_atual:
                return
            
            # Converter data atual para datetime
            try:
                data_dt = datetime.strptime(data_atual, "%d/%m/%Y")
            except ValueError:
                # Se não conseguir converter, usar data atual
                data_dt = datetime.now()
            
            # Subtrair um dia
            dia_anterior = data_dt - timedelta(days=1)
            
            # Atualizar campo
            nova_data = dia_anterior.strftime("%d/%m/%Y")
            self.entry_data_filtro.delete(0, tk.END)
            self.entry_data_filtro.insert(0, nova_data)
            
            # Atualizar pendências
            self.atualizar_pendencias()
            
        except Exception as e:
            print(f"✗ Erro ao navegar para dia anterior: {e}")
    
    def _dia_proximo(self):
        """Navega para o próximo dia"""
        print("✓ Navegando para próximo dia...")
        try:
            from datetime import datetime, timedelta
            
            data_atual = self.entry_data_filtro.get().strip()
            if not data_atual:
                return
            
            # Converter data atual para datetime
            try:
                data_dt = datetime.strptime(data_atual, "%d/%m/%Y")
            except ValueError:
                # Se não conseguir converter, usar data atual
                data_dt = datetime.now()
            
            # Adicionar um dia
            dia_proximo = data_dt + timedelta(days=1)
            
            # Atualizar campo
            nova_data = dia_proximo.strftime("%d/%m/%Y")
            self.entry_data_filtro.delete(0, tk.END)
            self.entry_data_filtro.insert(0, nova_data)
            
            # Atualizar pendências
            self.atualizar_pendencias()
            
        except Exception as e:
            print(f"✗ Erro ao navegar para próximo dia: {e}")
    
    def _voltar_hoje(self):
        """Volta para o dia atual"""
        print("✓ Voltando para hoje...")
        try:
            from datetime import datetime
            
            # Obter data atual
            hoje = datetime.now()
            data_hoje = hoje.strftime("%d/%m/%Y")
            
            # Atualizar campo
            self.entry_data_filtro.delete(0, tk.END)
            self.entry_data_filtro.insert(0, data_hoje)
            
            # Atualizar pendências
            self.atualizar_pendencias()
            
        except Exception as e:
            print(f"✗ Erro ao voltar para hoje: {e}")
    
    def _formatar_data_automatica(self, event=None):
        """Formata automaticamente a data enquanto o usuário digita"""
        valor = self.entry_data_filtro.get()
        
        # Se o campo está vazio, não fazer nada
        if not valor:
            return
        
        # Remover caracteres não numéricos
        apenas_numeros = ''.join(filter(str.isdigit, valor))
        
        # Limitar a 8 dígitos (DDMMAAAA)
        if len(apenas_numeros) > 8:
            apenas_numeros = apenas_numeros[:8]
        
        # Formatar automaticamente
        if len(apenas_numeros) >= 2:
            # DD/MM/AAAA
            if len(apenas_numeros) == 2:
                formato = f"{apenas_numeros[:2]}/"
            elif len(apenas_numeros) == 4:
                formato = f"{apenas_numeros[:2]}/{apenas_numeros[2:4]}/"
            elif len(apenas_numeros) >= 6:
                formato = f"{apenas_numeros[:2]}/{apenas_numeros[2:4]}/{apenas_numeros[4:8]}"
            else:
                formato = apenas_numeros
            
            # Atualizar campo se diferente
            if formato != valor:
                self.entry_data_filtro.delete(0, tk.END)
                self.entry_data_filtro.insert(0, formato)
                self.entry_data_filtro.config(foreground='black')
        
        # Atualizar pendências após formatação
        self.atualizar_pendencias()
    
    def _aplicar_filtro_data_simples(self, pendencias, data_filtro):
        """Aplica filtro de data simples às pendências (filtra por data específica)"""
        try:
            from datetime import datetime
            
            # Converter data para datetime
            data_filtro_dt = None
            
            try:
                # Aceitar formatos: DD/MM/YYYY, DD/MM/YY, DD-MM-YYYY, DD-MM-YY
                for formato in ['%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y']:
                    try:
                        data_filtro_dt = datetime.strptime(data_filtro, formato)
                        break
                    except ValueError:
                        continue
                
                if not data_filtro_dt:
                    print(f"✗ Formato de data inválido: {data_filtro}")
                    return pendencias
                    
            except Exception as e:
                print(f"✗ Erro ao converter data: {e}")
                return pendencias
            
            # Filtrar pendências pela data específica
            pendencias_filtradas = []
            for pend in pendencias:
                # Obter data de criação da pendência
                data_criacao_iso = pend.get('data_criacao', '')
                if not data_criacao_iso:
                    continue
                
                try:
                    data_criacao = datetime.fromisoformat(data_criacao_iso)
                    data_criacao = data_criacao.replace(hour=0, minute=0, second=0, microsecond=0)
                    
                    # Verificar se é a mesma data
                    if data_criacao.date() == data_filtro_dt.date():
                        pendencias_filtradas.append(pend)
                        
                except Exception as e:
                    print(f"✗ Erro ao processar data da pendência {pend.get('numero', '')}: {e}")
                    continue
            
            return pendencias_filtradas
            
        except Exception as e:
            print(f"✗ Erro no filtro de data: {e}")
            return pendencias
    
    def _aplicar_filtro_data(self, pendencias, data_inicial, data_final):
        """Aplica filtro de data às pendências"""
        try:
            from datetime import datetime
            
            # Converter datas para datetime
            data_inicio = None
            data_fim = None
            
            if data_inicial:
                try:
                    # Aceitar formatos: DD/MM/YYYY, DD/MM/YY, DD-MM-YYYY, DD-MM-YY
                    for formato in ['%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y']:
                        try:
                            data_inicio = datetime.strptime(data_inicial, formato)
                            break
                        except ValueError:
                            continue
                    
                    if not data_inicio:
                        print(f"✗ Formato de data inicial inválido: {data_inicial}")
                        return pendencias
                        
                except Exception as e:
                    print(f"✗ Erro ao converter data inicial: {e}")
                    return pendencias
            
            if data_final:
                try:
                    # Aceitar formatos: DD/MM/YYYY, DD/MM/YY, DD-MM-YYYY, DD-MM-YY
                    for formato in ['%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y']:
                        try:
                            data_fim = datetime.strptime(data_final, formato)
                            break
                        except ValueError:
                            continue
                    
                    if not data_fim:
                        print(f"✗ Formato de data final inválido: {data_final}")
                        return pendencias
                        
                except Exception as e:
                    print(f"✗ Erro ao converter data final: {e}")
                    return pendencias
            
            # Filtrar pendências
            pendencias_filtradas = []
            for pend in pendencias:
                # Obter data de criação da pendência
                data_criacao_iso = pend.get('data_criacao', '')
                if not data_criacao_iso:
                    continue
                
                try:
                    data_criacao = datetime.fromisoformat(data_criacao_iso)
                    data_criacao = data_criacao.replace(hour=0, minute=0, second=0, microsecond=0)
                    
                    # Verificar se está dentro do intervalo
                    incluir = True
                    
                    if data_inicio:
                        if data_criacao < data_inicio:
                            incluir = False
                    
                    if data_fim and incluir:
                        if data_criacao > data_fim:
                            incluir = False
                    
                    if incluir:
                        pendencias_filtradas.append(pend)
                        
                except Exception as e:
                    print(f"✗ Erro ao processar data da pendência {pend.get('numero', '')}: {e}")
                    continue
            
            return pendencias_filtradas
            
        except Exception as e:
            print(f"✗ Erro no filtro de data: {e}")
            return pendencias
    
    def _restaurar_selecao_segura(self, item_id):
        """Restaura seleção de forma segura após renderização"""
        try:
            if item_id in self.tree_pendencias.get_children():
                self.tree_pendencias.selection_set(item_id)
                self.tree_pendencias.see(item_id)
                self.tree_pendencias.focus(item_id)
        except Exception as e:
            print(f"✗ Erro ao restaurar seleção: {e}")
    
    def _aplicar_ordenacao_salva(self, coluna, reversa):
        """Aplica ordenação salva após recarregar pendências"""
        try:
            if not coluna:
                return
            
            # Restaurar estado de ordenação
            self.ordenacao_coluna = coluna
            self.ordenacao_reversa = reversa
            
            # Aplicar ordenação diretamente (sem inverter)
            self._aplicar_ordenacao_direta(coluna, reversa)
            
            print(f"✓ Ordenação restaurada: {coluna} {'(reversa)' if reversa else '(normal)'}")
        except Exception as e:
            print(f"✗ Erro ao aplicar ordenação salva: {e}")
    
    def _aplicar_ordenacao_direta(self, coluna, reversa):
        """Aplica ordenação diretamente sem inverter"""
        try:
            # Obter todos os itens do TreeView
            items = list(self.tree_pendencias.get_children(''))
            
            if not items:
                return
            
            # Função de ordenação baseada no tipo de coluna
            def obter_valor_ordenacao(item):
                valores = self.tree_pendencias.item(item, 'values')
                
                if coluna == 'Pendência':
                    # Ordenar por número da pendência
                    numero = valores[0].replace('#', '')
                    try:
                        return int(numero)
                    except:
                        return 0
                elif coluna == 'Data':
                    # Ordenar por data (formato DD/MM/YYYY)
                    data_str = valores[1]
                    try:
                        from datetime import datetime
                        return datetime.strptime(data_str, '%d/%m/%Y')
                    except:
                        return datetime.min
                elif coluna == 'Hora':
                    # Ordenar por horário (formato HH:MM)
                    horario_str = valores[2]
                    try:
                        from datetime import datetime, time
                        return datetime.strptime(horario_str, '%H:%M').time()
                    except:
                        return time.min
                else:
                    # Ordenar alfabeticamente (Situação)
                    return valores[3] if coluna == 'Situação' else ''
            
            # Ordenar itens
            items_ordenados = sorted(items, key=obter_valor_ordenacao, reverse=reversa)
            
            # Reorganizar itens no TreeView de forma mais suave
            # Usar update_idletasks() para evitar piscadas
            self.tree_pendencias.update_idletasks()
            
            for i, item in enumerate(items_ordenados):
                self.tree_pendencias.move(item, '', i)
            
            # Atualizar indicadores visuais
            self._atualizar_indicadores_ordenacao(coluna)
            
        except Exception as e:
            print(f"✗ Erro ao aplicar ordenação direta: {e}")
    
    def _obter_pendencia_selecionada(self, usar_ativa=True):
        """
        Obtém a pendência selecionada - USA SEMPRE A PENDÊNCIA ATIVA (mais confiável)
        
        Args:
            usar_ativa: Se True (padrão), usa a pendência ATIVA ao invés da seleção do TreeView
        
        Returns:
            tuple: (numero, valores_completos) ou (None, None) se não houver seleção
        """
        try:
            # PRIORIDADE 1: Usar PENDÊNCIA ATIVA (seleção definitiva e persistente)
            if usar_ativa and self.pendencia_ativa:
                # Buscar dados atualizados da pendência ativa
                from gerenciador_pendencias_json import GerenciadorPendenciasJSON
                ger = GerenciadorPendenciasJSON()
                pendencia = ger.ler_pendencia(self.pendencia_ativa)
                
                if pendencia:
                    # Construir valores no formato esperado
                    from datetime import datetime
                    data_criacao_iso = pendencia.get('data_criacao', '')
                    if data_criacao_iso:
                        try:
                            dt = datetime.fromisoformat(data_criacao_iso)
                            data_fmt = dt.strftime("%d/%m/%Y")
                        except:
                            data_fmt = ''
                    else:
                        data_fmt = ''
                    
                    cliente_data = pendencia.get('cliente', {})
                    cliente_nome = cliente_data.get('razao_social', '') or '(Sem nome)'
                    # Suportar tanto 'usuario' (canônico) quanto 'vendedor' (compatibilidade)
                    usuario = pendencia.get('usuario') or pendencia.get('vendedor', '')
                    status = pendencia.get('status', '')
                    
                    valores = (
                        self.pendencia_ativa,
                        data_fmt,
                        cliente_nome,
                        usuario,
                        status
                    )
                    
                    return self.pendencia_ativa, valores
            
            # FALLBACK: Usar seleção do TreeView (apenas se não houver pendência ativa)
            selecao = self.tree_pendencias.selection()
            
            if selecao:
                item_id = selecao[0]
                valores = self.tree_pendencias.item(item_id, 'values')
                
                if valores and len(valores) >= 1:
                    numero = valores[0]
                    if numero and str(numero).strip():
                        return numero, valores
            
            return None, None
        
        except Exception as e:
            print(f"✗ Erro ao obter seleção: {e}")
            import traceback
            traceback.print_exc()
            return None, None
    
    def _on_pendencia_clique_unico(self, event=None):
        """Ativa uma pendência com UM CLIQUE (seleção definitiva)"""
        try:
            # Obter seleção atual do TreeView
            selecao = self.tree_pendencias.selection()
            
            if selecao:
                # Obter valores do item
                item_id = selecao[0]
                valores = self.tree_pendencias.item(item_id, 'values')
                
                if valores and len(valores) >= 1:
                    numero = valores[0]
                    
                    # ATIVAR esta pendência (seleção definitiva)
                    self.ativar_pendencia(numero)
        
        except Exception as e:
            print(f"✗ Erro ao processar clique: {e}")
    
    def ativar_pendencia(self, numero):
        """
        Ativa uma pendência (seleção única definitiva e persistente)
        
        Args:
            numero: Número da pendência a ativar
        """
        try:
            from gerenciador_pendencias_json import GerenciadorPendenciasJSON
            ger = GerenciadorPendenciasJSON()
            
            # Carregar dados completos
            pendencia = ger.ler_pendencia(numero)
            
            if not pendencia:
                print(f"✗ Pendência {numero} não encontrada")
                return
            
            # ATIVAR pendência (seleção definitiva)
            self.pendencia_ativa = numero
            self.pendencia_ativa_dados = pendencia
            
            # Atualizar label informativo
            self._atualizar_label_pendencia_ativa()
            
            # Atualizar visual da lista (amarelo)
            self.atualizar_pendencias(preservar_selecao=False, preservar_ordenacao=True)
            
            # Atualizar painel de detalhes
            self._on_pendencia_selecionada()
            
            print(f"✓ Pendência {numero} ATIVADA (seleção definitiva)")
        
        except Exception as e:
            print(f"✗ Erro ao ativar pendência: {e}")
            import traceback
            traceback.print_exc()
    
    def _on_esc_deselecionar(self, event=None):
        """Desseleciona a pendência ativa quando ESC é pressionado"""
        try:
            if self.pendencia_ativa:
                print(f"✓ Desselecionando pendência ativa: {self.pendencia_ativa}")
                
                # Limpar seleção do TreeView primeiro
                try:
                    self.tree_pendencias.selection_remove(self.tree_pendencias.selection())
                except Exception as e:
                    print(f"✗ Erro ao limpar seleção do TreeView: {e}")
                
                # Limpar pendência ativa
                self.limpar_pendencia_ativa()
                
                print("✓ Pendência desselecionada com ESC")
            else:
                print("✓ Nenhuma pendência ativa para desselecionar")
                
        except Exception as e:
            print(f"✗ Erro ao desselecionar com ESC: {e}")
            import traceback
            traceback.print_exc()
    
    def limpar_pendencia_ativa(self):
        """Limpa a pendência ativa (remove seleção definitiva)"""
        try:
            if self.pendencia_ativa:
                print(f"✓ Limpando pendência ativa: {self.pendencia_ativa}")
                self.pendencia_ativa = None
                self.pendencia_ativa_dados = None
                
                # Atualizar label
                try:
                    self._atualizar_label_pendencia_ativa()
                except Exception as e:
                    print(f"✗ Erro ao atualizar label: {e}")
                
                # Atualizar visual (remover amarelo)
                try:
                    self.atualizar_pendencias(preservar_selecao=False, preservar_ordenacao=True)
                except Exception as e:
                    print(f"✗ Erro ao atualizar pendências: {e}")
                
                # Limpar painel de detalhes
                try:
                    for widget in self.detail_frame.winfo_children():
                        widget.destroy()
                    
                    ttk.Label(self.detail_frame,
                             text="← Clique em uma pendência para ativá-la",
                             font=('Arial', 11),
                             foreground='gray').pack(pady=100)
                except Exception as e:
                    print(f"✗ Erro ao limpar painel de detalhes: {e}")
                    
        except Exception as e:
            print(f"✗ Erro geral ao limpar pendência ativa: {e}")
            import traceback
            traceback.print_exc()
    
    def _atualizar_label_pendencia_ativa(self):
        """Atualiza o label que mostra qual pendência está ativa (UI removida, lógica mantida)"""
        # Label removido da UI, mas função mantida para compatibilidade
        # A lógica de pendência ativa continua funcionando nos bastidores
        pass
    
    def _on_pendencia_selecionada(self, event=None):
        """Mostra detalhes da pendência selecionada no painel direito"""
        numero, _ = self._obter_pendencia_selecionada()
        if not numero:
            return
        for widget in self.detail_frame.winfo_children():
            widget.destroy()
        try:
            from detalhes_pendencia import renderizar_painel_detalhes
            renderizar_painel_detalhes(self, numero)
        except Exception as e:
            import traceback
            print(f"✗ Erro ao carregar detalhes: {e}")
            traceback.print_exc()
            ttk.Label(self.detail_frame, text=f"Erro ao carregar detalhes:\n{str(e)}", foreground='red').pack(pady=20)
    
    def _editar_pendencia_completa(self):
        """Interface centralizada para editar pendência - combina todas as funções"""
        print("✓ Abrindo editor de pendência...")
        from tkinter import messagebox
        numero, valores = self._obter_pendencia_selecionada()
        
        if not numero:
            messagebox.showwarning("Aviso", "Selecione uma pendência primeiro.")
            return
        
        # Chamar interface centralizada
        self._editar_pendencia_centralizada(numero)
    
    def _obter_dados_pendencia(self, numero_pendencia):
        """Obtém dados completos da pendência"""
        try:
            from gerenciador_pendencias_json import GerenciadorPendenciasJSON
            
            gerenciador = GerenciadorPendenciasJSON()
            dados = gerenciador.ler_pendencia(numero_pendencia)
            
            return dados
            
        except Exception as e:
            print(f"❌ Erro ao obter dados da pendência {numero_pendencia}: {e}")
            return None
    
    def _editar_dados_pendencia_ativa(self):
        """Edita dados do cliente da pendência ATIVA"""
        print("✓ Editando dados da pendência ativa...")
        from tkinter import messagebox
        numero, valores = self._obter_pendencia_selecionada()
        
        if not numero:
            messagebox.showwarning("Aviso", "Nenhuma pendência ativa.\n\nClique em uma pendência para ativá-la.")
            return
        
        # Chamar método de edição existente
        self._editar_dados_cliente(numero)
    
    
    def _editar_pendencia_centralizada(self, numero_pendencia):
        """Interface centralizada para editar pendência - combina todas as funcionalidades"""
        # Verificar permissão de edição
        from gerenciador_pendencias_json import GerenciadorPendenciasJSON
        ger = GerenciadorPendenciasJSON()
        pendencia = ger.ler_pendencia(numero_pendencia)
        if pendencia and not self._verificar_permissao_editar(pendencia):
            from tkinter import messagebox
            messagebox.showwarning("Acesso Negado", 
                                 "Você não tem permissão para editar esta pendência.\n\n"
                                 "Nível 1: apenas visualização\n"
                                 "Nível 2: pode editar apenas suas próprias pendências\n"
                                 "Nível 3: pode editar pendências do seu setor\n"
                                 "Nível 4: pode editar todas as pendências")
            return
        
        try:
            from editor_pendencias import EditorPendencias

            # Criar instância do editor
            editor = EditorPendencias(self.root, self.usuario_detectado)
            
            # Definir callback para atualização
            def callback_atualizacao():
                # Invalidar cache para garantir que mudanças sejam vistas imediatamente
                self._invalidar_cache_pendencias()
                self.monitor_mudancas.resetar_cache()
                self.atualizar_pendencias()
                self._recarregar_pendencia_ativa()  # Recarregar dados da pendência ativa (incluindo telefone atualizado)
                self._on_pendencia_selecionada()
            
            # Abrir editor
            editor.abrir_editor_pendencia(numero_pendencia, callback_atualizacao)
            
        except ImportError as e:
            messagebox.showerror("Erro", f"Erro ao importar editor de pendências: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir editor: {e}")
    
    
    def criar_nova_pendencia(self):
        """Abre janela para criar uma nova pendência manualmente"""
        # Verificar permissão
        if not self._verificar_permissao_criar():
            messagebox.showwarning("Acesso Negado", 
                                 "Você não tem permissão para criar pendências.\n\n"
                                 "Níveis 1 e 2: apenas visualização/edição de suas próprias pendências.")
            return
        
        print("✓ Abrindo criador de pendências...")
        try:
            from criador_pendencias import CriadorPendencias
            
            # Definir callback para atualização recebendo o número criado
            def callback_atualizacao(numero_criado=None):
                # Invalidar cache para garantir que nova pendência apareça imediatamente
                self._invalidar_cache_pendencias()
                self.monitor_mudancas.resetar_cache()
                self.atualizar_pendencias()
                if numero_criado:
                    self.ativar_pendencia(numero_criado)
                    self.atualizar_status(f"Pendência {numero_criado} registrada e ativada.", 'sucesso')
                else:
                    self.atualizar_status("Pendência registrada.", 'sucesso')
            
            # Criar e abrir criador de pendências (toda lógica está no criador_pendencias.py)
            criador = CriadorPendencias(self.root, self.usuario_detectado, callback_atualizacao)
            criador.abrir_janela_criacao()
            
        except ImportError as e:
            messagebox.showerror("Erro", f"Erro ao importar criador de pendências: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir criador: {e}")
    
    def transferir_pendencia(self):
        """Transfere uma pendência para outro setor ou usuário"""
        from datetime import datetime
        print("✓ Abrindo transferência de pendência...")
        numero_proposta, valores = self._obter_pendencia_selecionada()
        
        if not numero_proposta:
            messagebox.showwarning("Aviso", "Selecione uma pendência primeiro.")
            return
        
        # Verificar permissão de edição
        from gerenciador_pendencias_json import GerenciadorPendenciasJSON
        ger = GerenciadorPendenciasJSON()
        pendencia = ger.ler_pendencia(numero_proposta)
        if pendencia and not self._verificar_permissao_editar(pendencia):
            messagebox.showwarning("Acesso Negado", 
                                 "Você não tem permissão para transferir esta pendência.\n\n"
                                 "Nível 1: apenas visualização\n"
                                 "Nível 2: pode editar apenas suas próprias pendências\n"
                                 "Nível 3: pode editar pendências do seu setor\n"
                                 "Nível 4: pode editar todas as pendências")
            return
        
        # Obter dados completos da pendência
        pendencia = ger.ler_pendencia(numero_proposta)
        if not pendencia:
            messagebox.showerror("Erro", "Pendência não encontrada")
            return
        
        setor_atual = pendencia.get('setor', '')
        # Suportar tanto 'usuario' (canônico) quanto 'vendedor' (compatibilidade)
        usuario_atual = pendencia.get('usuario') or pendencia.get('vendedor', '')
        
        # Criar janela de transferência
        janela_transf = tk.Toplevel(self.root)
        janela_transf.title("Transferir Pendência")
        janela_transf.geometry("500x500")
        janela_transf.resizable(False, False)
        
        # Centralizar janela de transferência
        janela_transf.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 500) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 500) // 2
        janela_transf.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(janela_transf, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text=f"Transferir Pendência: {numero_proposta}", 
                 font=('Arial', 11, 'bold')).pack(pady=(0, 15))
        
        # Informações atuais
        info_frame = ttk.LabelFrame(frame, text=" 📋 Informações Atuais ", padding="10")
        info_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(info_frame, text=f"Setor: {setor_atual or 'Não definido'}", 
                 font=('Arial', 10)).pack(anchor='w', pady=2)
        ttk.Label(info_frame, text=f"Usuário: {usuario_atual or 'Não definido'}", 
                 font=('Arial', 10)).pack(anchor='w', pady=2)
        
        # Opções de transferência
        opcoes_frame = ttk.LabelFrame(frame, text=" 🔄 Transferir ", padding="10")
        opcoes_frame.pack(fill='x', pady=(0, 15))
        
        # Radio buttons para escolher tipo de transferência
        tipo_transferencia = tk.StringVar(value='usuario')
        
        ttk.Radiobutton(opcoes_frame, text="Transferir Usuário Responsável", 
                       variable=tipo_transferencia, value='usuario').pack(anchor='w', pady=5)
        ttk.Radiobutton(opcoes_frame, text="Transferir Setor Responsável", 
                       variable=tipo_transferencia, value='setor').pack(anchor='w', pady=5)
        
        # Frame para setor
        frame_setor = ttk.Frame(opcoes_frame)
        frame_setor.pack(fill='x', pady=(10, 0))
        
        ttk.Label(frame_setor, text="Novo Setor:", font=('Arial', 10)).pack(side='left', padx=(0, 10))
        combo_setor = ttk.Combobox(frame_setor, state='readonly', width=30)
        try:
            from mapeamento_usuarios import obter_lista_setores
            setores = obter_lista_setores()
            combo_setor['values'] = setores
        except Exception as e:
            print(f"✗ Erro ao carregar setores: {e}")
            combo_setor['values'] = []
        combo_setor.pack(side='left')
        
        # Frame para usuário
        frame_usuario = ttk.Frame(opcoes_frame)
        frame_usuario.pack(fill='x', pady=(10, 0))
        
        ttk.Label(frame_usuario, text="Novo Usuário:", font=('Arial', 10)).pack(side='left', padx=(0, 10))
        combo_usuario = ttk.Combobox(frame_usuario, state='readonly', width=30)
        combo_usuario.pack(side='left')
        
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
                except Exception as e:
                    print(f"Erro ao carregar usuários do setor: {e}")
                    combo_usuario['values'] = []
            else:
                combo_usuario['values'] = []
        
        combo_setor.bind('<<ComboboxSelected>>', atualizar_usuarios_por_setor)
        
        # Função para mostrar/ocultar campos baseado no tipo de transferência
        def atualizar_visibilidade_campos():
            if tipo_transferencia.get() == 'setor':
                frame_setor.pack(fill='x', pady=(10, 0))
                frame_usuario.pack_forget()
            else:
                frame_setor.pack_forget()
                frame_usuario.pack(fill='x', pady=(10, 0))
                # Carregar todos os usuários se transferindo apenas usuário
                if tipo_transferencia.get() == 'usuario':
                    try:
                        from mapeamento_usuarios import obter_lista_usuarios
                        usuarios = obter_lista_usuarios()
                        combo_usuario['values'] = usuarios
                    except Exception as e:
                        print(f"Erro ao carregar usuários: {e}")
                        combo_usuario['values'] = []
        
        tipo_transferencia.trace('w', lambda *args: atualizar_visibilidade_campos())
        atualizar_visibilidade_campos()  # Inicializar
        
        ttk.Label(frame, text="Motivo (opcional):", font=('Arial', 10)).pack(pady=(15, 5))
        entry_motivo = ttk.Entry(frame, width=45)
        entry_motivo.pack(pady=(0, 10))
        
        def confirmar_transferencia():
            tipo = tipo_transferencia.get()
            
            if tipo == 'setor':
                setor_destino = combo_setor.get()
                if not setor_destino:
                    messagebox.showwarning("Aviso", "Selecione o setor de destino.")
                    return
                
                if setor_destino == setor_atual:
                    messagebox.showwarning("Aviso", "Setor de destino é o mesmo da origem.")
                    return
                
                # Transferir setor (e usuário se necessário)
                usuario_destino = combo_usuario.get()
                if not usuario_destino:
                    # Se não selecionou usuário, manter o atual ou usar primeiro do setor
                    usuario_destino = usuario_atual
                    if not usuario_destino:
                        try:
                            from mapeamento_usuarios import obter_usuarios_por_setor, obter_usuario_por_codigo
                            codigos = obter_usuarios_por_setor(setor_destino)
                            if codigos:
                                usuario_destino = obter_usuario_por_codigo(codigos[0])['nome']
                        except:
                            pass
                
                motivo = entry_motivo.get().strip()
                usuario = self.usuario_detectado['nome'] if self.usuario_detectado else 'Sistema'
                
                # Atualizar pendência (usando campo canônico 'usuario')
                atualizacoes = {
                    'setor': setor_destino,
                    'usuario': usuario_destino  # Campo canônico (antigo: vendedor)
                }
                
                resultado = ger.atualizar_pendencia(
                    numero=numero_proposta,
                    atualizacoes=atualizacoes,
                    usuario=usuario
                )
                
                if resultado.get('sucesso'):
                    # Adicionar ao histórico
                    pendencia_atualizada = ger.ler_pendencia(numero_proposta)
                    if pendencia_atualizada:
                        obs_texto = f"TRANSFERIDO - Setor: {setor_atual} → {setor_destino}"
                        if usuario_destino != usuario_atual:
                            obs_texto += f" | Usuário: {usuario_atual} → {usuario_destino}"
                        if motivo:
                            obs_texto += f" - Motivo: {motivo}"
                        
                        timestamp_iso = datetime.now().isoformat()
                        pendencia_atualizada['historico'].append({
                            "data": timestamp_iso,
                            "status_anterior": "",
                            "status_novo": obs_texto,
                            "usuario": usuario
                        })
                        ger._salvar_pendencia(numero_proposta, pendencia_atualizada)
                    
                    messagebox.showinfo("Sucesso", f"Pendência transferida para o setor {setor_destino}")
                    janela_transf.destroy()
                    self._invalidar_cache_pendencias()
                    self.monitor_mudancas.resetar_cache()
                    self.atualizar_pendencias()
                    self.atualizar_status(f"Pendência {numero_proposta} transferida para setor {setor_destino}", 'sucesso')
                else:
                    messagebox.showerror("Erro", f"Erro ao transferir: {resultado.get('mensagem', 'Erro desconhecido')}")
            
            else:  # tipo == 'usuario'
                usuario_destino = combo_usuario.get()
                if not usuario_destino:
                    messagebox.showwarning("Aviso", "Selecione o usuário de destino.")
                    return
                
                if usuario_destino == usuario_atual:
                    messagebox.showwarning("Aviso", "Usuário de destino é o mesmo da origem.")
                    return
                
                motivo = entry_motivo.get().strip()
                usuario = self.usuario_detectado['nome'] if self.usuario_detectado else 'Sistema'
                
                # Usar função de transferência existente
                if ger.transferir_pendencia(numero_proposta, usuario_destino, motivo, usuario):
                    messagebox.showinfo("Sucesso", f"Pendência transferida para {usuario_destino}")
                    janela_transf.destroy()
                    self._invalidar_cache_pendencias()
                    self.monitor_mudancas.resetar_cache()
                    self.atualizar_pendencias()
                    self.atualizar_status(f"Pendência {numero_proposta} transferida para {usuario_destino}", 'sucesso')
                else:
                    messagebox.showerror("Erro", "Erro ao transferir pendência")
        
        # Separador visual
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=15)
        
        # Frame de botões
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="✓ Transferir", command=confirmar_transferencia, width=15).pack(side='left', padx=8)
        ttk.Button(btn_frame, text="✗ Cancelar", command=janela_transf.destroy, width=15).pack(side='left', padx=8)
    
    def atualizar_situacao_pendencia(self):
        """Abre janela para atualizar situação de uma pendência"""
        print("✓ Abrindo atualizador de situação...")
        numero_proposta, valores = self._obter_pendencia_selecionada()
        
        if not numero_proposta:
            messagebox.showwarning("Aviso", "Selecione uma pendência primeiro.")
            return
        
        # Verificar permissão de edição
        from gerenciador_pendencias_json import GerenciadorPendenciasJSON
        ger = GerenciadorPendenciasJSON()
        pendencia = ger.ler_pendencia(numero_proposta)
        if pendencia and not self._verificar_permissao_editar(pendencia):
            messagebox.showwarning("Acesso Negado", 
                                 "Você não tem permissão para editar esta pendência.\n\n"
                                 "Nível 1: apenas visualização\n"
                                 "Nível 2: pode editar apenas suas próprias pendências\n"
                                 "Nível 3: pode editar pendências do seu setor\n"
                                 "Nível 4: pode editar todas as pendências")
            return
        
        try:
            from atualizador_situacao import AtualizadorSituacao
            
            # Obter dados completos da pendência
            from gerenciador_pendencias_json import GerenciadorPendenciasJSON
            ger_pend = GerenciadorPendenciasJSON()
            dados_pendencia = ger_pend.ler_pendencia(numero_proposta)
            
            if not dados_pendencia:
                messagebox.showerror("Erro", "Pendência não encontrada.")
                return
            
            # Definir callback para atualização
            def callback_atualizacao():
                self._invalidar_cache_pendencias()  # Invalidar cache para ver mudança imediatamente
                self.monitor_mudancas.resetar_cache()
                self.atualizar_pendencias()
                self._recarregar_pendencia_ativa()  # Recarregar dados da pendência ativa após atualização
                self._on_pendencia_selecionada()
                self.atualizar_status("Situação da pendência atualizada com sucesso!", 'sucesso')
            
            # Criar e abrir atualizador de situação
            atualizador = AtualizadorSituacao(self.root, callback_atualizacao)
            atualizador.abrir_atualizador_situacao(numero_proposta, dados_pendencia)
            
        except ImportError as e:
            messagebox.showerror("Erro", f"Erro ao importar atualizador de situação: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir atualizador: {e}")

    def arquivar_pendencia_dialog(self):
        """Abre janela para arquivar uma pendência"""
        print("✓ Abrindo arquivamento de pendência...")
        numero_proposta, valores = self._obter_pendencia_selecionada()
        
        if not numero_proposta:
            messagebox.showwarning("Aviso", "Selecione uma pendência primeiro.")
            return
        
        # Índices: 0:N°Proposta, 1:Data, 2:Hora, 3:Situação
        # Obter dados completos da pendência
        numero_proposta = valores[0]
        from gerenciador_pendencias_json import GerenciadorPendenciasJSON
        ger = GerenciadorPendenciasJSON()
        pendencia = ger.ler_pendencia(numero_proposta)
        if not pendencia:
            messagebox.showerror("Erro", "Pendência não encontrada")
            return
        
        cliente_data = pendencia.get('cliente', {})
        cliente = cliente_data.get('razao_social', '') or cliente_data.get('contato', '') or 'Cliente não identificado'
        status_atual = valores[3]
        
        # Não permitir arquivar se já está arquivada
        if status_atual == 'Venda Perdida':
            messagebox.showinfo("Informação", "Esta pendência já está arquivada.")
            return
        
        # Criar janela de arquivamento
        janela_arq = tk.Toplevel(self.root)
        janela_arq.title("Arquivar Pendência")
        janela_arq.geometry("550x350")
        janela_arq.resizable(False, False)
        
        # Centralizar
        janela_arq.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 550) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 350) // 2
        janela_arq.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(janela_arq, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Arquivar Pendência", 
                 font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        ttk.Label(frame, text=f"Proposta: {numero_proposta}", 
                 font=('Arial', 10), foreground='blue').pack(pady=5)
        
        ttk.Label(frame, text=f"Cliente: {cliente}", 
                 font=('Arial', 9)).pack(pady=(0, 15))
        
        ttk.Label(frame, text="⚠️ Esta ação mudará o status da pendência para 'Venda Perdida'.", 
                 font=('Arial', 9), foreground='orange').pack(pady=10)
        
        ttk.Label(frame, text="Motivo do arquivamento (opcional):", 
                 font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        entry_motivo = ttk.Entry(frame, width=50)
        entry_motivo.pack(pady=5)
        
        def confirmar_arquivamento():
            motivo = entry_motivo.get().strip()
            
            # Confirmar com usuário
            confirma = messagebox.askyesno(
                "Confirmar Arquivamento",
                f"Tem certeza que deseja arquivar a pendência {numero_proposta}?\n\n"
                f"Situação atual: {status_atual}\n"
                f"Novo status: Venda Perdida"
            )
            
            if not confirma:
                return
            
            # Executar arquivamento
            from gerenciador_pendencias_json import GerenciadorPendenciasJSON
            ger_pend = GerenciadorPendenciasJSON()
            
            usuario = self.usuario_detectado['nome'] if self.usuario_detectado else 'Sistema'
            if ger_pend.arquivar_pendencia(numero_proposta, motivo, usuario):
                messagebox.showinfo("Sucesso", f"Pendência {numero_proposta} arquivada com sucesso!")
                janela_arq.destroy()
                self._invalidar_cache_pendencias()  # Invalidar cache para ver mudança imediatamente
                self.monitor_mudancas.resetar_cache()  # Força refresh em todos os PCs
                self.atualizar_pendencias()  # Atualiza imediatamente
                self.atualizar_status(f"Pendência {numero_proposta} arquivada", 'sucesso')
            else:
                messagebox.showerror("Erro", "Erro ao arquivar pendência.")
        
        # Separador
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=15)
        
        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="📦 Arquivar", command=confirmar_arquivamento, width=15).pack(side='left', padx=8)
        ttk.Button(btn_frame, text="✗ Cancelar", command=janela_arq.destroy, width=15).pack(side='left', padx=8)
    
    def deletar_pendencia_dialog(self):
        """Abre janela para deletar uma pendência (apenas nível 4)"""
        print("✓ Abrindo deleção de pendência...")
        # Verificar permissão - apenas nível 4 pode deletar
        if not self.codigo_usuario or self.nivel_usuario != 4:
            messagebox.showerror("Acesso Negado", 
                               "Apenas usuários de nível 4 têm permissão para deletar pendências.")
            return
        
        numero_proposta, valores = self._obter_pendencia_selecionada()
        
        if not numero_proposta:
            messagebox.showwarning("Aviso", "Selecione uma pendência primeiro.")
            return
        
        # Índices: 0:N°Proposta, 1:Data, 2:Hora, 3:Situação
        # Obter dados completos da pendência
        numero_proposta = valores[0]
        from gerenciador_pendencias_json import GerenciadorPendenciasJSON
        ger = GerenciadorPendenciasJSON()
        pendencia = ger.ler_pendencia(numero_proposta)
        if not pendencia:
            messagebox.showerror("Erro", "Pendência não encontrada")
            return
        
        cliente_data = pendencia.get('cliente', {})
        cliente = cliente_data.get('razao_social', '') or cliente_data.get('contato', '') or 'Cliente não identificado'
        status_atual = valores[3]
        
        # Criar janela de confirmação
        janela_del = tk.Toplevel(self.root)
        janela_del.title("⚠️ Deletar Pendência")
        janela_del.geometry("600x520")
        janela_del.resizable(False, False)
        
        # Centralizar
        janela_del.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 600) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 520) // 2
        janela_del.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(janela_del, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="⚠️ ATENÇÃO: AÇÃO IRREVERSÍVEL", 
                 font=('Arial', 12, 'bold'), foreground='red').pack(pady=(0, 10))
        
        ttk.Label(frame, text=f"Proposta: {numero_proposta}", 
                 font=('Arial', 10), foreground='blue').pack(pady=5)
        
        ttk.Label(frame, text=f"Cliente: {cliente}", 
                 font=('Arial', 9)).pack(pady=(0, 5))
        
        ttk.Label(frame, text=f"Situação: {status_atual}", 
                 font=('Arial', 9)).pack(pady=(0, 20))
        
        # Aviso
        aviso_frame = ttk.Frame(frame)
        aviso_frame.pack(fill='x', pady=10)
        
        ttk.Label(aviso_frame, text="🚨 Esta ação irá DELETAR permanentemente a pendência.", 
                 font=('Arial', 9, 'bold'), foreground='red', wraplength=400).pack()
        ttk.Label(aviso_frame, text="Não será possível recuperar após deletar.", 
                 font=('Arial', 9), foreground='red', wraplength=400).pack()
        ttk.Label(aviso_frame, text="Considere ARQUIVAR ao invés de deletar.", 
                 font=('Arial', 9), foreground='orange', wraplength=400).pack(pady=(10, 0))
        
        ttk.Label(frame, text="Motivo da deleção:", 
                 font=('Arial', 10, 'bold')).pack(pady=(20, 5))
        entry_motivo = ttk.Entry(frame, width=50)
        entry_motivo.pack(pady=5)
        
        def confirmar_delecao():
            motivo = entry_motivo.get().strip()
            
            if not motivo:
                messagebox.showwarning("Aviso", "Informe o motivo da deleção.")
                entry_motivo.focus()
                return
            
            # Dupla confirmação
            confirma = messagebox.askyesno(
                "⚠️ CONFIRMAR DELEÇÃO",
                f"TEM CERTEZA ABSOLUTA?\n\n"
                f"Proposta: {numero_proposta}\n"
                f"Cliente: {cliente}\n\n"
                f"Esta ação é IRREVERSÍVEL!\n"
                f"A pendência será PERMANENTEMENTE deletada!\n\n"
                f"Deseja continuar?",
                icon='warning'
            )
            
            if not confirma:
                return
            
            # Executar deleção (remoção permanente do arquivo)
            from gerenciador_pendencias_json import GerenciadorPendenciasJSON
            ger_pend = GerenciadorPendenciasJSON()
            
            if ger_pend.deletar_pendencia(numero_proposta, motivo):
                messagebox.showinfo(
                    "Deletada", 
                    f"Pendência {numero_proposta} foi DELETADA PERMANENTEMENTE.\n\n"
                    f"Motivo: {motivo}\n\n"
                    f"O arquivo foi removido das pastas de pendências (ATIVAS/ARQUIVADAS)."
                )
                janela_del.destroy()
                self._invalidar_cache_pendencias()  # Invalidar cache para ver mudança imediatamente
                self.monitor_mudancas.resetar_cache()  # Força refresh em todos os PCs
                self.atualizar_pendencias()  # Atualiza imediatamente
                self.atualizar_status(f"Pendência {numero_proposta} deletada (motivo: {motivo})", 'aviso')
            else:
                messagebox.showerror("Erro", "Erro ao deletar pendência.")
        
        # Separador
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=15)
        
        # Botões
        btn_frame_del = ttk.Frame(frame)
        btn_frame_del.pack(pady=10)
        
        ttk.Button(btn_frame_del, text="🗑️ Deletar", command=confirmar_delecao, width=15).pack(side='left', padx=8)
        ttk.Button(btn_frame_del, text="✗ Cancelar", command=janela_del.destroy, width=15).pack(side='left', padx=8)
    
    def atualizar_status_pendencia(self):
        """Atualiza o status de uma pendência selecionada"""
        print("✓ Atualizando status da pendência...")
        numero_proposta, valores = self._obter_pendencia_selecionada()
        
        if not numero_proposta:
            messagebox.showwarning("Aviso", "Selecione uma pendência primeiro.")
            return
        
        # Índices: 0:N°Proposta, 1:Data, 2:Hora, 3:Situação
        status_atual = valores[3]
        
        # Criar janela de atualização de status
        janela_status = tk.Toplevel(self.root)
        janela_status.title("Atualizar Situação")
        janela_status.geometry("550x350")
        janela_status.resizable(False, False)
        
        # Centralizar janela
        janela_status.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 550) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 350) // 2
        janela_status.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(janela_status, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text=f"Proposta: {numero_proposta}", 
                 font=('Arial', 11, 'bold')).pack(pady=(0, 15))
        
        ttk.Label(frame, text=f"Situação Atual: {status_atual}", 
                 font=('Arial', 10), foreground='blue').pack(pady=5)
        
        ttk.Label(frame, text="Nova Situação:", font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        combo_status = ttk.Combobox(frame, state='readonly', width=35)
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
        combo_status['values'] = situacoes_comerciais
        # Pré-selecionar situação atual se possível
        if status_atual in situacoes_comerciais:
            combo_status.set(status_atual)
        else:
            combo_status.set('Novo contato')  # Padrão
        combo_status.pack(pady=5)
        
        ttk.Label(frame, text="Observação:", font=('Arial', 10)).pack(pady=(10, 5))
        entry_obs = ttk.Entry(frame, width=40)
        entry_obs.pack(pady=5)
        
        def confirmar_status():
            novo_status = combo_status.get()
            if not novo_status:
                messagebox.showwarning("Aviso", "Selecione o novo status.")
                return
            
            observacao = entry_obs.get().strip()
            
            from atualizador_situacao import atualizar_situacao
            usuario = self.usuario_detectado['nome'] if self.usuario_detectado else 'Sistema'
            if atualizar_situacao(numero_proposta, novo_status, observacao, usuario):
                messagebox.showinfo("Sucesso", f"Situação atualizada para: {novo_status}")
                janela_status.destroy()
                self._invalidar_cache_pendencias()  # Invalidar cache para ver mudança imediatamente
                self.monitor_mudancas.resetar_cache()  # Força refresh em todos os PCs
                self.atualizar_pendencias()  # Atualiza imediatamente
                self.atualizar_status(f"Situação da proposta {numero_proposta} atualizada", 'sucesso')
            else:
                messagebox.showerror("Erro", "Erro ao atualizar situação")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=15)
        
        ttk.Button(btn_frame, text="Atualizar", command=confirmar_status).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=janela_status.destroy).pack(side='left', padx=5)
    
    def exportar_relatorio(self):
        """Exporta relatório de estatísticas"""
        try:
            # Funcionalidade de rastreamento de propostas foi removida
            messagebox.showinfo(
                "Funcionalidade Removida",
                "A funcionalidade de rastreamento de propostas foi removida.\n"
                "Não é mais possível exportar relatórios de propostas."
            )
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar relatório:\n{str(e)}")
    
    def abrir_registro_csv(self):
        """Abre o arquivo de registro CSV"""
        print("✓ Abrindo registro CSV...")
        try:
            from config_rede import ConfiguracaoRede
            os.startfile(str(ConfiguracaoRede.ARQUIVO_REGISTRO))
            self.atualizar_status("Registro CSV aberto", 'info')
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir arquivo:\n{str(e)}")
    
    def _on_tab_changed(self, event=None):
        """Chamado quando muda de aba"""
        try:
            aba_atual = self.notebook.index(self.notebook.select())
            
            # Aba 1 = Geração (índice 1)
            if aba_atual == 1:
                # Atualizar lista de pendências no dropdown
                if hasattr(self, 'app_geracao') and self.app_geracao:
                    self.app_geracao._atualizar_lista_pendencias()
            
        except Exception as e:
            print(f"✗ Erro ao trocar aba: {e}")
    
    def _iniciar_auto_refresh(self):
        """Inicia o sistema de auto-refresh"""
        try:
            from monitor_mudancas import MonitorMudancas
            from config_rede import ConfiguracaoRede
            
            # Inicializar monitor
            pasta_registros = ConfiguracaoRede.PASTA_REGISTROS_JSON
            # Por padrão, focar em ATIVAS; arquivadas só serão monitoradas
            # quando o usuário marcar "Mostrar Arquivadas".
            monitorar_arquivadas = False
            if hasattr(self, 'var_mostrar_arquivadas'):
                try:
                    monitorar_arquivadas = bool(self.var_mostrar_arquivadas.get())
                except Exception:
                    monitorar_arquivadas = False
            self.monitor_mudancas = MonitorMudancas(pasta_registros, monitorar_arquivadas=monitorar_arquivadas)
            
            print("✓ Auto-refresh ativado.")
            print("✓ Sincronização multi-usuário ativa.")
            print("✓ Proteção contra edições simultâneas ativa.")
            
            # Agendar primeira verificação
            self._verificar_mudancas_periodicas()
        
        except Exception as e:
            print(f"✗ Erro ao iniciar auto-refresh: {e}")
            self.auto_refresh_ativo = False
    
    def _verificar_mudancas_periodicas(self):
        """Verifica mudanças periodicamente e atualiza interface (OTIMIZADO)"""
        if not self.auto_refresh_ativo:
            return
        
        # OTIMIZAÇÃO: Pular verificação se janela está minimizada ou não está visível
        try:
            if not self.root.winfo_viewable() or self.root.state() == 'iconic':
                # Janela minimizada - reagendar sem verificar
                if self.auto_refresh_ativo:
                    self.timer_refresh = self.root.after(self.intervalo_refresh, self._verificar_mudancas_periodicas)
                return
        except:
            pass  # Continuar mesmo se não conseguir verificar estado
        
        try:
            # Verificar se houve mudanças (monitor otimizado já faz verificação eficiente)
            if self.monitor_mudancas:
                mudancas = self.monitor_mudancas.verificar_mudancas()
                
                if mudancas['qualquer_mudanca']:
                    # Houve mudanças - atualizar interface
                    print(f"✓ Mudanças detectadas - Atualizando interface...")
                    
                    # Invalidar cache de pendências quando há mudanças
                    self._invalidar_cache_pendencias()
                    
                    # Atualizar aba atual
                    aba_atual = self.notebook.index(self.notebook.select())
                    
                    if aba_atual == 0:  # Aba Pendências
                        self.atualizar_pendencias()
                        self._notificar_mudanca("Pendências atualizadas automaticamente")
                    elif aba_atual == 1:  # Aba Estatísticas
                        self.atualizar_estatisticas()
                    
                    self._atualizar_timestamp()
        
        except Exception as e:
            print(f"✗ Erro na verificação de mudanças: {e}")
        
        # Reagendar próxima verificação
        if self.auto_refresh_ativo:
            self.timer_refresh = self.root.after(self.intervalo_refresh, self._verificar_mudancas_periodicas)
    
    def _on_focus_in(self, event=None):
        """Atualiza dados quando janela ganha foco"""
        try:
            # Atualizar apenas se passou mais de 2 segundos desde última atualização
            from datetime import datetime
            
            if self.ultima_atualizacao:
                tempo_decorrido = (datetime.now() - self.ultima_atualizacao).total_seconds()
                if tempo_decorrido < 2:
                    return
            
            # Atualizar aba atual
            aba_atual = self.notebook.index(self.notebook.select())
            
            if aba_atual == 0:  # Pendências
                self.atualizar_pendencias()
            elif aba_atual == 1:  # Estatísticas
                self.atualizar_estatisticas()
            
            self._atualizar_timestamp()
        
        except Exception as e:
            print(f"✗ Erro no refresh ao ganhar foco: {e}")
    
    def _invalidar_cache_pendencias(self):
        """Invalida o cache de pendências, forçando nova leitura"""
        self._cache_pendencias = {}
        self._cache_pendencias_timestamp = None
    
    def _atualizar_timestamp(self):
        """Atualiza timestamp da última atualização"""
        from datetime import datetime
        
        self.ultima_atualizacao = datetime.now()
        
        # Atualizar label de status se existir
        if hasattr(self, 'status_label_ultima_atualizacao'):
            hora = self.ultima_atualizacao.strftime("%H:%M:%S")
            self.status_label_ultima_atualizacao.config(text=f"Última atualização: {hora}")
    
    def _notificar_mudanca(self, mensagem):
        """Mostra notificação breve sobre mudança"""
        self.atualizar_status(f"🔄 {mensagem}", 'info')
    
    def pausar_auto_refresh(self):
        """Pausa o auto-refresh temporariamente"""
        self.auto_refresh_ativo = False
        if self.timer_refresh:
            self.root.after_cancel(self.timer_refresh)
        print("✓ Auto-refresh pausado")
    
    def retomar_auto_refresh(self):
        """Retoma o auto-refresh"""
        if not self.auto_refresh_ativo:
            self.auto_refresh_ativo = True
            self._verificar_mudancas_periodicas()
            print("✓ Auto-refresh retomado")
    
    def atualizar_status(self, mensagem, tipo='info'):
        """Atualiza o status na barra inferior"""
        icones = {
            'sucesso': ('✓', 'green'),
            'erro': ('✗', 'red'),
            'aviso': ('⚠', 'orange'),
            'info': ('ℹ', 'blue'),
            'processando': ('⟳', 'blue')
        }
        
        icone, cor = icones.get(tipo, ('•', 'gray'))
        
        self.status_icone.config(text=icone, foreground=cor)
        self.status_label.config(text=mensagem, foreground=cor)
    
    def _adicionar_indicadores_ordenacao(self):
        """Adiciona indicadores visuais de ordenação nas colunas"""
        # Por enquanto, apenas inicializar - os indicadores serão adicionados dinamicamente
        pass
    
    def _ordenar_por_coluna(self, coluna):
        """Ordena o TreeView pela coluna especificada"""
        print(f"✓ Ordenando por coluna: {coluna}")
        try:
            # Obter todos os itens do TreeView
            items = list(self.tree_pendencias.get_children(''))
            
            if not items:
                return
            
            # Determinar se deve inverter a ordenação
            if self.ordenacao_coluna == coluna:
                self.ordenacao_reversa = not self.ordenacao_reversa
            else:
                self.ordenacao_reversa = False
                self.ordenacao_coluna = coluna
            
            # Função de ordenação baseada no tipo de coluna
            def obter_valor_ordenacao(item):
                valores = self.tree_pendencias.item(item, 'values')
                
                if coluna == 'Pendência':
                    # Ordenar por número da pendência
                    numero = valores[0].replace('#', '')
                    try:
                        return int(numero)
                    except:
                        return 0
                elif coluna == 'Data':
                    # Ordenar por data (formato DD/MM/YYYY)
                    data_str = valores[1]
                    try:
                        from datetime import datetime
                        return datetime.strptime(data_str, '%d/%m/%Y')
                    except:
                        return datetime.min
                elif coluna == 'Hora':
                    # Ordenar por horário (formato HH:MM)
                    horario_str = valores[2]
                    try:
                        from datetime import datetime, time
                        return datetime.strptime(horario_str, '%H:%M').time()
                    except:
                        return time.min
                else:
                    # Ordenar alfabeticamente (Situação)
                    return valores[3] if coluna == 'Situação' else ''
            
            # Ordenar itens
            items_ordenados = sorted(items, key=obter_valor_ordenacao, reverse=self.ordenacao_reversa)
            
            # Reorganizar itens no TreeView de forma mais suave
            # Usar update_idletasks() para evitar piscadas
            self.tree_pendencias.update_idletasks()
            
            for i, item in enumerate(items_ordenados):
                self.tree_pendencias.move(item, '', i)
            
            # Atualizar indicadores visuais
            self._atualizar_indicadores_ordenacao(coluna)
            
        except Exception as e:
            print(f"✗ Erro ao ordenar por {coluna}: {e}")
    
    def _atualizar_indicadores_ordenacao(self, coluna_atual):
        """Atualiza os indicadores visuais de ordenação"""
        try:
            # Limpar indicadores de todas as colunas
            for coluna in ['Pendência', 'Data', 'Hora', 'Situação']:
                texto_base = coluna
                if coluna == coluna_atual:
                    # Adicionar seta indicando direção da ordenação
                    seta = " ↓" if self.ordenacao_reversa else " ↑"
                    texto_base += seta
                
                self.tree_pendencias.heading(coluna, text=texto_base)
        except Exception as e:
            print(f"✗ Erro ao atualizar indicadores: {e}")
    
    def _on_cabecalho_botao_direito(self, event):
        """Remove a ordenação quando clica com botão direito no cabeçalho"""
        try:
            # Verificar se há uma coluna sendo ordenada
            if self.ordenacao_coluna:
                # Remover ordenação
                self.ordenacao_coluna = None
                self.ordenacao_reversa = False
                
                # Atualizar indicadores visuais (remover setas)
                self._atualizar_indicadores_ordenacao(None)
                
                # Recarregar pendências na ordem original
                self.atualizar_pendencias()
                
                print(f"✓ Ordenação removida - voltando à ordem original")
                
        except Exception as e:
            print(f"✗ Erro ao remover ordenação: {e}")
    
    def _ordenar_dados_antes_insercao(self, pendencias, coluna, reversa):
        """Ordena os dados antes de inserir na TreeView para evitar piscadas"""
        try:
            from datetime import datetime
            
            def obter_valor_ordenacao(pend):
                if coluna == 'Pendência':
                    numero = pend.get('numero', '').replace('#', '')
                    try:
                        return int(numero)
                    except:
                        return 0
                elif coluna == 'Data':
                    data_criacao_iso = pend.get('data_criacao', '')
                    if data_criacao_iso:
                        try:
                            return datetime.fromisoformat(data_criacao_iso)
                        except:
                            return datetime.min
                    return datetime.min
                elif coluna == 'Hora':
                    data_criacao_iso = pend.get('data_criacao', '')
                    if data_criacao_iso:
                        try:
                            dt = datetime.fromisoformat(data_criacao_iso)
                            return dt.time()
                        except:
                            return datetime.min.time()
                    return datetime.min.time()
                elif coluna == 'Situação':
                    return pend.get('situacao', '')
                else:
                    return ''
            
            # Ordenar lista de pendências
            return sorted(pendencias, key=obter_valor_ordenacao, reverse=reversa)
            
        except Exception as e:
            print(f"✗ Erro ao ordenar dados antes da inserção: {e}")
            return pendencias
    
    def _detectar_codigo_usuario(self):
        """Detecta o código do usuário atual baseado no nome do computador ou primeiro usuário do CSV"""
        try:
            from mapeamento_usuarios import USUARIOS, obter_usuario_por_nome
            import os
            
            # Se não há usuários carregados, não definir código (sistema não funcionará)
            if not USUARIOS:
                print("❌ ERRO: Nenhum usuário carregado do CSV. Sistema requer DADOS_LOGIN.csv para funcionar.")
                self.codigo_usuario = None
                self.nivel_usuario = None
                return
            
            # Tentar detectar por nome do computador
            nome_computador = os.environ.get('COMPUTERNAME', '').strip()
            if nome_computador:
                for codigo, dados in USUARIOS.items():
                    if dados.get('computador', '').strip().upper() == nome_computador.upper():
                        self.codigo_usuario = codigo
                        self.nivel_usuario = dados.get('nivel', 1)
                        print(f"✓ Usuário detectado: {dados['nome']} (Código {codigo}, Nível {self.nivel_usuario})")
                        return
            
            # Se não encontrou, usar o primeiro usuário do CSV como padrão
            if USUARIOS:
                primeiro_codigo = list(USUARIOS.keys())[0]
                primeiro_usuario = USUARIOS[primeiro_codigo]
                self.codigo_usuario = primeiro_codigo
                self.nivel_usuario = primeiro_usuario.get('nivel', 1)
                print(f"⚠️ Usuário não detectado automaticamente. Usando: {primeiro_usuario['nome']} (Código {primeiro_codigo}, Nível {self.nivel_usuario})")
            else:
                self.codigo_usuario = None
                self.nivel_usuario = None
                
        except Exception as e:
            print(f"❌ Erro ao detectar código do usuário: {e}")
            self.codigo_usuario = None
            self.nivel_usuario = None
    
    def _obter_usuario_ativo(self):
        """Obtém o usuário ativo para usar como filtro padrão"""
        try:
            # Verificar se há usuário detectado
            if hasattr(self, 'usuario_detectado') and self.usuario_detectado:
                nome = self.usuario_detectado.get('nome', '')
                # Atualizar nível do usuário
                if hasattr(self, 'codigo_usuario') and self.codigo_usuario:
                    from mapeamento_usuarios import obter_nivel_usuario
                    self.nivel_usuario = obter_nivel_usuario(self.codigo_usuario)
                return nome
            
            # Se temos código de usuário, buscar nome
            if hasattr(self, 'codigo_usuario') and self.codigo_usuario:
                from mapeamento_usuarios import obter_usuario_por_codigo
                usuario = obter_usuario_por_codigo(self.codigo_usuario)
                if usuario:
                    return usuario.get('nome', '')
            
            # Se temos código de usuário, buscar nome
            if hasattr(self, 'codigo_usuario') and self.codigo_usuario:
                from mapeamento_usuarios import obter_usuario_por_codigo
                usuario = obter_usuario_por_codigo(self.codigo_usuario)
                if usuario:
                    return usuario.get('nome', '')
            
            # Se não encontrou, retornar vazio (não usar fallback hardcoded)
            return ''
        except Exception as e:
            print(f"✗ Erro ao obter usuário ativo: {e}")
            return ''
    
    def _verificar_permissao_visualizar(self, pendencia):
        """Verifica se o usuário pode visualizar uma pendência"""
        try:
            from mapeamento_usuarios import verificar_permissao_visualizar, USUARIOS
            
            # Se não há código de usuário definido, permitir visualização (modo temporário até CSV configurado)
            if not self.codigo_usuario:
                return True
            
            # Se não há usuários carregados, permitir visualização (modo temporário até CSV configurado)
            if not USUARIOS:
                return True
            
            # Se código_usuario não existe no CSV, permitir visualização (modo temporário)
            if self.codigo_usuario not in USUARIOS:
                return True
            
            # Aplicar regras de permissão baseadas no nível do CSV
            return verificar_permissao_visualizar(self.codigo_usuario, pendencia)
        except Exception as e:
            print(f"⚠️ Erro ao verificar permissão de visualização: {e}. Permitindo visualização.")
            return True  # Em caso de erro, permitir visualização (modo temporário)
    
    def _verificar_permissao_criar(self):
        """Verifica se o usuário pode criar pendências"""
        try:
            from mapeamento_usuarios import verificar_permissao_criar, USUARIOS
            
            # Se não há código de usuário ou usuários carregados, negar
            if not self.codigo_usuario or not USUARIOS or self.codigo_usuario not in USUARIOS:
                return False
            
            return verificar_permissao_criar(self.codigo_usuario)
        except Exception as e:
            print(f"❌ Erro ao verificar permissão de criação: {e}")
            return False  # Em caso de erro, negar acesso (mais seguro)
    
    def _verificar_permissao_editar(self, pendencia):
        """Verifica se o usuário pode editar uma pendência"""
        try:
            from mapeamento_usuarios import verificar_permissao_editar, USUARIOS
            
            # Se não há código de usuário ou usuários carregados, negar
            if not self.codigo_usuario or not USUARIOS or self.codigo_usuario not in USUARIOS:
                return False
            
            return verificar_permissao_editar(self.codigo_usuario, pendencia)
        except Exception as e:
            print(f"❌ Erro ao verificar permissão de edição: {e}")
            return False  # Em caso de erro, negar acesso (mais seguro)
    
    def _atualizar_permissoes_botoes(self):
        """Atualiza o estado dos botões baseado no nível do usuário"""
        try:
            from mapeamento_usuarios import USUARIOS, obter_nivel_usuario
            
            # Se não há usuário válido, desabilitar todos os botões
            if not self.codigo_usuario or not USUARIOS or self.codigo_usuario not in USUARIOS:
                if hasattr(self, 'btn_nova_pendencia'):
                    self.btn_nova_pendencia.config(state='disabled')
                if hasattr(self, 'btn_editar'):
                    self.btn_editar.config(state='disabled')
                if hasattr(self, 'btn_atualizar_situacao'):
                    self.btn_atualizar_situacao.config(state='disabled')
                if hasattr(self, 'btn_transferir'):
                    self.btn_transferir.config(state='disabled')
                return
            
            # Atualizar nível do usuário do CSV
            self.nivel_usuario = obter_nivel_usuario(self.codigo_usuario)
            
            # Desabilitar botão criar para níveis 1 e 2
            if hasattr(self, 'btn_nova_pendencia'):
                pode_criar = self._verificar_permissao_criar()
                self.btn_nova_pendencia.config(state='normal' if pode_criar else 'disabled')
            
            # Nível 1 não pode editar nada
            if hasattr(self, 'btn_editar'):
                self.btn_editar.config(state='normal' if self.nivel_usuario and self.nivel_usuario >= 2 else 'disabled')
            
            if hasattr(self, 'btn_atualizar_situacao'):
                self.btn_atualizar_situacao.config(state='normal' if self.nivel_usuario and self.nivel_usuario >= 2 else 'disabled')
            
            # Botão transferir - mesmo nível de permissão que editar
            if hasattr(self, 'btn_transferir'):
                self.btn_transferir.config(state='normal' if self.nivel_usuario and self.nivel_usuario >= 2 else 'disabled')
                
        except Exception as e:
            print(f"❌ Erro ao atualizar permissões dos botões: {e}")
    
    def _recarregar_pendencia_ativa(self):
        """Recarrega os dados da pendência ativa após edição"""
        try:
            if self.pendencia_ativa:
                from gerenciador_pendencias_json import GerenciadorPendenciasJSON
                ger = GerenciadorPendenciasJSON()
                self.pendencia_ativa_dados = ger.ler_pendencia(self.pendencia_ativa)
                print(f"✓ Pendência ativa {self.pendencia_ativa} recarregada")
        except Exception as e:
            print(f"✗ Erro ao recarregar pendência ativa: {e}")
    
    def _atualizar_label_periodo(self):
        """Atualiza o label mostrando o período atual"""
        try:
            from datetime import date
            if hasattr(self, 'semana_inicio') and hasattr(self, 'semana_fim'):
                inicio_str = self.semana_inicio.strftime("%d/%m/%Y")
                fim_str = self.semana_fim.strftime("%d/%m/%Y")
                self.label_periodo.config(text=f"{inicio_str} a {fim_str}")
        except Exception as e:
            print(f"✗ Erro ao atualizar label período: {e}")
    
    def _semana_anterior(self):
        """Navega para semana anterior"""
        try:
            from datetime import timedelta
            # Mover período 7 dias para trás
            self.semana_inicio = self.semana_inicio - timedelta(days=7)
            self.semana_fim = self.semana_fim - timedelta(days=7)
            self._atualizar_label_periodo()
            self.atualizar_pendencias()
            print(f"✓ Navegando para semana anterior: {self.semana_inicio} a {self.semana_fim}")
        except Exception as e:
            print(f"✗ Erro ao navegar semana anterior: {e}")
    
    def _semana_proxima(self):
        """Navega para próxima semana"""
        try:
            from datetime import timedelta, date
            # Mover período 7 dias para frente
            self.semana_inicio = self.semana_inicio + timedelta(days=7)
            self.semana_fim = self.semana_fim + timedelta(days=7)
            
            # Não permitir navegar para futuro além de hoje
            hoje = date.today()
            if self.semana_inicio > hoje:
                self.semana_inicio = hoje - timedelta(days=6)
                self.semana_fim = hoje
                print("⚠️ Não é possível navegar para semanas futuras")
            
            self._atualizar_label_periodo()
            self.atualizar_pendencias()
            print(f"✓ Navegando para próxima semana: {self.semana_inicio} a {self.semana_fim}")
        except Exception as e:
            print(f"✗ Erro ao navegar próxima semana: {e}")
    
    def _carregar_pendencias_inicial(self):
        """Carrega pendências automaticamente ao abrir o programa"""
        try:
            # Garantir que está na semana atual
            from datetime import date, timedelta
            hoje = date.today()
            self.semana_inicio = hoje - timedelta(days=6)  # 7 dias incluindo hoje
            self.semana_fim = hoje
            
            # Atualizar label do período
            if hasattr(self, 'label_periodo'):
                self._atualizar_label_periodo()
            
            # Carregar pendências
            print("✓ Carregando pendências automaticamente ao abrir...")
            self.atualizar_pendencias()
            print(f"✓ Pendências carregadas para período: {self.semana_inicio} a {self.semana_fim}")
        except Exception as e:
            print(f"✗ Erro ao carregar pendências iniciais: {e}")
    
    def _voltar_semana_atual(self):
        """Volta para semana atual (últimos 7 dias)"""
        try:
            from datetime import date, timedelta
            hoje = date.today()
            self.semana_inicio = hoje - timedelta(days=6)  # 7 dias incluindo hoje
            self.semana_fim = hoje
            self._atualizar_label_periodo()
            self.atualizar_pendencias()
            print(f"✓ Voltando para semana atual: {self.semana_inicio} a {self.semana_fim}")
        except Exception as e:
            print(f"✗ Erro ao voltar semana atual: {e}")


def main():
    """Função principal"""
    root = tk.Tk()
    
    def bring_to_front():
        """Traz a janela para frente garantindo visibilidade"""
        root.deiconify()
        root.lift()
        root.focus_force()
        root.attributes('-topmost', True)
        root.after(10, lambda: root.attributes('-topmost', False))
    
    app = InterfacePrincipalAbas(root)
    
    # Garantir que a janela apareça corretamente após inicialização
    root.after(200, bring_to_front)
    
    # Bind para Alt+Tab e foco
    root.bind('<FocusIn>', lambda e: bring_to_front() if e.widget == root else None)
    
    root.mainloop()


if __name__ == "__main__":
    main()

