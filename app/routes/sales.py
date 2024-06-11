import io
from flask import request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from app import db
from app.models import Sale, User
from app.routes import sales_bp

@sales_bp.route('/sales', methods=['GET'])
@jwt_required()
def get_sales():
    user_id = get_jwt_identity()
    sales = Sale.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': sale.id,
        'nome_cliente': sale.client_name,
        'produto': sale.product,
        'valor': sale.amount,
        'data_venda': sale.sale_date
    } for sale in sales]), 200

@sales_bp.route('/sales', methods=['POST'])
@jwt_required()
def add_sale():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_sale = Sale(
        client_name=data['nome_cliente'],
        product=data['produto'],
        amount=data['valor'],
        sale_date=data['data_venda'],
        user_id=user_id
    )
    db.session.add(new_sale)
    db.session.commit()
    return jsonify({'message': 'Sale added successfully'}), 201

@sales_bp.route('/sales/<int:id>', methods=['PUT'])
@jwt_required()
def update_sale(id):
    user_id = get_jwt_identity()
    sale = Sale.query.filter_by(id=id, user_id=user_id).first()

    if sale is None:
        return jsonify({'message': 'Sale not found'}), 404

    data = request.get_json()
    sale.client_name = data.get('nome_cliente', sale.client_name)
    sale.product = data.get('produto', sale.product)
    sale.amount = data.get('valor', sale.amount)
    sale.sale_date = data.get('data_venda', sale.sale_date)
    db.session.commit()
    return jsonify({'message': 'Sale updated successfully'}), 200

@sales_bp.route('/sales/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_sale(id):
    user_id = get_jwt_identity()
    sale = Sale.query.filter_by(id=id, user_id=user_id).first()

    if sale is None:
        return jsonify({'message': 'Sale not found'}), 404

    db.session.delete(sale)
    db.session.commit()
    return jsonify({'message': 'Sale deleted successfully'}), 200

@sales_bp.route('/sales/pdf', methods=['GET'])
@jwt_required()
def generate_sales_pdf():
    user_id = get_jwt_identity()
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    try:
        start_date = datetime.strptime(start_date_str, '%d-%m-%Y')
        end_date = datetime.strptime(end_date_str, '%d-%m-%Y')
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use DD-MM-YYYY.'}), 400
    
    sales = Sale.query.filter(Sale.user_id == user_id, Sale.sale_date >= start_date, Sale.sale_date <= end_date).all()
    
    if not sales:
        return jsonify({'message': 'No sales found in the given date range.'}), 404
    
    pdf_buffer = io.BytesIO()
    p = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter
    
    p.drawString(30, height - 50, f'Sales Report from {start_date_str} to {end_date_str}')
    p.drawString(30, height - 80, 'ID    Client Name    Product    Amount    Sale Date')
    
    y_position = height - 100
    for sale in sales:
        p.drawString(30, y_position, f'{sale.id}    {sale.client_name}    {sale.product}    {sale.amount}    {sale.sale_date.strftime("%d-%m-%Y")}')
        y_position -= 20
        if y_position < 50:  # Create a new page if necessary
            p.showPage()
            p.drawString(30, height - 50, f'Sales Report from {start_date_str} to {end_date_str}')
            p.drawString(30, height - 80, 'ID    Client Name    Product    Amount    Sale Date')
            y_position = height - 100

    p.save()
    
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, as_attachment=True, download_name='sales_report.pdf', mimetype='application/pdf')
