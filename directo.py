# ============================================================
# DIAGRAMA 2: ACCESO DIRECTO
# Inicio -> Solicitar ID del producto -> Calcular posición del registro
#        -> Ir directamente a la posición buscada -> Leer registro
#        -> ¿Registro activo? (Yes) Mostrar datos / (No) Mostrar eliminado
#        -> Fin
# ============================================================

# Cada registro ocupa siempre el mismo tamaño en bytes, por eso se
# puede calcular su posición exacta en el archivo (id-1) * REGISTRO_LEN.
REGISTRO_LEN = 71


def construir_registro(activo, id, nombre, proveedor, stock, precio, categoria):
    """Arma un registro de longitud fija, con espacios de relleno,
    para que todos ocupen exactamente REGISTRO_LEN bytes."""
    return (
        str(activo).ljust(1) +
        str(id).zfill(4) +
        nombre[:20].ljust(20) +
        proveedor[:15].ljust(15) +
        str(stock).zfill(5) +
        str(precio).zfill(8) +
        categoria[:10].ljust(10) +
        "\n"
    )


def agregar_directo(id, nombre, proveedor, stock, precio, categoria):
    """Paso 'Calcular posición del registro' + 'Ir directamente a la
    posición buscada': se ubica con seek() y se escribe ahí mismo."""
    registro = construir_registro(1, id, nombre, proveedor, stock, precio, categoria)
    with open("productos_directo.txt", "r+", encoding="utf-8") as archivo:
        archivo.seek((id - 1) * REGISTRO_LEN)
        archivo.write(registro)


def leer_directo(id):
    """Flujo completo del diagrama 2: Solicitar ID -> Calcular posición
    -> Ir directamente a la posición -> Leer registro -> ¿Registro activo?"""
    with open("productos_directo.txt", "r", encoding="utf-8") as archivo:
        archivo.seek((id - 1) * REGISTRO_LEN)          # Ir directamente a la posición
        registro = archivo.read(REGISTRO_LEN)           # Leer registro
        activo = registro[0:1]

        if activo == "0":                                # ¿Registro activo? -> No
            print(f"Registro {id}: ELIMINADO")
            return

        # ¿Registro activo? -> Yes -> Mostrar datos
        nombre = registro[5:25].strip()
        proveedor = registro[25:40].strip()
        stock = registro[40:45].strip()
        precio = registro[45:53].strip()
        categoria = registro[53:63].strip()

        print(nombre, " - ", proveedor, " - ", categoria, " - ", precio, " - ", stock)


def actualizar_directo(id, nombre):
    """Va directo a la posición del registro, lee sus datos actuales,
    y los reescribe con el nombre nuevo (sin mover ningún otro registro)."""
    with open("productos_directo.txt", "r+", encoding="utf-8") as archivo:
        archivo.seek((id - 1) * REGISTRO_LEN)
        registro = archivo.read(REGISTRO_LEN)
        activo = registro[0:1]
        proveedor = registro[25:40].strip()
        stock = registro[40:45].strip()
        precio = registro[45:53].strip()
        categoria = registro[53:63].strip()

        nuevo_registro = construir_registro(
            activo, id, nombre, proveedor, stock, precio, categoria
        )

        archivo.seek((id - 1) * REGISTRO_LEN)
        archivo.write(nuevo_registro)


def eliminar_directo(id):
    """Va directo a la posición del registro y solo cambia su bandera
    de 'activo' a '0' (borrado lógico, sin mover el resto del archivo)."""
    with open("productos_directo.txt", "r+", encoding="utf-8") as archivo:
        archivo.seek((id - 1) * REGISTRO_LEN)
        archivo.write("0")


if __name__ == "__main__":
    # Se crea el archivo si no existe, antes de escribir por posición
    open("productos_directo.txt", "a", encoding="utf-8").close()

    agregar_directo(1, "Camiseta", "Textiles SA", 30, 45000, "Ropa")
    agregar_directo(2, "Cuaderno", "Norma", 100, 8000, "Papeleria")
    agregar_directo(3, "Mouse", "Logitech", 50, 35000, "Tecnologia")

    actualizar_directo(2, "Cuaderno A5")
    leer_directo(2)      # Registro activo -> Mostrar datos

    eliminar_directo(1)
    leer_directo(1)      # Registro eliminado -> Mostrar eliminado
