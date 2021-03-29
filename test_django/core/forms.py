from django import forms
from core import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

# делаем регистрацию пользователей с помощью средств django - класса Form (библиотека django.forms)
class RegistrationForm(forms.Form):
	email = forms.EmailField(
		widget=forms.EmailInput(
			attrs=dict(required=True, # перечисляем аттрибуты, которые нам нужны в полях html-формы
			max_length=30, 
			placeholder='На какой емаил вам прислать документы')
			), 
		label=_("Email адрес"), 
		error_messages={ 'invalid': _('Email уже существует') }
	)
	password1 = forms.CharField(
		widget=forms.PasswordInput(
			attrs=dict(required=True, max_length=30, 
						render_value=False, placeholder='Придумайте надежный пароль')
			),
		label=_("Пароль"),
		error_messages={ 'invalid': _('Пароли не совпадают') }
	)
	password2 = forms.CharField(
		widget=forms.PasswordInput(
			attrs=dict(required=True, max_length=30, 
						render_value=False, placeholder='Повторите пароль')
			),
		label=_("Пароль (еще раз)")
	)
	first_name = forms.RegexField(
		regex=r'^\w+$', 
		widget=forms.TextInput(
			attrs=dict(required=True, max_length=30, placeholder='Введите имя, пожалуйста')),
		label=_('Имя'),
		error_messages={ 'invalid': _('Имя может содержать только буквы') }
	)
	last_name = forms.RegexField(
		regex=r'^\w+$', 
		widget=forms.TextInput(
			attrs=dict(required=True, max_length=30, placeholder='Введите фамилию, пожалуйста')),
		label=_('Фамилия'),
		error_messages={ 'invalid': _('Фамилия может содержать только буквы') }
	)

	#first_name = models.CharField(max_length=20, null=False, blank=False, unique=False, verbose_name="Имя")
	#last_name = models.CharField(max_length=30, null=True, blank=True, unique=False, verbose_name="Фамилия")
	#pen_name = models.CharField(max_length=50, null=True, blank=False, unique=True) # уникальное имя (псевдоним), null=True - означает, означает, что джанго при создании таблицы укажет не доп. ограничение NOT NULL
	#email = models.EmailField(null=False, blank=False, unique=True) # email уникален, но пустое значение (blank) допускается
	#headshot = models.ImageField(null=True, blank=True, unique=False, upload_to='tmp', verbose_name="фотография")
	#website = models.URLField(null=True, blank=True, unique=False, verbose_name="Веб-страница")


# метод clean() применяется, если нужно добавить кастомных валидаций полей форм
def clean(self):
	if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data: # form.cleaned_data - словарь с "нормализаванными"" значениями полей формы
		if self.cleaned_data['password1'] != self.cleaned_data['password2']:
			raise forms.ValidationError(_("Пароли не совпадают"))
	email = self.cleaned_data.get('email', None)
	if not email:
		raise forms.ValidationError(_("Ошибка сервера, обновите страницу"))
	else:
		if models.User.objects.filter(email__iexact=email).exists():
			raise forms.ValidationError(_("Пользователь с таким email уже существует"))
	return self.cleaned_data

	