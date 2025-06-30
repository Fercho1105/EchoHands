import pickle
import cv2
import mediapipe as mp
import numpy as np
import random
import time
import os
from labels import labels_dict

# Cargar modelo entrenado
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Inicializar cámara y MediaPipe
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Lista de palabras válidas sin J ni Z
valid_words = [
    "mano", "cielo", "perro", "gato", "hola", "mesa", "libro", "verde",
    "silla", "piano", "raton", "botella", "casa", "puerta", "flor", "lago",
    "roca", "punto", "nube", "copa"
]
valid_words = [w.upper() for w in valid_words if 'J' not in w and 'Z' not in w]

# Variables del juego
current_word = random.choice(valid_words)
current_index = 0
last_letter_time = time.time()
puntos = 0
mostrar_correcto = False
correcto_timer = 0

# Menú de inicio
def show_menu():
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        menu = np.zeros_like(frame)
        for i in range(menu.shape[0]):
            intensity = 50 + int(i / menu.shape[0] * 100)
            menu[i, :, :] = (intensity, intensity, intensity)

        color = (255, 0, 0)  # Azul
        border_thickness = 10
        cv2.rectangle(menu, (0, 0), (menu.shape[1] - 1, menu.shape[0] - 1), color, border_thickness)

        cv2.putText(menu, 'EchoHands', (80, 120), cv2.FONT_HERSHEY_DUPLEX, 2.2, (0, 0, 0), 6)
        cv2.putText(menu, 'EchoHands', (80, 120), cv2.FONT_HERSHEY_DUPLEX, 2.2, (255, 0, 0), 3)
        cv2.putText(menu, 'Practica ASL deletreando palabras', (80, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.putText(menu, 'Presiona "I" para iniciar', (100, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 255), 1)
        cv2.putText(menu, 'Presiona "Q" para salir', (100, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 200), 1)
        cv2.putText(menu, 'v1.0', (menu.shape[1] - 80, menu.shape[0] - 30), cv2.FONT_HERSHEY_PLAIN, 1.5, (180, 180, 180), 2)

        cv2.imshow("EchoHands - Menu", menu)
        key = cv2.waitKey(1)
        if key == ord('i'):
            break
        elif key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()

# Mostrar menú
show_menu()

# Bucle principal
while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()
    if not ret:
        continue

    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    predicted_character = ""

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        if len(data_aux) == 42:  # 21 puntos * 2 coords
            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = labels_dict[int(prediction[0])]

            # Dibujar el cuadro alrededor de la mano
            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10
            x2 = int(max(x_) * W) + 10
            y2 = int(max(y_) * H) + 10
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            # Mostrar letra detectada dentro del cuadro
            cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)

            # Comparar con letra esperada
            if predicted_character == current_word[current_index]:
                if time.time() - last_letter_time > 1.0:
                    current_index += 1
                    last_letter_time = time.time()

                    if current_index == len(current_word):
                        puntos += 1
                        mostrar_correcto = True
                        correcto_timer = time.time()
                        current_word = random.choice(valid_words)
                        current_index = 0
                        time.sleep(0.5)

    # Mostrar interfaz
    cv2.putText(frame, f"Palabra: {current_word}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(frame, f"Letra esperada: {current_word[current_index]}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    cv2.putText(frame, f"Puntuacion: {puntos}", (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
    if mostrar_correcto and time.time() - correcto_timer < 1.5:
        cv2.putText(frame, "CORRECTO!", (W//2 - 150, H//2), cv2.FONT_HERSHEY_DUPLEX, 2.0, (0, 255, 0), 4)
    else:
        mostrar_correcto = False

    cv2.putText(frame, 'Presiona "Q" para salir', (30, H - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 255), 2)

    cv2.imshow("EchoHands - Juego ASL", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
