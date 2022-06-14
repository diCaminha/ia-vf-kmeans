from random import randint
import math
import numpy 
import pandas
import matplotlib.pyplot as plt
import seaborn

from google.colab import files
uploaded = files.upload()

import io
df = pandas.read_csv(io.BytesIO(uploaded['data.csv']))

%matplotlib inline

df.plot(kind='scatter',x='x',y='y',color="blue")
data_points = list(df.T.to_dict().values())

def generate_clusters(centroide_1, centroide_2, centroide_3):

  for idx,point in enumerate(data_points):
    
    # Calculando a distancia do ponto em questao para cada um dos centroides
    d_1 = math.sqrt(((point['x'] - centroide_1['x'])*(point['x'] - centroide_1['x'])) + ((point['y'] - centroide_1['y'])*(point['y'] - centroide_1['y'])))
    d_2 = math.sqrt(((point['x'] - centroide_2['x'])*(point['x'] - centroide_2['x'])) + ((point['y'] - centroide_2['y'])*(point['y'] - centroide_2['y'])))
    d_3 = math.sqrt(((point['x'] - centroide_3['x'])*(point['x'] - centroide_3['x'])) + ((point['y'] - centroide_3['y'])*(point['y'] - centroide_3['y'])))
    
    # Configura de qual cluster é aquele ponto, atraves da menor distancia entre
    # os tres possiveis
    if d_1 <= d_2 and d_1 <= d_3:
      data_points[idx]['cluster'] = "1"
    elif d_2 <= d_1 and d_2 <= d_3:
      data_points[idx]['cluster'] = "2"
    elif d_3 <= d_1 and d_3 <= d_2:
      data_points[idx]['cluster'] = "3"

  return data_points
# FIM metodo generate_clusters


init_centr_1 = randint(0,len(data_points))
init_centr_2 = randint(0,len(data_points))
init_centr_3 = randint(0,len(data_points))

centroide_1 = data_points[init_centr_1]
centroide_2 = data_points[init_centr_2]
centroide_3 = data_points[init_centr_3]

for i in range(50):

  # Execucao da logica de setar o cluster de cada um dos pontos
  data_points = generate_clusters(centroide_1, centroide_2, centroide_3)
  
  sum_x_cluster_1 = 0
  sum_y_cluster_1 = 0
  
  sum_x_cluster_2 = 0
  sum_y_cluster_2 = 0
  
  sum_x_cluster_3 = 0
  sum_y_cluster_3 = 0
  
  qt_cluster_1 = 0
  qt_cluster_2 = 0
  qt_cluster_3 = 0


  # Somatorio dos valores de x,y para cada um dos pontos no data_points
  # para ser calculado o proximos candidatos a centroide
  for el in data_points:
    if el['cluster'] == "1":
      qt_cluster_1 += 1
      sum_x_cluster_1 += el['x']
      sum_y_cluster_1 += el['y']
    elif el['cluster'] == "2":
      qt_cluster_2 += 1
      sum_x_cluster_2 += el['x']
      sum_y_cluster_2 += el['y']
    else:
      qt_cluster_3 += 1
      sum_x_cluster_3 += el['x']
      sum_y_cluster_3 += el['y']


  
  # Identificacao dos novos centroides usando os somatorios do passo anterior
  new_centroide_1 = {'x': (sum_x_cluster_1 / qt_cluster_1), 'y': (sum_y_cluster_1/qt_cluster_1)}
  new_centroide_2 = {'x': (sum_x_cluster_2 / qt_cluster_2), 'y': (sum_y_cluster_2/qt_cluster_2)}
  new_centroide_3 = {'x': (sum_x_cluster_3 / qt_cluster_3), 'y': (sum_y_cluster_3/qt_cluster_3)}

  # Verifica se os centroides estao se repedindo (se o novo centroide é igual ao antigo)
  # Se for, termina o loop de procura de centroides
  if new_centroide_1['x'] == centroide_1['x'] and new_centroide_1['y'] == centroide_1['y'] and new_centroide_2['x'] == centroide_2['x'] and new_centroide_2['y'] == centroide_2['y'] and new_centroide_3['x'] == centroide_3['x'] and new_centroide_3['y'] == centroide_3['y']:
    break
  else:
    centroide_1 = new_centroide_1
    centroide_2 = new_centroide_2
    centroide_3 = new_centroide_3


# Configurando o dataframe para adicionar uma nova coluna referente ao clusters
clusters = list(map(lambda x: x['cluster'], data_points))
df['cluster'] = clusters

seaborn.scatterplot(x='x', y='y', data=df, hue='cluster', ec=None)
