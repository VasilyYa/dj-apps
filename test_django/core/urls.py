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
  #path('redirected/<int:reg_success>/', views.index, name='r_site_index'),
    			                
  path('scores', views.scores, name='site_scores'),
  path('login', views.login, name='site_login'),
  path('logout', views.logout, name='site_logout'),
  path('meta', views.display_meta, name='site_metainfo'), # чтобы посмотреть словарь request.META 
                                                          #(!!содержит все заголовки текущего HTTP-запроса)
  path('register', views.register, name='site_register'),
  path('scores/<int:score_id>/star/', views.StarScore.as_view(), name='star_score'),

]