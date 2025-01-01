import sqlite3
from flask import request, render_template, session, redirect, url_for, flash, make_response
from datetime import datetime
from fpdf import FPDF

def get_db_connection():
    conn = sqlite3.connect('SalonBellezaLurvin.db')
    conn.row_factory = sqlite3.Row
    return conn

def handle_factura():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    productos_servicios = conn.execute('SELECT * FROM ProductosServicios').fetchall()
    if request.method == 'POST':
        nombre_cliente = request.form['nombre_cliente']
        productos_seleccionados = request.form.getlist('productos_servicios')
        tipo_pago = request.form['tipo_pago']
        total_factura = 0
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M:%S")
        factura_id = None
        for producto_id in productos_seleccionados:
            producto = conn.execute('SELECT * FROM ProductosServicios WHERE id = ?', (producto_id,)).fetchone()
            total_factura += producto['Precio']
            cursor = conn.execute('''
                INSERT INTO FacturasClientes (ProductoServicio, Descripcion, Precio, Nombre, IdCliente, TipoPago, TotalFactura, Fecha, Hora)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (producto['ProductoServicio'], producto['Descripcion'], producto['Precio'], nombre_cliente, session['user_id'], tipo_pago, total_factura, fecha, hora))
            if factura_id is None:
                factura_id = cursor.lastrowid
        conn.commit()
        flash('Factura generada exitosamente', 'success')
        
        # Generar PDF de la factura
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Título
        pdf.cell(200, 10, txt="Salon Belleza Lurvin", ln=True, align='C')
        
        # Información de la factura
        pdf.cell(200, 10, txt=f"Factura ID: {factura_id}", ln=True)
        pdf.cell(200, 10, txt=f"Nombre: {nombre_cliente}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha: {fecha}", ln=True)
        pdf.cell(200, 10, txt=f"Hora: {hora}", ln=True)
        
        # Tabla de productos/servicios
        pdf.cell(200, 10, txt="Productos/Servicios:", ln=True)
        for producto_id in productos_seleccionados:
            producto = conn.execute('SELECT * FROM ProductosServicios WHERE id = ?', (producto_id,)).fetchone()
            pdf.cell(200, 10, txt=f"{producto['ProductoServicio']} - {producto['Descripcion']} - L{producto['Precio']}", ln=True)
        
        # Total a pagar
        pdf.cell(200, 10, txt=f"Total a Pagar: L{total_factura}", ln=True)
        
        # Tipo de pago
        pdf.cell(200, 10, txt=f"Tipo de Pago: {tipo_pago}", ln=True)
        
        response = make_response(pdf.output(dest='S').encode('latin1'))
        response.headers.set('Content-Disposition', 'attachment', filename='factura.pdf')
        response.headers.set('Content-Type', 'application/pdf')
        
        return response
        
    conn.close()
    return render_template('factura.html', productos_servicios=productos_servicios)
