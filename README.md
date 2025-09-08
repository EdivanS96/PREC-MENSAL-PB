# PB-MPGRID | Paraíba Monthly Precipitation Gridded Data ☔  

Repositório destinado à organização, análise e disponibilização do **PB-MPGRID**, um conjunto de dados **gridded de precipitação mensal** para o estado da **Paraíba (PB-Brasil)**, desenvolvido a partir da rede de postos pluviométricos da **AESA-PB (Agência Executiva de Gestão das Águas da Paraíba)**.  

Os dados são processados por interpolação espacial (**IDW**) em resolução de **500 m**, cobrindo o período de **1994 a 2024**, e disponibilizados para uso colaborativo no **Google Earth Engine (GEE)**, além de suporte a análises em **Python (via geemap, geopandas, matplotlib)**.  

> 🔗 **Acesse a coleção no Earth Engine:**  
> [https://code.earthengine.google.com/?asset=projects/edivansilva/assets/PB-MPGRID](https://code.earthengine.google.com/?asset=projects/edivansilva/assets/PB-MPGRID)

Este projeto está em desenvolvimento 🚧  
Novos conteúdos serão adicionados em breve.  

---

## 📌 Objetivo

Democratizar o acesso aos dados pluviométricos da Paraíba por meio de:  

- **Visualização geoespacial** no Google Earth Engine  
- **Análises em Python**, com suporte a `geemap`, `geopandas` e `matplotlib`  
- **Reprodutibilidade**, através do compartilhamento de scripts, notebooks e metadados  
- **Integração interdisciplinar**, possibilitando aplicações em climatologia, hidrologia, agricultura e gestão de recursos hídricos  

---

## 🛰️ O que é o PB-MPGRID?

O **PB-MPGRID** (*Paraíba Monthly Precipitation Gridded Data*) é um **dataset interpolado de precipitação mensal** baseado em **242 estações pluviométricas da AESA-PB**.  

- **Cobertura temporal:** janeiro/1994 – dezembro/2024  
- **Resolução espacial:** 500 m (~0,005° WGS84)  
- **Interpolação:** IDW (Inverse Distance Weighting, p=2)  
- **Formato de saída:** GeoTIFF (raster)  
- **Disponibilização:** Google Earth Engine (coleção pública)  
- **Link direto para a coleção:**  
  [https://code.earthengine.google.com/?asset=projects/edivansilva/assets/PB-MPGRID](https://code.earthengine.google.com/?asset=projects/edivansilva/assets/PB-MPGRID)

---

## 🔜 Em breve neste repositório

- Scripts JavaScript para uso no **GEE**  
- Notebooks Python/Colab para análises estatísticas e gráficos  
- Dados auxiliares (CSV, shapefiles e metadados)  
- Documentação detalhada com exemplos de uso  

---

## 🗂 Estrutura planejada

```text
PREC_MENSAL_PB/
├── scripts/      # Scripts JavaScript para GEE
├── notebooks/    # Notebooks Python/Colab
├── data/         # Dados auxiliares (CSV, shapefiles etc.)
└── docs/         # Documentação e tutoriais
