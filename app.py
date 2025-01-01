from flask import Flask, render_template, redirect, url_for, flash, session, request
from appsTools.login import login_user
from appsTools.factura import handle_factura, get_db_connection

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_user()

@app.route('/escritorio')
def escritorio():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('escritorio.html')

@app.route('/factura', methods=['GET', 'POST'])
def factura():
    return handle_factura()

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
