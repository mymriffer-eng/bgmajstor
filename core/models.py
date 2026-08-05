from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator


class City(models.Model):
    """Градове в България"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Име на града")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="URL slug")
    region = models.CharField(max_length=100, blank=True, verbose_name="Област")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.IntegerField(default=0, verbose_name="Ред на показване")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Град"
        verbose_name_plural = "Градове"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Category(models.Model):
    """Категории услуги с пълна SEO оптимизация"""
    
    # Основна информация
    name = models.CharField(max_length=100, unique=True, verbose_name="Име на категория")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="URL slug")
    icon = models.CharField(max_length=50, default="🔧", verbose_name="Икона/емоджи")
    
    # SEO полета
    meta_title = models.CharField(max_length=60, verbose_name="SEO заглавие (Title)")
    meta_description = models.CharField(max_length=160, verbose_name="SEO описание (Meta Description)")
    h1_title = models.CharField(max_length=100, verbose_name="H1 заглавие")
    
    # Съдържание
    description = models.TextField(verbose_name="Описание на категорията")
    keywords = models.CharField(max_length=255, blank=True, verbose_name="Ключови думи")
    
    # SEO съдържание
    seo_content = models.TextField(blank=True, verbose_name="Допълнително SEO съдържание")
    
    # Статистика (за динамично показване)
    professionals_count = models.IntegerField(default=0, verbose_name="Брой майстори")
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.50, verbose_name="Среден рейтинг")
    completed_jobs = models.IntegerField(default=0, verbose_name="Завършени проекти")
    
    # Организация
    order = models.IntegerField(default=0, verbose_name="Ред на показване")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('category_detail', kwargs={'slug': self.slug})


class ClientProfile(models.Model):
    """Профил на клиент - може само да коментира"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    avatar = models.ImageField(upload_to='avatars/clients/', blank=True, null=True, verbose_name="Снимка")
    bio = models.TextField(max_length=500, blank=True, verbose_name="За мен")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенти"
    
    def __str__(self):
        return f"Клиент: {self.user.get_full_name() or self.user.username}"


class ProfessionalProfile(models.Model):
    """Профил на професионалист/майстор"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professional_profile')
    
    # Основна информация
    title = models.CharField(max_length=200, verbose_name="Заглавие на профила")
    slug = models.SlugField(max_length=220, unique=True, blank=True, verbose_name="URL slug")
    description = models.TextField(
        max_length=2000, 
        validators=[MaxLengthValidator(2000)],
        verbose_name="Описание"
    )
    
    # Категории услуги
    categories = models.ManyToManyField(Category, related_name='professionals', verbose_name="Категории услуги")
    
    # Контакти
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Имейл")
    website = models.URLField(blank=True, verbose_name="Уебсайт")
    facebook = models.URLField(blank=True, verbose_name="Facebook")
    
    # Локация
    city = models.CharField(max_length=100, blank=True, verbose_name="Град")
    address = models.CharField(max_length=255, blank=True, verbose_name="Адрес")
    
    # Статус и видимост
    is_active = models.BooleanField(default=True, verbose_name="Активен профил")
    is_verified = models.BooleanField(default=False, verbose_name="Верифициран")
    
    # Статистика
    views_count = models.IntegerField(default=0, verbose_name="Брой прегледи")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name="Рейтинг")
    reviews_count = models.IntegerField(default=0, verbose_name="Брой отзиви")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Професионалист"
        verbose_name_plural = "Професионалисти"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while ProfessionalProfile.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('professional_detail', kwargs={'slug': self.slug})
    
    @property
    def images_count(self):
        return self.images.count()


class ProfessionalImage(models.Model):
    """Снимки в профила на професионалист"""
    professional = models.ForeignKey(
        ProfessionalProfile, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name="Професионалист"
    )
    image = models.ImageField(upload_to='professionals/images/', verbose_name="Снимка")
    caption = models.CharField(
        max_length=250, 
        blank=True,
        validators=[MaxLengthValidator(250)],
        verbose_name="Описание"
    )
    order = models.IntegerField(default=0, verbose_name="Ред на показване")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Снимка на професионалист"
        verbose_name_plural = "Снимки на професионалисти"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"Снимка на {self.professional.title}"
