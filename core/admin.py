from django.contrib import admin
from .models import City, Category, ClientProfile, ProfessionalProfile, ProfessionalImage


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'is_active', 'order']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'region']
    search_fields = ['name', 'region']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Основна информация', {
            'fields': ('name', 'slug', 'region', 'is_active', 'order')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'professionals_count', 'average_rating', 'is_active', 'order']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description', 'keywords']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Основна информация', {
            'fields': ('name', 'slug', 'icon', 'is_active', 'order')
        }),
        ('SEO оптимизация', {
            'fields': ('meta_title', 'meta_description', 'h1_title', 'keywords')
        }),
        ('Съдържание', {
            'fields': ('description', 'seo_content')
        }),
        ('Статистика', {
            'fields': ('professionals_count', 'average_rating', 'completed_jobs')
        }),
    )


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username', 'user__email']
    list_filter = ['created_at']


class ProfessionalImageInline(admin.TabularInline):
    model = ProfessionalImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(ProfessionalProfile)
class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'city', 'is_active', 'is_verified', 'rating', 'created_at']
    list_editable = ['is_active', 'is_verified']
    list_filter = ['is_active', 'is_verified', 'city', 'created_at']
    search_fields = ['title', 'description', 'user__username', 'user__email']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['categories']
    inlines = [ProfessionalImageInline]
    
    fieldsets = (
        ('Основна информация', {
            'fields': ('user', 'title', 'slug', 'description', 'categories')
        }),
        ('Контакти', {
            'fields': ('phone', 'email', 'website', 'facebook')
        }),
        ('Локация', {
            'fields': ('city', 'address')
        }),
        ('Статус', {
            'fields': ('is_active', 'is_verified')
        }),
        ('Статистика', {
            'fields': ('views_count', 'rating', 'reviews_count')
        }),
    )


@admin.register(ProfessionalImage)
class ProfessionalImageAdmin(admin.ModelAdmin):
    list_display = ['professional', 'caption', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['professional__title', 'caption']

