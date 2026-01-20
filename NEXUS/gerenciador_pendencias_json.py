# -*- coding: utf-8 -*-
import json
from datetime import datetime, time, date
from NEXUS.database import Database

class GerenciadorPendenciasJSON:
    PASTAS_STATUS = {'Ativa': 'Ativa', 'Arquivada': 'Arquivada', 'Fechada': 'Fechada'}
    def __init__(self, pasta_registros=None): pass

    def criar_pendencia(self, cliente='', telefone='', equipamento='', cnpj='', vendedor_manual=None, setor_manual=None, observacoes='', prioridade='normal', prazo_resposta=''):
        try:
            res_u = Database.execute_query("SELECT codigo_usuario FROM nexus.usuarios WHERE nome_usuario = %s", (vendedor_manual,), fetch=True)
            id_usuario = res_u[0]['codigo_usuario'] if res_u else None
            res_s = Database.execute_query("SELECT id_setor FROM nexus.setores WHERE nome_setor = %s", (setor_manual,), fetch=True)
            id_setor = res_s[0]['id_setor'] if res_s else None
            numero = self._gerar_numero_sequencial()
            agora = datetime.now()
            cliente_dict = {"razao_social": cliente, "telefone": telefone, "cnpj": cnpj, "cidade": "", "contato": "", "email": "", "inscricao_estadual": "", "endereco": ""} if isinstance(cliente, str) else cliente
            historico = [{"data": agora.isoformat(), "status_anterior": "", "status_novo": f"Pendência registrada no setor {setor_manual}.", "usuario": vendedor_manual}]
            query = "INSERT INTO nexus.pendencias (numero, data_criacao, data_atualizacao, equipamento, situacao, status, prioridade, prazo_resposta, origem, observacoes, versao, ultima_modificacao, modificado_por, id_usuario, id_setor, cliente, historico, propostas_vinculadas) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            params = (numero, agora, agora, equipamento, "Novo contato", "Ativa", prioridade, int(prazo_resposta) if str(prazo_resposta).isdigit() else None, "manual", observacoes, "1.0", agora, vendedor_manual, id_usuario, id_setor, json.dumps(cliente_dict), json.dumps(historico), json.dumps([]))
            Database.execute_query(query, params)
            return {'numero': numero, 'usuario': vendedor_manual, 'vendedor': vendedor_manual, 'setor': setor_manual, 'data_criacao': agora.isoformat(), 'cliente': cliente_dict, 'situacao': "Novo contato"}
        except Exception as e: return None

    def _gerar_numero_sequencial(self):
        prefixo = datetime.now().strftime("%y%m%d")
        res = Database.execute_query("SELECT COUNT(*) AS total FROM nexus.pendencias WHERE numero LIKE %s", (f"{prefixo}%",), fetch=True)
        return f"{prefixo}{(res[0]['total'] + 1):04d}"

    def ler_pendencia(self, numero):
        query = "SELECT p.*, u.nome_usuario as vendedor, s.nome_setor as setor FROM nexus.pendencias p LEFT JOIN nexus.usuarios u ON u.codigo_usuario = p.id_usuario LEFT JOIN nexus.setores s ON s.id_setor = p.id_setor WHERE p.numero = %s"
        res = Database.execute_query(query, (numero,), fetch=True)
        if res:
            p = dict(res[0])
            for f in ['cliente', 'historico', 'propostas_vinculadas']:
                if f in p and p[f]: p[f] = json.loads(p[f]) if isinstance(p[f], str) else p[f]
            p['usuario'] = p.get('vendedor')
            for k in ['data_criacao', 'data_atualizacao', 'ultima_modificacao']:
                if k in p and p[k] and hasattr(p[k], 'isoformat'): p[k] = p[k].isoformat()
            return p
        return None

    def listar_pendencias(self, filtro_status=None, filtro_situacao=None, filtro_vendedor=None, filtro_setor=None, apenas_ativas=None, data_inicio=None, data_fim=None):
        try:
            query = "SELECT * FROM nexus.v_pendencias_com_detalhes WHERE 1=1"
            params = []
            if filtro_status and filtro_status != 'Todas':
                query += " AND status = %s"; params.append(filtro_status)
            if filtro_situacao and filtro_situacao != 'Todas':
                query += " AND situacao = %s"; params.append(filtro_situacao)
            if filtro_vendedor and filtro_vendedor != 'Todos':
                query += " AND nome_usuario = %s"; params.append(filtro_vendedor)
            if filtro_setor and filtro_setor != 'Todos':
                query += " AND nome_setor = %s"; params.append(filtro_setor)
            if apenas_ativas: query += " AND status = 'Ativa'"
            
            # Tratamento de data simplificado e seguro
            if data_inicio:
                if isinstance(data_inicio, str): data_inicio = datetime.fromisoformat(data_inicio.replace('Z', '+00:00'))
                d_ini = data_inicio if isinstance(data_inicio, datetime) else datetime.combine(data_inicio, time.min)
                query += " AND data_criacao >= %s"; params.append(d_ini)
            if data_fim:
                if isinstance(data_fim, str): data_fim = datetime.fromisoformat(data_fim.replace('Z', '+00:00'))
                d_fim = datetime.combine(data_fim if isinstance(data_fim, date) else data_fim.date(), time(23, 59, 59))
                query += " AND data_criacao <= %s"; params.append(d_fim)

            query += " ORDER BY data_criacao DESC"
            result = Database.execute_query(query, tuple(params) if params else None, fetch=True)
            pendencias = []
            if result:
                for row in result:
                    p = dict(row)
                    p['vendedor'] = p['usuario'] = p.get('nome_usuario', '-')
                    p['setor'] = p.get('nome_setor', '-')
                    for k in ['data_criacao', 'data_atualizacao', 'ultima_modificacao']:
                        if k in p and p[k] and hasattr(p[k], 'isoformat'): p[k] = p[k].isoformat()
                    pendencias.append(p)
            return pendencias
        except Exception as e:
            print(f"DEBUG: Erro ao listar: {e}")
            return []

    def atualizar_pendencia(self, numero, atualizacoes, usuario='Sistema'):
        try:
            campos, params = [], []
            for k, v in atualizacoes.items():
                campos.append(f"{k} = %s")
                params.append(json.dumps(v) if k in ['cliente', 'historico', 'propostas_vinculadas'] else v)
            agora = datetime.now()
            campos.extend(["data_atualizacao = %s", "ultima_modificacao = %s", "modificado_por = %s"])
            params.extend([agora, agora, usuario, numero])
            query = f"UPDATE nexus.pendencias SET {', '.join(campos)} WHERE numero = %s"
            Database.execute_query(query, tuple(params))
            return {"sucesso": True}
        except Exception as e: return {"sucesso": False, "mensagem": str(e)}

    def atualizar_status(self, numero, nova_situacao, observacao='', usuario='Sistema'):
        p = self.ler_pendencia(numero)
        if not p: return False
        h = p.get('historico', [])
        h.append({"data": datetime.now().isoformat(), "status_anterior": p.get('situacao', ''), "status_novo": nova_situacao, "usuario": usuario})
        upd = {'situacao': nova_situacao, 'historico': h}
        if observacao: upd['observacoes'] = f"{p.get('observacoes', '')}\n\n[{datetime.now().strftime('%d/%m/%Y %H:%M')}] {observacao}"
        return self.atualizar_pendencia(numero, upd, usuario).get('sucesso', False)

    def atualizar_observacoes(self, numero, novas_obs, usuario='Sistema'):
        return self.atualizar_pendencia(numero, {'observacoes': novas_obs}, usuario)
