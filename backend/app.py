import mysql.connector
import os
from flask_cors import CORS
from flask import Flask, jsonify, request, send_file
import io
import base64
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'mysql'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', 'manut_area_verdes'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# Maximum file size (in MB)
MAX_FILE_SIZE_MB = 5


def get_db_connection():
    """Create a new database connection."""
    return mysql.connector.connect(**DB_CONFIG)


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





# Pasta para salvar as fotos localmente
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
import base64

@app.route('/api/detalhes', methods=['POST'])
def upload_foto():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        nome = request.json.get('nome')
        fotos = request.json.get('fotos')

        if not nome or not fotos:
            return jsonify({'error': "Os campos 'nome' e 'fotos' são obrigatórios."}), 400

        for char, base64_image in fotos.items():
            # Verifica e remove o prefixo Base64
            if base64_image.startswith("data:image/"):
                base64_image = base64_image.split(",")[1]

            # Decodifica o Base64 para binário
            try:
                foto_bin = base64.b64decode(base64_image)
            except Exception as e:
                print(f"Erro ao decodificar a imagem {char}: {e}")
                return jsonify({'error': f"Erro ao processar a imagem {char}."}), 400

            # Insere no banco
            query = "INSERT INTO fotos (nome, foto) VALUES (%s, %s)"
            cursor.execute(query, (nome, foto_bin))
            print(f"Foto '{char}' inserida no banco com sucesso.")

        conn.commit()
        return jsonify({'message': 'Fotos salvas com sucesso!'}), 201

    except Exception as e:
        print(f"Erro ao salvar fotos: {e}")
        conn.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()



@app.route('/foto/<int:id>', methods=['GET'])
def get_foto(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Retrieve the photo
        query = "SELECT nome, foto FROM fotos WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()

        if result:
            nome, foto = result
            return send_file(
                io.BytesIO(foto),
                mimetype='image/jpeg',
                as_attachment=True,
                download_name=nome
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