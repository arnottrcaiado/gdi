
from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__)

# Caminho para o arquivo CSV onde os dados serão salvos
# Define o caminho absoluto para o arquivo CSV na pasta 'data'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'data', 'submissions.csv')
LIFECYCLE_CSV = os.path.join(BASE_DIR, 'data', 'lifecycle_data.csv')

# Rota para exibir o formulário principal
@app.route('/')
def form():
    return render_template('form.html')

# Rota para exibir o formulário de mapeamento do ciclo de vida das informações
@app.route('/ciclo')
def map_lifecycle_form():
    return render_template('map_lifecycle_form.html')

# Rota para processar o formulário principal e salvar os dados
@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.form.to_dict()
    save_to_csv(data, CSV_FILE)
    return "Formulário enviado com sucesso!"

# Rota para processar o formulário de mapeamento do ciclo de vida das informações e salvar os dados
@app.route('/submit_lifecycle', methods=['POST'])
def submit_lifecycle():
    data = request.form.to_dict()
    save_to_csv(data, LIFECYCLE_CSV)
    return "Mapeamento do ciclo de vida das informações enviado com sucesso!"

# Função para salvar os dados no arquivo CSV usando ';' como separador
def save_to_csv(data, file_path):
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys(), delimiter=';')  # Usando ';' como separador
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# Rota para obter os dados do formulário principal em formato JSON
@app.route('/data', methods=['GET'])
def get_data():
    record = request.args.get('record', 'all')
    return read_csv_data(CSV_FILE, record)

# Rota para obter os dados de mapeamento do ciclo de vida das informações em formato JSON
@app.route('/dataciclo', methods=['GET'])
def get_lifecycle_data():
    record = request.args.get('record', 'all')
    return read_csv_data(LIFECYCLE_CSV, record)

# Função para ler os dados do CSV e retornar em formato JSON
def read_csv_data(file_path, record):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')  # Usando ';' como separador
        data = list(reader)
        if record == 'all':
            return jsonify(data)
        else:
            try:
                record_index = int(record)
                if record_index < len(data):
                    return jsonify(data[record_index])
                else:
                    return jsonify({"error": "Registro não encontrado"}), 404
            except ValueError:
                return jsonify({"error": "Valor de 'record' inválido"}), 400

if __name__ == '__main__':
    app.run(debug=True)
