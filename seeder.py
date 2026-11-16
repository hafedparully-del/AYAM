from app import create_app
from app.extensions import db
from app.models import Product

app = create_app()

with app.app_context():
    # Pastikan data bersih dari sisa-sisa sebelumnya
    Product.query.delete()

    # Tambahkan data produk ayam yang baru
    produk_baru = [
        Product(name='Ati Ampela', category='Sampingan', price_per_unit=25000.0, unit_type='kg', stock_available=35,
                image_file='ATIAMPELA.png'),
        Product(name='Ceker Ayam Bersih', category='Sampingan', price_per_unit=22000.0, unit_type='kg',
                stock_available=60, image_file='CEKER.png'),
        Product(name='Kepala Ayam', category='Sampingan', price_per_unit=15000.0, unit_type='kg', stock_available=30,
                image_file='KEPALA.png')
    ]

    db.session.bulk_save_objects(produk_baru)
    db.session.commit()
    print("Mantap! Data produk sampingan berhasil dimasukkan ke Kandang.")