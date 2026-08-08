#!/usr/bin/env python
"""
Seed database with initial categories and cities for BGMaistor
"""

import os
import sys
import django

print("=" * 60)
print("BGMaistor - Initial Data Seed")
print("=" * 60)

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production'
sys.path.insert(0, os.path.dirname(__file__))

try:
    django.setup()
    from core.models import Category, City
    print("✓ Django setup successful!")
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    sys.exit(1)

# Bulgarian cities data
CITIES_DATA = [
    {"name": "София", "region": "София-град", "order": 1},
    {"name": "Пловдив", "region": "Пловдив", "order": 2},
    {"name": "Варна", "region": "Варна", "order": 3},
    {"name": "Бургас", "region": "Бургас", "order": 4},
    {"name": "Русе", "region": "Русе", "order": 5},
    {"name": "Стара Загора", "region": "Стара Загора", "order": 6},
    {"name": "Плевен", "region": "Плевен", "order": 7},
    {"name": "Сливен", "region": "Сливен", "order": 8},
    {"name": "Добрич", "region": "Добрич", "order": 9},
    {"name": "Шумен", "region": "Шумен", "order": 10},
    {"name": "Перник", "region": "Перник", "order": 11},
    {"name": "Хасково", "region": "Хасково", "order": 12},
    {"name": "Ямбол", "region": "Ямбол", "order": 13},
    {"name": "Пазарджик", "region": "Пазарджик", "order": 14},
    {"name": "Благоевград", "region": "Благоевград", "order": 15},
    {"name": "Велико Търново", "region": "Велико Търново", "order": 16},
    {"name": "Враца", "region": "Враца", "order": 17},
    {"name": "Габрово", "region": "Габрово", "order": 18},
    {"name": "Кърджали", "region": "Кърджали", "order": 19},
    {"name": "Кюстендил", "region": "Кюстендил", "order": 20},
]

# Categories data with full SEO
CATEGORIES_DATA = [
    {
        "name": "Електричар",
        "icon": "⚡",
        "order": 1,
        "meta_title": "Електричар София - Професионални Електро Услуги",
        "meta_description": "Намери проверен електричар в София и цяла България. Електро инсталации, ремонт, подмяна. Бързо, качествено, с гаранция.",
        "h1_title": "Електричари - Електро Услуги",
        "description": "Професионални електро услуги - инсталации, ремонт, подмяна на табла и контакти. Проверени майстори с опит и гаранция за изпълнение.",
        "seo_content": "Нашите електричари имат необходимите удостоверения и опит за всички видове електро услуги - от смяна на контакт до цялостна инсталация.",
        "keywords": "електричар, електро услуги, инсталации, ремонт",
        "professionals_count": 245,
        "average_rating": 4.8,
        "completed_jobs": 1580,
    },
    {
        "name": "Водопроводчик",
        "icon": "🚰",
        "order": 2,
        "meta_title": "Водопроводчик София - ВиК Услуги 24/7",
        "meta_description": "Спешен водопроводчик в София и цяла България. ВиК ремонти, течове, запушени канали. Бърза намеса, професионално изпълнение.",
        "h1_title": "Водопроводчици - ВиК Услуги",
        "description": "Водопроводни услуги и ремонти - течове, запушени канали, подмяна на санитария. Професионални майстори, достъпни 24/7.",
        "seo_content": "Водопроводчиците ни реагират бързо при аварии, предлагат качествени ВиК услуги с гаранция. Работим с всички райони.",
        "keywords": "водопроводчик, вик услуги, течове, запушване",
        "professionals_count": 198,
        "average_rating": 4.7,
        "completed_jobs": 2140,
    },
    {
        "name": "Ремонт на климатици",
        "icon": "❄️",
        "order": 3,
        "meta_title": "Ремонт и Монтаж на Климатици - Професионални Услуги",
        "meta_description": "Монтаж, ремонт и сервиз на климатици в София и страната. Професионални техници, качествено оборудване, гаранция.",
        "h1_title": "Климатични Техници - Ремонт и Монтаж",
        "description": "Монтаж, ремонт и профилактика на климатични системи. Сертифицирани техници, бързо обслужване, коректни цени.",
        "seo_content": "Нашите специалисти работят с всички марки климатици - монтаж, ремонт, зареждане с фреон, годишна профилактика.",
        "keywords": "климатици, монтаж, ремонт, сервиз",
        "professionals_count": 156,
        "average_rating": 4.9,
        "completed_jobs": 890,
    },
    {
        "name": "Строител",
        "icon": "🏗️",
        "order": 4,
        "meta_title": "Строителни Услуги - Професионални Строители",
        "meta_description": "Строителни ремонти и услуги от майстори с опит. Зидария, мазилки, шпакловки, замазки. Качество и коректност.",
        "h1_title": "Строители - Ремонти и Строителство",
        "description": "Пълен спектър строителни услуги - зидария, мазилки, шпакловки, гипсокартон, замазки. Професионални екипи с дългогодишен опит.",
        "seo_content": "Извършваме всички видове строителни работи - от основен ремонт до довършителни работи. Гаранция за качество.",
        "keywords": "строител, ремонт, зидария, мазилка",
        "professionals_count": 312,
        "average_rating": 4.6,
        "completed_jobs": 1950,
    },
    {
        "name": "Боядисване",
        "icon": "🎨",
        "order": 5,
        "meta_title": "Боядисване - Майстори Бояджии",
        "meta_description": "Професионално боядисване на жилища и офиси. Опитни бояджии, качествени материали, прецизно изпълнение.",
        "h1_title": "Бояджии - Боядисване и Декорация",
        "description": "Боядисване на стени, тавани, дограма. Латекс, масло, бояджийски услуги с гаранция за качество и срокове.",
        "seo_content": "Нашите бояджии работят бързо и прецизно. Използваме качествени бои и материали. Консултация при избор на цветове.",
        "keywords": "боядисване, бояджия, латекс, ремонт",
        "professionals_count": 178,
        "average_rating": 4.7,
        "completed_jobs": 1320,
    },
    {
        "name": "Дърводелец",
        "icon": "🪚",
        "order": 6,
        "meta_title": "Дърводелски Услуги - Майстори Дърводелци",
        "meta_description": "Дърводелски услуги - мебели по поръчка, врати, прозорци, ремонт на мебели. Качествено дърво, прецизно изработване.",
        "h1_title": "Дърводелци - Мебели и Дървени Изделия",
        "description": "Изработка на мебели по поръчка, монтаж на врати и прозорци, ремонт на дървени изделия. Професионално изпълнение.",
        "seo_content": "Дърводелците ни работят с масивно дърво и ПДЧ. Правим кухни, гардероби, шкафове и всякакви мебели по поръчка.",
        "keywords": "дърводелец, мебели, врати, дърво",
        "professionals_count": 134,
        "average_rating": 4.8,
        "completed_jobs": 760,
    },
    {
        "name": "Ключар",
        "icon": "🔑",
        "order": 7,
        "meta_title": "Ключар София - Спешна Помощ 24/7",
        "meta_description": "Спешен ключар в София и цяла България. Отваряне на врати, смяна на брави, аварийна помощ 24/7. Бърза реакция.",
        "h1_title": "Ключари - Аварийни и Планови Услуги",
        "description": "Ключарски услуги - аварийно отваряне, смяна на брави и патрони, изработка на ключове, монтаж на секретни брави.",
        "seo_content": "Ключарите ни работят 24/7. Реагираме бързо при спешни случаи - заключени врати, счупени ключове, дефектни брави.",
        "keywords": "ключар, брави, аварийно отваряне, 24/7",
        "professionals_count": 89,
        "average_rating": 4.9,
        "completed_jobs": 2350,
    },
    {
        "name": "Ламинат и подови настилки",
        "icon": "🪵",
        "order": 8,
        "meta_title": "Полагане на Ламинат - Професионални Настилки",
        "meta_description": "Полагане на ламинат, паркет, винил и други подови настилки. Професионални майстори, прецизно изпълнение.",
        "h1_title": "Подови Настилки - Ламинат и Паркет",
        "description": "Полагане на всички видове подови настилки - ламинат, паркет, винил, балатум. Подготовка на основа, монтаж, лакиране.",
        "seo_content": "Работим с всички видове подови материали. Професионално изравняване и подготовка преди полагане. Гаранция за изпълнение.",
        "keywords": "ламинат, паркет, подови настилки, монтаж",
        "professionals_count": 145,
        "average_rating": 4.8,
        "completed_jobs": 980,
    },
]

