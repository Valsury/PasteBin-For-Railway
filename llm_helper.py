import requests
import json
import time

class OllamaHelper:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.model = None
        self.available_models = []
        self._load_available_models()

    def _load_available_models(self):
        """Загружает список доступных моделей"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models_data = response.json()
                self.available_models = [model['name'] for model in models_data.get('models', [])]
                print(f"Доступные модели Ollama: {self.available_models}")
                if self.available_models and self.model is None:
                    self.model = self.available_models[0]
                    print(f"Автоматически выбрана модель: {self.model}")
            else:
                print(f"Не удалось загрузить модели: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при загрузке моделей: {e}")

    def set_model(self, model_name):
        """Устанавливает активную модель"""
        if model_name in self.available_models:
            self.model = model_name
            print(f"Модель изменена на: {self.model}")
            return True
        else:
            print(f"Модель {model_name} не найдена")
            return False

    def get_available_models(self):
        """Возвращает список доступных моделей"""
        return self.available_models

    def is_available(self):
        """Проверяет доступность Ollama сервера"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False

    def generate_text(self, prompt, max_tokens=800):
        """Генерирует текст на основе промпта"""
        if not self.model:
            return {"error": "Модель не выбрана"}
        
        try:
            response = requests.post(f"{self.base_url}/api/generate", json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens
                }
            })
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "text": result.get("response", ""),
                    "model": self.model,
                    "tokens_used": len(result.get("response", "").split())
                }
            else:
                return {"error": f"HTTP ошибка: {response.status_code}"}
        except Exception as e:
            return {"error": f"Ошибка запроса: {str(e)}"}

    def generate_code(self, language, description, max_tokens=600):
        """Генерирует код на указанном языке"""
        prompt = f"Напиши код на языке {language} для следующей задачи: {description}. Код должен быть рабочим и хорошо прокомментированным."
        return self.generate_text(prompt, max_tokens)

    def improve_code(self, code, language, description, max_tokens=800):
        """Улучшает существующий код"""
        prompt = f"Улучши следующий код на языке {language}:\n\n{code}\n\nОписание улучшений: {description}\n\nПокажи улучшенную версию с объяснениями."
        return self.generate_text(prompt, max_tokens)

    def explain_code(self, code, language, max_tokens=600):
        """Объясняет код на указанном языке"""
        prompt = f"Объясни следующий код на языке {language} простыми словами:\n\n{code}\n\nОбъяснение должно быть понятным для начинающих программистов."
        return self.generate_text(prompt, max_tokens)

    def generate_documentation(self, code, language, max_tokens=500):
        """Генерирует документацию для кода"""
        prompt = f"Создай документацию для следующего кода на языке {language}:\n\n{code}\n\nДокументация должна включать описание функций, параметров и примеры использования."
        return self.generate_text(prompt, max_tokens)

    # === УНИВЕРСАЛЬНЫЕ МЕТОДЫ ГЕНЕРАЦИИ ТЕКСТА ===
    
    def generate_creative_text(self, topic, style="общий", max_tokens=800):
        """Генерирует креативный текст на заданную тему"""
        prompt = f"Создай креативный текст в стиле '{style}' на тему '{topic}'. Текст должен быть интересным, оригинальным и захватывающим внимание читателя."
        return self.generate_text(prompt, max_tokens)

    def generate_business_text(self, topic, text_type="описание", max_tokens=600):
        """Генерирует бизнес-текст"""
        prompt = f"Создай профессиональный бизнес-текст типа '{text_type}' на тему '{topic}'. Текст должен быть структурированным, убедительным и подходящим для деловой аудитории."
        return self.generate_text(prompt, max_tokens)

    def generate_educational_text(self, topic, level="средний", max_tokens=700):
        """Генерирует образовательный текст"""
        prompt = f"Создай образовательный текст уровня '{level}' на тему '{topic}'. Текст должен быть понятным, структурированным и содержать полезную информацию для обучения."
        return self.generate_text(prompt, max_tokens)

    def generate_story(self, genre, theme, max_tokens=1000):
        """Генерирует рассказ или историю"""
        prompt = f"Создай {genre} рассказ на тему '{theme}'. История должна быть увлекательной, с интересными персонажами и захватывающим сюжетом."
        return self.generate_text(prompt, max_tokens)

    def generate_article(self, topic, style="информационный", max_tokens=800):
        """Генерирует статью"""
        prompt = f"Напиши {style} статью на тему '{topic}'. Статья должна быть информативной, хорошо структурированной и интересной для чтения."
        return self.generate_text(prompt, max_tokens)

    def generate_social_media_content(self, platform, topic, tone="дружелюбный", max_tokens=300):
        """Генерирует контент для социальных сетей"""
        prompt = f"Создай {tone} пост для {platform} на тему '{topic}'. Контент должен быть привлекательным, вовлекающим и подходящим для выбранной платформы."
        return self.generate_text(prompt, max_tokens)

    def generate_poem(self, theme, style="современный", max_tokens=400):
        """Генерирует стихотворение"""
        prompt = f"Создай {style} стихотворение на тему '{theme}'. Стихотворение должно быть эмоциональным, образным и ритмичным."
        return self.generate_text(prompt, max_tokens)

    def generate_marketing_copy(self, product, target_audience, max_tokens=500):
        """Генерирует маркетинговый текст"""
        prompt = f"Создай привлекательный маркетинговый текст для продукта '{product}', ориентированный на аудиторию '{target_audience}'. Текст должен быть убедительным и мотивирующим к действию."
        return self.generate_text(prompt, max_tokens)

    def generate_email_template(self, purpose, tone="профессиональный", max_tokens=400):
        """Генерирует шаблон email"""
        prompt = f"Создай {tone} шаблон email для {purpose}. Email должен быть четким, вежливым и эффективным в достижении цели."
        return self.generate_text(prompt, max_tokens)

    def generate_presentation_outline(self, topic, audience, max_tokens=600):
        """Генерирует план презентации"""
        prompt = f"Создай структурированный план презентации на тему '{topic}' для аудитории '{audience}'. План должен включать введение, основные пункты и заключение."
        return self.generate_text(prompt, max_tokens)
