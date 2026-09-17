def agregar_producto(id, nombre, categoria, precio, stock, proveedor):
    with open("productos.txt", "a", encoding="utf-8") as archivo:
        linea = f"{id},{nombre},{categoria},{precio},{stock},{proveedor}\n"
        archivo.write(linea)


def listar_productos():
    with open("productos.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split(",")
            print(campos)


def actualizar_producto(id_buscado, nuevo_precio):
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
    lineas_nuevas = []
    with open("productos.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split(",")
            if campos[0] != str(id_buscado):
                lineas_nuevas.append(linea.strip())

    with open("productos.txt", "w", encoding="utf-8") as archivo:
        for linea in lineas_nuevas:
            archivo.write(linea + "\n")


def construir_registro(activo, id, nombre, proveedor, stock, precio, categoria):
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


REGISTRO_LEN = 71

with open("productos_directo.txt", "a", encoding="utf-8") as archivo:
    pass


def agregar_directo(id, nombre, proveedor, stock, precio, categoria):
    registro = construir_registro(1, id, nombre, proveedor, stock, precio, categoria)
    with open("productos_directo.txt", "r+", encoding="utf-8") as archivo:
        archivo.seek((id - 1) * REGISTRO_LEN)
        archivo.write(registro)


def leer_directo(id):
    with open("productos_directo.txt", "r", encoding="utf-8") as archivo:
        archivo.seek((id - 1) * REGISTRO_LEN)
        registro = archivo.read(REGISTRO_LEN)
        activo = registro[0:1]
        if activo == "0":
            print(f"Registro {id}: ELIMINADO")
            return
        nombre = registro[5:25].strip()
        proveedor = registro[25:40].strip()
        stock = registro[40:45].strip()
        precio = registro[45:53].strip()
        categoria = registro[53:63].strip()

        print(nombre, " - ", proveedor, " - ", categoria, " - ", precio, " - ", stock)


def actualizar_directo(id, nombre):
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
    with open("productos_directo.txt", "r+", encoding="utf-8") as archivo:
        archivo.seek((id - 1) * REGISTRO_LEN)
        archivo.write("0")


def agregar_para_ordenar(id, nombre, proveedor, categoria, anio, precio):
    with open("productos_usados.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"0,{id},{nombre},{proveedor},{categoria},{anio},{precio}\n")


def contar_registros(archivo):
    total = 0
    with open(archivo, "r", encoding="utf-8") as archivo_full:
        for _ in archivo_full:
            total += 1
    return total


def buscar_minimo_no_usado(archivo, indice_campo):
    minimo = None

    with open(archivo, "r", encoding="utf-8") as archivo_full:
        for linea in archivo_full:
            campos = linea.strip().split(",")
            if campos[0] == "1":
                continue

            valor = int(campos[indice_campo])
            if minimo is None or valor < minimo[1]:
                minimo = (campos, valor)

    return minimo[0] if minimo is not None else None


def marcar_usado(archivo, id_registro):
    lineas_nuevas = []
    with open(archivo, "r", encoding="utf-8") as archivo_full:
        for linea in archivo_full:
            campos = linea.strip().split(",")

            if campos[1] == id_registro:
                campos[0] = "1"
            lineas_nuevas.append(",".join(campos))

    with open(archivo, "w", encoding="utf-8") as archivo_full:
        for linea in lineas_nuevas:
            archivo_full.write(linea + "\n")


def ordenar_externa(archivo_entrada, archivo_salida, indice_campo):
    total = contar_registros(archivo_entrada)
    with open(archivo_salida, "w", encoding="utf-8") as archivo_ordenado:
        for _ in range(total):
            registro = buscar_minimo_no_usado(archivo_entrada, indice_campo)
            if registro is None:
                break
            archivo_ordenado.write(",".join(registro) + "\n")
            marcar_usado(archivo_entrada, registro[1])


if __name__ == "__main__":
    agregar_producto(1, "Camiseta", "Ropa", 45000, 30, "Textiles SA")
    agregar_producto(2, "Cuaderno", "Papeleria", 8000, 100, "Norma")
    agregar_producto(3, "Mouse", "Tecnologia", 35000, 50, "Logitech")
    listar_productos()
    actualizar_producto(2, 9000)
    eliminar_producto(1)
    listar_productos()

    agregar_directo(1, "Camiseta", "Textiles SA", 30, 45000, "Ropa")
    agregar_directo(2, "Cuaderno", "Norma", 100, 8000, "Papeleria")
    agregar_directo(3, "Mouse", "Logitech", 50, 35000, "Tecnologia")
    actualizar_directo(2, "Cuaderno A5")
    leer_directo(2)
    eliminar_directo(1)
    leer_directo(1)

    agregar_para_ordenar(1, "Camiseta", "Textiles SA", "Ropa", 2022, 45000)
    agregar_para_ordenar(2, "Cuaderno", "Norma", "Papeleria", 2023, 8000)
    agregar_para_ordenar(3, "Mouse", "Logitech", "Tecnologia", 2021, 35000)
    ordenar_externa("productos_usados.txt", "productos_ordenados.txt", 6)
    with open("productos_ordenados.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            print(linea.strip())
