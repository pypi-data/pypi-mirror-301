# Оценка текста:

TextEvaluator использует модель **AI-TQA1 Basic** для оценки текста и определения наличия в нем плохих слов или выражений. 

Алгоритм **автоматически** очищает текст от ненужных символов (например, заменяет "я-бло/ко" на "яблоко"), что **улучшает точность оценки**.

# Извлечение текста с фото:

Модуль может извлекать текст из фотографии для последующей обработки, используя бесплатный API ключ [Free OCR API](https://ocr.space/ocrapi)

# Точность работы:

Модель продемонстрировала **87.46**% точности в оценках на основе результатов тестирования, проведенного на **500** предложениях.

# Поддерживаемые языки:

- **Украинский**
- **Русский**

# Установка:

`pip install ai-tqa`

# Обновление:

`pip install --upgrade ai-tqa`

# Оценка текста:

```python
from ai_tqa import TextEvaluator

evaluator = TextEvaluator()

text = "Привет, даун!" # Текст для оценки

result_with_detail = evaluator.evaluate_text(text, detail=True) # Функция возвращает оценку со списком плохих слов
result_without_detail = evaluator.evaluate_text(text, detail=False) # Функция возвращает оценку текста

print(f"Результат с деталями: Оценка: {result_with_detail[0]}, Плохие слова: {result_with_detail[1]}") # Вывод результата оценки
print(f"Результат без деталей: Оценка: {result_without_detail}") # Вывод результата оценки
```

# Извлечение текста с фото:

```python
from ai_tqa import TextEvaluator

evaluator = TextEvaluator()

image_path = "example.png" # Путь к фото
api_key = "FREE_OCR_API" # API ключ Free OCR API
language = "rus" # Язык для обнаружения
extracted_text = evaluator.read_image(image_path, api_key=api_key, language=language) # Извлечение текста из фото

print(f"Извлеченный текст: {extracted_text}") # Вывод извлечённого текста
```

- [Получить ключ](https://ocr.space/ocrapi/freekey)
- [Документация](https://ocr.space/ocrapi)

# Контрибьюторы:

- **`_KroZen_`**