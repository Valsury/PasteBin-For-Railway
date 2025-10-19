# 🔄 Исправление синхронизации статуса паст

## 🚨 Проблема

### **Что происходило:**
- Паста показывала "Истекла" в колонке "ВРЕМЯ ЖИЗНИ"
- Но при этом в колонке "СТАТУС" показывала "Активна"
- Это создавало противоречие в интерфейсе

### **Причина:**
- Функция `get_remaining_time_formatted()` возвращала "Истекла" для истекших паст
- Но поле `is_expired` в базе данных не обновлялось автоматически
- Статус пасты не синхронизировался с реальным временем истечения

## ✅ Решение

### **1. Автоматическая проверка истечения:**
- **При загрузке страниц** (`/`, `/recent`) автоматически проверяется истечение паст
- **При попытке просмотра** пасты проверяется истечение
- **Автоматическое обновление** поля `is_expired` в базе данных

### **2. Синхронизация статуса:**
- **Backend**: обновляет `is_expired` в БД
- **Frontend**: JavaScript обновляет отображение статуса в реальном времени
- **Единообразие**: статус и время жизни всегда синхронизированы

## 🔧 Техническая реализация

### **Backend изменения:**

#### **Функция `recent_pastes()`:**
```python
@app.route('/recent')
def recent_pastes():
    """Страница недавних паст"""
    try:
        # Получаем недавние пасты из БД
        pastes = Paste.query.filter_by(is_expired=False).order_by(
            Paste.created_at.desc()
        ).all()
        
        # Проверяем истечение паст и обновляем их статус
        expired_pastes_ids = []
        for paste in pastes:
            if paste.expires_at and paste.expires_at < datetime.now(timezone.utc):
                paste.is_expired = True
                expired_pastes_ids.append(paste.id)
        
        # Сохраняем изменения в БД если есть истекшие пасты
        if expired_pastes_ids:
            db.session.commit()
            print(f"Пасты {expired_pastes_ids} помечены как истекшие")
        
        # ... остальной код
```

#### **Функция `index()`:**
```python
@app.route('/')
def index():
    """Главная страница"""
    try:
        # Получаем недавние пасты из БД
        recent_pastes = Paste.query.filter_by(is_expired=False).order_by(
            Paste.created_at.desc()
        ).limit(5).all()
        
        # Проверяем истечение паст и обновляем их статус
        expired_pastes_ids = []
        for paste in recent_pastes:
            if paste.expires_at and paste.expires_at < datetime.now(timezone.utc):
                paste.is_expired = True
                expired_pastes_ids.append(paste.id)
        
        # Сохраняем изменения в БД если есть истекшие пасты
        if expired_pastes_ids:
            db.session.commit()
            print(f"Пасты {expired_pastes_ids} помечены как истекшие на главной странице")
        
        # ... остальной код
```

#### **Функция `view_paste()`:**
```python
@app.route('/paste/<int:paste_id>')
def view_paste(paste_id):
    """Страница просмотра пасты"""
    try:
        # Получаем пасту из БД
        paste = Paste.query.get_or_404(paste_id)
        
        # Проверяем, не истекла ли паста
        if paste.expires_at and paste.expires_at < datetime.now(timezone.utc):
            # Помечаем как истекшую если еще не помечена
            if not paste.is_expired:
                paste.is_expired = True
                db.session.commit()
                print(f"Паста {paste_id} помечена как истекшая при попытке просмотра")
            
            flash('Паста истекла', 'error')
            return redirect(url_for('index'))
        
        # ... остальной код
```

### **Frontend изменения:**

#### **JavaScript обновление статуса:**
```javascript
if (remainingMinutes <= 0) {
    // Паста истекла
    timeDisplay.textContent = "Истекла";
    timeDisplay.className = "time-display text-danger";
    
    // Обновляем статус на "Истекла"
    const statusCell = timeElement.closest('tr').querySelector('.badge');
    if (statusCell) {
        if (statusCell.classList.contains('bg-success')) {
            statusCell.className = 'badge bg-danger';
            statusCell.innerHTML = '<i class="fas fa-times-circle me-1"></i>Истекла';
        } else if (statusCell.classList.contains('bg-warning')) {
            statusCell.className = 'badge bg-danger';
            statusCell.innerHTML = '<i class="fas fa-times-circle me-1"></i>Истекла';
        }
    }
} else {
    // ... код для активных паст
}
```

## 🎯 Результат

### **До исправления:**
- ❌ "ВРЕМЯ ЖИЗНИ": "Истекла"
- ❌ "СТАТУС": "Активна"
- ❌ **Противоречие** в интерфейсе

### **После исправления:**
- ✅ "ВРЕМЯ ЖИЗНИ": "Истекла"
- ✅ "СТАТУС": "Истекла"
- ✅ **Полная синхронизация** статуса и времени

## 🚀 Преимущества

### **Для пользователей:**
- ✅ **Консистентность** - статус и время жизни всегда совпадают
- ✅ **Актуальность** - статус обновляется в реальном времени
- ✅ **Понятность** - нет противоречий в интерфейсе

### **Для системы:**
- ✅ **Автоматизация** - не нужно вручную обновлять статус
- ✅ **Надежность** - статус всегда соответствует реальности
- ✅ **Производительность** - проверка происходит только при необходимости

## 📱 Обновленные файлы

- `app.py` - функции `recent_pastes()`, `index()`, `view_paste()`
- `templates/recent.html` - JavaScript обновление статуса
- `templates/index.html` - JavaScript обновление статуса

## 🔮 Возможные улучшения

### **В будущих версиях:**
- **WebSocket уведомления** о истечении паст в реальном времени
- **Автоматическое скрытие** истекших паст из списков
- **Уведомления** пользователям о приближении истечения
- **Архивирование** истекших паст вместо удаления

---

**Теперь статус паст всегда синхронизирован с временем жизни!** 🔄✨
