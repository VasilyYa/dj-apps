#

from django.urls import path, re_path, include
from . import views

urlpatterns = [
  path('', views.index, name='site_index'),
  #path('redirected', views.index, name='r_site_index'),
  #path('hello', views.hello),
  #path('time', views.current_datetime),
  #re_path(r'^time/plus/(\d+)/$', views.hours_ahead), 
  				# re_path отличается от функции path возможностью использования регулярных выражений
  				# исп. шаблон \d+ для выделения одной или более цифр
  				# r - raw-строка python
  				# заключенное в скобки выражение (\d+) будет передано вторым параметром в функцию hours_ahead)
  path('redirected/<int:reg_success>/', views.index, name='r_site_index'),			                
  

]