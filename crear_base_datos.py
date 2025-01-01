import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('SalonBellezaLurvin.db')
cursor = conn.cursor()

# Eliminar la tabla FacturasClientes si existe
cursor.execute('DROP TABLE IF EXISTS FacturasClientes')

# Crear la tabla FacturasClientes con las nuevas columnas
cursor.execute('''
CREATE TABLE FacturasClientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductoServicio TEXT,
    Descripcion TEXT,
    Precio REAL,
    Nombre TEXT,
    IdCliente INTEGER,
    TipoPago TEXT,
    TotalFactura REAL,
    Fecha TEXT,
    Hora TEXT
)
''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("La tabla FacturasClientes ha sido eliminada y creada con las nuevas columnas exitosamente.")
