from flask import Flask

app = Flask(__name__)

@app.route("/")
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