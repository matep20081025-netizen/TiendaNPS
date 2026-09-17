# ============================================================
# DIAGRAMA 5: RESUMEN GENERAL
# Inicio -> Registrar productos -> Guardar en archivo
#        -> Consultar o modificar datos -> Acceso directo a registros
#        -> Ordenar información -> Mostrar datos organizados -> Fin
#
# Este archivo no agrega lógica nueva: solo llama, en orden, a las
# funciones ya definidas en secuencial.py, directo.py, seleccion.py
# y mezcla.py, siguiendo los pasos del diagrama general.
# ============================================================

import secuencial
import directo
import seleccion
import mezcla


def main():
    # Paso 'Registrar productos' + 'Guardar en archivo'
    # (equivale al diagrama 1: acceso secuencial)
    secuencial.agregar_producto(1, "Camiseta", "Ropa", 45000, 30, "Textiles SA")
    secuencial.agregar_producto(2, "Cuaderno", "Papeleria", 8000, 100, "Norma")

    # Paso 'Consultar o modificar datos'
    # (también parte del diagrama 1)
    secuencial.listar_productos()
    secuencial.actualizar_producto(2, 9000)

    # Paso 'Acceso directo a registros'
    # (equivale al diagrama 2: acceso directo)
    open("productos_directo.txt", "a", encoding="utf-8").close()
    directo.agregar_directo(1, "Camiseta", "Textiles SA", 30, 45000, "Ropa")
    directo.leer_directo(1)

    # Paso 'Ordenar información'
    # (equivale a los diagramas 3 y 4: ordenamiento por selección o por mezcla)
    seleccion.agregar_para_ordenar(1, "Camiseta", "Textiles SA", "Ropa", 2022, 45000)
    seleccion.agregar_para_ordenar(2, "Cuaderno", "Norma", "Papeleria", 2023, 8000)
    seleccion.ordenar_externa("productos_usados.txt", "productos_ordenados.txt", 6)

    # Paso 'Mostrar datos organizados' -> Fin
    with open("productos_ordenados.txt", "r", encoding="utf-8") as archivo:
        print("--- Productos ordenados ---")
        for linea in archivo:
            print(linea.strip())


if __name__ == "__main__":
    main()
