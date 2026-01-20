# -*- coding: utf-8 -*-
import psycopg2
from NEXUS.database import Database

def diagnosticar():
    print("--- DIAGNÓSTICO DE CONEXÃO NEXUS ---")
    Database.initialize()
    conn = Database.get_connection()
    
    if not conn:
        print("❌ Não foi possível conectar ao banco através do Database.py")
        return

    try:
        with conn.cursor() as cur:
            # 1. Verificar em qual banco estamos
            cur.execute("SELECT current_database(), current_user, current_schema();")
            db, user, schema = cur.fetchone()
            print(f"✓ Conectado ao Banco: {db}")
            print(f"✓ Usuário: {user}")
            print(f"✓ Schema Atual: {schema}")

            # 2. Verificar se a tabela existe no schema nexus
            cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'nexus' AND table_name = 'pendencias');")
            existe = cur.fetchone()[0]
            print(f"✓ Tabela nexus.pendencias existe? {'SIM' if existe else 'NÃO'}")

            # 3. Listar colunas da tabela pendencias
            print("\n--- Colunas encontradas na tabela nexus.pendencias ---")
            cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_schema = 'nexus' AND table_name = 'pendencias'
                ORDER BY column_name;
            """)
            columns = cur.fetchall()
            found_cliente = False
            for col in columns:
                print(f"  - {col[0]} ({col[1]})")
                if col[0] == 'cliente': found_cliente = True
            
            if not found_cliente:
                print("\n❌ A COLUNA 'cliente' REALMENTE NÃO FOI ENCONTRADA PELO PYTHON.")
                print("DICA: Verifique se você não criou a coluna em outro banco de dados por engano no pgAdmin.")
            else:
                print("\n✅ A COLUNA 'cliente' EXISTE! O erro pode ser de cache ou permissão.")

    except Exception as e:
        print(f"❌ Erro durante diagnóstico: {e}")
    finally:
        Database.return_connection(conn)

if __name__ == "__main__":
    diagnosticar()
