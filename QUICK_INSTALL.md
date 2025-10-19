# 🚀 Быстрый старт PasteBin Pro

## ⚡ Установка за 5 минут

### 1. Автоматическая установка (Windows)

```powershell
# Запустите PowerShell от имени администратора
.\install-dependencies.ps1
```

### 2. Ручная установка

```bash
# Создание виртуального окружения
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# Установка зависимостей
pip install -r requirements.txt

# Если psycopg2-binary не устанавливается:
pip install psycopg2-binary --upgrade
```

### 3. Запуск сервисов

```powershell
# Запуск PostgreSQL и MinIO
.\start-services.ps1 start

# Проверка статуса
.\start-services.ps1 status
```

### 4. Запуск приложения

```bash
# Активируйте виртуальное окружение
.\.venv\Scripts\Activate.ps1

# Запуск Flask
py app.py
```

### 5. Откройте браузер

🌐 **http://127.0.0.1:5000**

## 🔧 Решение проблем с psycopg2

### Windows - Альтернативные источники:

```bash
# Вариант 1: Обновление pip
python -m pip install --upgrade pip
pip install psycopg2-binary

# Вариант 2: Альтернативный источник
pip install --only-binary=all psycopg2-binary

# Вариант 3: Установка wheel
pip install wheel
pip install psycopg2-binary

# Вариант 4: Conda (если установлен)
conda install psycopg2
```

### Если ничего не помогает:

1. Установите **Visual Studio Build Tools**
2. Установите **PostgreSQL** для Windows
3. Добавьте `C:\Program Files\PostgreSQL\[version]\bin` в PATH
4. Выполните: `pip install psycopg2`

## 📱 Доступные URL

- **Приложение**: http://127.0.0.1:5000
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin123)
- **PostgreSQL**: localhost:5432

## 🎯 Команды управления

```powershell
.\start-services.ps1 start      # Запуск
.\start-services.ps1 stop       # Остановка
.\start-services.ps1 restart    # Перезапуск
.\start-services.ps1 status     # Статус
.\start-services.ps1 health     # Проверка здоровья
.\start-services.ps1 logs       # Логи
```

## 🚨 Частые проблемы

1. **Docker не запущен** → Запустите Docker Desktop
2. **Порты заняты** → Остановите другие сервисы
3. **psycopg2 не устанавливается** → См. раздел "Решение проблем"
4. **База не подключается** → Подождите 15 секунд после запуска

---

**🎉 Готово! Создавайте пасты и используйте AI-помощника!**
