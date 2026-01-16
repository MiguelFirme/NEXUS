# -*- coding: utf-8 -*-
"""
Mapeamento de Usuários e Setores
Sistema de Gestão de Pendências - Olivo Guindastes

Módulo responsável por gerenciar usuários, setores e distribuição de pendências
"""

import csv
from pathlib import Path
from collections import defaultdict

# Estruturas de dados
USUARIOS = {}  # {codigo: {'nome': str, 'setor': str, 'telefone': str, 'email': str, 'computador': str, 'cargo': str, 'nivel': int}}
SETORES = {}  # {setor: [codigos_usuarios]}
SETOR_PARA_USUARIOS = defaultdict(list)  # {setor: [codigos]}


def _carregar_mapeamento_usuarios():
    """
    Carrega mapeamento de usuários e setores do CSV centralizado
    """
    global USUARIOS, SETORES, SETOR_PARA_USUARIOS
    
    try:
        from .config_rede import ConfiguracaoRede
        arquivo_usuarios = ConfiguracaoRede.ARQUIVO_USUARIOS
    except:
        try:
            from config_rede import ConfiguracaoRede
            arquivo_usuarios = ConfiguracaoRede.ARQUIVO_USUARIOS
        except:
            # Fallback para caminho direto
            arquivo_usuarios = Path(r"Z:\GERENCIAMENTO\DADOS_LOGIN.csv")
    
    if not arquivo_usuarios.exists():
        print(f"❌ ERRO: Arquivo DADOS_LOGIN.csv não encontrado em: {arquivo_usuarios}")
        print("O sistema requer o arquivo CSV para funcionar. Verifique o caminho em config_rede.py")
        USUARIOS = {}
        SETORES = {}
        SETOR_PARA_USUARIOS = defaultdict(list)
        return
    
    try:
        with open(arquivo_usuarios, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            
            for row in reader:
                # Obter dados do usuário
                codigo_str = (row.get('CODIGO_USUARIO', '') or 
                             row.get('(CODIGO_USUARIO)', '')).strip()
                if not codigo_str:
                    continue
                    
                codigo = int(codigo_str)
                
                # Ler dados do usuário
                nome = (row.get('NOME_USUARIO', '') or 
                       row.get('(NOME_USUARIO)', '')).strip()
                
                telefone = (row.get('TELEFONE_USUARIO', '') or 
                           row.get('(TELEFONE_USUARIO)', '')).strip()
                
                email = (row.get('E-MAIL_USUARIO', '') or 
                        row.get('(E-MAIL_USUARIO)', '')).strip()
                
                computador = (row.get('COMPUTADOR_USUARIO', '') or 
                             row.get('(COMPUTADOR_USUARIO)', '') or
                             row.get('COMPUTADOR', '') or 
                             row.get('(COMPUTADOR)', '')).strip()
                
                setor = (row.get('SETOR_USUARIO', '') or 
                        row.get('(SETOR_USUARIO)', '')).strip()
                
                cargo = (row.get('CARGO_USUARIO', '') or 
                        row.get('(CARGO_USUARIO)', '') or
                        row.get('CARGO', '') or 
                        row.get('(CARGO)', '')).strip()
                
                nivel_str = (row.get('NIVEL_USUARIO', '') or 
                            row.get('(NIVEL_USUARIO)', '')).strip()
                try:
                    nivel = int(nivel_str) if nivel_str else None
                except ValueError:
                    nivel = None
                
                # Adicionar usuário
                USUARIOS[codigo] = {
                    'nome': nome,
                    'setor': setor,
                    'telefone': telefone,
                    'email': email,
                    'computador': computador,
                    'cargo': cargo,
                    'nivel': nivel
                }
                
                # Mapear setor
                if setor:
                    if setor not in SETORES:
                        SETORES[setor] = []
                    SETORES[setor].append(codigo)
                    SETOR_PARA_USUARIOS[setor].append(codigo)
        
        print(f"✓ Mapeamento carregado: {len(USUARIOS)} usuarios, {len(SETORES)} setores")
        
    except Exception as e:
        print(f"❌ ERRO ao carregar mapeamento do CSV: {e}")
        print(f"Arquivo esperado: {arquivo_usuarios}")
        print("O sistema requer o arquivo CSV para funcionar corretamente.")
        USUARIOS = {}
        SETORES = {}
        SETOR_PARA_USUARIOS = defaultdict(list)
        raise  # Re-raise para que a validação detecte o erro


def validar_dados_usuarios():
    """
    Detecta o computador atual e valida apenas os dados do usuário correspondente no CSV
    
    Returns:
        tuple: (sucesso: bool, erros: list, avisos: list, codigo_usuario: int ou None)
    """
    import os
    
    erros = []
    avisos = []
    codigo_usuario_encontrado = None
    
    # Verificar se há usuários carregados
    if not USUARIOS or len(USUARIOS) == 0:
        erros.append("Nenhum usuário encontrado no CSV DADOS_LOGIN.csv")
        return (False, erros, avisos, None)
    
    # Detectar nome do computador atual
    nome_computador = os.environ.get('COMPUTERNAME', '').strip()
    if not nome_computador:
        erros.append("Não foi possível detectar o nome do computador (variável COMPUTERNAME não encontrada)")
        return (False, erros, avisos, None)
    
    print(f"🔍 Detectando computador: {nome_computador}")
    
    # Procurar usuário correspondente ao computador
    usuario_encontrado = None
    for codigo, dados in USUARIOS.items():
        computador_csv = dados.get('computador', '').strip().upper()
        if computador_csv == nome_computador.upper():
            usuario_encontrado = dados
            codigo_usuario_encontrado = codigo
            print(f"✓ Usuário encontrado: {dados.get('nome', 'N/A')} (Código {codigo})")
            break
    
    if not usuario_encontrado:
        erros.append(f"Computador '{nome_computador}' não encontrado no CSV DADOS_LOGIN.csv")
        erros.append("Verifique se o campo COMPUTADOR_USUARIO corresponde ao nome do seu computador")
        return (False, erros, avisos, None)
    
    # Validar APENAS o usuário encontrado
    dados = usuario_encontrado
    
    # Verificar cada campo obrigatório
    if not dados.get('nome') or not dados['nome'].strip():
        erros.append(f"NOME_USUARIO está vazio para o computador '{nome_computador}'")
    
    if not dados.get('telefone') or not dados['telefone'].strip():
        erros.append(f"TELEFONE_USUARIO está vazio para o computador '{nome_computador}'")
    
    if not dados.get('email') or not dados['email'].strip():
        erros.append(f"E-MAIL_USUARIO está vazio para o computador '{nome_computador}'")
    
    if not dados.get('computador') or not dados['computador'].strip():
        erros.append(f"COMPUTADOR_USUARIO está vazio para o computador '{nome_computador}'")
    
    if not dados.get('setor') or not dados['setor'].strip():
        erros.append(f"SETOR_USUARIO está vazio para o computador '{nome_computador}'")
    
    if not dados.get('cargo') or not dados['cargo'].strip():
        erros.append(f"CARGO_USUARIO está vazio para o computador '{nome_computador}'")
    
    if dados.get('nivel') is None:
        erros.append(f"NIVEL_USUARIO está vazio ou inválido para o computador '{nome_computador}'")
    else:
        nivel = dados.get('nivel')
        if nivel not in [1, 2, 3, 4]:
            erros.append(f"NIVEL_USUARIO deve ser 1, 2, 3 ou 4 (encontrado: {nivel}) para o computador '{nome_computador}'")
    
    sucesso = len(erros) == 0
    
    if sucesso:
        print(f"✓ Validação concluída: Todos os campos do usuário estão preenchidos corretamente")
        print(f"  - Nome: {dados.get('nome')}")
        print(f"  - Setor: {dados.get('setor')}")
        print(f"  - Cargo: {dados.get('cargo')}")
        print(f"  - Nível: {dados.get('nivel')}")
    
    return (sucesso, erros, avisos, codigo_usuario_encontrado)


# Carregar mapeamento ao importar módulo
# TODOS OS DADOS VÊM DO CSV - NÃO HÁ DADOS HARDCODED
_carregar_mapeamento_usuarios()


def obter_lista_usuarios():
    """
    Retorna lista de nomes dos usuários disponíveis
    
    Returns:
        list: Lista com nomes dos usuários
    """
    return [usuario['nome'] for usuario in USUARIOS.values()]


def obter_usuarios_por_setor(setor):
    """
    Retorna lista de códigos de usuários de um setor específico
    
    Args:
        setor: Nome do setor
        
    Returns:
        list: Lista de códigos de usuários
    """
    return SETOR_PARA_USUARIOS.get(setor, [])


def obter_lista_setores():
    """
    Retorna lista de setores disponíveis
    
    Returns:
        list: Lista com nomes dos setores
    """
    return list(SETORES.keys())


def obter_usuario_por_codigo(codigo):
    """
    Retorna informações de um usuário pelo código
    
    Args:
        codigo: Código do usuário
        
    Returns:
        dict: {'nome': str, 'setor': str, 'telefone': str, 'email': str, 'computador': str, 'cargo': str, 'nivel': int} ou None
    """
    return USUARIOS.get(codigo)


def obter_usuario_por_nome(nome):
    """
    Retorna informações de um usuário pelo nome
    
    Args:
        nome: Nome do usuário
        
    Returns:
        dict: {'codigo': int, 'nome': str, 'setor': str, 'cargo': str, 'nivel': int, ...} ou None
    """
    for codigo, dados in USUARIOS.items():
        if dados['nome'] == nome:
            return {'codigo': codigo, **dados}
    return None


def obter_nivel_usuario(codigo_usuario):
    """
    Retorna o nível de um usuário
    
    Args:
        codigo_usuario: Código do usuário
        
    Returns:
        int: Nível do usuário (1-4) ou 1 se não encontrado
    """
    usuario = USUARIOS.get(codigo_usuario)
    if usuario:
        return usuario.get('nivel', 1)
    return 1


def verificar_permissao_visualizar(codigo_usuario, pendencia):
    """
    Verifica se o usuário pode visualizar uma pendência
    
    Args:
        codigo_usuario: Código do usuário
        pendencia: Dict com dados da pendência (deve ter 'usuario' e 'setor')
        
    Returns:
        bool: True se pode visualizar
    """
    usuario = USUARIOS.get(codigo_usuario)
    if not usuario:
        return False
    
    nivel = usuario.get('nivel', 1)
    usuario_nome = usuario.get('nome', '')
    usuario_setor = usuario.get('setor', '')
    # Suportar tanto 'usuario' (canônico) quanto 'vendedor' (compatibilidade)
    pendencia_usuario = pendencia.get('usuario') or pendencia.get('vendedor', '')
    pendencia_setor = pendencia.get('setor', '')
    
    if nivel == 1:
        # Nível 1: apenas pendências do próprio usuário
        return pendencia_usuario == usuario_nome
    elif nivel == 2:
        # Nível 2: apenas pendências do próprio usuário
        return pendencia_usuario == usuario_nome
    elif nivel == 3:
        # Nível 3: pendências do setor
        return pendencia_setor == usuario_setor
    elif nivel == 4:
        # Nível 4: todas as pendências
        return True
    
    return False


def verificar_permissao_criar(codigo_usuario):
    """
    Verifica se o usuário pode criar pendências
    
    Args:
        codigo_usuario: Código do usuário
        
    Returns:
        bool: True se pode criar (níveis 3 e 4)
    """
    nivel = obter_nivel_usuario(codigo_usuario)
    return nivel >= 3


def verificar_permissao_editar(codigo_usuario, pendencia):
    """
    Verifica se o usuário pode editar uma pendência
    
    Args:
        codigo_usuario: Código do usuário
        pendencia: Dict com dados da pendência
        
    Returns:
        bool: True se pode editar
    """
    nivel = obter_nivel_usuario(codigo_usuario)
    
    if nivel == 1:
        # Nível 1: não pode editar
        return False
    elif nivel == 2:
        # Nível 2: pode editar apenas suas próprias pendências
        usuario = USUARIOS.get(codigo_usuario)
        if not usuario:
            return False
        # Suportar tanto 'usuario' (canônico) quanto 'vendedor' (compatibilidade)
        pendencia_usuario = pendencia.get('usuario') or pendencia.get('vendedor', '')
        return pendencia_usuario == usuario.get('nome', '')
    elif nivel == 3:
        # Nível 3: pode editar pendências do setor
        usuario = USUARIOS.get(codigo_usuario)
        if not usuario:
            return False
        return pendencia.get('setor', '') == usuario.get('setor', '')
    elif nivel == 4:
        # Nível 4: pode editar tudo
        return True
    
    return False


def distribuir_pendencia_por_setor(setor_desejado=None):
    """
    Distribui uma pendência para um setor específico ou roteiriza automaticamente
    
    Args:
        setor_desejado: Setor específico (opcional). Se None, usa roteirização automática
        
    Returns:
        dict: {'codigo': int, 'nome': str, 'setor': str} ou None
    """
    if setor_desejado:
        # Buscar usuários do setor específico
        usuarios_setor = obter_usuarios_por_setor(setor_desejado)
        if usuarios_setor:
            # Por enquanto, retorna o primeiro usuário do setor
            # TODO: Implementar roteirização inteligente (round-robin, carga de trabalho, etc.)
            codigo = usuarios_setor[0]
            usuario = obter_usuario_por_codigo(codigo)
            if usuario:
                return {'codigo': codigo, 'nome': usuario['nome'], 'setor': usuario['setor']}
    
    # Roteirização automática: usar o primeiro setor disponível no CSV
    if SETORES:
        setor_padrao = list(SETORES.keys())[0]  # Primeiro setor encontrado no CSV
        usuarios_setor = obter_usuarios_por_setor(setor_padrao)
        if usuarios_setor:
            codigo = usuarios_setor[0]
            usuario = obter_usuario_por_codigo(codigo)
            if usuario:
                return {'codigo': codigo, 'nome': usuario['nome'], 'setor': usuario['setor']}
    
    return None


def obter_setor_por_usuario(codigo_usuario):
    """
    Retorna o setor de um usuário
    
    Args:
        codigo_usuario: Código do usuário
        
    Returns:
        str: Nome do setor ou None
    """
    usuario = USUARIOS.get(codigo_usuario)
    if usuario:
        return usuario.get('setor')
    return None


# Funções de compatibilidade (para transição gradual)
def detectar_usuario_por_telefone(telefone):
    """
    DEPRECATED: Função mantida para compatibilidade
    Agora distribui pendências por setor, não por DDD/UF
    
    Args:
        telefone: String com telefone (não usado mais, mantido para compatibilidade)
        
    Returns:
        dict: {'codigo': int, 'nome': str, 'setor': str} ou None
    """
    # Distribui para o primeiro setor disponível no CSV
    if SETORES:
        primeiro_setor = list(SETORES.keys())[0]
        return distribuir_pendencia_por_setor(primeiro_setor)
    return None


# Testes (executar apenas se chamado diretamente)
if __name__ == '__main__':
    print("🔍 Teste de Mapeamento de Usuários e Setores\n")
    print(f"Total de usuários: {len(USUARIOS)}")
    print(f"Total de setores: {len(SETORES)}\n")
    
    print("📋 Usuários por Setor:\n")
    for setor, codigos in SETORES.items():
        print(f"{setor}:")
        for codigo in codigos:
            usuario = USUARIOS[codigo]
            print(f"  - {usuario['nome']} (Código {codigo})")
        print()
    
    print("\n" + "="*70)
    print("\n🔍 Teste de Distribuição de Pendências:\n")
    
    # Teste de distribuição por setor
    setores_teste = ['COMERCIAL GUINDASTES', 'ENGENHARIA GUINDASTES', 'ENGENHARIA IMPLEMENTOS']
    for setor in setores_teste:
        resultado = distribuir_pendencia_por_setor(setor)
        if resultado:
            print(f"Setor: {setor} → Usuário: {resultado['nome']} (Código {resultado['codigo']})")
        else:
            print(f"Setor: {setor} → ❌ Nenhum usuário encontrado")
