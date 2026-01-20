# -*- coding: utf-8 -*-
"""
Script de Migração: CSV -> PostgreSQL
Sistema NEXUS - Olivo Guindastes
"""

import csv
import json
from pathlib import Path
from datetime import datetime
from database import Database

def migrar_usuarios_e_setores():
    print("Iniciando migração de usuários e setores...")
    
    # Caminho do CSV (ajustado para a estrutura do projeto)
    csv_path = Path(__file__).parent.parent / "GERENCIAMENTO" / "DADOS_LOGIN.csv"
    
    if not csv_path.exists():
        print(f"❌ Arquivo {csv_path} não encontrado.")
        return

    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            
            for row in reader:
                # Extrair dados
                codigo = int((row.get('CODIGO_USUARIO', '') or row.get('(CODIGO_USUARIO)', '')).strip())
                nome = (row.get('NOME_USUARIO', '') or row.get('(NOME_USUARIO)', '')).strip()
                telefone = (row.get('TELEFONE_USUARIO', '') or row.get('(TELEFONE_USUARIO)', '')).strip()
                email = (row.get('E-MAIL_USUARIO', '') or row.get('(E-MAIL_USUARIO)', '')).strip()
                computador = (row.get('COMPUTADOR_USUARIO', '') or row.get('(COMPUTADOR_USUARIO)', '')).strip()
                setor_nome = (row.get('SETOR_USUARIO', '') or row.get('(SETOR_USUARIO)', '')).strip()
                cargo = (row.get('CARGO_USUARIO', '') or row.get('(CARGO_USUARIO)', '')).strip()
                nivel = int((row.get('NIVEL_USUARIO', '') or row.get('(NIVEL_USUARIO)', '')).strip())

                # 1. Garantir que o setor existe e pegar o ID
                Database.execute_query(
                    "INSERT INTO nexus.setores (nome_setor) VALUES (%s) ON CONFLICT (nome_setor) DO NOTHING",
                    (setor_nome,)
                )
                res_setor = Database.execute_query(
                    "SELECT id_setor FROM nexus.setores WHERE nome_setor = %s",
                    (setor_nome,), fetch=True
                )
                id_setor = res_setor[0]['id_setor'] if res_setor else None

                # 2. Inserir usuário
                Database.execute_query(
                    """
                    INSERT INTO nexus.usuarios 
                    (codigo_usuario, nome_usuario, telefone_usuario, email_usuario, computador_usuario, cargo_usuario, nivel_usuario, id_setor)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (codigo_usuario) DO UPDATE SET
                    nome_usuario = EXCLUDED.nome_usuario,
                    id_setor = EXCLUDED.id_setor
                    """,
                    (codigo, nome, telefone, email, computador, cargo, nivel, id_setor)
                )
        print("✓ Migração de usuários e setores concluída.")
    except Exception as e:
        print(f"❌ Erro na migração de usuários: {e}")

def migrar_pendencias_json():
    print("Iniciando migração de pendências (JSON)...")
    
    base_path = Path(__file__).parent.parent / "GERENCIAMENTO" / "PENDENCIAS"
    pastas = ["ATIVAS", "ARQUIVADAS", "CANCELADAS", "CONCLUÍDAS", "EM ATRASO"]
    
    count = 0
    for pasta in pastas:
        folder_path = base_path / pasta
        if not folder_path.exists():
            continue
            
        for json_file in folder_path.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Buscar IDs de usuário e setor pelo nome
                res_u = Database.execute_query("SELECT codigo_usuario FROM nexus.usuarios WHERE nome_usuario = %s", (data['usuario'],), fetch=True)
                id_usuario = res_u[0]['codigo_usuario'] if res_u else None
                
                res_s = Database.execute_query("SELECT id_setor FROM nexus.setores WHERE nome_setor = %s", (data['setor'],), fetch=True)
                id_setor = res_s[0]['id_setor'] if res_s else None

                # Inserir pendência
                Database.execute_query(
                    """
                    INSERT INTO nexus.pendencias 
                    (numero, data_criacao, data_atualizacao, equipamento, situacao, status, prioridade, prazo_resposta, 
                     origem, observacoes, versao, ultima_modificacao, modificado_por, id_usuario, id_setor,
                     cliente, historico, propostas_vinculadas)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (numero) DO NOTHING
                    """,
                    (
                        data['numero'],
                        data['data_criacao'],
                        data['data_atualizacao'],
                        data['equipamento'],
                        data['situacao'],
                        data['status'],
                        data['prioridade'],
                        int(data['prazo_resposta']) if data['prazo_resposta'] and str(data['prazo_resposta']).isdigit() else None,
                        data['origem'],
                        data['observacoes'],
                        data.get('metadata', {}).get('versao', '1.0'),
                        data.get('metadata', {}).get('ultima_modificacao'),
                        data.get('metadata', {}).get('modificado_por'),
                        id_usuario,
                        id_setor,
                        json.dumps(data.get('cliente', {})),
                        json.dumps(data.get('historico', [])),
                        json.dumps(data.get('propostas_vinculadas', []))
                    )
                )
                count += 1
            except Exception as e:
                print(f"❌ Erro ao migrar pendência {json_file.name}: {e}")
                
    print(f"✓ Migração de {count} pendências concluída.")

if __name__ == "__main__":
    Database.initialize()
    migrar_usuarios_e_setores()
    migrar_pendencias_json()
