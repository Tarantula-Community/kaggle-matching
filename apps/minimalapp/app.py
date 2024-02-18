from email_validator import validate_email, EmailNotValidError
from flask import Flask, render_template, url_for, current_app, g, request, redirect, flash, make_response, session
import logging
import os
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message
app = Flask(__name__)
app.config['SECRET_KEY'] = '2AZSMss3p5QpbcY2hBsJ'
# ログレベルを設定
app.logger.setLevel(logging.DEBUG)
# リダイレクトを中断しないようにする
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# flask-mail拡張を登録する
mail = Mail(app)
# DebugToolbarExtensionにアプリケーションをセットする
toolbar = DebugToolbarExtension(app)

@app.route('/')
def index():
  return "Hello, Flask!"

@app.route('/hello/<name>', methods=['GET', 'POST'], endpoint='hello-endpoint')
def hello(name):
  return f"Hello, {name}!"

@app.route('/name/<name>')
def show_name(name):
  return render_template('index.html', name=name)

with app.test_request_context():
  print(url_for('index'))
  
  print(url_for('hello-endpoint', name='workd'))
  
  print(url_for('show_name', name='ichiro', page='1'))
  
ctx = app.app_context()
ctx.push()

print(current_app.name)

g.conection = 'connection'
print(g.conection)

with app.test_request_context('/users?updated=true'):
  print(request.args.get('updated'))
  
@app.route('/contact')
def contact():
  response = make_response(render_template('contact.html'))
  # クッキーを設定
  response.set_cookie('kagglematching key', 'kagglematching value')
  session['username'] = "ichiro"
  return response

@app.route('/contact/complete', methods=['POST', 'GET'])
def contact_complete():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    description = request.form['description']
    
    is_valid = True
    if not username:
      flash('ユーザー名は必須です')
      is_valid = False
      
    if not email:
      flash('メールアドレスは必須です')
      is_valid = False
      
    try:
      validate_email(email)
    except EmailNotValidError as e:
      flash('メールアドレスの形式で入力してください')
      is_valid = False
      
    if not description:
      flash('問い合わせ内容は必須です')
      is_valid = False
      
    if not is_valid:
      return redirect(url_for('contact'))
    # メールを送る
    send_email(
      email,
      "お問い合わせありがとうございます",
      "contact_mail",
      username=username,
      description=description,
    )
    
    flash("問い合わせ内容はメールに送信されました。問い合わせありがとうございます。")
    # contactエンドポイントにリダイレクト
    return redirect(url_for('contact_complete'))
  
  return render_template('contact_complete.html')

def send_email(to, subject, template, **kwargs):
  msg = Message(
    subject,
    recipients=[to]
    )
  msg.body = render_template(template + ".txt", **kwargs)
  msg.html = render_template(template + ".html", **kwargs)
  mail.send(msg)