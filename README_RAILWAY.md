# 🚂 PasteBin Pro - Railway Deployment

## 🚀 Быстрый старт на Railway

### 1. Подготовка репозитория
```bash
git init
git add .
git commit -m "Initial commit for Railway"
git remote add origin https://github.com/yourusername/pastebin-pro-railway.git
git push -u origin main
```

### 2. Развертывание на Railway
1. Зайти на [railway.app](https://railway.app)
2. Войти через GitHub
3. Создать новый проект из репозитория
4. Добавить PostgreSQL сервис
5. Настроить переменные окружения

### 3. Переменные окружения
```
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
FLASK_DEBUG=false
```

### 4. Доступ к приложению
После развертывания приложение будет доступно по адресу:
`https://your-app-name.railway.app`

## 🔧 Архитектура

- **Flask приложение** - основной веб-сервер
- **PostgreSQL** - управляемая база данных Railway
- **Файловое хранилище** - локальные файлы (вместо MinIO)
- **Gunicorn** - WSGI сервер для продакшена

## 📊 Мониторинг

- **Логи**: Railway Dashboard → Logs
- **Метрики**: Railway Dashboard → Metrics
- **База данных**: Railway Dashboard → PostgreSQL

## 🆓 Лимиты бесплатного плана

- **500 часов/месяц** работы приложения
- **1GB RAM**
- **1GB дискового пространства**
- **Управляемая PostgreSQL**

## 🔄 Keep-alive

Для предотвращения сна приложения можно настроить:
- UptimeRobot: `https://your-app.railway.app/ping`
- Интервал: каждые 10 минут

