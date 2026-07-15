import sys
from collections import Counter

# Recibe como argumento el fragmento a procesar, ej: splits/part_00.txt
filename = sys.argv[1]
counter = Counter()

with open(filename, "r") as f:
    for linea in f:
        linea = linea.strip()
        if not linea:
            continue

        # Formato esperado: Ana, view, 2026-07-01, 20:00:00, video1
        partes = [p.strip() for p in linea.split(",")]
        if len(partes) != 5:
            continue

        usuario, tipo, fecha, hora, video = partes

        # Contador por tipo de interaccion y video (view/like/comment/shared)
        counter[("video_" + tipo, video)] += 1

        # Contador de participacion por usuario
        counter[("usuario", usuario)] += 1

        # Contador de interacciones por hora (para detectar hora pico)
        counter[("hora", hora)] += 1

# Salida intermedia: namespace <TAB> clave <TAB> valor
with open(filename + ".out", "w") as out:
    for (ns, key), val in counter.items():
        out.write(f"{ns}\t{key}\t{val}\n")

print(f"[mapper] procesado {filename} -> {filename}.out ({len(counter)} claves)")
