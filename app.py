import os
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    query = request.args.get('medicine', '').strip()
    category = request.args.get('category', 'human').strip()
    if not query:
        return jsonify({'results': [], 'source': 'none'})

    conn = get_db()
    rows = conn.execute(
        """
        SELECT m.name AS medicine_name,
               p.name AS pharmacy_name,
               p.address,
               p.phone,
               p.lat,
               p.lng,
               m.last_updated_timestamp
        FROM medicines m
        JOIN pharmacies p ON m.pharmacy_id = p.id
        WHERE LOWER(m.name) LIKE ? AND m.category = ?
        """,
        (f'%{query.lower()}%', category)
    ).fetchall()
    conn.close()

    if rows:
        results = [
            {
                'medicine': row['medicine_name'],
                'pharmacy': row['pharmacy_name'],
                'address': row['address'],
                'phone': row['phone'],
                'lat': row['lat'],
                'lng': row['lng'],
                'last_updated': row['last_updated_timestamp']
            }
            for row in rows
        ]
        return jsonify({'results': results, 'source': 'verified'})

    return jsonify({'results': [], 'source': 'fallback'})


@app.route('/medicines')
def medicines():
    category = request.args.get('category', 'human').strip()

    conn = get_db()
    rows = conn.execute(
        """
        SELECT DISTINCT m.name, COUNT(DISTINCT m.pharmacy_id) AS shop_count
        FROM medicines m
        WHERE m.category = ?
        GROUP BY m.name
        ORDER BY m.name
        """,
        (category,)
    ).fetchall()
    conn.close()

    result = [{'name': row['name'], 'shops': row['shop_count']} for row in rows]
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
