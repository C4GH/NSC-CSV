import numpy as np

def similitud_coseno(vec1, vec2):
    producto_punto = np.dot(vec1, vec2)
    norma1 = np.linalg.norm(vec1)
    norma2 = np.linalg.norm(vec2)
    similitud = producto_punto / (norma1 * norma2)
    return similitud

def calcular_distancia(palabra1, palabra2, vocabulario, embeddings):
    try:
        idx1 = vocabulario.index(palabra1)
        idx2 = vocabulario.index(palabra2)
        emb1 = embeddings[idx1]
        emb2 = embeddings[idx2]
        similitud = similitud_coseno(emb1, emb2)
        return similitud
    except ValueError as e:
        print(f"Error: {e}")
        return None

def guardar_resultados_consulta(ruta_archivo, consulta, resultado):
    with open(ruta_archivo, 'a', encoding='utf-8') as f:
        f.write(f"Consulta: {consulta}\n")
        f.write(f"Resultado: {resultado}\n\n")

if __name__ == '__main__':
    with open('vectors_filtrado.txt', 'rt', encoding='utf-8') as fi:
        contenido = fi.read().strip().split('\n')

    vocabulario, embeddings = [], []

    for i in range(len(contenido)):
        palabra = contenido[i].split(' ')[0]
        vector = [float(val) for val in contenido[i].split(' ')[1:]]
        vocabulario.append(palabra)
        embeddings.append(vector)

    vocabulario_npa = np.array(vocabulario)
    embs_npa = np.array(embeddings)

    # Pedir al usuario las palabras para medir la distancia (ignorar espacios)
    palabra1 = input("Ingresa la primera palabra: ").replace(" ", "")
    palabra2 = input("Ingresa la segunda palabra (sinónimo): ").replace(" ", "")
    palabra3 = input("Ingresa la tercera palabra (antónimo): ").replace(" ", "")

    # Calcular y mostrar la distancia si las palabras están en el vocabulario
    distancia1 = calcular_distancia(palabra1, palabra2, vocabulario, embeddings)
    distancia2 = calcular_distancia(palabra1, palabra3, vocabulario, embeddings)
    distancia3 = calcular_distancia(palabra2, palabra3, vocabulario, embeddings)

    if all(dist is not None for dist in [distancia1, distancia2, distancia3]):
        print(f"Distancia entre '{palabra1}' y '{palabra2}' (sinónimo): {distancia1}")
        print(f"Distancia entre '{palabra1}' y '{palabra3}' (antónimo): {distancia2}")
        print(f"Distancia entre '{palabra2}' y '{palabra3}': {distancia3}")

        # Guardar la consulta y resultados en un archivo
        consulta = f"{palabra1} - {palabra2} - {palabra3}"
        resultado = f"Distancias: {distancia1}, {distancia2}, {distancia3}"
        guardar_resultados_consulta('consultas.txt', consulta, resultado)
