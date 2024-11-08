import http.server
import json
import sqlite3
from urllib.parse import parse_qs, urlparse
import jwt
import bcrypt
import os

CHAVE_SECRETA = "industrias_wayne_gotham_2024"

class ManipuladorRequest(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def configurar_headers(self):
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_POST(self):
        tamanho_conteudo = int(self.headers.get('Content-Length', 0))
        dados_post = self.rfile.read(tamanho_conteudo)
        dados = json.loads(dados_post)

        if self.path == '/login':
            self.processar_login(dados)
        elif self.path == '/recursos/adicionar':
            self.adicionar_recurso(dados)

    def do_GET(self):
        if self.path.startswith('/recursos'):
            self.obter_recursos()
        elif self.path.startswith('/dashboard/dados'):
            self.obter_dados_dashboard()

    def processar_login(self, dados):
        email = dados.get('email')
        senha = dados.get('senha')

        conn = sqlite3.connect('industrias_wayne.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, senha, nivel_acesso FROM usuarios WHERE email = ?', (email,))
        usuario = cursor.fetchone()
        
        if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario[1]):
            token = jwt.encode({
                'id': usuario[0],
                'nivel_acesso': usuario[2]
            }, CHAVE_SECRETA, algorithm='HS256')
            
            self.send_response(200)
            self.configurar_headers()
            self.wfile.write(json.dumps({'token': token}).encode())
        else:
            self.send_response(401)
            self.configurar_headers()
            self.wfile.write(json.dumps({'erro': 'Credenciais inválidas'}).encode())

    def adicionar_recurso(self, dados):
        token = self.headers.get('Authorization')
        if not self.verificar_autorizacao(token, ['admin', 'gerente']):
            self.send_response(403)
            self.configurar_headers()
            return

        conn = sqlite3.connect('industrias_wayne.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO recursos (nome, tipo, quantidade, localizacao)
            VALUES (?, ?, ?, ?)
        ''', (dados['nome'], dados['tipo'], dados['quantidade'], dados['localizacao']))
        
        conn.commit()
        self.send_response(201)
        self.configurar_headers()

    def verificar_autorizacao(self, token, niveis_permitidos):
        try:
            if not token:
                return False
            token = token.split(' ')[1]
            dados = jwt.decode(token, CHAVE_SECRETA, algorithms=['HS256'])
            return dados['nivel_acesso'] in niveis_permitidos
        except:
            return False