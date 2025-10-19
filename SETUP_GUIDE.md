# 🚀 Руководство по установке PasteBin с MinIO + PostgreSQL

## 📋 Предварительные требования

- Windows 10/11
- Docker Desktop (уже установлен ✅)
- PowerShell 5.0+

## 🐳 Установка сервисов

### 1. Запуск сервисов

```powershell
# Запустить все сервисы
.\start-services.ps1

# Или с параметром
.\start-services.ps1 start
```

### 2. Проверка статуса

```powershell
.\start-services.ps1 status
```

### 3. Просмотр логов

```powershell
.\start-services.ps1 logs
```

## 🔧 Установка Python зависимостей

```bash
pip install -r requirements.txt
```

## 🌐 Доступ к сервисам

### PostgreSQL
- **Хост**: localhost
- **Порт**: 5432
- **База данных**: pastebin_db
- **Пользователь**: pastebin_user
- **Пароль**: pastebin_password

### MinIO
- **API Endpoint**: http://localhost:9000
- **Web Console**: http://localhost:9001
- **Access Key**: minioadmin
- **Secret Key**: minioadmin123

## 📁 Структура проекта

```
PasteBin/
├── docker-compose.yml          # Конфигурация Docker
├── init-db.sql                # Инициализация БД
├── config.env                  # Конфигурация окружения
├── start-services.ps1         # Скрипт управления
├── requirements.txt            # Python зависимости
├── app.py                     # Основное приложение
└── templates/                 # HTML шаблоны
```

## 🚀 Управление сервисами

### Доступные команды:

```powershell
.\start-services.ps1 start     # Запустить сервисы
.\start-services.ps1 stop      # Остановить сервисы
.\start-services.ps1 restart   # Перезапустить сервисы
.\start-services.ps1 status    # Показать статус
.\start-services.ps1 logs      # Показать логи
.\start-services.ps1 clean     # Очистить все данные
```

## 🔍 Проверка работы

### 1. Проверка PostgreSQL
```bash
# Подключение к БД
psql -h localhost -U pastebin_user -d pastebin_db
```

### 2. Проверка MinIO
- Откройте http://localhost:9001
- Войдите с minioadmin / minioadmin123
- Создайте bucket "pastes"

### 3. Проверка приложения
```bash
python app.py
```

## 🛠️ Устранение неполадок

### Проблема: Порт занят
```powershell
# Остановить все контейнеры
docker-compose down

# Проверить занятые порты
netstat -ano | findstr :5432
netstat -ano | findstr :9000
```

### Проблема: Docker не запущен
- Запустите Docker Desktop
- Дождитесь полной загрузки
- Попробуйте снова

### Проблема: Не удается подключиться к БД
```powershell
# Перезапустить сервисы
.\start-services.ps1 restart

# Проверить логи
.\start-services.ps1 logs
```

## 📊 Мониторинг

### Логи в реальном времени
```powershell
.\start-services.ps1 logs
```

### Статистика контейнеров
```powershell
docker stats
```

### Использование диска
```powershell
docker system df
```

## 🧹 Очистка

### Удаление всех данных
```powershell
.\start-services.ps1 clean
```

### Очистка Docker
```powershell
docker system prune -a
docker volume prune
```

## 🔐 Безопасность

### Изменение паролей по умолчанию
1. Отредактируйте `config.env`
2. Измените `POSTGRES_PASSWORD`
3. Измените `MINIO_ACCESS_KEY` и `MINIO_SECRET_KEY`
4. Перезапустите сервисы

### Ограничение доступа
- Измените порты в `docker-compose.yml`
- Настройте firewall
- Используйте VPN для удаленного доступа

## 📚 Следующие шаги

1. ✅ Установить сервисы
2. 🔄 Интегрировать в код
3. 🧪 Протестировать
4. 🚀 Запустить в продакшене

## 🆘 Поддержка

При возникновении проблем:
1. Проверьте логи: `.\start-services.ps1 logs`
2. Проверьте статус: `.\start-services.ps1 status`
3. Перезапустите: `.\start-services.ps1 restart`
4. Очистите и переустановите: `.\start-services.ps1 clean && .\start-services.ps1 start`
