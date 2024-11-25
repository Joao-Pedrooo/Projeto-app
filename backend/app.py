import mysql.connector
import os
from flask_cors import CORS
from flask import Flask, jsonify, request, send_file
import io

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

@app.route('/api/detalhes', methods=['POST'])
def upload_foto():
    conn = get_db_connection()
    cursor = conn.cursor()
    

    try:
        nome = request.json.get('nome')
        print(nome)
        if not nome:
           return jsonify({'error': "Nao informado"}), 400
        # Processa os arquivos enviados
        for key in request.files:
            file = request.files[key]
            if file:
                # Salva o arquivo localmente
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                # Salva a referência no banco de dados
                with open(filepath, 'rb') as f:
                    foto_bin = f.read()
                query = "INSERT INTO fotos (nome, foto) VALUES (%s, %s)"
                cursor.execute(query, (nome, foto_bin))
                print(f"Foto '{filename}' inserida no banco com sucesso.")
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
