from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="data",
        user="postgres",
        password=""
    )
    return conn

@app.route('/')
def home():
    query = """
        SELECT * FROM data
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

def fetch_data(state, date=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if date:
        query = """
            SELECT state, suspected, tested, confirmed, deaths
            FROM data
            WHERE state = %s AND date = %s
        """
        cursor.execute(query, (state, date))
    else:
        query = """
            SELECT state, suspected, tested, confirmed, deaths
            FROM data
            WHERE state = %s
        """
        cursor.execute(query, (state,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data

@app.route('/api/data', methods=['GET'])
def get_covid_data():
    state = request.args.get('state')
    date = request.args.get('date')
    if not state:
        return jsonify({'error': 'State parameter is required'}), 400

    data = fetch_data(state, date)

    if data:
        return jsonify({
            'state': data[0],
            'suspected': data[1],
            'tested': data[2],
            'confirmed': data[3],
            'deaths': data[4]
        })
    else:
        return jsonify({'error': 'No data found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
