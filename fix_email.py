from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Mengubah nama kolom username menjadi email di tabel user
        db.session.execute(text("ALTER TABLE user RENAME COLUMN username TO email"))
        db.session.commit()
        print("Mantap! Kolom di database berhasil diubah menjadi email.")
    except Exception as e:
        print("Terjadi kesalahan atau kolom sudah pernah diubah:", e)