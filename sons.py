import pygame
import os

class GerenciadorSons:
    def __init__(self):
        pygame.mixer.init()
        
        # Configurar volumes
        self.volume_musica = 0.5
        self.volume_efeitos = 0.7
        pygame.mixer.music.set_volume(self.volume_musica)
        
        # Carregar efeitos sonoros
        self.efeitos = {}
        self.carregar_efeitos()
        
        # Carregar músicas
        self.musicas = {}
        self.carregar_musicas()
    
    def carregar_efeitos(self):
        """Carrega os efeitos sonoros"""
        try:
            efeitos = {
                'acerto': 'sons/efeitos/acerto.wav',
                'erro': 'sons/efeitos/erro.wav',
                'nivel': 'sons/efeitos/nivel_up.wav',
                'bonus': 'sons/efeitos/bonus.wav',
                'vida_perdida': 'sons/efeitos/vida_perdida.wav',
                'muito_bem': 'sons/efeitos/muito_bem.wav',
                'tente_novamente': 'sons/efeitos/tente_novamente.wav',
                'digitou': 'sons/efeitos/digitou.wav'
            }
            
            for nome, caminho in efeitos.items():
                try:
                    self.efeitos[nome] = pygame.mixer.Sound(caminho)
                except:
                    print(f"Aviso: Não foi possível carregar o efeito sonoro {nome}")
        except:
            print("Aviso: Pasta de efeitos sonoros não encontrada")
    
    def carregar_musicas(self):
        """Carrega as músicas do jogo"""
        try:
            musicas = {
                'tema_principal': 'sons/musicas/tema_principal.mp3',
                'nivel_1': 'sons/musicas/nivel_1.mp3',
                'nivel_2': 'sons/musicas/nivel_2.mp3',
                'nivel_3': 'sons/musicas/nivel_3.mp3'
            }
            
            for nome, caminho in musicas.items():
                try:
                    self.musicas[nome] = caminho
                except:
                    print(f"Aviso: Não foi possível carregar a música {nome}")
        except:
            print("Aviso: Pasta de músicas não encontrada")
    
    def tocar_efeito(self, nome):
        """Toca um efeito sonoro"""
        if nome in self.efeitos:
            self.efeitos[nome].play()
        else:
            print(f"Aviso: Efeito sonoro {nome} não encontrado")
    
    def tocar_musica(self, nome):
        """Toca uma música"""
        try:
            if nome in self.musicas:
                pygame.mixer.music.load(self.musicas[nome])
                pygame.mixer.music.play(-1)  # -1 para tocar em loop
            else:
                print(f"Aviso: Música {nome} não encontrada")
        except:
            print(f"Aviso: Não foi possível tocar a música {nome}")
    
    def tocar_musica_nivel(self, nivel):
        """Toca a música do nível atual"""
        nome_musica = f'nivel_{nivel}'
        self.tocar_musica(nome_musica)
    
    def parar_musica(self):
        """Para a música atual"""
        pygame.mixer.music.stop()
    
    def definir_volume_musica(self, volume):
        """Define o volume da música (0.0 a 1.0)"""
        self.volume_musica = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume_musica)
    
    def definir_volume_efeitos(self, volume):
        """Define o volume dos efeitos sonoros (0.0 a 1.0)"""
        self.volume_efeitos = max(0.0, min(1.0, volume))
        for efeito in self.efeitos.values():
            efeito.set_volume(self.volume_efeitos) 