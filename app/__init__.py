import os
from flask import Flask
from sqlalchemy import event
from sqlalchemy.engine import Engine
from .config import Config
from .extensions import db, login_manager, csrf


# Optimasi SQLite WAL Mode untuk konkurensi produksi
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    # Buat direktori instance database jika belum ada
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

        # Pastikan blok ini hanya tertulis SATU KALI
        from app.blueprints.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')

        from app.blueprints.main import bp as main_bp
        app.register_blueprint(main_bp)

        # Tambahkan dua baris ini:
        from app.blueprints.customer import bp as customer_bp
        app.register_blueprint(customer_bp, url_prefix='/customer')

        # Tambahkan dua baris ini:
        from app.blueprints.admin import bp as admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

        with app.app_context():
            db.create_all()

        return app
