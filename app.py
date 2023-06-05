import jwt
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'esgcesar'

global df_users
df_users = pd.read_csv("./csv-database/users.csv")

# Função para gerar o token de acesso do usuário
def generate_token(user_id):
    payload = {
        'usuario_id': user_id,
        # Foi uma escolha deixar o token sem tempo para expirar.
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return token

@app.route("/login", methods=["POST"])
def login():    
    content = request.get_json()
    
    email = content["email"]
    password = content["password"]

    for index, row in df_users.iterrows():
        if row["email"] == email:
            user_id = row["id"]
            hash_password = row["password"]
            break
        else:
            return jsonify({"status": "Error", "message": "User not found!"}), 404

    back_password = check_password_hash(hash_password, password)
    if back_password:
        token = generate_token(user_id)
        response = {
            "status": "Success", 
            "message": "Login Done!", 
            "token": token
        }
        return jsonify(response), 200
    else:
        return jsonify({"status": "Error", "message": "Password incorrect!"}), 401

@app.route("/visao-geral")
def geral():
    return "Visao Geral"

@app.route("/camada/E")
def camadaE():
    return "Camada E"

@app.route("/camada/S")
def camadaS():
    return "Camada S"

@app.route("/camada/G")
def camadaG():
    return "Camada G"

@app.route("/monitoramento")
def monitoramente():
    return "Monitoramento"

@app.route("/email")
def email():
    return "Email"

@app.route("/projecao")
def projecao():
    return "Projecao"

@app.route("/relatorio")
def relatorio():
    return "Relatorio"

app.run(debug=True)