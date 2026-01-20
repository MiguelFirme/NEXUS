# -*- coding: utf-8 -*-
from NEXUS.database import Database
from NEXUS.gerenciador_pendencias_json import GerenciadorPendenciasJSON

def teste():
    print("--- TESTE DE LEITURA BRUTA ---")
    Database.initialize()
    
    # 1. Teste direto via SQL
    print("\n1. Consultando direto via SQL (SELECT * FROM nexus.pendencias):")
    res = Database.execute_query("SELECT numero, data_criacao, situacao FROM nexus.pendencias", fetch=True)
    if res:
        for row in res:
            print(f"  - Pendência: {row['numero']} | Data: {row['data_criacao']} | Situação: {row['situacao']}")
    else:
        print("  ❌ Nenhuma pendência encontrada na tabela física!")

    # 2. Teste via Gerenciador (Sem filtros)
    print("\n2. Consultando via Gerenciador (Sem filtros):")
    ger = GerenciadorPendenciasJSON()
    lista = ger.listar_pendencias() # Sem passar nenhum argumento
    print(f"✓ O gerenciador retornou {len(lista)} pendências.")

if __name__ == "__main__":
    teste()
