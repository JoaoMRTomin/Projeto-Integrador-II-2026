from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

# Inicializa a aplicação Flask
app = Flask(__name__)

# Libera o acesso para o seu JS no navegador fazer requisições fetch
CORS(app)

# Configuração de conexão com o banco MySQL
def conectar_banco():
    return mysql.connector.connect(
        host='localhost',
        user='root',          # Seu usuário do MySQL
        password='josetomin',          # Sua senha do MySQL (deixe vazia se não tiver)
        database='pathstudy'  # Nome do seu banco de dados
    )

# ROTA DE LOGIN (Atende ao fetch('.../api/login'))
@app.route('/api/login', methods=['POST'])
def login():
    # 1. Pega os dados enviados no JSON pelo JS (email e senha)
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    # --- LINHAS DE TESTE (Aparecerão no terminal do VS Code) ---
    print("\n========================================")
    print(f" [LOGIN] E-mail recebido do site: {email}")
    print("========================================\n")

    # ... restante do código do banco de dados ...

    # 2. Conecta ao MySQL e cria o cursor para rodar comandos
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True) # dictionary=True traz o resultado como chave:valor

    # 3. Executa a busca segura no banco (%s evita ataques de SQL Injection)
    cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
    usuario = cursor.fetchone() # Pega o primeiro registro encontrado

    # 4. Fecha a conexão com o banco
    cursor.close()
    conn.close()

    # 5. Validações
    if not usuario:
        return jsonify({'mensagem': 'E-mail não cadastrado.'}), 404

    if usuario['senha'] != senha: # Futuramente aqui usaremos criptografia
        return jsonify({'mensagem': 'Senha incorreta.'}), 401

    # 6. Sucesso: envia os dados do usuário de volta para o JS
    return jsonify({
        'mensagem': 'Login realizado com sucesso!',
        'usuario': {
            'id': usuario['id_usuario'],
            'nome': usuario['nome']
        }
    }), 200

# ROTA DE CADASTRO (Atende ao fetch('.../api/cadastro'))
@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    dados = request.get_json()
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')

    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    # Verifica se o e-mail já existe no banco
    cursor.execute('SELECT id_usuario FROM usuarios WHERE email = %s', (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({'mensagem': 'Este e-mail já está em uso.'}), 400

    # Insere o novo usuário na tabela
    sql = 'INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)'
    cursor.execute(sql, (nome, email, senha))
    conn.commit() # Confirma a alteração no MySQL

    cursor.close()
    conn.close()

    return jsonify({'mensagem': 'Conta criada com sucesso!'}), 201

# Inicia o servidor na porta 3000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)