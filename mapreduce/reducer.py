import os
from collections import defaultdict


acumulado = defaultdict(lambda: defaultdict(int))

for archivo in os.listdir("splits"):
    if archivo.endswith(".out"):
        with open(f"splits/{archivo}", "r") as f:
            for linea in f:
                ns, key, val = linea.strip().split("\t")
                acumulado[ns][key] += int(val)


def top(ns, n=1):
    items = sorted(acumulado[ns].items(), key=lambda x: -x[1])
    return items[:n]




video_mas_visto        = top("video_view", 1)
video_mas_likes        = top("video_like", 1)
video_mas_comentado    = top("video_comment", 1)
usuario_mas_recurrente = top("usuario", 1)
hora_mas_interaccion   = top("hora", 1)

videos = set()
for ns in ["video_view", "video_like", "video_comment", "video_shared"]:
    videos.update(acumulado[ns].keys())

ratios = {}
for v in videos:
    views    = acumulado["video_view"].get(v, 0)
    likes    = acumulado["video_like"].get(v, 0)
    comments = acumulado["video_comment"].get(v, 0)
    shares   = acumulado["video_shared"].get(v, 0)
    if views > 0:
        ratios[v] = (likes + comments + shares) / views

video_mejor_ratio = sorted(ratios.items(), key=lambda x: -x[1])[:1]

with open("resultado.txt", "w") as out:
    out.write("=== METRICAS DE INTERACCION - RED SOCIAL POWERESFOT ===\n\n")
    out.write(f"1. Video mas visto: {video_mas_visto}\n")
    out.write(f"2. Video con mas likes: {video_mas_likes}\n")
    out.write(f"3. Video mas comentado: {video_mas_comentado}\n")
    out.write(f"4. Usuario mas recurrente: {usuario_mas_recurrente}\n")
    out.write(f"5. Hora con mas interaccion: {hora_mas_interaccion}\n")
    out.write(f"6. Video con mayor Ratio de Interaccion: {video_mejor_ratio}\n")

    out.write("\n--- Ratios de interaccion por video (todos, ordenados) ---\n")
    for v, r in sorted(ratios.items(), key=lambda x: -x[1]):
        views    = acumulado["video_view"].get(v, 0)
        likes    = acumulado["video_like"].get(v, 0)
        comments = acumulado["video_comment"].get(v, 0)
        shares   = acumulado["video_shared"].get(v, 0)
        out.write(f"{v}: ratio={round(r,3)}  (likes={likes}, comments={comments}, shares={shares}, views={views})\n")

print(open("resultado.txt").read())
