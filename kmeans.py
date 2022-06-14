from random import randint
import math
import numpy 
import pandas
import matplotlib.pyplot as plt
import seaborn

from google.colab import files
import io

# Lendo o arquivo de entrada com as informacoes de (x,y)
uploaded = files.upload()
df = pandas.read_csv(io.BytesIO(uploaded['data.csv']))

%matplotlib inline

# Plotando o gráfico inicial
df.plot(kind='scatter',x='x',y='y',color="red")
data_points = list(df.T.to_dict().values())

def calcula_distancia_entre_pontos(p1,p2):
  return math.sqrt(((p1['x'] - p2['x'])*(p1['x'] - p2['x'])) + ((p1['y'] - p2['y'])*(p1['y'] - p2['y'])))



def gera_clusters(data_points, centroide_1, centroide_2, centroide_3):

  for idx,point in enumerate(data_points):
    
    # Calculando a distancia do ponto em questao para cada um dos centroides
    d_1 = calcula_distancia_entre_pontos(point, centroide_1)
    d_2 = calcula_distancia_entre_pontos(point, centroide_2)
    d_3 = calcula_distancia_entre_pontos(point, centroide_3)
    
    # Configura de qual cluster é aquele ponto, atraves da menor distancia entre
    # os tres possiveis
    if d_1 <= d_2 and d_1 <= d_3:
      data_points[idx]['cluster'] = "1"
    elif d_2 <= d_1 and d_2 <= d_3:
      data_points[idx]['cluster'] = "2"
    elif d_3 <= d_1 and d_3 <= d_2:
      data_points[idx]['cluster'] = "3"

  return data_points
# FIM metodo gera_clusters



def escolher_novos_centroides(data_point):
  # Somatorio dos valores de x,y para cada um dos pontos no data_points
  # para ser calculado o proximos candidatos a centroide
  sum_x_cluster_1 = 0
  sum_y_cluster_1 = 0
  qt_cluster_1 = 0

  sum_x_cluster_2 = 0
  sum_y_cluster_2 = 0
  qt_cluster_2 = 0

  sum_x_cluster_3 = 0
  sum_y_cluster_3 = 0  
  qt_cluster_3 = 0

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
  
  print(qt_cluster_1, qt_cluster_3)
  # Identificacao dos novos centroides usando os somatorios do passo anterior
  new_centroide_1 = {'x': (sum_x_cluster_1 / qt_cluster_1), 'y': (sum_y_cluster_1/qt_cluster_1)}
  new_centroide_2 = {'x': (sum_x_cluster_2 / qt_cluster_2), 'y': (sum_y_cluster_2/qt_cluster_2)}
  new_centroide_3 = {'x': (sum_x_cluster_3 / qt_cluster_3), 'y': (sum_y_cluster_3/qt_cluster_3)}

  return new_centroide_1, new_centroide_2, new_centroide_3




def possui_mudanca_de_centroides(nc1, c1, nc2, c2, nc3, c3):
  if nc1['x'] == c1['x'] and nc1['y'] == c1['y'] and nc2['x'] == c2['x'] and nc2['y'] == c2['y'] and nc3['x'] == c3['x'] and nc3['y'] == c3['y']:
    return False
  return True



#######################################
#### INICIO DA LOGICA DO K-MEANS ######
#######################################
init_centr_1 = 0
init_centr_2 = 0
init_centr_3 = 0

# Gerando centroides iniciais
while init_centr_1 == init_centr_2 or init_centr_1 == init_centr_3 or init_centr_2 == init_centr_3:
  init_centr_1 = randint(0,len(data_points)-1)
  init_centr_2 = randint(0,len(data_points)-1)
  init_centr_3 = randint(0,len(data_points)-1)

centroide_1 = data_points[init_centr_1]
centroide_2 = data_points[init_centr_2]
centroide_3 = data_points[init_centr_3]


# Loop de execucoes do k-means
for i in range(50):

  data_points = gera_clusters(data_points, centroide_1, centroide_2, centroide_3)
  
  new_centroide_1, new_centroide_2, new_centroide_3 = escolher_novos_centroides(data_points)  

  if possui_mudanca_de_centroides(new_centroide_1, centroide_1, 
                                  new_centroide_2, centroide_2, 
                                  new_centroide_3, centroide_3):
    centroide_1 = new_centroide_1
    centroide_2 = new_centroide_2
    centroide_3 = new_centroide_3
  else:
    break




# Configurando o dataframe para adicionar uma nova coluna referente ao clusters
clusters = list(map(lambda x: x['cluster'], data_points))
df['cluster'] = clusters

seaborn.scatterplot(x='x', y='y', data=df, hue='cluster', ec=None)

# Configurando o dataframe para adicionar uma nova coluna referente ao clusters
clusters = list(map(lambda x: x['cluster'], data_points))
df['cluster'] = clusters

seaborn.scatterplot(x='x', y='y', data=df, hue='cluster', ec=None)
