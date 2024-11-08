import sqlite3
import bcrypt

def inicializar_banco():
    conn = sqlite3.connect('industrias_wayne.db')
    cursor = conn.cursor()

    # Criação das tabelas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        nivel_acesso TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recursos (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        tipo TEXT NOT NULL,
        quantidade INTEGER,
        localizacao TEXT,
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Inserir usuário admin padrão
    senha_admin = bcrypt.hashpw("batman123".encode('utf-8'), bcrypt.gensalt())
    cursor.execute('''
    INSERT OR IGNORE INTO usuarios (email, senha, nome, nivel_acesso)
    VALUES (?, ?, ?, ?)
    ''', ('bruce@wayne.com', senha_admin, 'Bruce Wayne', 'admin'))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    inicializar_banco()
    print("Banco de dados inicializado com sucesso!")