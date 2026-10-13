from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

# Inicializa a aplicação Flask
app = Flask(__name__)

# Libera o acesso para o JavaScript no navegador fazer requisições fetch
CORS(app)

# Configuração de conexão com o banco MySQL
def conectar_banco():
    try:
        return mysql.connector.connect(
            host='127.0.0.1',     # Usar 127.0.0.1 evita problemas de IPv6 no Windows
            user='root',          # O teu utilizador do MySQL
            password='josetomin', # A tua palavra-passe do MySQL
            database='pathstudy'  # Nome da base de dados
        )
    except mysql.connector.Error as err:
        print(f"\n[ERRO DE LIGAÇÃO AO MYSQL]: {err}\n")
        return None

# ============================================================
# ROTA DE LOGIN
# ============================================================
@app.route('/api/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    conn = conectar_banco()
    if not conn:
        return jsonify({'mensagem': 'Erro crítico ao ligar à base de dados.'}), 500

    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({'mensagem': 'E-mail não cadastrado.'}), 404

        if usuario['senha'] != senha:
            return jsonify({'mensagem': 'Senha incorreta.'}), 401

        return jsonify({
            'mensagem': 'Login realizado com sucesso!',
            'usuario': {
                'id': usuario['id_usuario'],
                'nome': usuario['nome']
            }
        }), 200

    except mysql.connector.Error as err:
        return jsonify({'mensagem': f'Erro na consulta: {err}'}), 500
    finally:
        cursor.close()
        conn.close()

# ============================================================
# ROTA DE CADASTRO
# ============================================================
@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    dados = request.get_json()
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')

    conn = conectar_banco()
    if not conn:
        return jsonify({'mensagem': 'Erro crítico ao ligar à base de dados.'}), 500

    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Verifica se o e-mail já existe
        cursor.execute('SELECT id_usuario FROM usuarios WHERE email = %s', (email,))
        if cursor.fetchone():
            return jsonify({'mensagem': 'Este e-mail já está em uso.'}), 400

        # 2. Insere o novo utilizador
        sql = 'INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)'
        cursor.execute(sql, (nome, email, senha))
        conn.commit()

        # 3. Descobre o ID gerado automaticamente para este novo registo
        novo_id = cursor.lastrowid

        # 4. Retorna a mensagem E os dados do utilizador para o JavaScript guardar
        return jsonify({
            'mensagem': 'Conta criada com sucesso!',
            'usuario': {
                'id': novo_id,
                'nome': nome,
                'email': email
            }
        }), 201

    except mysql.connector.Error as err:
        return jsonify({'mensagem': f'Erro ao inserir dados: {err}'}), 500
    finally:
        cursor.close()
        conn.close()

# Inicia o servidor na porta 3000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)