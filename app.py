import jwt
import pandas as pd
from functools import wraps
from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'esgcesar'

### Usuários Válidos para teste:
# 1 - email: test@cesar, password: test123
# 2 - email: test2@cesar, password: test123
df_users = pd.read_csv("./csv-database/users.csv")

### Dados para teste:
df_adm = pd.read_csv("./csv-database/dados_adm.csv")
df_socio = pd.read_csv("./csv-database/dados_socio.csv")
df_socioamb = pd.read_csv("./csv-database/dados_socioamb.csv")

# Função para gerar o token de acesso do usuário
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        # Foi uma escolha deixar o token sem tempo para expirar.
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return token

def required_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer ", "")
        
        if not token:
            return jsonify({"message": "Token not valid"}), 403

        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload['user_id']
        except Exception as e:
            return jsonify({"message": "Token invalid"}), 401

        return f(*args, **kwargs)

    return decorated

@app.route("/login", methods=["POST"])
def login():  
    content = request.get_json()
    
    email = content["email"]
    password = content["password"]
    user_id = None

    for index, row in df_users.iterrows():
        if row["email"] == email:
            user_id = row["id"]
            hash_password = row["password"]
            break
    
    if user_id == None:
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

@app.route("/overview", methods=["GET"])
@required_token
def geral():
    x = df_adm.head(5)
    return jsonify(x.to_dict(orient="records")), 200

@app.route("/camada/E")
@required_token
def camadaE():
    return "Camada E"

@app.route("/camada/S")
@required_token
def camadaS():
    return "Camada S"

@app.route("/camada/G")
@required_token
def camadaG():
    return "Camada G"

@app.route("/monitoramento")
@required_token
def monitoramente():
    return "Monitoramento"

@app.route("/email")
@required_token
def email():
    return "Email"

@app.route("/projecao")
@required_token
def projecao():
    return "Projecao"

@app.route("/relatorio")
@required_token
def relatorio():
    return "Relatorio"

app.run(debug=True)