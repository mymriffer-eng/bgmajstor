# 🔐 Production Settings Security Notice

## ⚠️ ВАЖНО: Чувствителни данни

Файлът `config/settings_production.py` съдържа чувствителна информация:
- SECRET_KEY
- Database credentials (password)
- Email SMTP password

## 🚫 Защо НЕ е в Git?

`config/settings_production.py` е добавен в `.gitignore` защото GitHub repository-то е **PUBLIC**.

**НИКОГА не качвайте credentials в публично repo!**

## ✅ Как да setup-наш production настройките?

### 1. Копирай template файла:
```bash
cp config/settings_production.py.template config/settings_production.py
```

### 2. Попълни реалните credentials:

Отвори `config/settings_production.py` и замени:

**SECRET_KEY:**
```python
# Генерирай нов:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Database credentials (от cPanel → MySQL Databases):**
```python
'NAME': 'your_actual_database_name',
'USER': 'your_actual_database_user',
'PASSWORD': 'your_actual_database_password',
```

**Email SMTP credentials (от cPanel → Email Accounts):**
```python
EMAIL_HOST_USER = 'support@bgmajstor.eu',
EMAIL_HOST_PASSWORD = 'your_actual_email_password',
```

### 3. Проверка:
```bash
# Убедете се че settings_production.py НЕ е в Git:
git status

# Трябва да видите:
# Untracked files:
#   config/settings_production.py.template
# 
# settings_production.py НЕ трябва да се появява!
```

## 📋 За deployment на cPanel:

1. Upload на всички файлове **БЕЗ** `settings_production.py`
2. На сървъра (SSH или File Manager) създай `settings_production.py` директно с реалните credentials
3. Или използвай template файла и попълни данните на сървъра

## 🔒 Best Practices:

- ✅ Пазете credentials само на production сървъра
- ✅ Използвайте различни SECRET_KEY за development и production
- ✅ Използвайте силни пароли за database и email
- ❌ Никога не споделяйте credentials в Slack, Discord или други chat apps
- ❌ Никога не commit-вайте credentials в Git (дори в private repo)

## 🆘 Ако случайно качите credentials в Git:

1. Променете всички пароли ВЕДНАГА
2. Генерирайте нов SECRET_KEY
3. Използвайте `git filter-branch` или BFG Repo-Cleaner за изчистване на историята
4. Свържете се с хостинг провайдера ако е необходимо
