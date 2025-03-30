import json
import os
from datetime import datetime

class GerenciadorConquistas:
    def __init__(self):
        self.arquivo_save = "save.json"
        self.conquistas = {
            'mascotes': {
                'padrao': {'nome': 'Mascote Padrão', 'desbloqueado': True},
                'astronauta': {'nome': 'Astronauta', 'desbloqueado': False},
                'super_heroi': {'nome': 'Super Herói', 'desbloqueado': False},
                'fada': {'nome': 'Fada', 'desbloqueado': False},
                'dinossauro': {'nome': 'Dinossauro', 'desbloqueado': False}
            },
            'cores_fundo': {
                'padrao': {'nome': 'Azul Claro', 'desbloqueado': True},
                'verde': {'nome': 'Verde Natureza', 'desbloqueado': False},
                'roxo': {'nome': 'Roxo Mágico', 'desbloqueado': False},
                'amarelo': {'nome': 'Amarelo Sol', 'desbloqueado': False},
                'rosa': {'nome': 'Rosa Doce', 'desbloqueado': False}
            },
            'musicas': {
                'padrao': {'nome': 'Música Padrão', 'desbloqueado': True},
                'rock': {'nome': 'Rock Kids', 'desbloqueado': False},
                'classica': {'nome': 'Clássica Kids', 'desbloqueado': False},
                'pop': {'nome': 'Pop Kids', 'desbloqueado': False},
                'jazz': {'nome': 'Jazz Kids', 'desbloqueado': False}
            }
        }
        self.estrelas_nivel = {
            1: 0, 2: 0, 3: 0, 4: 0, 5: 0
        }
        self.nome_jogador = ""
        self.carregar_save()

    def carregar_save(self):
        """Carrega o arquivo de save se existir"""
        try:
            if os.path.exists(self.arquivo_save):
                with open(self.arquivo_save, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.conquistas = dados.get('conquistas', self.conquistas)
                    self.estrelas_nivel = dados.get('estrelas_nivel', self.estrelas_nivel)
                    self.nome_jogador = dados.get('nome_jogador', self.nome_jogador)
        except Exception as e:
            print(f"Erro ao carregar save: {e}")

    def salvar_save(self):
        """Salva o estado atual do jogo"""
        try:
            dados = {
                'conquistas': self.conquistas,
                'estrelas_nivel': self.estrelas_nivel,
                'nome_jogador': self.nome_jogador,
                'ultima_atualizacao': datetime.now().isoformat()
            }
            with open(self.arquivo_save, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erro ao salvar save: {e}")

    def definir_nome_jogador(self, nome):
        """Define o nome do jogador"""
        self.nome_jogador = nome
        self.salvar_save()

    def calcular_estrelas_nivel(self, nivel, acertos, vidas_perdidas):
        """Calcula quantas estrelas o jogador ganhou no nível"""
        if acertos >= 10 and vidas_perdidas == 0:
            return 3
        elif acertos >= 8 and vidas_perdidas <= 1:
            return 2
        elif acertos >= 5:
            return 1
        return 0

    def atualizar_estrelas_nivel(self, nivel, acertos, vidas_perdidas):
        """Atualiza as estrelas do nível"""
        estrelas = self.calcular_estrelas_nivel(nivel, acertos, vidas_perdidas)
        self.estrelas_nivel[nivel] = max(self.estrelas_nivel[nivel], estrelas)
        self.salvar_save()
        return estrelas

    def desbloquear_conquista(self, categoria, item):
        """Desbloqueia uma conquista"""
        if categoria in self.conquistas and item in self.conquistas[categoria]:
            self.conquistas[categoria][item]['desbloqueado'] = True
            self.salvar_save()
            return True
        return False

    def verificar_desbloqueios_nivel(self, nivel):
        """Verifica se há conquistas para desbloquear no nível"""
        desbloqueios = []
        
        if nivel == 1 and self.estrelas_nivel[1] >= 2:
            desbloqueios.append(('mascotes', 'astronauta'))
            desbloqueios.append(('cores_fundo', 'verde'))
        
        elif nivel == 2 and self.estrelas_nivel[2] >= 2:
            desbloqueios.append(('mascotes', 'super_heroi'))
            desbloqueios.append(('musicas', 'rock'))
        
        elif nivel == 3 and self.estrelas_nivel[3] >= 2:
            desbloqueios.append(('mascotes', 'fada'))
            desbloqueios.append(('cores_fundo', 'roxo'))
        
        elif nivel == 4 and self.estrelas_nivel[4] >= 2:
            desbloqueios.append(('mascotes', 'dinossauro'))
            desbloqueios.append(('musicas', 'classica'))
        
        elif nivel == 5 and self.estrelas_nivel[5] >= 2:
            desbloqueios.append(('cores_fundo', 'amarelo'))
            desbloqueios.append(('musicas', 'jazz'))
        
        # Desbloquear conquistas
        for categoria, item in desbloqueios:
            self.desbloquear_conquista(categoria, item)
        
        return desbloqueios

    def gerar_certificado(self):
        """Gera um certificado de conclusão"""
        if not self.nome_jogador:
            return None
            
        data_atual = datetime.now().strftime("%d/%m/%Y")
        total_estrelas = sum(self.estrelas_nivel.values())
        
        certificado = {
            'nome': self.nome_jogador,
            'data': data_atual,
            'total_estrelas': total_estrelas,
            'estrelas_por_nivel': self.estrelas_nivel.copy(),
            'conquistas_desbloqueadas': {
                categoria: [item for item, info in items.items() if info['desbloqueado']]
                for categoria, items in self.conquistas.items()
            }
        }
        
        return certificado 