from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile
from django.core.validators import RegexValidator


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="To'g'ri email manzilini kiriting.")
    first_name = forms.CharField(max_length=30, required=True, help_text="Ismingizni kiriting.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Familiyangizni kiriting.")

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu email allaqachon ro'yxatdan o'tgan.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if hasattr(user, 'username'):  # Agar username maydoni mavjud bo'lsa
            user.username = user.email
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", help_text="Email manzilingizni kiriting.")

    class Meta:
        model = UserProfile
        fields = ('username', 'password')


class ProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        validators=[RegexValidator(r'^\+?[1-9]\d{1,14}$', message="Telefon raqami to'g'ri formatda bo'lishi kerak.")],
        help_text="Masalan, +998901234567"
    )
    address = forms.CharField(widget=forms.Textarea, required=False, help_text="Manzilingizni kiriting.")
    profile_picture = forms.ImageField(required=False, help_text="Profilingiz uchun rasm yuklang.")
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Tug'ilgan sanangizni kiriting (ixtiyoriy)."
    )
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=False, help_text="Jinsingizni tanlang.")

    class Meta:
        model = UserProfile
        fields = ('phone_number', 'address', 'profile_picture', 'date_of_birth', 'gender')
