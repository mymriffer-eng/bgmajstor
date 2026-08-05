from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ClientProfile, ProfessionalProfile, Category


class ClientRegistrationForm(UserCreationForm):
    """Форма за регистрация на клиент"""
    first_name = forms.CharField(max_length=30, required=True, label="Име")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    email = forms.EmailField(required=True, label="Имейл")
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Български labels
        self.fields['password1'].label = 'Парола'
        self.fields['password2'].label = 'Потвърди парола'
        
        # Добави CSS класове
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Този имейл вече е регистриран.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # Използвай имейла като username
        user.username = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Създай клиентски профил
            ClientProfile.objects.create(user=user)
        return user


class ProfessionalRegistrationForm(UserCreationForm):
    """Форма за регистрация на професионалист - стъпка 1"""
    first_name = forms.CharField(max_length=30, required=True, label="Име")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    email = forms.EmailField(required=True, label="Имейл")
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Български labels
        self.fields['password1'].label = 'Парола'
        self.fields['password2'].label = 'Потвърди парола'
        
        # Добави CSS класове
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Този имейл вече е регистриран.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # Използвай имейла като username
        user.username = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user


class ProfessionalProfileForm(forms.ModelForm):
    """Форма за профила на професионалист - стъпка 2"""
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Категории услуги (изберете една или повече)"
    )
    
    class Meta:
        model = ProfessionalProfile
        fields = [
            'title', 'description', 'categories', 
            'phone', 'email', 'website', 'facebook',
            'city', 'address'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Напр. "Майстор електричар в София"'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'maxlength': 2000,
                'placeholder': 'Опишете вашите услуги, опит и специализации...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+359 888 123 456'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourwebsite.com'
            }),
            'facebook': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://facebook.com/yourpage'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'София'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес (опционално)'
            }),
        }
        labels = {
            'title': 'Заглавие на профила',
            'description': 'Описание (до 2000 символа)',
            'phone': 'Телефон за контакт (опционално)',
            'email': 'Имейл за контакт',
            'website': 'Уебсайт (опционално)',
            'facebook': 'Facebook страница (опционално)',
            'city': 'Град',
            'address': 'Адрес (опционално)',
        }
