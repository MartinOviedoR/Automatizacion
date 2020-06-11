import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
sns.set()

df = pd.read_excel("QuizResponses.xlsx", header=1)

#Ahora vamos a hacer un forloop para que solo nos traiga las columnas de points que sabemos que son las que tienen los puntos de cada pregutna
mis_columnas = []
for col in df.columns:
    if 'Points' in col:
        mis_columnas.append(col)
cols = [col for col in df.columns if 'Points' in col]
test = df[cols].apply(lambda s: s.str[0])
test.apply(pd.to_numeric).dtypes
test = test.apply(pd.to_numeric, downcast="float")
test[test.columns[0:5]].mean(axis=1)
#ahora definimos los grupos que seran fundamentales para nuestra clasificacion pues hacen parte de las categorias previamente analizadas de
#madurez digital
steps = [0, 7, 17, 23, 34, 41, 48]
for i in range(len(steps)-1):
    test[f'mean_G{i}'] = test.iloc[:, steps[i]:steps[i+1]].mean(axis=1)
#Ahora vamos a hacer para que solo nos traiga las columnas de mean que sabemos que son las que tienen los puntos de cada sección
cols2 = [col for col in test.columns if 'mean' in col]
#El dataframe 2 tendra solo las columnas de mean
df2 = test[cols2]
#cambiemosle los nombres para que luis entienda a que hacemos referencia
df2 = df2.rename(columns={"mean_G0": "Estrategia y liderazgo", "mean_G1": "Cliente y propuesta de valor", "mean_G2": "Talento y Cultura", "mean_G3": "Cadena de valor y procesos", "mean_G4": "Informacion y digitalizacion", "mean_G5": "Innovacion y agilismo"})
#como no queremos la media con todos los numeros decimales lo que hacemos es aproximarla solamente a un numero decimal
df2 = df2.round(1)
export_excel = df2.to_excel(r'C:\Users\DNCIESQUENAZI\Desktop\Python projects\ValueScan\dfsurveymonkey.xlsx', header=True)
#segunda parte
dftextos = pd.read_excel("textos.xlsx")
x = []
cols = df2.columns
for i, client in df2.iterrows():
    for col in cols:
        score = client[col]
        format(round(score, 1))
        if score < 1.5:
            par = dftextos.loc[0, col]
        elif 1.5 <= score < 2.6:
            par = dftextos.loc[1, col]
        elif 2.6 <= score < 3.4:
            par = dftextos.loc[2, col]
        elif 3.4 <= score < 4.3:
            par = dftextos.loc[3, col]
        else:
            par = dftextos.loc[4, col]
        x.append(f'Estimado cliente {i} usted obtuvo un puntaje de {format(round(score,2))} en la seccion {col}.')
        x.append(f'Esto nos permite señalar que su organizacion esta en el siguiente estadio: {par}')
        x.append(" ")
str(x)
scores = np.floor(df2[cols]).astype('int')

#creamos los labels para poder sacar el grafico de araña
labels=np.array(df2.columns)

#creamos los angulos para que se puedan ubicar al interior del radar los datos
angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)

#creamos la seccion means
means=df2.loc[0].values

#concatemos means conjuntamente con angles para que nos arroje el resultado
means = np.concatenate((means,[means[0]]))
angles = np.concatenate((angles,[angles[0]]))

#creamos ya la figura de radar que necesitmaos para enviar al cliente
#esta solución sin embargo es mejor enviarla en excel o power bi por estetica
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot(angles, means, 'o-', linewidth=2)
ax.fill(angles, means, alpha=0.25)
ax.set_thetagrids(angles * 180/np.pi, labels)
ax.set_title("Value Scan Digital")
ax.grid(True)
plt.ylim(0,5)
fig.savefig('valuescan.png')

#esta grafica de plotly es mas bonita, es necesario abrirla desde jupyter notebook pues en lab aun no se puede ver y no hay soporte

fig = go.Figure(data=go.Scatterpolar(
  r=means,
  theta=labels,
  fill='toself'
))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True
    ),
  ),
  showlegend=False
)

fig.show()