import requests

# URL вашего FastAPI сервера (если запущен локально)
API_URL_IMG = "http://127.0.0.1:8000/parse_card_from_img/"
API_URL_TXT = "http://127.0.0.1:8000/create_struct_from_desc/"

# Путь к изображению, которое хотите отправить
IMAGE_PATH = "imgs/iron-golem.png"  # замените на реальный путь

DESCRIPTION = """
Это огромное существо похоже на смесь тролля и дракона. Его кожа покрыта чешуей, он испускает лёгкий дым из ноздрей, а его когти как лезвия. Обитает в горах и охраняет древние руины.
"""


def send_image_to_api():
    try:
        # Открываем файл изображения в бинарном режиме
        with open(IMAGE_PATH, "rb") as image_file:
            # Создаем словарь с файлом для отправки
            files = {"file": (IMAGE_PATH, image_file, "image/jpeg")}

            # Отправляем POST-запрос
            response = requests.post(API_URL_IMG, files=files)

            # Проверяем статус ответа
            if response.status_code == 200:
                print("Успешный ответ:")
                print(response.json())
            else:
                print(f"Ошибка: {response.status_code}")
                print(response.json())

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

def send_description_to_api():
    try:
        payload = {"desc": DESCRIPTION}
        headers = {"Content-Type": "application/json"}

        response = requests.post(API_URL_TXT, json=payload, headers=headers)

        if response.status_code == 200:
            print("Успешный ответ:")
            print(response.json())
        else:
            print(f"Ошибка: {response.status_code}")
            print(response.json())

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    send_image_to_api()
    send_description_to_api()