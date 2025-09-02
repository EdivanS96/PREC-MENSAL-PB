# Instalar bibliotecas necessárias:
!pip install geopandas rasterio shapely pyproj scipy tqdm


#Conversão do CSV para IMG TIF
import pandas as pd
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio import mask
from shapely.geometry import Point
from scipy.spatial import cKDTree
from zipfile import ZipFile
import os
from tqdm import tqdm

# Parâmetros de interpolação
POWER = 5  #Distancia para o coeficiente P
PIXEL_SIZE = 0.0045  #Resolução espacial do pixel (500m)

# Caminhos (Importar os arquivos na MAQUINA ou NUVEM: Tanto CSV quanto o SHP)
csv_path = "/content/PREC_MENSAL_PB.csv"
shapefile_path = "/content/PB_UF_2024.zip"
output_dir = "/content/output_tiffs"
zip_output = "/content/prec_paraiba_1994_2024.zip"

# Criar diretório de saída
os.makedirs(output_dir, exist_ok=True)

# 1. Carrega o CSV com separador correto
df = pd.read_csv(csv_path, sep=';')

# 2. Carrega shapefile da Paraíba
gdf_pb = gpd.read_file(f"zip://{shapefile_path}")

# 3. Prepara os dados como GeoDataFrame
df['geometry'] = df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")

# 4. Define grade de interpolação
bounds = gdf_pb.total_bounds
minx, miny, maxx, maxy = bounds

grid_x = np.arange(minx, maxx + PIXEL_SIZE, PIXEL_SIZE)
grid_y = np.arange(miny, maxy + PIXEL_SIZE, PIXEL_SIZE)
grid_xx, grid_yy = np.meshgrid(grid_x, grid_y)
grid_points = np.c_[grid_xx.ravel(), grid_yy.ravel()]

# Função de interpolação IDW
def idw_interpolation(xy_obs, values, xy_grid, power=POWER):
    tree = cKDTree(xy_obs)
    dists, idxs = tree.query(xy_grid, k=len(xy_obs), distance_upper_bound=np.inf)

    with np.errstate(divide='ignore'):
        weights = 1 / np.power(dists, power)
    weights[np.isinf(weights)] = 0
    weights[dists == 0] = 1e12  # força peso altíssimo se distância for 0

    interpolated = np.sum(values[idxs] * weights, axis=1) / np.sum(weights, axis=1)
    return interpolated

# 5. Interpola mês a mês
for year in tqdm(range(1994, 2025), desc="Anos"):
    for month in range(1, 13):
        data_sel = gdf[(gdf['ano'] == year) & (gdf['mes'] == month)]
        if data_sel.empty:
            continue

        xy_obs = np.array([(pt.x, pt.y) for pt in data_sel.geometry])
        values = data_sel['prec'].values

        interpolated = idw_interpolation(xy_obs, values, grid_points)
        interpolated = interpolated.reshape(grid_yy.shape)

        # Corrigir orientação com flip vertical
        interpolated = np.flipud(interpolated)

        # Criar raster temporário
        transform = from_origin(minx, maxy, PIXEL_SIZE, PIXEL_SIZE)
        temp_tif = os.path.join(output_dir, f"temp_{year}_{month:02d}.tif")

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
            dst.write(interpolated.astype('float32'), 1)

        #Recortar com shapefile da PB
        with rasterio.open(temp_tif) as src:
            out_image, out_transform = mask.mask(src, gdf_pb.geometry, crop=True, all_touched=True)
            out_meta = src.meta.copy()

        out_meta.update({
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

        final_tif = os.path.join(output_dir, f"PB_prec_{year}_{month:02d}.tif")
        with rasterio.open(final_tif, "w", **out_meta) as dest:
            dest.write(out_image)

        # Remover temporário
        os.remove(temp_tif)

# 6. Compactar todos os GeoTIFFs
with ZipFile(zip_output, 'w') as zipf:
    for tif_file in os.listdir(output_dir):
        zipf.write(os.path.join(output_dir, tif_file), arcname=tif_file)

#Exportação das imagens em .ZIP
print(f"✅ Processo concluído. Arquivo ZIP salvo em: {zip_output}")
