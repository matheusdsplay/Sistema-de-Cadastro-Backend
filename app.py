from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configura o banco SQLite local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hash da senha

# Cria o banco e as tabelas (garante que existam)
with app.app_context():
    db.create_all()

# Suas rotas começam aqui
# Rota para página inicial (login)
@app.route('/', methods=['GET', 'POST'])
def home():
    nome = "Visitante"
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return redirect(url_for('dashboard', nome=user.name))
        else:
            return render_template('index.html', nome=nome, error='Email ou senha incorretos!')
    return render_template('index.html', nome=nome)

# Rota para criar usuário via API
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'error': 'Faltando dados'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email já cadastrado'}), 409

    hashed_password = generate_password_hash(password)
    user = User(name=name, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 201

# Rota para listar todos usuários
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{'id': u.id, 'name': u.name, 'email': u.email} for u in users]
    return jsonify(result)

# Rota para atualizar usuário
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    # Em caso real, valide se o novo email não existe em outro usuário

    db.session.commit()

    return jsonify({'id': user.id, 'name': user.name, 'email': user.email})

# Rota para deletar usuário
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Usuário deletado'})

# Saudação via formulário
@app.route('/saudacao', methods=['POST'])
def saudacao_post():
    nome = request.form.get('nome')
    if not nome:
        nome = 'Visitante'
    return redirect(url_for('saudacao', nome=nome))

@app.route('/saudacao/<nome>')
def saudacao(nome):
    return render_template('saudacao.html', nome=nome)

# Registro de novo usuário via formulário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([name, email, password]):
            return render_template('register.html', error='Preencha todos os campos!')

        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email já cadastrado!')

        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('register.html')

# Página de login separada (opcional)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return redirect(url_for('dashboard', nome=user.name))
        else:
            return render_template('login.html', error='Email ou senha incorretos!')

    return render_template('login.html')

@app.route('/dashboard/<nome>')
def dashboard(nome):
    return render_template('dashboard.html', nome=nome)

if __name__ == '__main__':
    app.run(debug=True)
