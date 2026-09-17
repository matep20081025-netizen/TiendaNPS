# ============================================================
# DIAGRAMA 3: ORDENAMIENTO EXTERNO POR SELECCIÓN
# Inicio -> Contar Registros del archivo entrada
#        -> Buscar el menor registro no usado
#        -> Escribir registro en archivo ordenado
#        -> Marcar registro como utilizado
#        -> ¿Quedan Registros? (Yes) Repetir / (No) Fin
# ============================================================


def agregar_para_ordenar(id, nombre, proveedor, categoria, anio, precio):
    """Prepara el archivo de entrada. El primer campo (0) es la
    bandera de 'usado', que se irá marcando en 1 a medida que cada
    registro se copie al archivo ordenado."""
    with open("productos_usados.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"0,{id},{nombre},{proveedor},{categoria},{anio},{precio}\n")


def contar_registros(archivo):
    """Paso 'Contar Registros del archivo entrada'."""
    total = 0
    with open(archivo, "r", encoding="utf-8") as archivo_full:
        for _ in archivo_full:
            total += 1
    return total


def buscar_minimo_no_usado(archivo, indice_campo):
    """Paso 'Buscar el menor registro no usado'.
    Recorre todo el archivo de entrada y se queda con el registro
    más pequeño (según indice_campo) entre los que no han sido usados."""
    minimo = None

    with open(archivo, "r", encoding="utf-8") as archivo_full:
        for linea in archivo_full:
            campos = linea.strip().split(",")
            if campos[0] == "1":   # ya fue usado, se ignora
                continue

            valor = int(campos[indice_campo])
            if minimo is None or valor < minimo[1]:
                minimo = (campos, valor)

    return minimo[0] if minimo is not None else None


def marcar_usado(archivo, id_registro):
    """Paso 'Marcar registro como utilizado': pone la bandera en 1
    para que 'buscar_minimo_no_usado' no lo vuelva a elegir."""
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
    """Flujo completo del diagrama 3.
    Se repite 'Buscar el menor -> Escribir -> Marcar usado' tantas
    veces como registros haya (¿Quedan Registros? -> Repetir/Fin)."""
    total = contar_registros(archivo_entrada)          # Contar Registros
    with open(archivo_salida, "w", encoding="utf-8") as archivo_ordenado:
        for _ in range(total):
            registro = buscar_minimo_no_usado(archivo_entrada, indice_campo)
            if registro is None:                       # ¿Quedan Registros? -> No
                break
            archivo_ordenado.write(",".join(registro) + "\n")  # Escribir registro
            marcar_usado(archivo_entrada, registro[1])          # Marcar como utilizado
            # ¿Quedan Registros? -> Yes -> Repetir (vuelve al for)


if __name__ == "__main__":
    agregar_para_ordenar(1, "Camiseta", "Textiles SA", "Ropa", 2022, 45000)
    agregar_para_ordenar(2, "Cuaderno", "Norma", "Papeleria", 2023, 8000)
    agregar_para_ordenar(3, "Mouse", "Logitech", "Tecnologia", 2021, 35000)

    # indice_campo=6 -> se ordena por precio
    ordenar_externa("productos_usados.txt", "productos_ordenados.txt", 6)

    with open("productos_ordenados.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            print(linea.strip())
