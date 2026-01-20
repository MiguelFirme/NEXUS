# -*- coding: utf-8 -*-
"""
Mapeamento de Usuários e Setores - Versão PostgreSQL
Sistema de Gestão de Pendências - Olivo Guindastes
"""

from collections import defaultdict
from NEXUS.database import Database

# Estruturas de dados mantidas para compatibilidade com a interface
USUARIOS = {}  # {codigo: {'nome': str, 'setor': str, ...}}
SETORES = {}  # {setor: [codigos_usuarios]}
SETOR_PARA_USUARIOS = defaultdict(list)

def _carregar_mapeamento_usuarios():
    """
    Carrega mapeamento de usuários e setores diretamente do PostgreSQL
    """
    global USUARIOS, SETORES, SETOR_PARA_USUARIOS
    
    try:
        # Usar a view que já existe no banco conforme estrutura.sql
        query = "SELECT * FROM nexus.v_usuarios_com_setor"
        usuarios_db = Database.execute_query(query, fetch=True)
        
        if not usuarios_db:
            print("⚠️ Aviso: Nenhum usuário encontrado no banco de dados.")
            return

        # Limpar estruturas atuais
        USUARIOS.clear()
        SETORES.clear()
        SETOR_PARA_USUARIOS.clear()

        for row in usuarios_db:
            codigo = row['codigo_usuario']
            setor = row['nome_setor']
            
            # Preencher dicionário de usuários
            USUARIOS[codigo] = {
                'nome': row['nome_usuario'],
                'setor': setor,
                'email': row['email_usuario'],
                'computador': row['computador_usuario'],
                # Campos adicionais podem ser buscados na tabela original se necessário
            }
            
            # Mapear setores
            if setor:
                if setor not in SETORES:
                    SETORES[setor] = []
                SETORES[setor].append(codigo)
                SETOR_PARA_USUARIOS[setor].append(codigo)
        
        print(f"✓ Mapeamento carregado do Banco: {len(USUARIOS)} usuários, {len(SETORES)} setores")
        
    except Exception as e:
        print(f"❌ ERRO ao carregar mapeamento do Banco de Dados: {e}")
        USUARIOS = {}
        SETORES = {}
        SETOR_PARA_USUARIOS = defaultdict(list)

def validar_dados_usuarios():
    """
    Detecta o computador atual e valida os dados no Banco de Dados
    """
    import os
    
    erros = []
    avisos = []
    codigo_usuario_encontrado = None
    
    if not USUARIOS:
        erros.append("Nenhum usuário carregado do banco de dados.")
        return (False, erros, avisos, None)
    
    nome_computador = os.environ.get('COMPUTERNAME', '').strip()
    if not nome_computador:
        # Fallback para linux/sandbox se necessário
        import socket
        nome_computador = socket.gethostname()
        
    print(f"🔍 Detectando computador: {nome_computador}")
    
    usuario_encontrado = None
    for codigo, dados in USUARIOS.items():
        computador_db = (dados.get('computador') or '').strip().upper()
        if computador_db == nome_computador.upper():
            usuario_encontrado = dados
            codigo_usuario_encontrado = codigo
            print(f"✓ Usuário encontrado: {dados.get('nome')} (Código {codigo})")
            break
    
    if not usuario_encontrado:
        erros.append(f"Computador '{nome_computador}' não vinculado a nenhum usuário no banco.")
        return (False, erros, avisos, None)
    
    return (True, erros, avisos, codigo_usuario_encontrado)

# Carregar dados ao importar
_carregar_mapeamento_usuarios()

def obter_lista_usuarios():
    return [u['nome'] for u in USUARIOS.values()]

def obter_usuarios_por_setor(setor):
    return SETOR_PARA_USUARIOS.get(setor, [])

def obter_lista_setores():
    return list(SETORES.keys())

def obter_usuario_por_codigo(codigo):
    return USUARIOS.get(codigo)

def obter_usuario_por_nome(nome):
    for codigo, dados in USUARIOS.items():
        if dados['nome'] == nome:
            return {'codigo': codigo, **dados}
    return None

def obter_nivel_usuario(codigo_usuario):
    # Como o nível não está na view, podemos buscar se necessário ou assumir padrão
    return 1 

def verificar_permissao_visualizar(codigo_usuario, pendencia):
    usuario = USUARIOS.get(codigo_usuario)
    if not usuario: return False
    # Lógica simplificada para migração
    return True

def verificar_permissao_criar(codigo_usuario):
    usuario = USUARIOS.get(codigo_usuario)
    if not usuario:
        return False
    return True
