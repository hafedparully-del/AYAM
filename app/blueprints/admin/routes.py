from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import Product
from app.extensions import db
from app.utils import role_required
from . import bp

@bp.route('/dashboard')
@login_required
@role_required('admin') # Hanya bisa diakses oleh role admin
def dashboard():
    products = Product.query.all()
    return render_template('dashboard.html', title='Admin Dashboard', products=products)

@bp.route('/product/delete/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash(f'Produk {product.name} berhasil dihapus!', 'success')
    return redirect(url_for('admin.dashboard'))