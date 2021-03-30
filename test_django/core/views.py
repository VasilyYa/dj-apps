import json
#import requests
# import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth import authenticate, login as sign_in, logout as sign_out
from django.contrib.auth.decorators import login_required


from . import models
from . import forms

from .mixins import JSONResponseMixin
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView


# Create your views here.
# Здесь описываем функции представления:

'''--------------------------------------------------------------------------------
#пример статичного представления
def index(request):
    return HttpResponse(json.dumps({'a': 'b'}), content_type='application/json')

#статичное представление(вар1)
#(см. соответствующий url-паттерн в urls.py)
def hello(request):
   return HttpResponse("Hello, people! This is \"hello\" function here! It returns this string via HttpResponse function")

#представление с динамическим содержимым генерируемой страницы(вар2)
#(см. соответствующий url-паттерн в urls.py)
def current_datetime(request):
   now = datetime.datetime.now()
   html = "<html><body>It is now %s</body></html>" % now
   return HttpResponse(html)

#представление с динамическим содержимым генерируемой страницы и динамическим URL (вар3)
#(см. соответствующий url-паттерн в urls.py)
def hours_ahead(request, offset):
  try:
    offset = int(offset)
  except ValueError:
    raise Http404()
  dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
  # assert False - вариант искусственного вызова ошибки - типа breakpoint (м.б. полезно, т.к. django-отчет об ошибке выдает значения переменных и др.)
  html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
  return HttpResponse(html)   

#шаблонное представление (реальный django)- разделение представления документа от его данных(вар4)
def index(request):
  return render(request, template_name='index.html', context={ "param1": "Вот что возвращает функция reverse (см.файл urls.py): " + reverse('r_site_index') })

#шаблонное представление (пример с авто-редиректом)
def index(request):
#параметр reg_success записывается в _id
  _id = request.GET.get('reg_success', None) # None - значение по умолчанию
  if _id is not None:
    #шаблонное представление
    return render(request, template_name='index.html', context={ "param1": "Вот что возвращает функция reverse (см.файл urls.py): " + reverse('r_site_index') })
  #при первом заходе на данное представление делается следующий авто-редирект:
  return redirect(to=reverse('r_site_index') + '?reg_success=1')

#шаблонное представление (передача списка и вывод его элементов в шаблоне)
def index(request):
  return render(request, template_name='index_test_list.html', context={ "test_list": [1, 2, 3, 4, 5] })

def index(request, reg_success=None):
  if reg_success is not None:
    # сформируем словарь объекта контекст
    # возьмем данные с url хэдхантера (например, список 20 вакансий по ИТ и Django)
    url = 'https://api.hh.ru/vacancies/'
    vacancies = []
    r = requests.get(url,params={
      'page': 0, 
      'per_page': 20, 
      'specialization': 1, # ИТ
      'text': 'django'}
      )
    items = r.json()['items']
    for item in items:
      if item.get('salary') and item['salary']['from']:
        salary = item['salary']['from']
      vacancies.append({
        'id': item['id'],
        'name': item['name'], # ПРОФЕССИЯ
        'salary': salary, # ЗАРПЛАТА
        'employer': item['employer']['name'] # ИМЯ РАБОТОДАТЕЛЯ
      })
    # формируем контекст для шаблонной системы django:
    ctx = {
     "reg_success": reg_success,
     "visitor_name": "Mike", 
     "vacancies": vacancies,
    }
    return render(request, template_name='index.html', context=ctx)
  return redirect(to=reverse('r_site_index', args=(1,)))
  --------------------------------------------------------------------------------'''
#вьюха, чтобы просто посмотреть, что лежит в request.META:
def display_meta(request):
  values = list(request.META.items())
  values.sort()
  #assert False
  html = []
  for k,v in values:
    html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
  return HttpResponse('<table>%s</table>' % '\n'.join(html))
'''-------------------------------------------------------------------------------'''
'''
def index(request, reg_success=None):
  #import pdb
  #pdb.set_trace() #инструмент для отладки!!!
  ctx = {}

  return render(request, template_name='index.html', context=ctx)
'''


@login_required(login_url='site_login')
def scores(request):
  ctx = {}

  ctx.update({ 'scores' : [s.to_json() for s in models.Score.objects.all()] })

  return render(request, template_name='scores.html', context=ctx)

