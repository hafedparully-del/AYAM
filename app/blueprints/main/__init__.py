from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('base.html', title='Katalog Ayam')
from flask import Blueprint, render_template
from app.models import Product

# Tambahkan template_folder agar Flask tahu letak file HTML-nya
bp = Blueprint('main', __name__, template_folder='../../templates/main')

@bp.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', title='Katalog Produk', products=products)