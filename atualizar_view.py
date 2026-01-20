# -*- coding: utf-8 -*-
import psycopg2
from NEXUS.database import Database

def atualizar_view():
    print("--- ATUALIZANDO VIEW DE PENDÊNCIAS ---")
    Database.initialize()
    conn = Database.get_connection()
    
    if not conn:
        print("❌ Erro de conexão.")
        return

    try:
        conn.autocommit = True
        with conn.cursor() as cur:
            print("1. Recriando a View nexus.v_pendencias_com_detalhes...")
            # Drop view se existir para garantir a nova estrutura
            cur.execute("DROP VIEW IF EXISTS nexus.v_pendencias_com_detalhes CASCADE;")
            
            # Criar a view com todos os campos necessários para a listagem
            cur.execute("""
                CREATE VIEW nexus.v_pendencias_com_detalhes AS
                SELECT 
                    p.id,
                    p.numero,
                    p.situacao,
                    p.status,
                    p.prioridade,
                    u.nome_usuario,
                    s.nome_setor,
                    p.data_criacao,
                    p.data_atualizacao,
                    p.ultima_modificacao,
                    p.equipamento,
                    p.observacoes
                FROM nexus.pendencias p
                LEFT JOIN nexus.usuarios u ON u.codigo_usuario = p.id_usuario
                LEFT JOIN nexus.setores s ON s.id_setor = p.id_setor;
            """)
            
            print("2. Verificando se a view está retornando dados...")
            cur.execute("SELECT COUNT(*) FROM nexus.v_pendencias_com_detalhes;")
            total = cur.fetchone()[0]
            print(f"✓ Total de pendências visíveis na View: {total}")
            
            if total > 0:
                print("\n✅ VIEW ATUALIZADA COM SUCESSO!")
            else:
                print("\n⚠️ A View foi criada, mas o banco parece não ter pendências registradas ainda.")

    except Exception as e:
        print(f"❌ ERRO AO ATUALIZAR VIEW: {e}")
    finally:
        Database.return_connection(conn)

if __name__ == "__main__":
    atualizar_view()
