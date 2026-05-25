# =========================================
# IMPORTAÇÕES
# =========================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import os
import sqlite3
from deepface import DeepFace
from datetime import datetime

# =========================================
# INICIA FLASK
# =========================================

app = Flask(__name__)

# =========================================
# LIBERA ACESSO PARA FRONTEND
# =========================================

# Isso permite o React acessar o Flask
CORS(app)

# =========================================
# CRIA BANCO SQLITE
# =========================================

# O banco será criado automaticamente
conn = sqlite3.connect("presencas.db")

cursor = conn.cursor()

# =========================================
# TABELA DE PRESENÇAS
# =========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS presencas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno TEXT,
    horario TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

# =========================================
# FUNÇÃO PARA SALVAR PRESENÇA
# =========================================

def salvar_presenca(aluno, horario, status):

    conn = sqlite3.connect("presencas.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO presencas (aluno, horario, status)
    VALUES (?, ?, ?)
    """, (aluno, horario, status))

    conn.commit()
    conn.close()

# =========================================
# RECONHECIMENTO FACIAL
# =========================================

def iniciar_reconhecimento_facial(nome_aluno_esperado, arquivo_foto):

    video_capture = cv2.VideoCapture(0)

    print(f"\n[IA ATIVADA] Monitorando ambiente. Esperado: {nome_aluno_esperado.upper()}.")

    contador_frames = 0

    status_validacao = "Analisando..."

    cor_quadrado = (255, 255, 0)

    while video_capture.isOpened():

        ret, frame = video_capture.read()

        if not ret:
            break

        contador_frames += 1

        if contador_frames % 5 == 0:

            try:

                resultado = DeepFace.verify(
                    img1_path=frame,
                    img2_path=arquivo_foto,
                    model_name="VGG-Face",
                    enforce_detection=False
                )

                # =========================================
                # ALUNO CORRETO
                # =========================================

                if resultado["verified"]:

                    status_validacao = f"{nome_aluno_esperado.upper()} CONFIRMADO"

                    cor_quadrado = (0, 255, 0)

                    # =========================================
                    # SALVA NO BANCO
                    # =========================================

                    horario = datetime.now().strftime("%H:%M:%S")

                    salvar_presenca(
                        nome_aluno_esperado,
                        horario,
                        "presente"
                    )

                else:

                    status_validacao = "ALUNO INCORRETO"

                    cor_quadrado = (0, 0, 255)

            except Exception as e:

                status_validacao = "Procurando rosto..."

                cor_quadrado = (255, 255, 0)

        classificador = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rostos = classificador.detectMultiScale(frame_cinza, 1.1, 5)

        for (x, y, largura, altura) in rostos:

            cv2.rectangle(
                frame,
                (x, y),
                (x + largura, y + altura),
                cor_quadrado,
                2
            )

            cv2.rectangle(
                frame,
                (x, y - 35),
                (x + largura, y),
                cor_quadrado,
                cv2.FILLED
            )

            cv2.putText(
                frame,
                status_validacao,
                (x + 6, y - 10),
                cv2.FONT_HERSHEY_DUPLEX,
                0.5,
                (255, 255, 255),
                1
            )

        cv2.imshow('Controle de Presenca Autenticado', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()

    cv2.destroyAllWindows()

# =========================================
# INICIAR CHAMADA
# =========================================

@app.route('/iniciar-chamada', methods=['POST'])
def iniciar_chamada():

    dados = request.get_json()

    if not dados or 'horario' not in dados or 'aluno_id' not in dados:

        return jsonify({
            "erro": "Dados incompletos!"
        }), 400

    aluno_id = dados['aluno_id'].strip().lower()

    foto_aluno = f"{aluno_id}.jpeg"

    if not os.path.exists(foto_aluno):

        foto_aluno = f"{aluno_id}.jpg"

        if not os.path.exists(foto_aluno):

            return jsonify({
                "erro": f"Aluno '{aluno_id}' nao possui foto cadastrada!"
            }), 404

    print(f"\n[API] Solicitada presenca para o aluno: {aluno_id}")

    iniciar_reconhecimento_facial(
        aluno_id,
        foto_aluno
    )

    return jsonify({
        "status": "Sucesso",
        "mensagem": f"Processamento de {aluno_id} finalizado."
    }), 200

# =========================================
# ROTA PARA FRONTEND PEGAR PRESENÇAS
# =========================================

@app.route('/presencas', methods=['GET'])
def listar_presencas():

    conn = sqlite3.connect("presencas.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM presencas
    ORDER BY id DESC
    """)

    dados = cursor.fetchall()

    conn.close()

    lista = []

    for item in dados:

        lista.append({
            "id": item[0],
            "aluno": item[1],
            "horario": item[2],
            "status": item[3]
        })

    return jsonify(lista)

# =========================================
# ROTA DASHBOARD
# =========================================

@app.route('/dashboard', methods=['GET'])
def dashboard():

    conn = sqlite3.connect("presencas.db")

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM presencas")

    total = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "total_presencas": total,
        "status": "BACKEND FUNCIONANDO"
    })

# =========================================
# CADASTRO DE ALUNOS
# =========================================

@app.route('/cadastrar-aluno', methods=['POST'])
def cadastrar_aluno():

    # =========================================
    # PEGA NOME
    # =========================================

    nome = request.form.get('nome')

    # =========================================
    # PEGA FOTO
    # =========================================

    foto = request.files.get('foto')

    if not nome or not foto:

        return jsonify({
            "erro": "Nome e foto obrigatorios"
        }), 400

    # =========================================
    # NOME DO ARQUIVO
    # =========================================

    nome_arquivo = f"alunos/{nome.lower()}.jpeg"

    # =========================================
    # SALVA FOTO
    # =========================================

    foto.save(nome_arquivo)

    return jsonify({
        "status": "sucesso",
        "mensagem": f"{nome} cadastrado com sucesso"
    })

# =========================================
# EXECUÇÃO
# =========================================

if __name__ == "__main__":
    app.run(debug=True)