# Create cities
print("\n1. Creating Cities...")
print("-" * 60)
created_cities = 0
updated_cities = 0

for city_data in CITIES_DATA:
    city, created = City.objects.get_or_create(
        name=city_data["name"],
        defaults={
            "region": city_data["region"],
            "order": city_data["order"],
            "is_active": True,
        }
    )
    if created:
        created_cities += 1
        print(f"  ✓ Created: {city.name}")
    else:
        # Update if exists
        city.region = city_data["region"]
        city.order = city_data["order"]
        city.save()
        updated_cities += 1
        print(f"  • Updated: {city.name}")

print(f"\n  Created: {created_cities} cities")
print(f"  Updated: {updated_cities} cities")

# Create categories
print("\n2. Creating Categories...")
print("-" * 60)
created_categories = 0
updated_categories = 0

for cat_data in CATEGORIES_DATA:
    category, created = Category.objects.get_or_create(
        name=cat_data["name"],
        defaults={
            "icon": cat_data["icon"],
            "order": cat_data["order"],
            "meta_title": cat_data["meta_title"],
            "meta_description": cat_data["meta_description"],
            "h1_title": cat_data["h1_title"],
            "description": cat_data["description"],
            "seo_content": cat_data["seo_content"],
            "keywords": cat_data["keywords"],
            "professionals_count": cat_data["professionals_count"],
            "average_rating": cat_data["average_rating"],
            "completed_jobs": cat_data["completed_jobs"],
            "is_active": True,
        }
    )
    if created:
        created_categories += 1
        print(f"  ✓ Created: {cat_data['icon']} {category.name}")
    else:
        # Update if exists
        category.icon = cat_data["icon"]
        category.order = cat_data["order"]
        category.meta_title = cat_data["meta_title"]
        category.meta_description = cat_data["meta_description"]
        category.h1_title = cat_data["h1_title"]
        category.description = cat_data["description"]
        category.seo_content = cat_data["seo_content"]
        category.keywords = cat_data["keywords"]
        category.professionals_count = cat_data["professionals_count"]
        category.average_rating = cat_data["average_rating"]
        category.completed_jobs = cat_data["completed_jobs"]
        category.save()
        updated_categories += 1
        print(f"  • Updated: {cat_data['icon']} {category.name}")

print(f"\n  Created: {created_categories} categories")
print(f"  Updated: {updated_categories} categories")

print("\n" + "=" * 60)
print("SUCCESS! Database seeded")
print("=" * 60)
print(f"\nTotal Cities: {City.objects.count()}")
print(f"Total Categories: {Category.objects.count()}")
print("\nYou can now:")
print("1. View categories: https://bgmajstor.eu")
print("2. Edit in admin: https://bgmajstor.eu/supereto/")
print("3. Add more cities/categories via admin panel")
print("=" * 60)
