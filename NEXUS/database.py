# -*- coding: utf-8 -*-
"""
Módulo de Conexão com Banco de Dados PostgreSQL
Sistema NEXUS - Olivo Guindastes
"""

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import os

class Database:
    _connection_pool = None

    @classmethod
    def initialize(cls):
        """Inicializa o pool de conexões"""
        if cls._connection_pool is None:
            try:
                # Configurações do banco (ajuste conforme necessário)
                cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                    1, 10,
                    user="postgres",
                    password="2696", # O usuário deve configurar a senha
                    host="localhost",
                    port="5432",
                    database="Nexus_DB"
                )
                print("✓ Pool de conexões PostgreSQL inicializado.")
            except Exception as e:
                print(f"❌ Erro ao inicializar pool de conexões: {e}")
                cls._connection_pool = None

    @classmethod
    def get_connection(cls):
        if cls._connection_pool is None:
            cls.initialize()
        if cls._connection_pool:
            return cls._connection_pool.getconn()
        return None

    @classmethod
    def return_connection(cls, conn):
        if cls._connection_pool and conn:
            cls._connection_pool.putconn(conn)

    @classmethod
    def execute_query(cls, query, params=None, fetch=False):
        """Executa uma query e retorna resultados se fetch=True"""
        conn = cls.get_connection()
        if not conn:
            return None
        
        result = None
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if fetch:
                    result = cur.fetchall()
                conn.commit()
        except Exception as e:
            print(f"❌ Erro na query: {e}")
            conn.rollback()
        finally:
            cls.return_connection(conn)
        return result
