from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Menambahkan kolom payment_method ke tabel order yang sudah ada
        db.session.execute(text("ALTER TABLE `order` ADD COLUMN payment_method VARCHAR(50) DEFAULT 'QRIS'"))
        db.session.commit()
        print("Mantap! Kolom metode pembayaran berhasil ditambahkan ke database.")
    except Exception as e:
        print("Info: Kolom sudah ada atau terjadi kesalahan:", e)