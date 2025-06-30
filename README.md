# ✋ EchoHands

**EchoHands** es una aplicación interactiva que permite practicar el alfabeto del lenguaje de señas americana (ASL) a través de visión por computadora. Utiliza modelos de aprendizaje automático y MediaPipe para reconocer letras del abecedario hechas con la mano en tiempo real mediante la cámara.

## 🧠 Descripción

EchoHands ofrece una forma divertida y educativa de practicar el deletreo de palabras en ASL. Se muestra una palabra aleatoria en pantalla, y el usuario debe representar cada letra con la mano. El sistema detecta la letra mediante un modelo de clasificación y otorga puntos al completarla correctamente.

## 🎯 Funcionalidades

- 📷 Captura de imágenes de manos para entrenamiento.
- 🧩 Extracción de puntos clave de la mano con MediaPipe.
- 🧠 Entrenamiento de modelo de clasificación con Random Forest.
- 🕹️ Juego interactivo para practicar palabras en ASL.
- 🎮 Interfaz visual con puntuación y retroalimentación.

## 📂 Estructura de archivos

| Archivo                  | Descripción |
|--------------------------|-------------|
| `collect_imgs.py`        | Captura imágenes de las manos por clase (letra). |
| `create_dataset.py`      | Procesa las imágenes y genera el dataset con coordenadas. |
| `train_classifier.py`    | Entrena un modelo Random Forest con el dataset. |
| `labels.py`              | Diccionario de mapeo entre índices y letras ASL. |
| `inference_classifier.py`| Ejecuta el juego interactivo de práctica en tiempo real. |

## 🛠️ Tecnologías utilizadas

- Python
- OpenCV
- MediaPipe
- scikit-learn
- NumPy
- pickle

## 🚀 Cómo ejecutar el proyecto

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/Fercho1105/EchoHands.git
   cd EchoHands
   ```

2. **Instala las dependencias**
   Asegúrate de tener Python 3 y luego instala:
   ```bash
   pip install opencv-python mediapipe scikit-learn matplotlib
   ```

3. **Recolecta imágenes**
   ```bash
   python collect_imgs.py
   ```
   Presiona `Q` para comenzar la captura de imágenes por clase.

4. **Genera el dataset**
   ```bash
   python create_dataset.py
   ```

5. **Entrena el modelo**
   ```bash
   python train_classifier.py
   ```

6. **Inicia el juego de práctica ASL**
   ```bash
   python inference_classifier.py
   ```

## 📦 Versión

v1.0
