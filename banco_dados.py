import sqlite3
from datetime import datetime

class BancoDados:
    def __init__(self):
        self.conn = sqlite3.connect('jogo_alfabeto.db')
        self.criar_tabelas()
    
    def criar_tabelas(self):
        """Cria as tabelas necessárias no banco de dados"""
        cursor = self.conn.cursor()
        
        # Tabela de jogadores
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Tabela de partidas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jogador_id INTEGER,
            pontuacao INTEGER NOT NULL,
            nivel INTEGER NOT NULL,
            modo_facil BOOLEAN NOT NULL,
            data_jogo DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (jogador_id) REFERENCES jogadores (id)
        )
        ''')
        
        # Tabela de estatísticas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS estatisticas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jogador_id INTEGER,
            total_partidas INTEGER DEFAULT 0,
            maior_pontuacao INTEGER DEFAULT 0,
            maior_nivel INTEGER DEFAULT 0,
            total_pontos INTEGER DEFAULT 0,
            FOREIGN KEY (jogador_id) REFERENCES jogadores (id)
        )
        ''')
        
        self.conn.commit()
    
    def adicionar_jogador(self, nome):
        """Adiciona um novo jogador ao banco de dados"""
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO jogadores (nome) VALUES (?)', (nome,))
        jogador_id = cursor.lastrowid
        
        # Inicializa as estatísticas do jogador
        cursor.execute('INSERT INTO estatisticas (jogador_id) VALUES (?)', (jogador_id,))
        self.conn.commit()
        return jogador_id
    
    def obter_jogador(self, nome):
        """Obtém o ID do jogador pelo nome"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM jogadores WHERE nome = ?', (nome,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    
    def salvar_partida(self, nome_jogador, pontuacao, nivel, modo_facil):
        """Salva os dados de uma partida"""
        cursor = self.conn.cursor()
        
        # Obtém ou cria o jogador
        jogador_id = self.obter_jogador(nome_jogador)
        if not jogador_id:
            jogador_id = self.adicionar_jogador(nome_jogador)
        
        # Salva a partida
        cursor.execute('''
        INSERT INTO partidas (jogador_id, pontuacao, nivel, modo_facil)
        VALUES (?, ?, ?, ?)
        ''', (jogador_id, pontuacao, nivel, modo_facil))
        
        # Atualiza as estatísticas
        cursor.execute('''
        UPDATE estatisticas 
        SET total_partidas = total_partidas + 1,
            maior_pontuacao = MAX(maior_pontuacao, ?),
            maior_nivel = MAX(maior_nivel, ?),
            total_pontos = total_pontos + ?
        WHERE jogador_id = ?
        ''', (pontuacao, nivel, pontuacao, jogador_id))
        
        self.conn.commit()
    
    def obter_ranking(self, limite=10):
        """Obtém o ranking dos jogadores por maior pontuação"""
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT j.nome, e.maior_pontuacao, e.maior_nivel, e.total_partidas
        FROM jogadores j
        JOIN estatisticas e ON j.id = e.jogador_id
        ORDER BY e.maior_pontuacao DESC
        LIMIT ?
        ''', (limite,))
        return cursor.fetchall()
    
    def obter_estatisticas_jogador(self, nome_jogador):
        """Obtém as estatísticas de um jogador específico"""
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT e.total_partidas, e.maior_pontuacao, e.maior_nivel, e.total_pontos
        FROM jogadores j
        JOIN estatisticas e ON j.id = e.jogador_id
        WHERE j.nome = ?
        ''', (nome_jogador,))
        return cursor.fetchone()
    
    def fechar(self):
        """Fecha a conexão com o banco de dados"""
        self.conn.close() 