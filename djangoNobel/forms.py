from django import forms
from django.contrib.auth.models import User, Permission

from .models import SportStructure, SportStructureImage, Category, Tag, Rating, Comment


class ConstructionsForm(forms.ModelForm):
    class Meta:
        model = SportStructure
        fields = ['name', 'description', 'rating', 'category', 'address', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'name': 'Назва',
            'description': 'Опис',
            'rating': 'Рейтинг',
            'category': 'Район',
            'address': 'Адрес',
            'tags': 'Послуги',
        }


class ConstructionsImageForm(forms.ModelForm):
    class Meta:
        model = SportStructureImage
        fields = ['sport_structure', 'image', 'description']
        labels = {
            'sport_structure': 'Підприємство',
            'image': 'Зображення',
            'description': 'Опис',
        }


class ServicesForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            'name': 'Назва',
        }


class DistrictsForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Назва',
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['sport_structure', 'user', 'rating']
        labels = {
            'sport_structure': 'Підприємство',
            'user': 'Користувач',
            'rating': 'Рейтинг',
        }


class RatingFormUser(forms.Form):
    rating = forms.ChoiceField(
        choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
        widget=forms.RadioSelect,
        label="Ваш рейтинг"
    )

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Підтвердження")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Паролі не збігаються.")
        return password2

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']


class UserPermissionsForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(content_type__app_label='djangoNobel'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Права користувача"
    )

    class Meta:
        model = User
        fields = ['permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['permissions'].initial = self.instance.user_permissions.all()

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.user_permissions.set(self.cleaned_data['permissions'])
        return user
