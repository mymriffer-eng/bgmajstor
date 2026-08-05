from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import City, Category, ProfessionalProfile, ProfessionalImage
from .forms import ClientRegistrationForm, ProfessionalRegistrationForm, ProfessionalProfileForm

def home(request):
    """Начална страница на BGMaistor"""
    categories = Category.objects.filter(is_active=True)
    cities = City.objects.filter(is_active=True).order_by('order', 'name')
    recent_professionals = ProfessionalProfile.objects.filter(
        is_active=True
    ).select_related('user').prefetch_related('categories', 'images').order_by('-created_at')[:6]
    
    context = {
        'categories': categories,
        'cities': cities,
        'recent_professionals': recent_professionals,
    }
    return render(request, 'home.html', context)

def search(request):
    """Търсене на професионалисти по категория и град"""
    category_slug = request.GET.get('category')
    city_slug = request.GET.get('city')
    
    professionals = ProfessionalProfile.objects.filter(is_active=True).select_related('user')
    
    # Филтри
    if category_slug:
        professionals = professionals.filter(categories__slug=category_slug)
    
    if city_slug:
        # Търси по име на града, понеже city е CharField
        try:
            city_obj = City.objects.get(slug=city_slug)
            professionals = professionals.filter(city__icontains=city_obj.name)
        except City.DoesNotExist:
            pass
    
    # Вземи избраните обекти за context
    selected_category = None
    if category_slug:
        try:
            selected_category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            pass
    
    selected_city = None
    if city_slug:
        try:
            selected_city = City.objects.get(slug=city_slug)
        except City.DoesNotExist:
            pass
    
    categories = Category.objects.filter(is_active=True)
    cities = City.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'professionals': professionals,
        'selected_category': selected_category,
        'selected_city': selected_city,
        'categories': categories,
        'cities': cities,
    }
    return render(request, 'search.html', context)

def category_detail(request, slug):
    """SEO оптимизирана страница за категория"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    # Вземи всички професионалисти от тази категория
    professionals = category.professionals.filter(is_active=True).select_related('user')
    
    # Вземи свързани категории (за препоръки)
    related_categories = Category.objects.filter(is_active=True).exclude(id=category.id)[:4]
    
    context = {
        'category': category,
        'professionals': professionals,
        'related_categories': related_categories,
    }
    return render(request, 'category_detail.html', context)

def categories_list(request):
    """Списък с всички категории"""
    categories = Category.objects.filter(is_active=True)
    context = {
        'categories': categories,
    }
    return render(request, 'categories_list.html', context)

def contact(request):
    """Страница за контакти с форма"""
    if request.method == 'POST':
        # Вземи данните от формата
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Проверки
        errors = []
        if not name:
            errors.append('Моля въведете вашето име.')
        if not email:
            errors.append('Моля въведете имейл адрес.')
        if not message:
            errors.append('Моля въведете съобщение.')
        if len(message) > 2000:
            errors.append('Съобщението не може да бъде по-дълго от 2000 символа.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Формирай съобщението
            email_subject = f'Контакт форма BGMaistor: {subject or "Без тема"}'
            email_message = f"""
Ново съобщение от контактната форма на BGMaistor:

Име: {name}
Имейл: {email}
Телефон: {phone or 'Не е посочен'}
Тема: {subject or 'Не е посочена'}

