# 📚 Руководство по миграциям Alembic

## 🎯 Обзор

Этот проект использует **Alembic** для управления миграциями базы данных PostgreSQL. Alembic позволяет:
- Отслеживать изменения схемы БД
- Применять миграции автоматически
- Откатывать изменения при необходимости
- Синхронизировать схему между окружениями

## 🚀 Быстрый старт

### 1. Проверка статуса миграций
```powershell
.\manage_migrations_simple.ps1 status
```

### 2. Применение всех миграций
```powershell
.\manage_migrations_simple.ps1 upgrade
```

### 3. Создание новой миграции
```powershell
.\manage_migrations_simple.ps1 create "Описание изменений"
```

## 🔧 Доступные команды

| Команда | Описание | Пример |
|---------|----------|---------|
| `status` | Показать статус и историю миграций | `.\manage_migrations_simple.ps1 status` |
| `current` | Показать текущую версию | `.\manage_migrations_simple.ps1 current` |
| `history` | Показать историю миграций | `.\manage_migrations_simple.ps1 history` |
| `upgrade` | Применить все миграции | `.\manage_migrations_simple.ps1 upgrade` |
| `downgrade` | Откатить на одну версию | `.\manage_migrations_simple.ps1 downgrade` |
| `create` | Создать новую миграцию | `.\manage_migrations_simple.ps1 create "Add user roles"` |
| `reset` | Сбросить БД и применить миграции | `.\manage_migrations_simple.ps1 reset` |

## 📁 Структура файлов

```
alembic/
├── alembic.ini          # Конфигурация Alembic
├── env.py               # Настройки окружения
├── script.py.mako       # Шаблон для миграций
└── versions/            # Папка с миграциями
    └── initial_migration.py  # Наша первая миграция
```

## 🗄️ Текущая схема базы данных

### Таблицы
- **`users`** - Пользователи системы
- **`pastes`** - Основная таблица паст
- **`tags`** - Теги для паст
- **`paste_tags`** - Связующая таблица паст и тегов

### Представления
- **`recent_pastes`** - Недавние пасты с информацией об авторах

### Индексы
- `idx_pastes_language` - по языку программирования
- `idx_pastes_title_search` - по названию
- `idx_pastes_created_at` - по дате создания
- `idx_pastes_expires_at` - по дате истечения

## 🔄 Жизненный цикл миграции

### 1. Создание миграции
```powershell
.\manage_migrations_simple.ps1 create "Add new field"
```

### 2. Редактирование миграции
Отредактируйте созданный файл в `alembic/versions/`

### 3. Применение миграции
```powershell
.\manage_migrations_simple.ps1 upgrade
```

### 4. Откат при необходимости
```powershell
.\manage_migrations_simple.ps1 downgrade
```

## ⚠️ Важные моменты

### Безопасность
- **ВНИМАНИЕ**: Команда `reset` удаляет все данные!
- Всегда делайте бэкап перед применением миграций в продакшене
- Тестируйте миграции на копии данных

### Порядок операций
1. Создайте миграцию
2. Протестируйте на тестовых данных
3. Примените на продакшене
4. Проверьте корректность работы

### Зависимости
- Убедитесь, что PostgreSQL запущен
- Проверьте подключение к базе данных
- Убедитесь, что все Python зависимости установлены

## 🐛 Решение проблем

### Ошибка "table already exists"
```powershell
.\manage_migrations_simple.ps1 reset
```

### Проблемы с подключением
1. Проверьте статус PostgreSQL: `docker ps`
2. Проверьте переменные окружения в `config.env`
3. Убедитесь, что порт 5432 доступен

### Конфликты миграций
1. Проверьте текущий статус: `.\manage_migrations_simple.ps1 status`
2. При необходимости откатитесь: `.\manage_migrations_simple.ps1 downgrade`
3. Создайте новую миграцию с исправлениями

## 📖 Полезные ссылки

- [Документация Alembic](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🎉 Готово!

Теперь у вас есть полноценная система управления миграциями для PasteBin! 

**Следующие шаги:**
1. Протестируйте создание пасты через веб-интерфейс
2. Создайте дополнительные миграции по мере необходимости
3. Настройте автоматическое применение миграций в CI/CD
