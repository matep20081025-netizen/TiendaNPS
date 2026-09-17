# ============================================================
# DIAGRAMA 4: ORDENAMIENTO EXTERNO POR MEZCLA (MERGE)
# Inicio -> Dividir archivo en bloques divididos
#        -> Comparar primeros registros de cada bloque
#        -> Copiar el menor al archivo resultado
#        -> Avanzar el bloque utilizado
#        -> ¿Quedan bloques por mezclar? (Yes) Repetir / (No) Fin
#
# Nota: este algoritmo no estaba en el código original, se construyó
# nuevo para que coincida exactamente con los pasos de este diagrama.
# ============================================================

import os


def dividir_en_bloques(archivo_entrada, indice_campo, tam_bloque, carpeta="bloques"):
    """Paso 'Dividir archivo en bloques divididos'.
    Se lee el archivo de entrada en trozos de 'tam_bloque' registros,
    cada trozo se ordena en memoria y se guarda como un bloque aparte."""
    os.makedirs(carpeta, exist_ok=True)
    rutas_bloques = []

    with open(archivo_entrada, "r", encoding="utf-8") as archivo:
        lineas = [linea.strip() for linea in archivo if linea.strip()]

    for i in range(0, len(lineas), tam_bloque):
        trozo = lineas[i:i + tam_bloque]
        trozo.sort(key=lambda linea: int(linea.split(",")[indice_campo]))

        ruta_bloque = os.path.join(carpeta, f"bloque_{i // tam_bloque}.txt")
        with open(ruta_bloque, "w", encoding="utf-8") as archivo_bloque:
            for linea in trozo:
                archivo_bloque.write(linea + "\n")

        rutas_bloques.append(ruta_bloque)

    return rutas_bloques


def mezclar_bloques(rutas_bloques, archivo_salida, indice_campo):
    """Pasos 'Comparar primeros registros de cada bloque' ->
    'Copiar el menor al archivo resultado' -> 'Avanzar el bloque
    utilizado' -> '¿Quedan bloques por mezclar?'.
    Se mantiene un archivo abierto por bloque y, en cada vuelta, se
    compara la línea actual de cada uno para copiar la más pequeña."""
    archivos = [open(ruta, "r", encoding="utf-8") for ruta in rutas_bloques]
    lineas_actuales = [archivo.readline().strip() for archivo in archivos]

    with open(archivo_salida, "w", encoding="utf-8") as salida:
        while True:
            # ¿Quedan bloques por mezclar? -> se revisa si algún bloque
            # todavía tiene una línea pendiente por comparar.
            candidatos = [
                (i, linea) for i, linea in enumerate(lineas_actuales) if linea
            ]
            if not candidatos:          # ¿Quedan bloques por mezclar? -> No
                break

            # Comparar primeros registros de cada bloque
            indice_menor, linea_menor = min(
                candidatos, key=lambda par: int(par[1].split(",")[indice_campo])
            )

            salida.write(linea_menor + "\n")   # Copiar el menor al archivo resultado

            # Avanzar el bloque utilizado (se lee su siguiente línea)
            lineas_actuales[indice_menor] = archivos[indice_menor].readline().strip()
            # -> Repetir (vuelve al inicio del while)

    for archivo in archivos:
        archivo.close()


def ordenar_por_mezcla(archivo_entrada, archivo_salida, indice_campo, tam_bloque=2):
    """Flujo completo del diagrama 4: primero divide en bloques
    ordenados y luego los mezcla todos en un solo archivo ordenado."""
    rutas_bloques = dividir_en_bloques(archivo_entrada, indice_campo, tam_bloque)
    mezclar_bloques(rutas_bloques, archivo_salida, indice_campo)


if __name__ == "__main__":
    with open("productos_para_mezclar.txt", "w", encoding="utf-8") as archivo:
        archivo.write("1,Camiseta,Textiles SA,Ropa,2022,45000\n")
        archivo.write("2,Cuaderno,Norma,Papeleria,2023,8000\n")
        archivo.write("3,Mouse,Logitech,Tecnologia,2021,35000\n")
        archivo.write("4,Teclado,Logitech,Tecnologia,2020,60000\n")

    # indice_campo=5 -> se ordena por precio (id=0, nombre=1, proveedor=2, categoria=3, anio=4, precio=5)
    ordenar_por_mezcla("productos_para_mezclar.txt", "productos_mezclados.txt", indice_campo=5)

    with open("productos_mezclados.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            print(linea.strip())
