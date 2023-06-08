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
df_gov = pd.read_csv("./csv-database/gov_data.csv")
df_social = pd.read_csv("./csv-database/social_data.csv")
df_env = pd.read_csv("./csv-database/env_data.csv")

# Função para gerar o token de acesso do usuário
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        # Foi uma escolha deixar o token sem tempo para expirar.
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return token

# Função para verificar se o token é válido
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

# Função para pegar os dados dos 5 primeiro dados do csv
def get_csv_head_data():
    obj_data = {
        "gov": df_gov.to_dict(orient="records"),
        "social": df_social.to_dict(orient="records"),
        "env": df_env.to_dict(orient="records")
    }
    
    return obj_data

def data_to_dataframe(data):
    df1 = pd.DataFrame(data['gov'])
    df2 = pd.DataFrame(data['social'])
    df3 = pd.DataFrame(data['env'])
    
    gov_row = pd.DataFrame([['Governance','-','-']], columns=['indicator','unit','complement'])
    social_row = pd.DataFrame([['Social','-','-']], columns=['indicator','unit','complement'])
    env_row = pd.DataFrame([['Environment','-','-']], columns=['indicator','unit','complement'])
    
    df_total = pd.concat([gov_row,df1,social_row,df2,env_row,df3], axis=0).reset_index(drop=True)
    
    return df_total

def check_valid_data():
    return True

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
            checked_password = check_password_hash(hash_password, password)
            break
    if user_id == None:
        return jsonify({"status": "Error", "message": "User not found!"}), 404

    if checked_password:
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
def overview():
    data = get_csv_head_data()
    head_gov = data["gov"][0:5]
    head_social = data["social"][0:5]
    head_env = data["env"][0:5]
    
    response = {
        "gov": head_gov,
        "social": head_social,
        "env": head_env
    }

    return response, 200

@app.route("/layer/E")
@required_token
def layerE():
    data = get_csv_head_data()
    env_data = data["env"]
    
    response = {
        "env": env_data
    }
    
    return response, 200

@app.route("/layer/S")
@required_token
def layerS():
    data = get_csv_head_data()
    social_data = data["social"]
    
    response = {
        "social": social_data
    }
    
    return response, 200

@app.route("/layer/G")
@required_token
def layerG():
    data = get_csv_head_data()
    gov_data = data["gov"]
    
    response = {
        "gov": gov_data
    }
    
    return response, 200

### Falta daqui pra baixo

@app.route("/monitoring")
@required_token
def monitoring():
    return "monitoring"

@app.route("/email")
@required_token
def email():
    return "Email"

@app.route("/projection")
@required_token
def projection():
    return "projection"

@app.route("/report")
@required_token
def report():
    data = get_csv_head_data()
    df = data_to_dataframe(data)
    for i,r in df.iterrows():
        if str(r['complement']) == "-":
            pass
        elif str(r['complement']).upper() == 'R$':
            df.loc[i,'unit'] = f"{r['complement']}{r['unit']}"
        elif str(r['complement']).lower() == 'anos':
            df.loc[i,'unit'] = f"{r['unit']} {r['complement']}"
        else:
            df.loc[i,'unit'] = f"{r['unit']}{r['complement']}"
    
    df = df.drop(columns=['complement'])
    df.to_csv("./report.csv")
    
    return "report"

app.run(debug=True)