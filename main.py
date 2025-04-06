from fastapi import FastAPI, File, UploadFile, Body
from fastapi.responses import JSONResponse
from google import genai
from dotenv import load_dotenv
from PIL import Image
import io
import json
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-2.0-flash"

app = FastAPI()


def load_example(structure_path="dnd_card_template.json"):
    with open(structure_path, "r", encoding="utf-8") as f:
        return json.load(f)


json_example = load_example()


def create_prompt_for_img_input():
    json_ex = json.dumps(json_example, ensure_ascii=False, indent=2)
    prompt = f"""
    На изображении — карточка персонажа из DnD.
    Проанализируй её и распарси содержимое в JSON, как в примере:

    {json_ex}

    Если чего-то нет на карточке — не добавляй это поле вовсе. Поля eng должны быть заполнены (сделай перевод сам)
    Ответ строго в формате JSON:
    """
    return prompt


def create_prompt_for_text_input(description):
    json_ex = json.dumps(json_example, ensure_ascii=False, indent=2)

    prompt = f"""
    Ты опытный мастер DnD. На основе описания существа создай его полную игровую карточку.
    Описание существа: {description}

    Пример структуры карточки: {json_ex}

    Заполняй те поля, которые считаешь необходимыми для данного персонажа. Остальные просто не добавляй.
    Поля eng должны быть заполнены (сделай перевод сам).
    В целом проявляй креативность и фантазию.

    Ответ строго в формате JSON:
    """

    return prompt


@app.post("/parse_card_from_img/")
async def parse_card_from_img(file: UploadFile = File(...)):
    """
    Обрабатывает изображение карточки DnD и возвращает JSON
    """
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    prompt = create_prompt_for_img_input()

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[
            prompt,
            image
        ]
    )

    cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
    # print(cleaned_response)

    try:
        result = json.loads(cleaned_response)
        return JSONResponse(content=result)
    except Exception:
        return JSONResponse(content={"error": "Не удалось распарсить ответ от модели"}, status_code=500)


@app.post("/create_struct_from_desc/")
async def create_struct_from_desc(body: dict = Body(...)):
    """
    Генерирует структуру существа DnD на основе текстового описания
    """

    prompt = create_prompt_for_text_input(body["desc"])

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt]
    )

    cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
    # print(cleaned_response)

    try:
        result = json.loads(cleaned_response)
        return JSONResponse(content=result)
    except Exception:
        return JSONResponse(content={"error": "Не удалось распарсить ответ от модели"}, status_code=500)
