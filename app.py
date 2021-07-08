from flask import (Flask, Blueprint, render_template,request)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bp = Blueprint('app', __name__)

user = 'fjypjyda'
password = 'u4Yw8ZN6AE5LTDDGctdM1yfeYRQNAwqH'
host = 'tuffi.db.elephantsql.com'
database = 'fjypjyda'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secreta'

db = SQLAlchemy(app)

class anos_dourados(db.Model):

  id = db.Column(db.Integer, primary_key = True)
  nome = db.Column(db.String(50), nullable = False)
  url_imagem = db.Column(db.String(255), nullable = False)
  ano_lancamento = db.Column(db.String(255), nullable = False)
  infancia_do = db.Column(db.String(255), nullable = False)
  trailer_desenho = db.Column(db.String(255), nullable = False)

  def __init__(self, nome, url_imagem, ano_lancamento, infancia_do, trailer_desenho):
    self.nome = nome
    self.url_imagem = url_imagem
    self.ano_lancamento = ano_lancamento
    self.infancia_do = infancia_do
    self.trailer_desenho = trailer_desenho.replace("watch?v=", "embed/", len(trailer_desenho))

  @staticmethod
  def read_all():
    return anos_dourados.query.order_by(anos_dourados.id.asc()).all()

  @staticmethod
  def read_single(desenho_id):
    return anos_dourados.query.get(desenho_id)
  
  def save(self): 
    db.session.add(self) 
    db.session.commit()

  def update(self, new_data):
    self.nome = new_data.nome
    self.url_imagem = new_data.url_imagem
    self.ano_lancamento = new_data.ano_lancamento
    self.infancia_do = new_data.infancia_do
    self.trailer_desenho = new_data.trailer_desenho
    self.save()

  def delete(self):
    db.session.delete(self) # estamos removendo as informações de um filme do banco de dados
    db.session.commit()
  
@bp.route('/')
def home():
  return render_template('index.html')

@bp.route('/read')
def listar_anos_dourados():
  desenhos = anos_dourados.read_all()
  return render_template('listar-desenhos.html', listaDeDesenhos=desenhos) # Passando para dentro do nosso HTML os dados da minha listagem de filmes!!!!

@bp.route('/read/<desenho_id>')
def lista_detalhe_filme(desenho_id):
  desenho = anos_dourados.read_single(desenho_id)
  return render_template('read_single.html', desenho=desenho)

@bp.route('/create', methods=('GET', 'POST'))
def create():

  id_atribuido = None
  if request.method =='POST':
    form=request.form
    desenhos = anos_dourados(form['nome'],form['url_imagem'],form['ano_lancamento'],form['infancia_do'],form['trailer_desenho']) 
    desenhos.save()
    id_atribuido=desenhos.id
  return render_template('create.html', id_atribuido=id_atribuido)

@bp.route('/update/<desenho_id>',methods=('GET', 'POST'))
def update(desenho_id):
  sucesso = None
  Desenho = anos_dourados.read_single(desenho_id)  

  if request.method =='POST':
    form=request.form
    new_data=anos_dourados(form['nome'],form['url_imagem'],form['ano_lancamento'],form['infancia_do'],form['trailer_desenho'])  
    Desenho.update(new_data)
    sucesso = True
  return render_template('update.html', desenho=Desenho,sucesso=sucesso)

@bp.route('/delete/<desenho_id>') 
def delete(desenho_id):
  desenho = anos_dourados.read_single(desenho_id)
  return render_template('delete.html', desenho=desenho)

@bp.route('/delete/<desenho_id>/confirmed') 
def delete_confirmed(desenho_id):
  sucesso = None
  desenho = anos_dourados.read_single(desenho_id)

  if desenho:
    desenho.delete()
    sucesso = True
  return render_template('delete.html', desenho=desenho, sucesso=sucesso)








# Pega os dados do blueprint da nossa aplicação (nome do app e as rotas) e registra dentro do app do Flask
app.register_blueprint(bp)


if __name__ == '__main__':
  app.run(debug=True)
