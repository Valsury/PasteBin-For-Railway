import os
import hashlib
import json
from datetime import datetime

class FileStorage:
    def __init__(self, upload_folder='uploads'):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)
    
    def save_paste_content(self, paste_id: int, content: str) -> str:
        """Сохраняет содержимое пасты в файл"""
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        filename = f"{paste_id}_{content_hash}.txt"
        filepath = os.path.join(self.upload_folder, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return content_hash
    
    def get_paste_content(self, paste_id: int, content_hash: str) -> str:
        """Получает содержимое пасты из файла"""
        filename = f"{paste_id}_{content_hash}.txt"
        filepath = os.path.join(self.upload_folder, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None
    
    def delete_paste_content(self, paste_id: int, content_hash: str):
        """Удаляет файл пасты"""
        filename = f"{paste_id}_{content_hash}.txt"
        filepath = os.path.join(self.upload_folder, filename)
        
        try:
            os.remove(filepath)
        except FileNotFoundError:
            pass
    
    def save_paste_metadata(self, paste_id: int, metadata: dict):
        """Сохраняет метаданные пасты"""
        filename = f"{paste_id}_metadata.json"
        filepath = os.path.join(self.upload_folder, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    def get_paste_metadata(self, paste_id: int) -> dict:
        """Получает метаданные пасты"""
        filename = f"{paste_id}_metadata.json"
        filepath = os.path.join(self.upload_folder, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def delete_paste_metadata(self, paste_id: int):
        """Удаляет метаданные пасты"""
        filename = f"{paste_id}_metadata.json"
        filepath = os.path.join(self.upload_folder, filename)
        
        try:
            os.remove(filepath)
        except FileNotFoundError:
            pass
    
    def list_paste_files(self, paste_id: int) -> list:
        """Список файлов пасты"""
        try:
            files = []
            for filename in os.listdir(self.upload_folder):
                if filename.startswith(f"{paste_id}_"):
                    filepath = os.path.join(self.upload_folder, filename)
                    stat = os.stat(filepath)
                    files.append({
                        'name': filename,
                        'size': stat.st_size,
                        'last_modified': datetime.fromtimestamp(stat.st_mtime)
                    })
            return files
        except Exception as e:
            print(f"Ошибка получения списка файлов: {e}")
            return []
    
    def get_bucket_info(self) -> dict:
        """Получает информацию о хранилище"""
        try:
            total_size = 0
            file_count = 0
            for filename in os.listdir(self.upload_folder):
                filepath = os.path.join(self.upload_folder, filename)
                if os.path.isfile(filepath):
                    total_size += os.path.getsize(filepath)
                    file_count += 1
            
            return {
                'bucket_name': self.upload_folder,
                'size': total_size,
                'file_count': file_count,
                'last_modified': datetime.now()
            }
        except Exception as e:
            return {
                'bucket_name': self.upload_folder,
                'size': 0,
                'file_count': 0,
                'last_modified': None
            }

