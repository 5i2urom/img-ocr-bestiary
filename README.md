### 1. Парсинг структуры из изображения карточки
`POST /parse_card_from_img/`  
**Content-Type:** `multipart/form-data`  
**Параметр:** `file` (изображение в формате JPG/PNG)  

### 2. Генерация структуры существа по описанию
`POST /create_struct_from_desc/`  
**Content-Type:** `application/json`  
**Тело запроса:**
```json
{"desc": "Текст описания существа"}