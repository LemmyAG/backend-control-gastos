from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from datetime import date

app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True)

def conectar():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='control_gastos'
    )

@app.route('/transacciones', methods=['GET'])
def obtener():
    db = conectar()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM transacciones ORDER BY fecha DESC")
    filas = cursor.fetchall()
    db.close()
    resultado = []
    for f in filas:
        resultado.append({
            'id': f[0],
            'tipo': f[1],
            'modo': f[2],
            'categoria': f[3],
            'monto': float(f[4]),
            'descripcion': f[5],
            'fecha': str(f[6])
        })
    return jsonify(resultado)

@app.route('/transacciones', methods=['POST'])
def agregar():
    d = request.json
    db = conectar()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO transacciones (tipo, modo, categoria, monto, descripcion, fecha) VALUES (%s, %s, %s, %s, %s, %s)",
        (d['tipo'], d['modo'], d['categoria'], d['monto'], d.get('descripcion', ''), date.today())
    )
    db.commit()
    db.close()
    return jsonify({'ok': True})

@app.route('/transacciones/<int:id>', methods=['PUT'])
def actualizar(id):
    d = request.json
    db = conectar()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE transacciones SET tipo=%s, modo=%s, categoria=%s, monto=%s, descripcion=%s WHERE id=%s",
        (d['tipo'], d['modo'], d['categoria'], d['monto'], d.get('descripcion', ''), id)
    )
    db.commit()
    db.close()
    return jsonify({'ok': True})

@app.route('/transacciones/<int:id>', methods=['DELETE'])
def eliminar(id):
    db = conectar()
    cursor = db.cursor()
    cursor.execute("DELETE FROM transacciones WHERE id=%s", (id,))
    db.commit()
    db.close()
    return jsonify({'ok': True})

@app.route('/categorias', methods=['GET'])
def obtener_categorias():
    db = conectar()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categorias")
    filas = cursor.fetchall()
    db.close()
    resultado = []
    for f in filas:
        resultado.append({
            'id': f[0],
            'nombre': f[1],
            'tipo': f[2]
        })
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True, port=5000)