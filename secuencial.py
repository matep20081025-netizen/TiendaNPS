# ============================================================
# DIAGRAMA 1: ACCESO SECUENCIAL
# Inicio -> Ingresar producto -> Guardar registro en productos.txt
#        -> Listar productos del archivo -> ¿Actualizar precio?
#        (Si) -> Modificar registro -> Eliminar Registro
#        (No) -> Eliminar producto
#        -> Mostrar Archivo actualizado -> Fin
# ============================================================


def agregar_producto(id, nombre, categoria, precio, stock, proveedor):
    """Paso 'Ingresar producto' + 'Guardar registro en productos.txt'.
    Se escribe el registro al final del archivo (acceso secuencial)."""
    with open("productos.txt", "a", encoding="utf-8") as archivo:
        linea = f"{id},{nombre},{categoria},{precio},{stock},{proveedor}\n"
        archivo.write(linea)


def listar_productos():
    """Paso 'Listar productos del archivo'.
    Se recorre el archivo de principio a fin, en orden secuencial."""
    with open("productos.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split(",")
            print(campos)


def actualizar_producto(id_buscado, nuevo_precio):
    """Rama 'Yes' de ¿Actualizar precio? -> Modificar registro.
    Como es secuencial, no se puede editar en el lugar: se reescribe
    todo el archivo con el precio ya modificado."""
    lineas_nuevas = []
    with open("productos.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split(",")
            if campos[0] == str(id_buscado):
                campos[3] = str(nuevo_precio)
            lineas_nuevas.append(",".join(campos) + "\n")

    with open("productos.txt", "w", encoding="utf-8") as archivo:
        for linea in lineas_nuevas:
            archivo.write(linea)


def eliminar_producto(id_buscado):
    """Rama 'No' de ¿Actualizar precio? -> Eliminar producto.
    (También cubre el paso 'Eliminar Registro' de la rama 'Yes').
    Se reescribe el archivo omitiendo el registro con ese id."""
    lineas_nuevas = []
    with open("productos.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split(",")
            if campos[0] != str(id_buscado):
                lineas_nuevas.append(linea.strip())

    with open("productos.txt", "w", encoding="utf-8") as archivo:
        for linea in lineas_nuevas:
            archivo.write(linea + "\n")


if __name__ == "__main__":
    # Inicio del flujo del diagrama 1
    agregar_producto(1, "Camiseta", "Ropa", 45000, 30, "Textiles SA")
    agregar_producto(2, "Cuaderno", "Papeleria", 8000, 100, "Norma")
    agregar_producto(3, "Mouse", "Tecnologia", 35000, 50, "Logitech")

    listar_productos()  # Mostrar Archivo actualizado (antes de cambios)

    actualizar_producto(2, 9000)   # ¿Actualizar precio? -> Yes
    eliminar_producto(1)           # ¿Actualizar precio? -> No

    listar_productos()  # Mostrar Archivo actualizado (Fin)
