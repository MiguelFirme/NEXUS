# -*- coding: utf-8 -*-
"""
Gerenciador de Pendências com Arquivos JSON Individuais
Sistema de Propostas Comerciais - Olivo Guindastes

Cada pendência é um arquivo JSON separado, permitindo:
- Histórico rico de alterações
- Anexos e observações ilimitadas
- Flexibilidade para novos campos
- Versionamento individual
"""

import json
import os
from pathlib import Path
from datetime import datetime


class GerenciadorPendenciasJSON:
    """Gerencia pendências usando arquivos JSON individuais"""
    
    # Pastas de status disponíveis
    PASTAS_STATUS = ["ATIVAS", "ARQUIVADAS", "CANCELADAS", "CONCLUÍDAS", "EM ATRASO"]
    
    def __init__(self, pasta_registros=None):
        """
        Inicializa o gerenciador de pendências JSON
        
        Args:
            pasta_registros: Caminho da pasta de pendências (None = usar rede)
        """
        if pasta_registros is None:
            # Usar pasta centralizada
            try:
                from config_rede import ConfiguracaoRede
                self.pasta_registros = ConfiguracaoRede.PASTA_REGISTROS_JSON
            except:
                # Fallback para pasta local relativa
                _BASE_DIR = Path(__file__).parent.parent
                self.pasta_registros = _BASE_DIR / "GERENCIAMENTO" / "PENDENCIAS"
        else:
            self.pasta_registros = Path(pasta_registros)
        
        # Criar estrutura de pastas
        self._inicializar_estrutura()
    
    def _inicializar_estrutura(self):
        """Cria a estrutura de pastas necessária"""
        try:
            self.pasta_registros.mkdir(parents=True, exist_ok=True)
            
            # Subpastas por status
            for pasta_status in self.PASTAS_STATUS:
                (self.pasta_registros / pasta_status).mkdir(exist_ok=True)
            
            # Log detalhado removido para evitar poluir o console a cada refresh
        except Exception as e:
            print(f"⚠️ Erro ao criar estrutura: {e}")
    
    def criar_pendencia(self, cliente='', telefone='', equipamento='', cnpj='', vendedor_manual=None,
                        setor_manual=None, observacoes='', inscricao='', endereco='', 
                        prioridade='normal', prazo_resposta=''):
        """
        Cria uma nova pendência com arquivo JSON individual
        
        Args:
            cliente: Nome/Razão social do cliente (opcional, mantido para compatibilidade)
            telefone: Telefone do cliente (opcional, mantido para compatibilidade)
            equipamento: Código do equipamento desejado (opcional)
            cnpj: CNPJ do cliente (opcional)
            vendedor_manual: Usuário selecionado manualmente (OBRIGATÓRIO) - mantido para compatibilidade
            setor_manual: Setor selecionado manualmente (OBRIGATÓRIO)
            observacoes: Observações adicionais (opcional)
            inscricao: Inscrição estadual (opcional)
            endereco: Endereço / cidade (opcional)
            prioridade: Prioridade da pendência ('baixa', 'normal', 'alta') - padrão: 'normal'
            prazo_resposta: Prazo para resolução em dias (opcional)
            
        Returns:
            dict: {'numero': str, 'usuario': str, 'setor': str, 'arquivo': Path}
        """
        try:
            # Validar usuário e setor obrigatórios
            if not vendedor_manual or not vendedor_manual.strip():
                print("❌ Usuário responsável é obrigatório")
                return None
            
            if not setor_manual or not setor_manual.strip():
                print("❌ Setor responsável é obrigatório")
                return None
            
            # Buscar informações do usuário
            from mapeamento_usuarios import obter_usuario_por_nome
            
            usuario_info = obter_usuario_por_nome(vendedor_manual.strip())
            if usuario_info:
                vendedor_nome = usuario_info['nome']
                setor_atribuido = setor_manual.strip()  # Usar setor fornecido
                print(f"✓ Usuário selecionado: {vendedor_nome} (Setor: {setor_atribuido})")
            else:
                # Se não encontrar, usar o nome fornecido
                vendedor_nome = vendedor_manual.strip()
                setor_atribuido = setor_manual.strip()
                print(f"✓ Usuário: {vendedor_nome} (Setor: {setor_atribuido})")
            
            # Gerar número sequencial
            numero_pendencia = self._gerar_numero_sequencial()
            
            # Timestamp
            agora = datetime.now()
            timestamp_iso = agora.isoformat()
            
            # Obter primeira situação da lista
            try:
                from config_rede import ConfiguracaoRede
                situacoes = ConfiguracaoRede.obter_valores_situacao()
                situacao_padrao = situacoes[0] if situacoes else "Novo contato"
            except Exception as e:
                print(f"⚠️ Erro ao carregar situações: {e}")
                situacao_padrao = "Novo contato"
            
            # Estrutura JSON completa (usando campos canônicos)
            pendencia = {
                "numero": numero_pendencia,
                "data_criacao": timestamp_iso,
                "data_atualizacao": timestamp_iso,
                "usuario": vendedor_nome,  # Campo canônico (antigo: vendedor)
                "setor": setor_atribuido,
                "cliente": {
                    "razao_social": cliente if cliente else '-',
                    "telefone": telefone if telefone else '-',
                    "cnpj": cnpj if cnpj else '-',
                    "cidade": '-',
                    "contato": '-',
                    "email": '-',
                    "inscricao_estadual": inscricao if inscricao else '',
                    "endereco": endereco if endereco else '',
                },
                "equipamento": equipamento if equipamento else '',
                # Campos canônicos separados
                "situacao": situacao_padrao,   # pipeline comercial (primeira da lista)
                "status": "Ativa",            # estado operacional (Ativa/Arquivada/Fechada/Deletada)
                "prioridade": prioridade if prioridade else "normal",
                "prazo_resposta": prazo_resposta if prazo_resposta else '',
                "origem": "manual",
                "observacoes": observacoes if observacoes else "",
                "historico": [
                    {
                        "data": timestamp_iso,
                        "status_anterior": "",
                        "status_novo": f"Pendência registrada no setor {setor_atribuido}.",
                        "usuario": vendedor_nome
                    }
                ],
                "propostas_vinculadas": [],
                "anexos": [],
                "tags": [],
                "metadata": {
                    "versao": "1.0",
                    "ultima_modificacao": timestamp_iso,
                    "modificado_por": vendedor_nome
                }
            }
            
            # Salvar arquivo JSON
            arquivo_path = self.pasta_registros / "ATIVAS" / f"{numero_pendencia}.json"
            
            with open(arquivo_path, 'w', encoding='utf-8') as f:
                json.dump(pendencia, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Pendência criada: {numero_pendencia} → {arquivo_path.name}")
            print(f"✓ Histórico criado: {timestamp_iso} - Pendência criada por {vendedor_nome} - Vendedor responsável")
            
            return {
                'numero': numero_pendencia,
                'usuario': vendedor_nome,  # Campo canônico (antigo: vendedor)
                'setor': setor_atribuido,
                'arquivo': arquivo_path
            }
        
        except Exception as e:
            print(f"❌ Erro ao criar pendência: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _gerar_numero_sequencial(self):
        """
        Gera número sequencial único (AAMMDDSSSS)
        Verifica todos os arquivos JSON existentes
        
        Returns:
            str: Número sequencial
        """
        agora = datetime.now()
        prefixo = agora.strftime("%y%m%d")  # AAMMDD
        
        # Buscar último número em todos os arquivos JSON
        numeros_existentes = []
        
        # Verificar todas as pastas consideradas no sequencial
        for pasta in self.PASTAS_STATUS:
            pasta_path = self.pasta_registros / pasta
            if pasta_path.exists():
                for arquivo in pasta_path.glob("*.json"):
                    nome = arquivo.stem  # Nome sem extensão
                    if len(nome) == 10 and nome.startswith(prefixo):
                        try:
                            sufixo = int(nome[-4:])
                            numeros_existentes.append(sufixo)
                        except ValueError:
                            pass
        
        # Próximo número
        proximo = max(numeros_existentes) + 1 if numeros_existentes else 1
        
        # Formatar: AAMMDD + SSSS
        numero = f"{prefixo}{proximo:04d}"
        
        return numero
    
    def ler_pendencia(self, numero):
        """
        Lê uma pendência específica
        
        Args:
            numero: Número da pendência
            
        Returns:
            dict: Dados da pendência ou None
        """
        # Procurar em todas as pastas existentes
        for pasta in self.PASTAS_STATUS:
            arquivo = self.pasta_registros / pasta / f"{numero}.json"
            if arquivo.exists():
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception as e:
                    print(f"❌ Erro ao ler {arquivo.name}: {e}")
                    return None
        
        print(f"⚠️ Pendência {numero} não encontrada")
        return None
    
    def atualizar_pendencia(self, numero, atualizacoes, usuario='Sistema', timestamp_ultima_leitura=None):
        """
        Atualiza uma pendência existente com proteção contra edições simultâneas
        
        Args:
            numero: Número da pendência
            atualizacoes: Dict com campos a atualizar
            usuario: Nome do usuário fazendo a alteração
            timestamp_ultima_leitura: Timestamp da última vez que leu (para detectar conflito)
            
        Returns:
            dict: {'sucesso': bool, 'mensagem': str, 'conflito': bool}
        """
        # Encontrar arquivo
        arquivo_path = None
        for pasta in self.PASTAS_STATUS:
            temp_path = self.pasta_registros / pasta / f"{numero}.json"
            if temp_path.exists():
                arquivo_path = temp_path
                break
        
        if not arquivo_path:
            print(f"⚠️ Pendência {numero} não encontrada")
            return {'sucesso': False, 'mensagem': 'Pendência não encontrada', 'conflito': False}
        
        try:
            # Ler dados atuais
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                pendencia = json.load(f)
            
            # VERIFICAR CONFLITO: Se outro usuário modificou desde que você leu
            if timestamp_ultima_leitura:
                ultima_modificacao = pendencia['metadata'].get('ultima_modificacao', '')
                
                if ultima_modificacao > timestamp_ultima_leitura:
                    # CONFLITO DETECTADO!
                    modificador = pendencia['metadata'].get('modificado_por', 'Outro usuário')
                    print(f"⚠️ CONFLITO: {modificador} modificou esta pendência enquanto você editava!")
                    
                    return {
                        'sucesso': False, 
                        'mensagem': f'CONFLITO: {modificador} modificou esta pendência há pouco. Atualize e tente novamente.',
                        'conflito': True,
                        'modificado_por': modificador,
                        'quando': ultima_modificacao
                    }
            
            # Timestamp
            agora = datetime.now()
            timestamp_iso = agora.isoformat()
            
            # Migrar campo 'vendedor' para 'usuario' se necessário (compatibilidade)
            if 'vendedor' in atualizacoes:
                atualizacoes['usuario'] = atualizacoes.pop('vendedor')
            
            # Atualizar campos (situação e status diferenciados)
            for campo, valor in atualizacoes.items():
                if campo == 'situacao':
                    if not (isinstance(valor, str) and valor.strip()):
                        # ignorar updates vazios
                        continue
                    situacao_atual = pendencia.get('situacao', '')
                    if situacao_atual != valor:
                        pendencia['historico'].append({
                            "data": timestamp_iso,
                            "status_anterior": situacao_atual,
                            "status_novo": valor,
                            "usuario": usuario
                        })
                        print(f"✓ Histórico atualizado (Situação): {situacao_atual} → {valor} ({usuario})")
                    pendencia['situacao'] = valor
                elif campo == 'status':
                    status_atual = pendencia.get('status', '')
                    if status_atual != valor:
                        pendencia['historico'].append({
                            "data": timestamp_iso,
                            "status_anterior": status_atual,
                            "status_novo": f"Status: {status_atual} → {valor} ({usuario})",
                            "usuario": usuario
                        })
                        print(f"✓ Histórico atualizado (Status): {status_atual} → {valor} ({usuario})")
                    pendencia['status'] = valor
                elif campo == 'usuario':
                    # Migrar de 'vendedor' para 'usuario' se necessário
                    if 'vendedor' in pendencia:
                        del pendencia['vendedor']
                    pendencia['usuario'] = valor
                else:
                    pendencia[campo] = valor
            
            # Migrar campo 'vendedor' para 'usuario' se ainda existir (compatibilidade)
            if 'vendedor' in pendencia and 'usuario' not in pendencia:
                pendencia['usuario'] = pendencia['vendedor']
                del pendencia['vendedor']
            
            # Atualizar metadata
            pendencia['data_atualizacao'] = timestamp_iso
            pendencia['metadata']['ultima_modificacao'] = timestamp_iso
            pendencia['metadata']['modificado_por'] = usuario
            
            # Salvar
            with open(arquivo_path, 'w', encoding='utf-8') as f:
                json.dump(pendencia, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Pendência {numero} atualizada por {usuario}")
            print(f"✓ Histórico atualizado com {len(pendencia.get('historico', []))} registros")
            return {'sucesso': True, 'mensagem': 'Atualizado com sucesso', 'conflito': False}
        
        except Exception as e:
            print(f"❌ Erro ao atualizar pendência: {e}")
            return {'sucesso': False, 'mensagem': f'Erro: {e}', 'conflito': False}
    
    def atualizar_observacoes(self, numero, novo_texto, usuario='Sistema'):
        """
        Atualiza observações de uma pendência e registra no histórico
        
        Args:
            numero: Número da pendência
            novo_texto: Novo texto das observações
            usuario: Nome do usuário
            
        Returns:
            bool: True se sucesso
        """
        pendencia = self.ler_pendencia(numero)
        if not pendencia:
            return False
        
        # Verificar se houve mudança
        texto_anterior = pendencia.get('observacoes', '')
        if texto_anterior == novo_texto:
            return True  # Nenhuma mudança
        
        # Registrar mudança no histórico
        timestamp_iso = datetime.now().isoformat()
        pendencia['historico'].append({
            "data": timestamp_iso,
            "status_anterior": "",
            "status_novo": f"Observações editadas ({usuario})",
            "usuario": usuario
        })
        
        print(f"✓ Histórico atualizado: {timestamp_iso} - Observações editadas por {usuario}")
        
        # Atualizar observações
        pendencia['observacoes'] = novo_texto
        pendencia['data_atualizacao'] = timestamp_iso
        pendencia['metadata']['ultima_modificacao'] = timestamp_iso
        pendencia['metadata']['modificado_por'] = usuario
        
        # Salvar arquivo
        resultado = self._salvar_pendencia(numero, pendencia)
        if resultado:
            print(f"✓ Pendência {numero} salva com histórico atualizado")
            print(f"✓ Histórico tem {len(pendencia.get('historico', []))} registros")
        return resultado
    
    def vincular_proposta(self, numero_pendencia, codigo_proposta, arquivo_pdf='', usuario='Sistema'):
        """
        Vincula uma proposta gerada a uma pendência
        
        Args:
            numero_pendencia: Número da pendência
            codigo_proposta: Código da proposta (ex: 2510210001-01)
            arquivo_pdf: Nome do arquivo PDF gerado
            usuario: Nome do usuário fazendo a vinculação
            
        Returns:
            bool: True se sucesso
        """
        pendencia = self.ler_pendencia(numero_pendencia)
        if not pendencia:
            return False
        
        # Adicionar proposta vinculada
        timestamp_iso = datetime.now().isoformat()
        pendencia['propostas_vinculadas'].append({
            "codigo": codigo_proposta,
            "data": timestamp_iso,
            "arquivo": arquivo_pdf if arquivo_pdf else f"{codigo_proposta}.pdf"
        })
        
        # Adicionar ao histórico
        pendencia['historico'].append({
            "data": timestamp_iso,
            "status_anterior": "",
            "status_novo": f"Proposta gerada: {codigo_proposta}",
            "usuario": usuario
        })
        # Mudança de situação, quando aplicável, será feita pelo chamador via API central
        
        return self._salvar_pendencia(numero_pendencia, pendencia)
    
    def listar_pendencias(self, filtro_status=None, filtro_situacao=None, filtro_vendedor=None, filtro_setor=None, apenas_ativas=True, 
                          data_inicio=None, data_fim=None):
        """
        Lista pendências com filtros (carregamento dinâmico por data)
        
        Args:
            filtro_status: Filtrar por status (Ativa, Arquivada, etc.)
            filtro_situacao: Filtrar por situação (Novo contato, Proposta enviada, etc.)
            filtro_vendedor: Filtrar por vendedor
            filtro_setor: Filtrar por setor
            apenas_ativas: Se True, lista só ATIVAS
            data_inicio: datetime.date - Data inicial para filtrar (None = sem limite)
            data_fim: datetime.date - Data final para filtrar (None = sem limite)
            
        Returns:
            list: Lista de dicionários com pendências
        """
        pendencias = []
        
        # Determinar pastas a verificar
        if apenas_ativas:
            pastas = ["ATIVAS"]
        else:
            # Incluir todas as pastas de status
            pastas = self.PASTAS_STATUS
        
        # Função auxiliar para extrair data do nome do arquivo (formato: AAMMDDSSSS)
        def extrair_data_do_nome(nome_arquivo):
            """Extrai data do nome do arquivo (AAMMDDSSSS)"""
            try:
                if len(nome_arquivo) >= 6:
                    # AAMMDD (primeiros 6 caracteres)
                    aa = int(nome_arquivo[0:2])
                    mm = int(nome_arquivo[2:4])
                    dd = int(nome_arquivo[4:6])
                    # Converter AA para ano completo (assumindo 2000-2099)
                    ano = 2000 + aa if aa < 50 else 1900 + aa
                    return datetime(ano, mm, dd).date()
            except (ValueError, IndexError):
                pass
            return None
        
        # Ler arquivos JSON com filtro por data ANTES de abrir o arquivo
        for pasta in pastas:
            pasta_path = self.pasta_registros / pasta
            if not pasta_path.exists():
                continue
            
            for arquivo in pasta_path.glob("*.json"):
                # FILTRO RÁPIDO: Verificar data pelo nome do arquivo ANTES de ler
                nome_sem_ext = arquivo.stem
                data_arquivo = extrair_data_do_nome(nome_sem_ext)
                
                # Se temos filtro de data, pular arquivos fora do intervalo
                if data_inicio or data_fim:
                    if data_arquivo is None:
                        continue  # Não conseguiu extrair data, pular
                    if data_inicio and data_arquivo < data_inicio:
                        continue  # Antes do período
                    if data_fim and data_arquivo > data_fim:
                        continue  # Depois do período
                
                # Só agora ler o arquivo (já filtrado por data)
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        pendencia = json.load(f)
                    
                    # Aplicar filtros adicionais
                    if filtro_status and filtro_status != 'Todas':
                        if pendencia.get('status') != filtro_status:
                            continue
                    
                    if filtro_situacao and filtro_situacao != 'Todas':
                        if pendencia.get('situacao') != filtro_situacao:
                            continue
                    
                    if filtro_vendedor and filtro_vendedor != 'Todos':
                        # Suportar tanto 'usuario' (canônico) quanto 'vendedor' (compatibilidade)
                        usuario_pendencia = pendencia.get('usuario') or pendencia.get('vendedor', '')
                        if usuario_pendencia != filtro_vendedor:
                            continue
                    
                    if filtro_setor and filtro_setor != 'Todos':
                        if pendencia.get('setor') != filtro_setor:
                            continue
                    
                    pendencias.append(pendencia)
                
                except Exception as e:
                    print(f"⚠️ Erro ao ler {arquivo.name}: {e}")
        
        # Ordenar por data (mais recentes primeiro)
        pendencias.sort(key=lambda x: x.get('data_criacao', ''), reverse=True)
        
        return pendencias
    
    def atualizar_status(self, numero, novo_status, observacao='', usuario='Sistema'):
        """
        Atualiza a situação de uma pendência (wrapper retrocompatível)
        
        Args:
            numero: Número da pendência
            novo_status: Novo status
            observacao: Observação adicional
            usuario: Nome do usuário fazendo a atualização
            
        Returns:
            bool: True se sucesso
        """
        # não permitir atualização vazia
        if not (isinstance(novo_status, str) and novo_status.strip()):
            return False
        atualizacoes = {'situacao': novo_status.strip()}
        
        # 1) Sempre registrar mudança de situação
        resultado = self.atualizar_pendencia(numero, atualizacoes, usuario)
        sucesso = resultado.get('sucesso', False)
        
        # 2) Se houver observação (não vazia após strip), registrar também
        if sucesso and isinstance(observacao, str) and observacao.strip():
            self.atualizar_observacoes(numero, observacao.strip(), usuario)
        
        return sucesso

    def atualizar_situacao(self, numero, nova_situacao, observacao='', usuario='Sistema'):
        """API explícita para atualização de situação."""
        return self.atualizar_status(numero, nova_situacao, observacao, usuario)
    
    def transferir_pendencia(self, numero, vendedor_destino, motivo='', usuario='Sistema'):
        """
        Transfere pendência para outro usuário
        
        Args:
            numero: Número da pendência
            vendedor_destino: Nome do usuário destino (mantido para compatibilidade)
            motivo: Motivo da transferência
            usuario: Nome do usuário fazendo a transferência
            
        Returns:
            bool: True se sucesso
        """
        pendencia = self.ler_pendencia(numero)
        if not pendencia:
            return False
        
        # Suportar tanto 'usuario' (canônico) quanto 'vendedor' (compatibilidade)
        usuario_origem = pendencia.get('usuario') or pendencia.get('vendedor', '')
        usuario_destino = vendedor_destino  # Alias para compatibilidade
        
        # Atualizar campo canônico 'usuario'
        timestamp_iso = datetime.now().isoformat()
        
        pendencia['usuario'] = usuario_destino
        # Remover campo antigo se existir
        if 'vendedor' in pendencia:
            del pendencia['vendedor']
        pendencia['data_atualizacao'] = timestamp_iso
        pendencia['metadata']['ultima_modificacao'] = timestamp_iso
        pendencia['metadata']['modificado_por'] = usuario_destino
        
        # Adicionar ao histórico
        obs_texto = f"TRANSFERIDO de {usuario_origem} para {usuario_destino}"
        if motivo:
            obs_texto += f" - Motivo: {motivo}"
            
        pendencia['historico'].append({
            "data": timestamp_iso,
            "status_anterior": "",
            "status_novo": f"{obs_texto} ({usuario})",
            "usuario": usuario
        })
        
        # Salvar
        if self._salvar_pendencia(numero, pendencia):
            print(f"✓ Pendência {numero} transferida: {usuario_origem} → {usuario_destino}")
            return True
        else:
            return False
    
    def arquivar_pendencia(self, numero, motivo='', usuario='Sistema'):
        """
        Move pendência para ARQUIVADAS
        
        Args:
            numero: Número da pendência
            motivo: Motivo do arquivamento
            usuario: Nome do usuário fazendo o arquivamento
            
        Returns:
            bool: True se sucesso
        """
        return self._mover_pendencia(numero, "ARQUIVADAS", motivo, usuario)
    
    def fechar_pendencia(self, numero, motivo='', usuario='Sistema'):
        """
        Fecha pendência.
        
        A partir da remoção das pastas 'FECHADAS' e 'DELETADAS', o fechamento
        passa a ser tratado como arquivamento lógico: o arquivo é movido para
        'ARQUIVADAS' e o histórico/metadata registram o fechamento.
        """
        # Reutiliza a lógica de arquivamento, diferenciando apenas pela mensagem
        return self._mover_pendencia(numero, "ARQUIVADAS", motivo, usuario, acao_forcada="FECHADA")
    
    def _mover_pendencia(self, numero, pasta_destino, motivo='', usuario='Sistema', acao_forcada=None):
        """Move pendência entre pastas de status.
        
        Args:
            numero: Número da pendência
            pasta_destino: Uma das pastas de status (ATIVAS, ARQUIVADAS, CANCELADAS, CONCLUÍDAS, EM ATRASO)
            motivo: Motivo da movimentação
            usuario: Nome do usuário
            acao_forcada: Força o texto da ação no histórico (ex.: 'FECHADA')
        """
        # Encontrar arquivo atual
        arquivo_origem = None
        pasta_origem = None
        
        for pasta in self.PASTAS_STATUS:
            temp_path = self.pasta_registros / pasta / f"{numero}.json"
            if temp_path.exists():
                arquivo_origem = temp_path
                pasta_origem = pasta
                break
        
        if not arquivo_origem:
            print(f"⚠️ Pendência {numero} não encontrada")
            return False
        
        try:
            # Ler pendência
            with open(arquivo_origem, 'r', encoding='utf-8') as f:
                pendencia = json.load(f)
            
            # Adicionar observação sobre movimento
            timestamp_iso = datetime.now().isoformat()
            
            # Definir ação baseado no destino (ou ação forçada)
            if acao_forcada:
                acao = acao_forcada
            elif pasta_destino == "ARQUIVADAS":
                acao = "ARQUIVADA"
            else:
                acao = "MOVIDA"
            
            obs_texto = f"{acao} - Movida de {pasta_origem} para {pasta_destino}"
            if motivo:
                obs_texto += f" - Motivo: {motivo}"
            
            pendencia['historico'].append({
                "data": timestamp_iso,
                "status_anterior": "",
                "status_novo": f"{obs_texto} ({usuario})",
                "usuario": usuario
            })
            
            pendencia['data_atualizacao'] = timestamp_iso
            pendencia['metadata']['ultima_modificacao'] = timestamp_iso
            
            # Criar arquivo no destino
            arquivo_destino = self.pasta_registros / pasta_destino / f"{numero}.json"
            with open(arquivo_destino, 'w', encoding='utf-8') as f:
                json.dump(pendencia, f, ensure_ascii=False, indent=2)
            
            # Deletar arquivo origem
            arquivo_origem.unlink()
            
            print(f"✓ Pendência {numero} movida: {pasta_origem} → {pasta_destino}")
            return True
        
        except Exception as e:
            print(f"❌ Erro ao mover pendência: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def deletar_pendencia(self, numero, motivo=''):
        """
        Deleta pendência de forma permanente.
        
        Antes, a deleção apenas movia para a pasta 'DELETADAS'. Com a remoção
        dessa pasta/estrutura, a deleção agora remove o arquivo físico
        (das pastas ATIVAS/ARQUIVADAS), mantendo apenas o registro em memória
        durante a operação.
        """
        # Encontrar arquivo atual
        arquivo_origem = None
        pasta_origem = None
        for pasta in self.PASTAS_STATUS:
            temp_path = self.pasta_registros / pasta / f"{numero}.json"
            if temp_path.exists():
                arquivo_origem = temp_path
                pasta_origem = pasta
                break
        
        if not arquivo_origem:
            print(f"⚠️ Pendência {numero} não encontrada para deleção")
            return False
        
        try:
            # Ler pendência para log/consistência
            with open(arquivo_origem, 'r', encoding='utf-8') as f:
                pendencia = json.load(f)
            
            timestamp_iso = datetime.now().isoformat()
            obs_texto = f"DELETADA PERMANENTEMENTE - Removida de {pasta_origem}"
            if motivo:
                obs_texto += f" - Motivo: {motivo}"
            
            pendencia.setdefault('historico', []).append({
                "data": timestamp_iso,
                "status_anterior": "",
                "status_novo": obs_texto,
                "usuario": "Sistema"
            })
            
            # Finalmente, remover arquivo físico
            arquivo_origem.unlink()
            print(f"✓ Pendência {numero} deletada permanentemente ({pasta_origem})")
            return True
        except Exception as e:
            print(f"❌ Erro ao deletar pendência {numero}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _salvar_pendencia(self, numero, pendencia_data):
        """Salva pendência no arquivo correto"""
        # Encontrar arquivo (nas pastas existentes)
        for pasta in self.PASTAS_STATUS:
            arquivo = self.pasta_registros / pasta / f"{numero}.json"
            if arquivo.exists():
                try:
                    with open(arquivo, 'w', encoding='utf-8') as f:
                        json.dump(pendencia_data, f, ensure_ascii=False, indent=2)
                    return True
                except Exception as e:
                    print(f"❌ Erro ao salvar: {e}")
                    return False
        
        return False
    
    def normalizar_registros(self):
        """Normaliza todos os arquivos de pendência para o formato canônico.
        - Converte entradas antigas do histórico (ex.: situacao_anterior/situacao_nova) para status_anterior/status_novo padronizados
        - Preenche status_novo vazio com "Situação atualizada (Usuário)"
        - Garante separação rígida entre 'situacao' (pipeline) e 'status' (operacional)
        - Ajusta 'status' conforme a pasta do arquivo
        """
        pasta_status_map = {
            'ATIVAS': 'Ativa',
            'ARQUIVADAS': 'Arquivada',
            'CANCELADAS': 'Cancelada',
            'CONCLUÍDAS': 'Concluída',
            'EM ATRASO': 'Em Atraso',
        }
        total_arquivos = 0
        total_modificados = 0
        for pasta in self.PASTAS_STATUS:
            pasta_path = self.pasta_registros / pasta
            if not pasta_path.exists():
                continue
            for arquivo in pasta_path.glob("*.json"):
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        pendencia = json.load(f)
                except Exception:
                    continue
                total_arquivos += 1
                modificado = False
                # Garantir campos principais
                if not isinstance(pendencia.get('situacao', ''), str) or not pendencia.get('situacao', '').strip():
                    # Tentar inferir da última entrada "Situação: X → Y (...)"
                    inferida = None
                    for h in reversed(pendencia.get('historico', [])):
                        texto = (h.get('status_novo') or '').strip()
                        if texto.startswith('Situação:'):
                            try:
                                parte = texto.split('→')[-1]
                                inferida = parte.split('(')[0].strip()
                                break
                            except Exception:
                                pass
                    pendencia['situacao'] = inferida if inferida else 'Novo contato'
                    modificado = True
                # Ajustar status operacional conforme pasta
                status_operacional = pasta_status_map.get(pasta, pendencia.get('status', 'Ativa'))
                if pendencia.get('status') != status_operacional:
                    pendencia['status'] = status_operacional
                    modificado = True
                # Normalizar histórico
                historico = pendencia.get('historico', [])
                if isinstance(historico, list):
                    for h in historico:
                        # Reformatar mensagens "Situação: A → B (Usuário)" para par canônico (A → B)
                        texto = (h.get('status_novo') or '').strip()
                        if texto.startswith('Situação:') and '→' in texto:
                            try:
                                corpo = texto.replace('Situação:', '', 1).strip()
                                partes = corpo.split('→')
                                ant = partes[0].strip()
                                pos = partes[1].strip()
                                if '(' in pos:
                                    pos = pos.split('(')[0].strip()
                                h['status_anterior'] = ant
                                h['status_novo'] = pos
                                modificado = True
                            except Exception:
                                pass
                        # Converter formato antigo do atualizador_situacao (chaves antigas)
                        if 'situacao_anterior' in h or 'situacao_nova' in h:
                            ant = h.get('situacao_anterior', '')
                            nova = h.get('situacao_nova', '')
                            h['status_anterior'] = ant
                            h['status_novo'] = nova if (ant or nova) else "Situação atualizada"
                            for k in ['tipo', 'situacao_anterior', 'situacao_nova', 'observacao']:
                                if k in h:
                                    del h[k]
                            modificado = True
                        # Preencher status_novo vazio
                        texto_novo = (h.get('status_novo') or '').strip()
                        if not texto_novo:
                            # Suportar tanto 'usuario' (canônico) quanto 'vendedor' (compatibilidade)
                            usuario_pendencia = pendencia.get('usuario') or pendencia.get('vendedor', 'Sistema')
                            usuario_h = h.get('usuario', pendencia.get('metadata', {}).get('modificado_por', usuario_pendencia))
                            h['status_novo'] = f"Situação atualizada ({usuario_h})"
                            modificado = True
                        # Garantir usuario
                        if not (h.get('usuario') and str(h.get('usuario')).strip()):
                            # Suportar tanto 'usuario' (canônico) quanto 'vendedor' (compatibilidade)
                            usuario_pendencia = pendencia.get('usuario') or pendencia.get('vendedor', 'Sistema')
                            h['usuario'] = pendencia.get('metadata', {}).get('modificado_por', usuario_pendencia)
                            modificado = True
                # Migrar campo 'vendedor' para 'usuario' se necessário
                if 'vendedor' in pendencia and 'usuario' not in pendencia:
                    pendencia['usuario'] = pendencia['vendedor']
                    del pendencia['vendedor']
                    modificado = True
                # Atualizar metadata
                if modificado:
                    pendencia['metadata'] = pendencia.get('metadata', {})
                    pendencia['metadata']['ultima_modificacao'] = datetime.now().isoformat()
                    # Suportar tanto 'usuario' (canônico) quanto 'vendedor' (compatibilidade)
                    usuario_pendencia = pendencia.get('usuario') or pendencia.get('vendedor', 'Sistema')
                    pendencia['metadata']['modificado_por'] = pendencia.get('metadata', {}).get('modificado_por', usuario_pendencia)
                    try:
                        with open(arquivo, 'w', encoding='utf-8') as f:
                            json.dump(pendencia, f, ensure_ascii=False, indent=2)
                        total_modificados += 1
                    except Exception:
                        pass
        print(f"✓ Normalização concluída: {total_modificados}/{total_arquivos} arquivos atualizados")
    
    def obter_estatisticas(self):
        """
        Gera estatísticas das pendências
        
        Returns:
            dict: Estatísticas
        """
        todas = self.listar_pendencias(apenas_ativas=False)
        
        stats = {
            'total': len(todas),
            'ativas': 0,
            'arquivadas': 0,
            'fechadas': 0,
            'por_status': {},
            'por_vendedor': {},
            'com_proposta': 0,
            'sem_proposta': 0
        }
        
        for p in todas:
            # Contar por pasta
            # (baseado no status atual - poderia melhorar lendo pasta do arquivo)
            
            # Por status
            status = p.get('status', 'Sem Status')
            stats['por_status'][status] = stats['por_status'].get(status, 0) + 1
            
            # Por usuário (suportar tanto 'usuario' quanto 'vendedor' para compatibilidade)
            usuario = p.get('usuario') or p.get('vendedor', 'Sem Usuário')
            stats['por_vendedor'][usuario] = stats['por_vendedor'].get(usuario, 0) + 1
            
            # Com/sem proposta
            if p.get('propostas_vinculadas'):
                stats['com_proposta'] += 1
            else:
                stats['sem_proposta'] += 1
        
        return stats

