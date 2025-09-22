# 🌧️ PB-MPGRID | Paraíba Monthly Precipitation Gridded Data  

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17180187.svg)](https://doi.org/10.5281/zenodo.17180187)

O **PB-MPGRID** é um conjunto de dados **gridded de precipitação mensal** para o estado da **Paraíba (PB - Brasil)**, desenvolvido a partir da rede de postos pluviométricos da **AESA-PB (Agência Executiva de Gestão das Águas da Paraíba)**.  

Os dados foram processados por interpolação espacial (**IDW**, p=5), em resolução de **500 m**, cobrindo o período de **1994 a 2024**, e são disponibilizados no **Google Earth Engine (GEE)** e em formato **GeoTIFF**, possibilitando aplicações em climatologia, hidrologia, agricultura e gestão de recursos hídricos.  

> 🔗 **Coleção no Earth Engine:**  
> [https://code.earthengine.google.com/?asset=projects/edivansilva/assets/PB-MPGRID](https://code.earthengine.google.com/?asset=projects/edivansilva/assets/PB-MPGRID)  

> 🔗 **Aplicativo Interativo (visualização + download):**  
> [https://edivansilva.projects.earthengine.app/view/pb-mpgrid](https://edivansilva.projects.earthengine.app/view/pb-mpgrid)  

---

## 📌 Objetivo

Democratizar o acesso aos dados pluviométricos da Paraíba por meio de:  

- 🗺️ **Visualização geoespacial** no Google Earth Engine  
- 🐍 **Análises em Python**, com suporte a `geemap`, `geopandas` e `matplotlib`  
- 🔁 **Reprodutibilidade**, através do compartilhamento de scripts, notebooks e metadados  
- 🌱 **Integração interdisciplinar**, com aplicações em climatologia, hidrologia, agricultura e gestão de recursos hídricos  

---

## 🛰️ Sobre o PB-MPGRID

- **Cobertura temporal:** jan/1994 – dez/2024  
- **Resolução espacial:** 500 m (~0,0045° WGS84)  
- **Interpolação:** IDW (Inverse Distance Weighting, p=5)  
- **Estações utilizadas:** 242 postos pluviométricos da AESA-PB  
- **Formato de saída:** GeoTIFF (raster)  
- **Disponibilização:** Google Earth Engine (coleção pública)  

---

## 🗂 Estrutura do Repositório

- `/data/` → links e documentação sobre os dados  
- `/scripts/` → códigos em GEE (JavaScript) e notebooks Python  
- `/app/` → README e imagens do aplicativo interativo  
- `/docs/` → documentação estendida e exemplos de uso  

---

## 📖 Como citar

Se utilizar este repositório, os dados ou o aplicativo em trabalhos acadêmicos ou técnicos, cite como:  

> DOS SANTOS, E. S.; SILVA, B. B.; BRAGA, C. C. **PB-MPGRID: Dados de Precipitação Mensal em Grade para o Estado da Paraíba.** Zenodo, 2025. DOI: [https://doi.org/10.5281/zenodo.17180187](https://doi.org/10.5281/zenodo.17180187)  

---

## 📄 Licença

Este projeto está licenciado sob a [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).  

Isso significa que você pode **compartilhar, adaptar e redistribuir** os dados em qualquer formato ou meio, **desde que atribua o devido crédito** aos autores e **não utilize para fins comerciais**. 

---
