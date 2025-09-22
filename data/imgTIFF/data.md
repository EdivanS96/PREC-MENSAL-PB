# 🌧️ Conversão de Dados de Precipitação para GeoTIFFs com IDW

Este repositório contém scripts desenvolvidos para processar dados mensais de precipitação no estado da Paraíba (PB), Brasil, convertendo-os de um arquivo CSV para imagens raster GeoTIFF, utilizando interpolação IDW (Inverse Distance Weighting).

## 📁 Estrutura do Repositório

- `org_data.py`: Script principal que automatiza a interpolação e geração de **372 imagens TIFF** (de 1994 a 2024) com resolução espacial de 500 metros.
- `PB_UF_2024.zip`: Arquivo shapefile da área de recorte (estado da Paraíba).
- `PREC_MENSAL_PB.csv`: Arquivo de entrada contendo os dados de precipitação mensal.
- `teste_data.py`: Script auxiliar utilizado para testar e validar a geração de uma única imagem GeoTIFF antes de processar todos os dados.

---

## ✅ Objetivo

Transformar dados de precipitação mensal em imagens raster com grade regular, permitindo visualização, análise espacial e uso em SIGs (Sistemas de Informação Geográfica).

---

## ⚙️ Tecnologias e Bibliotecas Utilizadas

- Python 3.x
- Pandas
- GeoPandas
- NumPy
- Rasterio
- Shapely
- SciPy
- tqdm
- pyproj

---

## 🔧 Instalação das Dependências

Execute no início do seu notebook ou ambiente Colab:

```bash
pip install geopandas rasterio shapely pyproj scipy tqdm
