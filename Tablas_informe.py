import pandas as pd
import matplotlib.pyplot as plt
from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin

#%% 
# Datos sumarios: Hipervinculos
data = pd.DataFrame({"Año":[2015,2016,2016,2017],
                      "N nodos":[3117,3257,3372,3668],
                      "K medio": [16.022, 16.633, 17.117, 16.862],
                      "K in máx": [954,	983,	1010,	1045],
                      "K out máx": [1269,1289,	1300,	1304],
                      "Clustering Medio"	:[0.366,	0.377,	0.378,	0.376],
                      "Transitividad":	[0.458	,0.555,0.554,0.49]
                    })

data = data[["Año","N nodos", "K medio", "K in máx","K out máx", "Clustering Medio"
             ,"Transitividad"]]
data.to_csv(osjoin(path_datos_global,"tabla1"))
print(data.to_latex())
#%%
## Datos sumarios: LSA

data = pd.DataFrame({"Año":[2015,2016,2016,2017],
                      "N nodos":[3117,3257,3372,3668],
                      "K medio": [181.045,18.883,19.347,21.558],
                      "K máx": [115,135,153,214],
                      "Clustering Medio"	:[0.464,0.467,0.455,0.433],
                      "Transitividad":	[0.640,0.655,0.663,0.727]
                    })
data = data[["Año","N nodos", "K medio","K máx", "Clustering Medio"
             ,"Transitividad"]]
data.to_csv(osjoin(path_datos_global,"tabla2"))
print(data.to_latex())

#%% Tablas de proporcion overlap
data = pd.DataFrame({"Año":[2015,2016,2016,2017],
                      "Proporcion": [0.086,	0.084,	0.080,	0.064]
                    })

#data = data[['red','N','L','k_medio',
#                 'k_max','k_min','densidad','c_local',
#                 'c_global','diam_CG']]


data.to_csv(osjoin(path_datos_global,"tabla_proporcion"))
print(data.to_latex())

#%% Tabla de Infomutua
data = pd.DataFrame({"Año":["2015","2016","2016","2017"],
                      "Hip": [0.086,	0.084,	0.080,	0.064],
                      "LSA":[ 0.4411,0.4547,0.4662,0.4829]
                    })
data.to_csv(osjoin(path_datos_global,"tabla_IM"))
print(data.to_latex())
#%% Pie chart de categorias

# Data to plot
labels = ['Statistical theory', 'Staticians', 'Applied statistics',
          'Statistical methods', 'Statistical sofwtware', 'Otras']
sizes = [14.46,13.46,10.7,
         10.16,5.91,100-(14.46+13.46+10.7+10.16+5.91)]
colors = ['gold', 'yellowgreen', 'lightcoral', 
          'lightskyblue','green','grey']
explode = (0, 0, 0, 0,0,0.1)  # explode 1st slice
 
# Plot
#plt.pie(sizes, explode=explode, colors=colors,
#        autopct='%1.1f%%', shadow=True, startangle=140)
patches, texts = plt.pie(sizes, colors=colors, startangle=90,
                         explode=explode, 
#                         autopct='%1.1f%%'
#                         labels=labels
                         )
plt.legend(patches, labels,fontsize = 25, loc="best")
plt.axis('equal')
plt.tight_layout()
plt.show()

#%% Pie chart de infomap hip
plt.figure()
# Data to plot
labels = ['_', 'Artificial Neural Network', '_','_','_',
         'Statistical Software','Applied Statistics']
sizes = [15.53,12.38,6.17,3.4,3.3,3.22,3.15]
colors = ['violet', 'lightgreen', 'lightblue', 
          'black','orange','red','green']
explode = (0, 0, 0,0,0,0,0)  # explode 1st slice
 
# Plot
#plt.pie(sizes, explode=explode, colors=colors,
#        autopct='%1.1f%%', shadow=True, startangle=140)
patches, texts = plt.pie(sizes, colors=colors, startangle=90,
                         explode=explode, 
#                         autopct='%1.1f%%'
#                         labels=labels
                         )
plt.legend(patches, labels,fontsize = 12, loc="best")
plt.axis('equal')
plt.tight_layout()
plt.show()

#%% Pie chart de infomap LSA
plt.figure()
# Data to plot
labels = ['_', 'Staticians','_' ,
          'Applied statistics','_']
sizes = [18.29,8.11,6.17,2.81,2.63,2.48,2.4]
colors = ['violet', 'lightgreen', 'lightblue', 
          'black','orange','red','green']
explode = (0, 0, 0,0,0,0,0)  # explode 1st slice
 
# Plot
#plt.pie(sizes, explode=explode, colors=colors,
#        autopct='%1.1f%%', shadow=True, startangle=140)
patches, texts = plt.pie(sizes, colors=colors, startangle=90,
                         explode=explode, 
#                         autopct='%1.1f%%'
#                         labels=labels
                         )
plt.legend(patches, labels,fontsize = 12, loc="best")
plt.axis('equal')
plt.tight_layout()
plt.show()


