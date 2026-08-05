"""
Production settings for BGMaistor
"""
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ВАЖНО: Замени с твоя домейн
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'yourdomain.eu', 'www.yourdomain.eu']

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'public_html/static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'public_html/media')

# Database - използвай MySQL в production
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'your_database_name',
#         'USER': 'your_database_user',
#         'PASSWORD': 'your_database_password',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# Email settings за cPanel
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.yourdomain.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'support@yourdomain.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
DEFAULT_FROM_EMAIL = 'support@yourdomain.com'
