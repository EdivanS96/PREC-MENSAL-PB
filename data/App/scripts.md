# PB-MPGRID | Scripts para o Google Earth Engine


Os scripts abaixo são feitos para o Google Earth Engine (GEE). Para usá-los, basta copiar e colar o código no [GEE Code Editor](https://code.earthengine.google.com/).

---

## ✅ Scripts Disponíveis

---

### 1. Ver e Baixar Precipitação Mensal

Este script permite que você visualize a precipitação de um mês específico e baixe o arquivo correspondente em formato GeoTIFF.
```javascript
// PASSO 1: Configure o mês e ano do PB-MPGRID que você quer ver e baixar. (Dados entre 1994 e 2024)
var ano = 2021;
var mes = 7; // Mês 7 (julho)

// ==========================================================

// PASSO 2: Adicionando Area de Estudo e PBMPGRID

var area_estudo = ee.FeatureCollection('projects/ee-edivanaesa/assets/Regioes_Pluvi_PB_2025_ByEdivanS');

var mpgrid = ee.ImageCollection("projects/edivansilva/assets/PB-MPGRID");

// PASSO 3: Preparando Imagem

var imagem_mensal = mpgrid.filter(ee.Filter.calendarRange(ano, ano, 'year'))
  .filter(ee.Filter.calendarRange(mes, mes, 'month'))
  .first()
  .select('prec');

var vis_mensal = {
  min: 0,
  max: 300,
  palette: ['f93537', 'fe5f35', 'fca973', 'facc9b', 'fdfd99', '9afd02', '73d973', '32cd31', '009b36', '007fff', '0065ff']
};

Map.centerObject(area_estudo, 8);
Map.addLayer(imagem_mensal.clip(area_estudo), vis_mensal, 'Precipitação ' + mes + '/' + ano);

Export.image.toDrive({
  image: imagem_mensal.clip(area_estudo),
  description: 'PBMPGRID_PREC_MENSAL_' + ano + '_' + mes,
  folder: 'GEE_Downloads_PBMPGRID',
  scale: 1000,
  region: area_estudo.geometry(),
  fileFormat: 'GeoTIFF'
});

print('✅ O download da imagem do PB-MPGRID vai começar no menu "Tasks" (Tarefas).');

```

### 2. Ver e Baixar Precipitação Anual

Use este script para visualizar a precipitação anual acumulada e baixá-la em formato GeoTIFF.

```javascript
// PASSO 1: Configure o ano do PB-MPGRID que você quer ver e baixar. (Dados entre 1994 e 2024)
var ano = 2020;

// ==========================================================

// PASSO 2: Adicionando Area de Estudo e PBMPGRID

var area_estudo = ee.FeatureCollection('projects/ee-edivanaesa/assets/Regioes_Pluvi_PB_2025_ByEdivanS');

var mpgrid = ee.ImageCollection("projects/edivansilva/assets/PB-MPGRID");

// PASSO 3: Preparando Imagem

var imagem_anual = mpgrid.filter(ee.Filter.calendarRange(ano, ano, 'year'))
  .select('prec')
  .sum();

var vis_anual = {
  min: 100,
  max: 2000,
  palette: ['f93537', 'fe5f35', 'fca973', 'facc9b', 'fdfd99', '9afd02', '73d973', '32cd31', '009b36', '007fff', '0065ff']
};

Map.centerObject(area_estudo, 8);
Map.addLayer(imagem_anual.clip(area_estudo), vis_anual, 'PBMPGRID Anual ' + ano);

Export.image.toDrive({
  image: imagem_anual.clip(area_estudo),
  description: 'PBMPGRID_PREC__ANUAL_' + ano,
  folder: 'GEE_Downloads_PBMPGRID',
  scale: 1000,
  region: area_estudo.geometry(),
  fileFormat: 'GeoTIFF'
});

print('✅ O download da imagem do PB-MPGRID vai começar no menu "Tasks" (Tarefas).');

```

### 3. Gerar Gráfico e Tabela de Série Temporal
Este script permite uma análise mais detalhada. Ele gera um gráfico mensal da precipitação em um período e cria uma tabela que você pode baixar em formato CSV.

```javascript
// PASSO 1: Definir período de análise do PB-MPGRID que você quer ver e baixar. (Dados entre 1994 e 2024)
var data_inicio = '2010-01-01';
var data_fim = '2015-12-31';


// PASSO 2: Adicionando Area de Estudo e PBMPGRID com filtros

var area_estudo = ee.FeatureCollection('projects/ee-edivanaesa/assets/Regioes_Pluvi_PB_2025_ByEdivanS');

var mpgrid = ee.ImageCollection("projects/edivansilva/assets/PB-MPGRID")
              .filterDate(data_inicio, data_fim)
              .filterBounds(area_estudo)
              .select('prec');


// PASSO 3: Criar gráfico de séries temporais
var grafico = ui.Chart.image.seriesByRegion({
  imageCollection: mpgrid,
  regions: area_estudo,
  reducer: ee.Reducer.mean(),
  band: 'prec',
  seriesProperty: 'Nomepluv',
  scale: 1000,
  xProperty: 'system:time_start'
}).setOptions({
  title: 'Precipitação Média Mensal por Região (PB-MPGRID)',
  hAxis: {title: 'Data'},
  vAxis: {title: 'Precipitação (mm)'},
  lineWidth: 2,
  pointSize: 3
});

print('📊 Gráfico de Precipitação Média Mensal:', grafico);

// Gerar tabela com dados médios por mês
var regioesReducidasMensal = mpgrid.map(function(imagem) {
  var reducao = imagem.reduceRegions({
    collection: area_estudo,
    reducer: ee.Reducer.mean(),
    scale: 1000
  });

  var dataComPropriedades = reducao.map(function(feature) {
    var prec = feature.get('mean');
    var formattedPrec = ee.Algorithms.If(
      prec,
      ee.Number(prec).format('%.1f'),
      null
    );

    return feature.set({
      'Posto': feature.get('Nomepluv'),
      'Ano': ee.Date(imagem.get('system:time_start')).get('year'),
      'Mes': ee.Date(imagem.get('system:time_start')).get('month'),
      'PREC (mm)': formattedPrec
    });
  });

  return dataComPropriedades;
}).flatten();

// Exportar a tabela em CSV
Export.table.toDrive({
  collection: regioesReducidasMensal,
  description: 'PREC_Tabela_Mensal_PBMPGRID',
  folder: 'GEE_Downloads_PBMPGRID',
  fileNamePrefix: 'PREC Mensal PB-MPGRID de ' + data_inicio + ' a ' + data_fim,
  fileFormat: 'CSV',
  selectors: ['Posto', 'Ano', 'Mes', 'PREC (mm)'],
  priority: 'default'
});

print('✅ O download da tabela estará em "Tasks" (Tarefas).');

```

### ℹ️ Informações Complementares
**Dataset:** 
```projects/edivansilva/assets/PB-MPGRID```

**Área de estudo:** 
```projects/ee-edivanaesa/assets/Regioes_Pluvi_PB_2025_ByEdivanS```

**Paleta de cores mensal:**

```
min: 0

max: 300

palette: ['f93537', 'fe5f35', 'fca973', 'facc9b', 'fdfd99', '9afd02', '73d973', '32cd31', '009b36', '007fff', '0065ff']
```

**Paleta de cores anual:**
```
min: 100

max: 2000

palette: ['f93537', 'fe5f35', 'fca973', 'facc9b', 'fdfd99', '9afd02', '73d973', '32cd31', '009b36', '007fff', '0065ff']
```

### 👤 Autor
Edivan Silva