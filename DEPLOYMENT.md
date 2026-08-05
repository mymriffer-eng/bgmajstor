# BGMaistor - Production Deployment Guide (cPanel)

## СТЪПКА 1: Подготовка на cPanel

### 1.1 Създай MySQL база данни
1. Влез в cPanel → MySQL Databases
2. Създай нова база: `bgmaistor_db`
3. Създай потребител: `bgmaistor_user`
4. Задай парола (запиши я!)
5. Добави потребителя към базата с ALL PRIVILEGES

### 1.2 Настрой Python App
1. Влез в cPanel → Setup Python App
2. Кликни "Create Application"
   - Python version: 3.9 или по-нова
   - Application root: `/home/yourusername/bgmaistor`
   - Application URL: `/` (root domain)
   - Application startup file: `passenger_wsgi.py`
   - Application Entry point: `application`

## СТЪПКА 2: Качване на файлове

### 2.1 Качи проекта през Git (препоръчително)
```bash
cd /home/yourusername
git clone https://github.com/mymriffer-eng/bgmajstor.git
cd bgmaistor
```

### 2.2 ИЛИ качи през File Manager/FTP
- Качи всички файлове в `/home/yourusername/bgmaistor`
- НЕ качвай: venv/, db.sqlite3, __pycache__, .git/ (опционално)

## СТЪПКА 3: Конфигурация на проекта

### 3.1 Активирай virtual environment и инсталирай зависимости
```bash
cd /home/yourusername/bgmaistor
source /home/yourusername/virtualenv/bgmaistor/3.9/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install mysqlclient  # За MySQL
```

### 3.2 Редактирай settings_production.py
```bash
nano config/settings_production.py
```

Промени:
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bgmaistor_db',
        'USER': 'bgmaistor_user',
        'PASSWORD': 'ТВОЯТА_ПАРОЛА',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Генерирай нов SECRET_KEY за production!
SECRET_KEY = 'генерирай-нов-secret-key-тук'
```

### 3.3 Генерирай SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3.4 Създай public_html директории
```bash
mkdir -p public_html/static
mkdir -p public_html/media
```

## СТЪПКА 4: Миграции и статични файлове

### 4.1 Приложи миграции
```bash
python manage.py migrate --settings=config.settings_production
```

### 4.2 Събери статични файлове
```bash
python manage.py collectstatic --settings=config.settings_production --noinput
```

### 4.3 Създай superuser
```bash
python manage.py createsuperuser --settings=config.settings_production
```

### 4.4 Популирай категориите
```bash
python manage.py populate_categories --settings=config.settings_production
```

### 4.5 Популирай градовете (от Django shell)
```bash
python manage.py shell --settings=config.settings_production
```

Изпълни в shell:
```python
from core.models import City
from django.utils.text import slugify

cities = [
    ('София', 'Софийска област'), ('Пловдив', 'Пловдивска област'),
    ('Варна', 'Варненска област'), ('Бургас', 'Бургаска област'),
    ('Русе', 'Русенска област'), ('Стара Загора', 'Старозагорска област'),
    ('Плевен', 'Плевенска област'), ('Сливен', 'Сливенска област'),
    ('Добрич', 'Добричка област'), ('Шумен', 'Шуменска област'),
    ('Перник', 'Пернишка област'), ('Хасково', 'Хасковска област'),
    ('Ямбол', 'Ямболска област'), ('Пазарджик', 'Пазарджишка област'),
    ('Благоевград', 'Благоевградска област'), ('Велико Търново', 'Великотърновска област'),
    ('Враца', 'Врачанска област'), ('Габрово', 'Габровска област'),
    ('Видин', 'Видинска област'), ('Асеновград', 'Пловдивска област'),
    ('Казанлък', 'Старозагорска област'), ('Кюстендил', 'Кюстендилска област'),
    ('Кърджали', 'Кърджалийска област'), ('Монтана', 'Монтанска област'),
    ('Димитровград', 'Хасковска област'), ('Разград', 'Разградска област'),
    ('Търговище', 'Търговищка област'), ('Силистра', 'Силистренска област'),
    ('Ловеч', 'Ловешка област')
]

for i, (city_name, region) in enumerate(cities, 1):
    City.objects.get_or_create(
        name=city_name,
        defaults={'slug': slugify(city_name, allow_unicode=True), 'region': region, 'order': i}
    )
print("Cities created!")
exit()
```

## СТЪПКА 5: Рестартирай приложението

### В cPanel Python App:
1. Отвори Setup Python App
2. Намери приложението
3. Кликни "Restart" или "Stop/Start"

### ИЛИ през SSH:
```bash
touch /home/yourusername/bgmaistor/tmp/restart.txt
```

## СТЪПКА 6: Тестване

### 6.1 Отвори сайта
- Основна страница: https://yourdomain.com
- Admin панел: https://yourdomain.com/admin

### 6.2 Провери логовете
```bash
tail -f /home/yourusername/logs/bgmaistor_error.log
```

## ВАЖНИ БЕЛЕЖКИ:

### Permissions
```bash
chmod 644 passenger_wsgi.py
chmod 644 config/settings_production.py
chmod 755 public_html/static
chmod 755 public_html/media
```

### При промени в кода:
```bash
cd /home/yourusername/bgmaistor
git pull  # Ако използваш Git
touch tmp/restart.txt  # Рестартира app
```

### Backup на базата данни (редовно!):
```bash
mysqldump -u bgmaistor_user -p bgmaistor_db > backup_$(date +%Y%m%d).sql
```

### SSL Сертификат (задължително за production):
1. cPanel → SSL/TLS Status
2. Включи AutoSSL или качи Let's Encrypt сертификат

## Помощ при проблеми:

### Ако сайтът не работи:
1. Провери error log: `tail -f ~/logs/bgmaistor_error.log`
2. Провери Python version в Python App
3. Провери че всички зависимости са инсталирани
4. Провери database credentials
5. Рестартирай app

### Често срещани грешки:
- **500 Error**: Провери DEBUG=False и ALLOWED_HOSTS
- **Static files не се зареждат**: Изпълни collectstatic отново
- **Database error**: Провери credentials в settings_production.py
- **Module not found**: pip install -r requirements.txt в venv

## Контакти за поддръжка:
- Email: support@bgmajstor.eu
- GitHub: https://github.com/mymriffer-eng/bgmajstor
