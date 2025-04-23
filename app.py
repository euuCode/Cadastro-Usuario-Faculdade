from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///produtos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200))
    estoque = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{
        'id': p.id,
        'nome': p.nome,
        'categoria': p.categoria,
        'preco': p.preco,
        'descricao': p.descricao,
        'estoque': p.estoque
    } for p in produtos])

@app.route('/api/produtos', methods=['POST'])
def adicionar_produto():
    data = request.json
    novo = Produto(
        nome=data['nome'],
        categoria=data['categoria'],
        preco=data['preco'],
        descricao=data.get('descricao', ''),
        estoque=data.get('estoque', 0)
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({'mensagem': 'Produto adicionado com sucesso!'})

@app.route('/api/produtos/<int:id>', methods=['PUT'])
def editar_produto(id):
    data = request.json
    produto = Produto.query.get_or_404(id)
    produto.nome = data['nome']
    produto.categoria = data['categoria']
    produto.preco = data['preco']
    produto.descricao = data.get('descricao', '')
    produto.estoque = data.get('estoque', 0)
    db.session.commit()
    return jsonify({'mensagem': 'Produto atualizado com sucesso!'})

@app.route('/api/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'mensagem': 'Produto removido com sucesso!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
