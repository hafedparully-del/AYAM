from app import create_app
from app.models import Product
from app.extensions import db

app = create_app()

with app.app_context():
    # Menghubungkan foto Ati Ampela
    ati = Product.query.filter(Product.name.ilike('%Ati Ampela%')).first()
    if ati:
        ati.image_file = 'ATIAMPELA.png'
        print(f"Foto berhasil ditambahkan ke: {ati.name}")

    # Menghubungkan foto Ceker Ayam
    ceker = Product.query.filter(Product.name.ilike('%Ceker%')).first()
    if ceker:
        ceker.image_file = 'CEKER.png'
        print(f"Foto berhasil ditambahkan ke: {ceker.name}")

    # Menghubungkan foto Kepala Ayam
    kepala = Product.query.filter(Product.name.ilike('%Kepala%')).first()
    if kepala:
        kepala.image_file = 'KEPALA.png'
        print(f"Foto berhasil ditambahkan ke: {kepala.name}")

    # Simpan perubahan ke database
    db.session.commit()
    print("Semua foto selesai diperbarui di database!")