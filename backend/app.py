import mysql.connector
import os
from flask_cors import CORS
from flask import Flask, jsonify, send_file
import io
import base64
from PIL import Image

app = Flask(__name__)
#CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, resources={r"/*": {"origins": "http://162.243.250.179:8080"}}, supports_credentials=True)


# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'mysql'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', 'manut_area_verdes'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# Função para obter conexão com o banco de dados
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Rota para obter lista de escolas
@app.route('/api/escolas', methods=['GET'])
def get_escolas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, endereco, metragem, status FROM escolas")
        escolas = cursor.fetchall()
        return jsonify(escolas)
    finally:
        cursor.close()
        conn.close()

# Função para redimensionar imagem para 600x600
def redimensionar_imagem(imagem_base64):
    # Verificar e adicionar prefixo, se necessário
    if not imagem_base64.startswith("data:image/"):
        raise ValueError("A string Base64 não contém o prefixo necessário.")

    # Remover o prefixo antes de decodificar
    imagem_base64 = imagem_base64.split(",")[1]

    # Decodificar Base64
    imagem_bytes = base64.b64decode(imagem_base64)

    # Tentar abrir a imagem com Pillow
    try:
        imagem = Image.open(io.BytesIO(imagem_bytes))
    except Exception as e:
        raise ValueError(f"Erro ao abrir a imagem: {e}")

    # Converter para RGB (necessário para alguns formatos)
    if imagem.mode != "RGB":
        imagem = imagem.convert("RGB")

    # Redimensionar para 600x600
    imagem = imagem.resize((600, 600))

    # Re-encode para Base64
    buffer = io.BytesIO()
    imagem.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer.read()

@app.route('/api/detalhes', methods=['POST'])
def upload_fotos():
    from flask import request

    try:
        data = request.json
        id_escola = data.get('id_escola')
        fotos = data.get('fotos')

        if not id_escola or not fotos:
            return jsonify({'error': "Campos 'id_escola' e 'fotos' são obrigatórios."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        for id_foto, base64_image in fotos.items():
            # Redimensionar a imagem
            try:
                foto_bin = redimensionar_imagem(base64_image)
            except ValueError as e:
                return jsonify({'error': f"Erro ao processar a imagem {id_foto}: {e}"}), 400

            # Salvar no banco de dados
            query = "INSERT INTO fotos (id_escola, id_foto, foto) VALUES (%s, %s, %s)"
            cursor.execute(query, (id_escola, id_foto, foto_bin))

        conn.commit()
        return jsonify({'message': 'Fotos salvas com sucesso!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Endpoint para obter foto por ID
@app.route('/foto/<int:id>', methods=['GET'])
def get_foto(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT id, foto FROM fotos WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()

        if result:
            _, foto = result
            return send_file(
                io.BytesIO(foto),
                mimetype='image/jpeg',
                as_attachment=True,
                download_name=f"foto_{id}.jpg"
            )
        else:
            return jsonify({'message': 'Foto não encontrada!'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