# (Class-Based Views): -------------------------------------------------------------
# описываем вьюхи-классы, основанные на встроенных в django общих вьюхах (Class-Based Views)
# ДЗ (лекция8) - переписать вьюхи index и scores - сделать их как Class-Based Views:

# На основе View:
# class IndexView(View):
# 	def get(self,request):
# 		return HttpResponse('Hello, this is View')

# На основе TemplateView:
class IndexView(TemplateView):
	template_name = 'index.html'
	# переопределяем get_context_data, чтобы добавить 
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['added_context'] = 'This is added context!'
		# print(context)
		return context


# class ScoresView(TemplateView):
# 	template_name = 'scores.html'

# 	def get(self, request, *args, **kwargs):
# 		context = self.get_context_data(**kwargs)
# 		return self.render_to_response(context)

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		context.update({ 'scores' : [s.to_json() for s in models.Score.objects.all()] })
# 		# print(context)
# 		return context


# class ScoresView(CreateView):
# 	template_name = 'scores.html'
# 	model = models.Score
# 	fields = ('title',)

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		context.update({ 'scores' : [s.to_json() for s in models.Score.objects.all()] })
# 		# print(context)
# 		return context


class ScoresView(TemplateView):
	template_name = 'scores.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({ 'scores' : [s.to_json() for s in models.Score.objects.all()] })
		# print(context)
		return context

	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			path = "/"
			return redirect(to=reverse('site_login'))
			# return HttpResponseForbidden()
			# return HttpResponse('Unauthorized', status=401)
		return super(ScoresView, self).dispatch(request, *args, *kwargs)

# ----------------------------------------------------------------------------------

#регистрация новых пользователей (композиторов)
def register(request):
	if request.method == 'POST': # т.е. были отправлены данные с формы регистрации пользователя
		form = forms.RegistrationForm(request.POST) # создаем форму (объект создается стандарт. django методом RegistrationForm)
		if form.is_valid(): # и 'вручную' проверяем ее валидность (станд.методом is_valid), если ок - регистрируем нового пользователя
			user = models.User.objects.create(
				first_name = form.cleaned_data['first_name'], # нужно учесть, какие поля обязательны (см. class User в models.py)
				last_name = form.cleaned_data['last_name'],
				email = form.cleaned_data['email'], # email у нас выступает в роли логина
				password = form.cleaned_data['password1'],)
			# user.save() - не нужно, т.к. create уже делает сохранение изменений в БД
			return redirect(to=reverse('site_login'))
	else:
		form = forms.RegistrationForm() # если не POST, то создаем пустую форму для регистрации нового пользователя и рендерим шаблон с ней
	return render(request, template_name="register.html", context={'form': form})


def login(request):
  ctx = {}
  if request.method == 'POST':
    email = request.POST.get('email', None) # у нас email выступает в роли username
    passwd = request.POST.get('password', None)

    if email and passwd:
      user = authenticate(request, username=email, password=passwd)
    else:
      ctx.update({'error':'Форма содержит пустые поля.'})

    #import pdb
    #pdb.set_trace()

    if user is not None and user.is_active:
      sign_in(request, user) # (from django.contrib.auth import ... login as sign_in...) - само залогинивание от django
      return redirect(to=reverse('site_index'), args=('asdasd', 123))
    else:
      ctx.update({'error':'Неверные учетные данные или пользователь не активен.'})
  return render(request, template_name='login.html', context=ctx)


def logout(request):
  sign_out(request) # (from django.contrib.auth import ... logout as sign_out...) - само разлогинивание от django
  
  path = request.GET.get('path', None)
  # if path is None:
    # path = '/'
  path = '/' # пока перенаправляем на главную страницу
  return redirect(to=path)




#пробуем сохранение данных в сессии пользователя
class StarScore(CreateView, JSONResponseMixin):

	model = models.ScoreStar
	fields = ['score', 'user']

	def get_context_data(self, **kwargs):
		ctx= super(StarScore,self).get_context_data()

		return ctx

	def post(self, requests, *args, **kwargs):
		super(StarScore, self).post()
		return HttpResponse(json.dumps({'Created_with_id': self.object.id}), content_type='application/json')
	# def get_queryset(self):
