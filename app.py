from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'clave_secreta'

MAX_INTENTOS = 3
USUARIO_CORRECTO = 'dani'
PASSWORD_CORRECTO = 'tristan'

@app.route('/')
def index():
    if 'intentos' not in session:
        session['intentos'] = 0
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    password = request.form['password']

    if 'intentos' not in session:
        session['intentos'] = 0

    session['intentos'] += 1

    if usuario.lower() == USUARIO_CORRECTO.lower() and password.lower() == PASSWORD_CORRECTO.lower():
        session.pop('intentos', None)  # Reinicia los intentos si acierta
        session['usuario'] = usuario
        return redirect(url_for('dashboard'))
    else:
        if session['intentos'] < MAX_INTENTOS:
            flash(f"Contraseña incorrecta. Intento {session['intentos']} de {MAX_INTENTOS}")
        else:
            flash(f"Has alcanzado el máximo de {MAX_INTENTOS} intentos. Intenta más tarde.")
            session.pop('intentos')  # Reinicia intentos después de agotarlos
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return render_template('dashboard.html', usuario=session['usuario'])
    return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
