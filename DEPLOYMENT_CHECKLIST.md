# ⚠️ ПРЕДИ DEPLOYMENT - ЗАДЪЛЖИТЕЛНИ СТЪПКИ

## 🔐 КРИТИЧНО: Промени SECRET_KEY

В `config/settings_production.py` на ред 17:

**Текущо:**
```python
SECRET_KEY = 'django-insecure-CHANGE-THIS-IN-PRODUCTION-GENERATE-NEW-KEY-12345'
```

**Генерирай нов ключ:**

### На локалната машина (преди upload):
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### ИЛИ на сървъра в SSH:
```bash
cd /home/bghranac/bgmajstor
source /home/bghranac/virtualenv/bgmajstor/3.9/bin/activate
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Копирай генерирания ключ и замени в settings_production.py!**

---

## ✅ Какво е готово:

1. ✓ **ALLOWED_HOSTS** → bgmajstor.eu, www.bgmajstor.eu
2. ✓ **CSRF_TRUSTED_ORIGINS** → https://bgmajstor.eu, https://www.bgmajstor.eu
3. ✓ **DATABASE** → MySQL активиран с credentials
4. ✓ **EMAIL** → SMTP конфигурация с support@bgmajstor.eu
5. ✓ **STATIC/MEDIA** → public_html директории
6. ✓ **LOGGING** → Error logs в logs/django_error.log
7. ✓ **SECURITY** → SSL redirect, secure cookies, HSTS

---

## 📋 Deployment checklist в cPanel:

### 1. Upload файлове
```bash
# Изключи от upload:
- venv/
- db.sqlite3
- __pycache__/
- *.pyc
- logs/*.log (само .gitkeep)
```

### 2. Setup Python App
- Python version: 3.9+
- App root: `/home/bghranac/bgmajstor`
- Startup file: `passenger_wsgi.py`

### 3. Инсталирай dependencies
```bash
cd /home/bghranac/bgmajstor
source /home/bghranac/virtualenv/bgmajstor/3.9/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install mysqlclient
```

### 4. Генерирай SECRET_KEY и обнови settings_production.py
```bash
nano config/settings_production.py
# Замени SECRET_KEY на ред 17
```

### 5. Създай директории
```bash
mkdir -p public_html/static
mkdir -p public_html/media
mkdir -p logs
chmod 755 public_html/static
chmod 755 public_html/media
chmod 755 logs
```

### 6. Django setup
```bash
python manage.py migrate --settings=config.settings_production
python manage.py collectstatic --settings=config.settings_production --noinput
python manage.py createsuperuser --settings=config.settings_production
```

### 7. Restart app
```bash
touch tmp/restart.txt
# ИЛИ в cPanel → Setup Python App → Restart
```

### 8. Включи SSL
- cPanel → SSL/TLS Status
- AutoSSL или Let's Encrypt

---

## 🧪 Test след deployment:

1. ✓ Homepage: https://bgmajstor.eu
2. ✓ Admin: https://bgmajstor.eu/admin
3. ✓ Static files зареждат
4. ✓ SSL работи (зелено катинарче)
5. ✓ Провери error log: `tail -f logs/django_error.log`

---

## ⚠️ Важни файлове с sensitive данни:

- `config/settings_production.py` → SECRET_KEY, DB password, Email password
- `.htaccess` → Passenger paths
- `passenger_wsgi.py` → WSGI config

**НЕ качвай чувствителни данни в публични Git repo!**
