from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import requests
# import json
# import datetime
# Create your views here.
# Здесь описываем функции представления:

'''
#пример статичного представления
def index(request):
    return HttpResponse(json.dumps({'a': 'b'}), content_type='application/json')
'''

'''
#статичное представление(вар1)
#(см. соответствующий url-паттерн в urls.py)
def hello(request):
   return HttpResponse("Hello, people! This is \"hello\" function here! It returns this string via HttpResponse function")
'''

'''
#представление с динамическим содержимым генерируемой страницы(вар2)
#(см. соответствующий url-паттерн в urls.py)
def current_datetime(request):
   now = datetime.datetime.now()
   html = "<html><body>It is now %s</body></html>" % now
   return HttpResponse(html)
'''

'''
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
'''

'''
#шаблонное представление (реальный django)- разделение представления документа от его данных(вар4)
def index(request):
  return render(request, template_name='index.html', context={ "param1": "Вот что возвращает функция reverse (см.файл urls.py): " + reverse('r_site_index') })
'''

'''
#шаблонное представление (пример с авто-редиректом)
def index(request):
#параметр reg_success записывается в _id
  _id = request.GET.get('reg_success', None) # None - значение по умолчанию
  if _id is not None:
    #шаблонное представление
    return render(request, template_name='index.html', context={ "param1": "Вот что возвращает функция reverse (см.файл urls.py): " + reverse('r_site_index') })
  #при первом заходе на данное представление делается следующий авто-редирект:
  return redirect(to=reverse('r_site_index') + '?reg_success=1')
'''

'''
#шаблонное представление (передача списка и вывод его элементов в шаблоне)
def index(request):
  return render(request, template_name='index_test_list.html', context={ "test_list": [1, 2, 3, 4, 5] })
'''

'''
def index(request, reg_success=None):
  if reg_success is not None:
    # сформируем словарь объекта контекст в переменной ctx
    ctx = {
     "reg_success": reg_success, # 
     "test_list": [  # список словарей
       {
          "k1":"AaAaA",
        },
        {
          "k1":"BbBbbB",
        },
        {
          "k1":"CccCccCCCc"
        }
     ] 
    }
    return render(request, template_name='index.html', context=ctx)
  
  return redirect(to=reverse('r_site_index', args=(1,)))
'''


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