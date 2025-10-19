from minio import Minio
from minio.error import S3Error
import hashlib
import json
import os
import io
from datetime import datetime

class MinioStorage:
    def __init__(self):
        """Инициализация MinIO клиента"""
        self.client = Minio(
            os.getenv('MINIO_ENDPOINT', 'localhost:9000'),
            access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
            secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin123'),
            secure=os.getenv('MINIO_SECURE', 'false').lower() == 'true'
        )
        self.bucket_name = os.getenv('MINIO_BUCKET_NAME', 'pastes')
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Создает bucket если он не существует"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"Bucket '{self.bucket_name}' создан успешно")
            else:
                print(f"Bucket '{self.bucket_name}' уже существует")
        except S3Error as e:
            print(f"Ошибка при работе с bucket: {e}")
    
    def save_paste_content(self, paste_id: int, content: str) -> str:
        """Сохраняет содержимое пасты и возвращает хеш"""
        try:
            # Создаем хеш содержимого
            content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            
            # Путь к файлу в bucket
            object_name = f"{paste_id}/content.txt"
            
            # Создаем BytesIO объект для MinIO
            content_bytes = content.encode('utf-8')
            content_stream = io.BytesIO(content_bytes)
            
            # Загружаем содержимое
            self.client.put_object(
                self.bucket_name,
                object_name,
                content_stream,
                length=len(content_bytes),
                content_type='text/plain'
            )
            
            print(f"Содержимое пасты {paste_id} сохранено в MinIO")
            return content_hash
            
        except S3Error as e:
            print(f"Ошибка сохранения в MinIO: {e}")
            raise
    
    def get_paste_content(self, paste_id: int, content_hash: str) -> str:
        """Получает содержимое пасты"""
        try:
            object_name = f"{paste_id}/content.txt"
            print(f"Пытаемся загрузить содержимое пасты {paste_id} из {object_name}")
            
            # Скачиваем объект
            response = self.client.get_object(self.bucket_name, object_name)
            content = response.read().decode('utf-8')
            
            # Закрываем соединение
            response.close()
            response.release_conn()
            
            print(f"Содержимое пасты {paste_id} загружено из MinIO, длина: {len(content)}")
            return content
            
        except S3Error as e:
            print(f"Ошибка чтения из MinIO для пасты {paste_id}: {e}")
            raise
        except Exception as e:
            print(f"Неожиданная ошибка при загрузке пасты {paste_id}: {e}")
            raise
    
    def delete_paste_content(self, paste_id: int, content_hash: str):
        """Удаляет содержимое пасты"""
        try:
            object_name = f"{paste_id}/content.txt"
            
            # Удаляем объект
            self.client.remove_object(self.bucket_name, object_name)
            
            print(f"Содержимое пасты {paste_id} удалено из MinIO")
            
        except S3Error as e:
            print(f"Ошибка удаления из MinIO: {e}")
            raise
    
    def save_paste_metadata(self, paste_id: int, metadata: dict):
        """Сохраняет метаданные пасты"""
        try:
            object_name = f"{paste_id}/metadata.json"
            
            # Преобразуем в JSON
            metadata_json = json.dumps(metadata, ensure_ascii=False, indent=2)
            
            # Создаем BytesIO объект для MinIO
            metadata_bytes = metadata_json.encode('utf-8')
            metadata_stream = io.BytesIO(metadata_bytes)
            
            # Загружаем метаданные
            self.client.put_object(
                self.bucket_name,
                object_name,
                metadata_stream,
                length=len(metadata_bytes),
                content_type='application/json'
            )
            
            print(f"Метаданные пасты {paste_id} сохранены в MinIO")
            
        except S3Error as e:
            print(f"Ошибка сохранения метаданных: {e}")
            raise
    
    def get_paste_metadata(self, paste_id: int) -> dict:
        """Получает метаданные пасты"""
        try:
            object_name = f"{paste_id}/metadata.json"
            
            # Скачиваем объект
            response = self.client.get_object(self.bucket_name, object_name)
            metadata_json = response.read().decode('utf-8')
            
            # Закрываем соединение
            response.close()
            response.release_conn()
            
            # Парсим JSON
            metadata = json.loads(metadata_json)
            print(f"Метаданные пасты {paste_id} загружены из MinIO")
            return metadata
            
        except S3Error as e:
            print(f"Ошибка чтения метаданных: {e}")
            return {}
    
    def list_paste_files(self, paste_id: int) -> list:
        """Список файлов пасты"""
        try:
            prefix = f"{paste_id}/"
            objects = self.client.list_objects(self.bucket_name, prefix=prefix, recursive=True)
            
            files = []
            for obj in objects:
                files.append({
                    'name': obj.object_name,
                    'size': obj.size,
                    'last_modified': obj.last_modified
                })
            
            return files
            
        except S3Error as e:
            print(f"Ошибка получения списка файлов: {e}")
            return []
    
    def rename_paste_content(self, old_id: int, new_id: int, content_hash: str):
        """Переименовывает файл содержимого пасты с временного ID на реальный"""
        try:
            old_object_name = f"{old_id}/content.txt"
            new_object_name = f"{new_id}/content.txt"
            
            # Сначала читаем содержимое старого файла
            response = self.client.get_object(self.bucket_name, old_object_name)
            content = response.read()
            response.close()
            response.release_conn()
            
            # Создаем новый файл с правильным именем
            self.client.put_object(
                self.bucket_name,
                new_object_name,
                content,
                length=len(content),
                content_type='text/plain'
            )
            
            # Удаляем старый объект
            self.client.remove_object(self.bucket_name, old_object_name)
            
            print(f"Файл содержимого переименован с {old_id} на {new_id}")
            
        except S3Error as e:
            print(f"Ошибка переименования файла: {e}")
            raise

    def delete_paste_metadata(self, paste_id: int):
        """Удаляет метаданные пасты"""
        try:
            object_name = f"{paste_id}/metadata.json"
            
            # Удаляем объект
            self.client.remove_object(self.bucket_name, object_name)
            
            print(f"Метаданные пасты {paste_id} удалены из MinIO")
            
        except S3Error as e:
            print(f"Ошибка удаления метаданных: {e}")
            # Не вызываем raise, так как метаданные не критичны

    def get_bucket_info(self) -> dict:
        """Получает информацию о bucket"""
        try:
            stats = self.client.stat_object(self.bucket_name, "")
            return {
                'bucket_name': self.bucket_name,
                'size': stats.size,
                'last_modified': stats.last_modified
            }
        except S3Error:
            return {
                'bucket_name': self.bucket_name,
                'size': 0,
                'last_modified': None
            }
