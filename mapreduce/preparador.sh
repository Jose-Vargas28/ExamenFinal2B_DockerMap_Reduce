#!/bin/bash
set -e

echo "Descargando datos desde el balanceador NGINX (/datos)..."

sleep 15
curl -s http://nginx/datos -o entrada.txt

LINEAS=$(wc -l < entrada.txt)
echo "Datos descargados: $LINEAS interacciones"

if [ "$LINEAS" -eq 0 ]; then
    echo "ERROR: no se recibieron datos. Verifica que MySQL, server1 y server2 esten arriba."
    exit 1
fi

mdir -p splits
rm -f splits/*.txt splits/*.out
split -n l/4 -d --additional-suffix=.txt entrada.txt splits/part_
echo "Fragmentado en $(ls splits/*.txt | wc -l) partes:"
ls splits/*.txt
