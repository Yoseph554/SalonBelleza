from flask import request, redirect, url_for, flash, session, render_template
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('SalonBellezaLurvin.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_user():
    if request.method == 'POST':
        user_or_email = request.form['user_or_email']
        password_or_code = request.form['password_or_code']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Usuarios WHERE (usuario = ? OR email = ?) AND (contrasena = ? OR codigo = ?)', 
                            (user_or_email, user_or_email, password_or_code, password_or_code)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('escritorio'))
        else:
            flash('Usuario, correo o contraseña incorrectos', 'danger')
    return render_template('login.html')
