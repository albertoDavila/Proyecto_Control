​​
# Instalar Python 3 en caso de no tenerlo

En el siguiente link se podrá instalar pyhton 3.
Para el desarrollo de este proyecto se utilizó pyhton 3.7

https://www.python.org/downloads/

#Descargar librerias requeridas

Escribir la siguiente línea de código en la terminal.
Si se cuenta con un ambiente virtual asegurarse que se haya activado previamente.

```
 pip install numpy pip install pandas pip install matplotlib pip install tk
```
# Ejecución del programa

Ir a la carpeta donde se encuentran los archivos y correr la siguiente linea de código:

```
pyhton main.py
```

# Instrucciones de uso

El modelo que está más avanzado es el de "Modelo de primer orden". Por el momento este modelo muestra los resultados de la salida c(k) y grafica estos valores y la entrada m(k).
Sin embargo, por el momento se requiere pausar el programa para modificar los valores.

Por otro lado, el modelo general ARX da como salida los valores de la respuesta c(k), esto tanto en un renglón del GUI y en una ventana emergente.
El programa acepta hasta 5 coeficientes de a's y b's. Es importante tener en cuenta que si no se quiere utilizar un coeficiente se tiene que poner este valor en 0.
Ejemplo de como deben de ir: 0.7,0,0,0,0

Se está trabajando en la integración completa de esta modelo

# Google Colab

Además, en lo que se obtiene la aplicación final se hizo se elaboraron archivos de Google Colab con  los dos modelos  terminados  y graficados.

Modelo ARX: https://drive.google.com/file/d/1-aJLNNSbMwBc9SRpWtNyA3CMGuLn3HEg/view?usp=sharing

Modelo Primer Orden: https://drive.google.com/file/d/1-aJLNNSbMwBc9SRpWtNyA3CMGuLn3HEg/view?usp=sharing

# Documento en excel

Se puede obtener el documento de excel con la simualción de los dos modelos en el siguiente lik:

https://drive.google.com/drive/folders/15rWiq1uEcsZmT0TMoa8sehna1xd0NsTH?usp=sharing
