# Instalar bibliotecas necessárias:
!pip install geopandas rasterio shapely pyproj scipy tqdm

#Teste de uma imagem para validação:
import pandas as pd
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio import mask
from shapely.geometry import Point
from scipy.spatial import cKDTree
import os

# Parâmetros
csv_path = "/content/PREC_MENSAL_PB.csv"
shapefile_path = "/content/PB_UF_2024.zip"
output_tif = "/content/prec_PB_NOVA.tif"
PIXEL_SIZE = 0.0045
POWER = 5  # IDW power

# Escolha o ano e mês aqui
ano_desejado = 2024
mes_desejado = 12

# 1. Carrega os dados
df = pd.read_csv(csv_path, sep=';')
df['geometry'] = df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")

# 2. Filtra o mês/ano
dados_filtrados = gdf[(gdf['ano'] == ano_desejado) & (gdf['mes'] == mes_desejado)]
if dados_filtrados.empty:
    raise ValueError(f"Nenhum dado encontrado para {ano_desejado}-{mes_desejado:02d}")

# 3. Carrega shapefile da Paraíba
gdf_pb = gpd.read_file(f"zip://{shapefile_path}")
bounds = gdf_pb.total_bounds
minx, miny, maxx, maxy = bounds

# 4. Gera grade de interpolação
grid_x = np.arange(minx, maxx + PIXEL_SIZE, PIXEL_SIZE)
grid_y = np.arange(miny, maxy + PIXEL_SIZE, PIXEL_SIZE)
grid_xx, grid_yy = np.meshgrid(grid_x, grid_y)
grid_points = np.c_[grid_xx.ravel(), grid_yy.ravel()]

# 5. Interpolação IDW
xy_obs = np.array([(pt.x, pt.y) for pt in dados_filtrados.geometry])
values = dados_filtrados['prec'].values

tree = cKDTree(xy_obs)
dists, idxs = tree.query(grid_points, k=len(xy_obs), distance_upper_bound=np.inf)

with np.errstate(divide='ignore'):
    weights = 1 / np.power(dists, POWER)
weights[np.isinf(weights)] = 0
weights[dists == 0] = 1e12

interpolated = np.sum(values[idxs] * weights, axis=1) / np.sum(weights, axis=1)
interpolated = interpolated.reshape(grid_yy.shape)

# 6. Exporta GeoTIFF recortado (com flip vertical corrigido)
transform = from_origin(minx, maxy, PIXEL_SIZE, PIXEL_SIZE)
temp_tif = "/content/temp_NOVA.tif"

with rasterio.open(
    temp_tif,
    'w',
    driver='GTiff',
    height=interpolated.shape[0],
    width=interpolated.shape[1],
    count=1,
    dtype='float32',
    crs='EPSG:4326',
    transform=transform,
) as dst:
    dst.write(np.flipud(interpolated).astype('float32'), 1)  # <- Flip vertical aqui!

# Recorte com shape da PB
with rasterio.open(temp_tif) as src:
    out_image, out_transform = mask.mask(src, gdf_pb.geometry, crop=True, all_touched=True)
    out_meta = src.meta.copy()

out_meta.update({
    "height": out_image.shape[1],
    "width": out_image.shape[2],
    "transform": out_transform
})

with rasterio.open(output_tif, "w", **out_meta) as dest:
    dest.write(out_image)

# Remove temporário
os.remove(temp_tif)

print(f"✅ GeoTIFF gerado para {ano_desejado}-{mes_desejado:02d}: {output_tif}")
