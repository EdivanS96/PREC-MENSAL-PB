#Definir datas de cada imagem

import subprocess
from datetime import datetime
import calendar

# Caminho base dos assets
ASSET_PATH = "projects/edivansilva/assets"

# Intervalo de anos e meses
anos = range(1994, 2025)  # 1994 até 2024
meses = range(1, 13)

for ano in anos:
    for mes in meses:
        nome = f"PBMPGRID_{ano}_{mes:02d}"
        asset_id = f"{ASSET_PATH}/{nome}"

        # Data inicial (primeiro dia do mês)
        start_date = datetime(ano, mes, 1)
        # Data final (último dia do mês, 23:59:59)
        last_day = calendar.monthrange(ano, mes)[1]
        end_date = datetime(ano, mes, last_day, 23, 59, 59)

        # Converter para string ISO8601
        start_str = start_date.strftime("%Y-%m-%dT%H:%M:%S")
        end_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")

        # Comando Earth Engine CLI
        cmd = [
            "earthengine", "asset", "set",
            f"--time_start={start_str}",
            f"--time_end={end_str}",
            asset_id
        ]

        print("Executando:", " ".join(cmd))
        subprocess.run(cmd)
