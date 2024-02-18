from pathlib import Path
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config

# LoginManagerをインスタンス化する
login_manager = LoginManager()
# login_view属性に未ログイン時にリダイレクトするエンドポイントを設定する
login_manager.login_view = "auth.signup"
# login_message属性にログイン後に表示するメッセージを設定する
# ここでは何も表示しないように空を指定する
login_manager.login_message = ""

# SQLAlchemyの初期化
db = SQLAlchemy()

csrf = CSRFProtect()

def create_app(config_key):
  app = Flask(__name__)
  # アプリのコンフィグを設定する
  app.config.from_object(config[config_key])
  csrf.init_app(app)
  db.init_app(app)
  Migrate(app, db)
  
  # login_managerをアプリケーションと連携する
  login_manager.init_app(app)
  
  from apps.crud import views as crud_views
  app.register_blueprint(crud_views.crud, url_prefix='/crud')
  
  from apps.auth import views as auth_views
  app.register_blueprint(auth_views.auth, url_prefix='/auth')
  
  return app