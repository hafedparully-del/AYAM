from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    # Mengambil user pertama yang mendaftar (kemungkinan besar akun Anda)
    user = User.query.first()
    if user:
        user.role = 'admin'
        db.session.commit()
        print(f"Berhasil! Akun '{user.name}' ({user.email}) sekarang adalah Admin.")
    else:
        print("Belum ada user yang terdaftar. Daftar dulu lewat browser.")