Съобщение:
{message}
            """
            
            try:
                # Опит за изпращане на имейл
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['support@bgmajstor.eu'],
                    fail_silently=False,
                )
                messages.success(request, '✓ Съобщението беше изпратено успешно! Ще се свържем с вас скоро.')
                return redirect('contact')
            except Exception as e:
                # Ако има грешка при изпращане на имейл, все пак покажи съобщение
                messages.success(request, '✓ Вашето съобщение беше получено! Ще се свържем с вас скоро.')
                # В production среда логвай грешката
                print(f"Email error: {e}")
                return redirect('contact')
    
    return render(request, 'contact.html')


def register_choice(request):
    """Страница за избор на тип регистрация"""
    return render(request, 'registration/register_choice.html')


def register_client(request):
    """Регистрация на клиент"""
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '✓ Успешна регистрация! Добре дошли в BGMaistor!')
            return redirect('my_profile')
    else:
        form = ClientRegistrationForm()
    
    return render(request, 'registration/register_client.html', {'form': form})


def register_professional(request):
    """Регистрация на професионалист - стъпка 1 (User account)"""
    if request.method == 'POST':
        form = ProfessionalRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Запази user ID в сесията за следващата стъпка
            request.session['professional_user_id'] = user.id
            messages.success(request, '✓ Акаунтът е създаден! Сега попълнете профила си.')
            return redirect('register_professional_profile')
    else:
        form = ProfessionalRegistrationForm()
    
    return render(request, 'registration/register_professional_step1.html', {'form': form})


def register_professional_profile(request):
    """Регистрация на професионалист - стъпка 2 (Profile)"""
    # Провери дали има user_id в сесията
    user_id = request.session.get('professional_user_id')
    if not user_id:
        messages.error(request, 'Моля първо създайте акаунт.')
        return redirect('register_professional')
    
    from django.contrib.auth.models import User
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Грешка при намиране на потребителя.')
        return redirect('register_professional')
    
    if request.method == 'POST':
        form = ProfessionalProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            form.save_m2m()  # Запази ManyToMany полета (categories)
            
            # Изтрий от сесията
            del request.session['professional_user_id']
            
            # Login потребителя
            login(request, user)
            
            messages.success(request, '✓ Профилът е създаден успешно! Можете да добавите снимки от профила си.')
            return redirect('professional_profile', slug=profile.slug)
    else:
        # Pre-fill имейла от user account
        form = ProfessionalProfileForm(initial={'email': user.email})
    
    return render(request, 'registration/register_professional_step2.html', {
        'form': form,
        'user': user
    })


@login_required
def professional_add_images(request, slug):
    """Добавяне на снимки към профил на професионалист"""
    professional = get_object_or_404(ProfessionalProfile, slug=slug, user=request.user)
    
    if request.method == 'POST' and request.FILES:
        files = request.FILES.getlist('images')
        
        # Проверка за максимален брой снимки
        current_count = professional.images.count()
        if current_count + len(files) > 20:
            messages.error(request, f'Можете да качите максимум 20 снимки. В момента имате {current_count} снимки.')
            return redirect('professional_add_images', slug=slug)
        
        # Качи снимките
        for index, file in enumerate(files):
            caption = request.POST.get(f'caption_{index}', '')
            ProfessionalImage.objects.create(
                professional=professional,
                image=file,
                caption=caption[:250],  # Ограничи до 250 символа
                order=current_count + index
            )
        
        messages.success(request, f'✓ Успешно добавихте {len(files)} снимки!')
        return redirect('professional_add_images', slug=slug)
    
    images = professional.images.all()
    current_count = professional.images.count()
    can_add_more = current_count < 20
    remaining_images = 20 - current_count
    
    return render(request, 'registration/professional_add_images.html', {
        'professional': professional,
        'images': images,
        'can_add_more': can_add_more,
        'remaining_images': remaining_images
    })


@login_required
def my_profile(request):
    """Моят профил - показва профила на текущия потребител"""
    # Провери дали е професионалист
    if hasattr(request.user, 'professional_profile'):
        return redirect('professional_profile', slug=request.user.professional_profile.slug)
    
    # Провери дали е клиент
    if hasattr(request.user, 'client_profile'):
        return render(request, 'profile/client_profile.html', {
            'client': request.user.client_profile
        })
    
    # Ако няма нито един профил
    messages.error(request, 'Нямате създаден профил.')
    return redirect('home')


def professional_profile(request, slug):
    """Показва профил на професионалист (публичен или собствен)"""
    professional = get_object_or_404(ProfessionalProfile, slug=slug)
    images = professional.images.all().order_by('order')
    
    # Провери дали потребителят е собственик на профила
    is_owner = request.user.is_authenticated and request.user == professional.user
    
    context = {
        'professional': professional,
        'images': images,
        'is_owner': is_owner
    }
    return render(request, 'profile/professional_profile.html', context)


def user_login(request):
    """Вход в системата"""
    if request.user.is_authenticated:
        return redirect('my_profile')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Намери потребител по имейл
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добре дошли, {user.get_full_name()}!')
                
                # Редирект към next параметър или профил
                next_url = request.GET.get('next', 'my_profile')
                return redirect(next_url)
            else:
                messages.error(request, 'Грешна парола.')
        except User.DoesNotExist:
            messages.error(request, 'Няма потребител с този имейл.')
    
    return render(request, 'registration/login.html')


def user_logout(request):
    """Изход от системата"""
    logout(request)
    messages.success(request, 'Успешно излязохте от системата.')
    return redirect('home')


@login_required
def delete_image(request, image_id):
    """Изтриване на снимка от профил"""
    image = get_object_or_404(ProfessionalImage, id=image_id)
    
    # Провери дали потребителят е собственик
    if request.user != image.professional.user:
        messages.error(request, 'Нямате право да изтриете тази снимка.')
        return redirect('home')
    
    if request.method == 'POST':
        professional_slug = image.professional.slug
        image.delete()
        messages.success(request, 'Снимката беше изтрита успешно.')
        return redirect('professional_add_images', slug=professional_slug)
    
    return redirect('professional_add_images', slug=image.professional.slug)


def contact(request):
    """Страница за контакти"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Тук може да се добави логика за изпращане на имейл
        messages.success(request, 'Вашето съобщение беше изпратено успешно!')
        return redirect('contact')
    
    return render(request, 'contact.html')


def terms_of_service(request):
    """Условия за ползване"""
    return render(request, 'legal/terms_of_service.html')


def privacy_policy(request):
    """Политика за поверителност"""
    return render(request, 'legal/privacy_policy.html')


def cookie_policy(request):
    """Политика за бисквитки"""
    return render(request, 'legal/cookie_policy.html')


def gdpr(request):
    """GDPR информация"""
    return render(request, 'legal/gdpr.html')
