# -*- coding: utf-8 -*-
"""
Script de Inicialização
Sistema de Gestão de Pendências e Estatísticas - Olivo Guindastes

Execute este arquivo para iniciar o sistema
"""

import sys
import os
# Ajustar caminho para o diretório do projeto (um nível abaixo deste arquivo)
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJETO_POSSIVEIS = ("NEXUS", "nexus")
_PROJETO_DIR = None

for _nome in _PROJETO_POSSIVEIS:
    _caminho = os.path.join(_BASE_DIR, _nome)
    if os.path.isdir(_caminho):
        _PROJETO_DIR = _caminho
        break

if _PROJETO_DIR:
    if _PROJETO_DIR not in sys.path:
        sys.path.insert(0, _PROJETO_DIR)
    try:
        os.chdir(_PROJETO_DIR)
    except OSError as _erro:
        print(f"⚠️  Não foi possível definir o diretório de trabalho para '{_PROJETO_DIR}': {_erro}")
else:
    print("⚠️  Diretório do projeto 'NEXUS' não encontrado ao lado deste arquivo. Verifique a estrutura de pastas.")

# Configurar encoding UTF-8
if sys.platform == 'win32':
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass


print("\nInicializando sistema...\n")

# VALIDAÇÃO OBRIGATÓRIA: Detectar computador e validar dados do usuário correspondente
def validar_e_carregar_dados():
    """
    Valida os dados do CSV antes de abrir o programa
    Retorna: (sucesso: bool, codigo_usuario: int ou None, dados_usuario: dict ou None)
    """
    import os
    import csv
    from pathlib import Path
    
    try:
        from NEXUS.config_rede import ConfiguracaoRede
        arquivo_usuarios = ConfiguracaoRede.ARQUIVO_USUARIOS
    except:
        arquivo_usuarios = Path(r"Z:\GERENCIAMENTO\DADOS_LOGIN.csv")
    
    erros = []
    avisos = []
    
    # Verificar se arquivo existe
    if not arquivo_usuarios.exists():
        erros.append(f"Arquivo DADOS_LOGIN.csv não encontrado em:\n{arquivo_usuarios}")
        return (False, None, None, erros, avisos)
    
    # Detectar nome do computador atual
    nome_computador = os.environ.get('COMPUTERNAME', '').strip()
    if not nome_computador:
        erros.append("Não foi possível detectar o nome do computador (variável COMPUTERNAME não encontrada)")
        return (False, None, None, erros, avisos)
    
    print(f"🔍 Detectando computador: {nome_computador}")
    
    # Ler CSV e encontrar linha do computador
    try:
        with open(arquivo_usuarios, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            linhas = list(reader)
    except Exception as e:
        erros.append(f"Erro ao ler arquivo CSV:\n{str(e)}")
        return (False, None, None, erros, avisos)
    
    if not linhas:
        erros.append("Arquivo CSV está vazio ou não contém dados")
        return (False, None, None, erros, avisos)
    
    # Procurar linha correspondente ao computador
    linha_encontrada = None
    codigo_usuario = None
    
    for idx, row in enumerate(linhas, start=2):  # start=2 porque linha 1 é cabeçalho
        computador_csv = (row.get('COMPUTADOR_USUARIO', '') or 
                          row.get('(COMPUTADOR_USUARIO)', '')).strip().upper()
        
        if computador_csv == nome_computador.upper():
            linha_encontrada = row
            codigo_str = (row.get('CODIGO_USUARIO', '') or 
                         row.get('(CODIGO_USUARIO)', '')).strip()
            try:
                codigo_usuario = int(codigo_str)
            except:
                erros.append(f"Linha {idx}: CODIGO_USUARIO inválido ou vazio")
            break
    
    if not linha_encontrada:
        erros.append(f"Computador '{nome_computador}' não encontrado no CSV")
        erros.append(f"Verifique se o campo COMPUTADOR_USUARIO corresponde ao nome do seu computador")
        erros.append(f"\nComputadores encontrados no CSV:")
        for idx, row in enumerate(linhas, start=2):
            comp = (row.get('COMPUTADOR_USUARIO', '') or row.get('(COMPUTADOR_USUARIO)', '')).strip()
            if comp:
                erros.append(f"  - Linha {idx}: {comp}")
        return (False, None, None, erros, avisos)
    
    # Validar campos obrigatórios da linha encontrada
    dados_usuario = {}
    
    # CODIGO_USUARIO
    codigo_str = (linha_encontrada.get('CODIGO_USUARIO', '') or 
                 linha_encontrada.get('(CODIGO_USUARIO)', '')).strip()
    if not codigo_str:
        erros.append("CODIGO_USUARIO está vazio")
    else:
        try:
            dados_usuario['codigo'] = int(codigo_str)
        except:
            erros.append(f"CODIGO_USUARIO inválido: '{codigo_str}' (deve ser um número)")
    
    # NOME_USUARIO
    nome = (linha_encontrada.get('NOME_USUARIO', '') or 
           linha_encontrada.get('(NOME_USUARIO)', '')).strip()
    if not nome:
        erros.append("NOME_USUARIO está vazio")
    else:
        dados_usuario['nome'] = nome
    
    # TELEFONE_USUARIO
    telefone = (linha_encontrada.get('TELEFONE_USUARIO', '') or 
               linha_encontrada.get('(TELEFONE_USUARIO)', '')).strip()
    if not telefone:
        erros.append("TELEFONE_USUARIO está vazio")
    else:
        dados_usuario['telefone'] = telefone
    
    # E-MAIL_USUARIO
    email = (linha_encontrada.get('E-MAIL_USUARIO', '') or 
            linha_encontrada.get('(E-MAIL_USUARIO)', '')).strip()
    if not email:
        erros.append("E-MAIL_USUARIO está vazio")
    else:
        dados_usuario['email'] = email
    
    # COMPUTADOR_USUARIO
    computador = (linha_encontrada.get('COMPUTADOR_USUARIO', '') or 
                 linha_encontrada.get('(COMPUTADOR_USUARIO)', '')).strip()
    if not computador:
        erros.append("COMPUTADOR_USUARIO está vazio")
    else:
        dados_usuario['computador'] = computador
    
    # SETOR_USUARIO
    setor = (linha_encontrada.get('SETOR_USUARIO', '') or 
            linha_encontrada.get('(SETOR_USUARIO)', '')).strip()
    if not setor:
        erros.append("SETOR_USUARIO está vazio")
    else:
        dados_usuario['setor'] = setor
    
    # CARGO_USUARIO
    cargo = (linha_encontrada.get('CARGO_USUARIO', '') or 
            linha_encontrada.get('(CARGO_USUARIO)', '') or
            linha_encontrada.get('CARGO', '') or 
            linha_encontrada.get('(CARGO)', '')).strip()
    if not cargo:
        erros.append("CARGO_USUARIO está vazio")
    else:
        dados_usuario['cargo'] = cargo
    
    # NIVEL_USUARIO
    nivel_str = (linha_encontrada.get('NIVEL_USUARIO', '') or 
                linha_encontrada.get('(NIVEL_USUARIO)', '')).strip()
    if not nivel_str:
        erros.append("NIVEL_USUARIO está vazio")
    else:
        try:
            nivel = int(nivel_str)
            if nivel not in [1, 2, 3, 4]:
                erros.append(f"NIVEL_USUARIO inválido: {nivel} (deve ser 1, 2, 3 ou 4)")
            else:
                dados_usuario['nivel'] = nivel
        except ValueError:
            erros.append(f"NIVEL_USUARIO inválido: '{nivel_str}' (deve ser um número entre 1 e 4)")
    
    sucesso = len(erros) == 0
    
    if sucesso:
        print(f"✓ Validação concluída: Todos os campos estão preenchidos corretamente")
        print(f"  - Nome: {dados_usuario.get('nome')}")
        print(f"  - Setor: {dados_usuario.get('setor')}")
        print(f"  - Cargo: {dados_usuario.get('cargo')}")
        print(f"  - Nível: {dados_usuario.get('nivel')}")
    
    return (sucesso, codigo_usuario, dados_usuario, erros, avisos)


def mostrar_erro_validacao(erros, avisos, nome_computador):
    """Mostra janela gráfica com erros de validação"""
    import tkinter as tk
    from tkinter import ttk, scrolledtext
    
    janela_erro = tk.Tk()
    janela_erro.title("❌ Erro de Validação - DADOS_LOGIN.csv")
    janela_erro.geometry("700x600")
    janela_erro.resizable(False, False)
    
    # Centralizar janela
    janela_erro.update_idletasks()
    x = (janela_erro.winfo_screenwidth() // 2) - (700 // 2)
    y = (janela_erro.winfo_screenheight() // 2) - (600 // 2)
    janela_erro.geometry(f"700x600+{x}+{y}")
    
    # Frame principal
    main_frame = ttk.Frame(janela_erro, padding="20")
    main_frame.pack(fill='both', expand=True)
    
    # Título
    titulo = ttk.Label(main_frame, 
                      text="❌ Erro: Dados do CSV inválidos ou incompletos",
                      font=('Arial', 14, 'bold'),
                      foreground='red')
    titulo.pack(pady=(0, 10))
    
    # Informação do computador
    info_comp = ttk.Label(main_frame,
                         text=f"Computador detectado: {nome_computador}",
                         font=('Arial', 10))
    info_comp.pack(pady=(0, 15))
    
    # Área de erros
    ttk.Label(main_frame, text="Erros encontrados:", font=('Arial', 11, 'bold')).pack(anchor='w', pady=(0, 5))
    
    texto_erros = scrolledtext.ScrolledText(main_frame, height=15, width=80, wrap='word', font=('Consolas', 9))
    texto_erros.pack(fill='both', expand=True, pady=(0, 10))
    
    # Preencher erros
    texto_erros.insert('1.0', '\n'.join(f"• {erro}" for erro in erros))
    texto_erros.config(state='disabled')
    
    # Avisos (se houver)
    if avisos:
        ttk.Label(main_frame, text="Avisos:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
        texto_avisos = scrolledtext.ScrolledText(main_frame, height=5, width=80, wrap='word', font=('Consolas', 9))
        texto_avisos.pack(fill='both', expand=True, pady=(0, 10))
        texto_avisos.insert('1.0', '\n'.join(f"⚠ {aviso}" for aviso in avisos))
        texto_avisos.config(state='disabled')
    
    # Informações sobre campos obrigatórios
    frame_info = ttk.LabelFrame(main_frame, text="Campos obrigatórios no CSV", padding="10")
    frame_info.pack(fill='x', pady=(10, 0))
    
    campos_texto = """• (CODIGO_USUARIO) - deve ser um número
• (NOME_USUARIO) - não pode estar vazio
• (TELEFONE_USUARIO) - não pode estar vazio
• (E-MAIL_USUARIO) - não pode estar vazio
• (COMPUTADOR_USUARIO) - deve corresponder ao nome do seu computador
• (SETOR_USUARIO) - não pode estar vazio
• (CARGO_USUARIO) - não pode estar vazio
• (NIVEL_USUARIO) - deve ser 1, 2, 3 ou 4

Nota: Apenas a linha do seu computador precisa estar completa.
      Outras linhas podem ter campos vazios."""
    
    ttk.Label(frame_info, text=campos_texto, font=('Arial', 9), justify='left').pack(anchor='w')
    
    # Botão fechar
    ttk.Button(main_frame, text="Fechar", command=janela_erro.destroy, width=20).pack(pady=(15, 0))
    
    janela_erro.mainloop()


# Executar validação
try:
    print("Validando dados do CSV DADOS_LOGIN.csv...")
    sucesso, codigo_usuario, dados_usuario, erros, avisos = validar_e_carregar_dados()
    
    if not sucesso:
        import os
        nome_computador = os.environ.get('COMPUTERNAME', 'N/A')
        mostrar_erro_validacao(erros, avisos, nome_computador)
        sys.exit(1)
    
    if avisos:
        print("\n⚠️  Avisos:")
        for aviso in avisos:
            print(f"  - {aviso}")
    
    print("✓ Todos os campos obrigatórios do usuário estão preenchidos corretamente\n")
    
except ImportError as e:
    print(f"❌ ERRO: Não foi possível importar módulo de validação: {e}")
    input("\nPressione Enter para sair...")
    sys.exit(1)
except Exception as e:
    print(f"❌ ERRO ao validar dados do CSV: {e}")
    import traceback
    traceback.print_exc()
    input("\nPressione Enter para sair...")
    sys.exit(1)

# Se validação passou, abrir interface com dados validados
try:
    from NEXUS.interface_abas import InterfacePrincipalAbas
    import tkinter as tk
    
    root = tk.Tk()
    # Passar código do usuário e dados validados para a interface
    app = InterfacePrincipalAbas(root, 
                                 codigo_usuario_validado=codigo_usuario,
                                 dados_usuario_validado=dados_usuario)
    
    print("✓ Interface carregada com sucesso!")
 
    root.mainloop()
    
except Exception as e:
    print(f"\n❌ ERRO CRÍTICO: {e}")
    print("\nO sistema não pôde ser iniciado.")
    import traceback
    traceback.print_exc()
    input("\nPressione Enter para sair...")
    sys.exit(1)

