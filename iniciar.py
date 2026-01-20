# -*- coding: utf-8 -*-
"""
Script de Inicialização - Versão PostgreSQL
Sistema NEXUS - Olivo Guindastes
"""

import sys
import os
from pathlib import Path

# Ajustar caminhos
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJETO_DIR = os.path.join(_BASE_DIR, "NEXUS")
if _PROJETO_DIR not in sys.path:
    sys.path.insert(0, _PROJETO_DIR)

def validar_e_carregar_dados():
    """Valida o acesso ao banco e identifica o usuário pelo computador"""
    try:
        from NEXUS.database import Database
        from NEXUS.mapeamento_usuarios import validar_dados_usuarios, USUARIOS
        
        Database.initialize()
        sucesso, erros, avisos, codigo_usuario = validar_dados_usuarios()
        
        if sucesso:
            dados_usuario = USUARIOS.get(codigo_usuario)
            # Adaptar para o formato esperado pela interface
            dados_usuario_formatado = {
                'codigo': codigo_usuario,
                'nome': dados_usuario['nome'],
                'setor': dados_usuario['setor'],
                'computador': dados_usuario['computador'],
                'nivel': 1 # Padrão
            }
            return (True, codigo_usuario, dados_usuario_formatado, [], [])
        else:
            return (False, None, None, erros, avisos)
            
    except Exception as e:
        return (False, None, None, [f"Erro na conexão com o banco: {e}"], [])

if __name__ == "__main__":
    print("\nInicializando NEXUS (PostgreSQL)...\n")
    
    sucesso, codigo, dados, erros, avisos = validar_e_carregar_dados()
    
    if not sucesso:
        print("❌ ERRO DE INICIALIZAÇÃO:")
        for erro in erros: print(f"  - {erro}")
        sys.exit(1)
        
    try:
        from NEXUS.interface_abas import InterfacePrincipalAbas
        import tkinter as tk
        
        root = tk.Tk()
        app = InterfacePrincipalAbas(root, 
                                     codigo_usuario_validado=codigo,
                                     dados_usuario_validado=dados)
        print("✓ Sistema iniciado com sucesso!")
        root.mainloop()
    except Exception as e:
        print(f"❌ Erro ao abrir interface: {e}")
        sys.exit(1)
