#Criação dos manifest.js de cada imagem para subir no GEE

import os
import json
from datetime import datetime, timedelta

# Configurações
input_folder = "./"  # pasta com os .tif
output_folder = "./manifests"
bucket_name = "gee-upload-edivansilva"
asset_folder = "projects/edivansilva/assets"
band_name = "prec"

# Propriedades comuns
fixed_props = {
    "banda": band_name,
    "fonte": "AESA - PB",
    "contact": "edivan.silva@estudante.ufcg.edu.br",
    "paper": "DOS SANTOS, E. S.; SILVA, B. B.; BRAGA, C. C.",
    "repositorio": "https://github.com/EdivanS96/PREC-MENSAL-PB",
    "units": "mm",
    "description_base": "Precipitação mensal interpolada IDW",
    "interpol_method": "IDW"
}

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def to_millis(dt):
    return int(dt.timestamp() * 1000)

def get_end_of_month(year, month):
    if month == 12:
        return datetime(year + 1, 1, 1) - timedelta(milliseconds=1)
    return datetime(year, month + 1, 1) - timedelta(milliseconds=1)

# Gera um manifest por arquivo .tif
for filename in os.listdir(input_folder):
    if not filename.endswith(".tif"):
        continue

    parts = filename.replace(".tif", "").split("_")
    if len(parts) != 3:
        print(f"❌ Nome inválido: {filename}")
        continue

    year = int(parts[1])
    month = int(parts[2])

    start_date = datetime(year, month, 1)
    end_date = get_end_of_month(year, month)

    props = {
        "system_time_start": to_millis(start_date),
        "system_time_end": to_millis(end_date),
        "year": year,
        "month": month,
        "banda": fixed_props["banda"],
        "fonte": fixed_props["fonte"],
        "contact": fixed_props["contact"],
        "paper": fixed_props["paper"],
        "repositorio": fixed_props["repositorio"],
        "units": fixed_props["units"],
        "description": f"{fixed_props['description_base']} para {year}-{month:02d}",
        "interpol_method": fixed_props["interpol_method"]
    }

    manifest = {
        "name": f"{asset_folder}/{filename.replace('.tif','')}",
        "tilesets": [
            {
                "sources": [
                    {
                        "uris": [f"gs://{bucket_name}/{filename}"]
                    }
                ]
            }
        ],
        "bands": [
            {
                "id": band_name
            }
        ],
        "properties": props
    }

    out_path = os.path.join(output_folder, filename.replace(".tif", ".json"))
    with open(out_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ Manifesto gerado: {out_path}")
