# -*- coding: utf-8 -*-
import psycopg2
from NEXUS.database import Database

def corrigir():
    print("--- TENTANDO CORREÇÃO DIRETA PELO PYTHON ---")
    Database.initialize()
    conn = Database.get_connection()
    
    if not conn:
        print("❌ Erro de conexão.")
        return

    try:
        conn.autocommit = True # Forçar aplicação imediata
        with conn.cursor() as cur:
            print("1. Tentando adicionar coluna 'cliente'...")
            cur.execute("ALTER TABLE nexus.pendencias ADD COLUMN IF NOT EXISTS cliente jsonb DEFAULT '{}';")
            
            print("2. Tentando adicionar coluna 'historico'...")
            cur.execute("ALTER TABLE nexus.pendencias ADD COLUMN IF NOT EXISTS historico jsonb DEFAULT '[]';")
            
            print("3. Verificando colunas agora...")
            cur.execute("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_schema = 'nexus' AND table_name = 'pendencias' 
                AND column_name IN ('cliente', 'historico');
            """)
            colunas = [row[0] for row in cur.fetchall()]
            print(f"✓ Colunas encontradas após tentativa: {colunas}")
            
            if 'cliente' in colunas:
                print("\n✅ SUCESSO! O Python conseguiu criar as colunas.")
                print("Agora você pode rodar o 'iniciar.py'!")
            else:
                print("\n❌ FALHA: O comando rodou mas a coluna ainda não aparece.")
                print("Isso sugere que 'nexus.pendencias' pode ser uma VIEW ou você não tem permissão de ALTER.")

    except Exception as e:
        print(f"❌ ERRO DURANTE A CORREÇÃO: {e}")
    finally:
        Database.return_connection(conn)

if __name__ == "__main__":
    corrigir()
