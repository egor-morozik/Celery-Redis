from celery import Celery
from PIL import Image
import os

app = Celery('tasks', 
             broker='redis://localhost:6379/0', 
             backend='redis://localhost:6379/0')

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

@app.task
def resize_image(filename, new_width=300):
    try:
        input_path = os.path.join(INPUT_DIR, filename)
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Файл {input_path} не найден")

        with Image.open(input_path) as img:
            original_width, original_height = img.size
            new_height = int((new_width / original_width) * original_height)

            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            output_filename = f"resized_{filename}"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            resized_img.save(output_path)
            
            print(f"Изображение успешно обработано и сохранено как {output_path}")
            return f"Изображение {filename} обработано, сохранено как {output_filename}"
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        raise e