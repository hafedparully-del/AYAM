from flask import render_template, session, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Product, Order, OrderItem
from app.extensions import db
from . import bp


@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = str(data.get('product_id'))

    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    session.modified = True

    total_items = sum(cart.values())
    return jsonify({'status': 'success', 'total': total_items})


@bp.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0

    for p_id, qty in cart.items():
        product = Product.query.get(int(p_id))
        if product:
            subtotal = product.price_per_unit * qty
            total_price += subtotal
            cart_items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})

    return render_template('cart.html', title='Keranjang Belanja', cart_items=cart_items, total_price=total_price)


@bp.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    session.modified = True
    flash('Pesanan berhasil dibatalkan dan keranjang telah dikosongkan.', 'success')
    return redirect(url_for('customer.view_cart'))


@bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Keranjang Anda kosong.', 'warning')
        return redirect(url_for('customer.view_cart'))

    total_amount = 0

    # 1. Buat pesanan baru
    new_order = Order(user_id=current_user.id, status='Menunggu Konfirmasi')
    db.session.add(new_order)
    db.session.flush()

    # 2. Proses setiap barang di keranjang
    for p_id, qty in cart.items():
        product = Product.query.get(int(p_id))
        if product:
            subtotal = product.price_per_unit * qty
            total_amount += subtotal

            # Kurangi ketersediaan stok di database
            product.stock_available -= qty

            # Catat detail barang yang dibeli
            item = OrderItem(order_id=new_order.id, product_id=product.id, quantity=qty,
                             price_at_time=product.price_per_unit)
            db.session.add(item)

    # 3. Masukkan total harga ke pesanan
    new_order.total_amount = total_amount

    # 4. Tangkap metode pembayaran dari form HTML (Default: QRIS)
    payment_method = request.form.get('payment_method', 'QRIS')
    new_order.payment_method = payment_method

    # 5. Kosongkan keranjang setelah sukses
    session.pop('cart', None)
    session.modified = True

    db.session.commit()

    flash(f'Pesanan berhasil dibuat! Silakan lanjutkan pembayaran menggunakan {payment_method}.', 'success')
    return redirect(url_for('main.index'))