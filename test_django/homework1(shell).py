from django.template import Template, Context
import datetime

# создаем содержимое шаблона - к примеру, это страница c информацией о выбранной из архива нотной партитуре :)
raw_template = """<p>Hello, {{ person_name }},</p>
<p>You've just selected {{ music_score.composer }} music score {{ music_score.title }}. 
It has {{ music_score.num_of_pages }} page(s).</p>
{% if music_score.date_of_creation != 'unknown' or music_score.date_of_creation is not None  %}
<p>The score was written in {{ music_score.date_of_creation |date:"F j, Y" }}.</p>
{% else %}
<p>The date of composing the score is unknown.</p>
{% endif %}
<p>You can send any suggestions about our site to our cheif_editor. His contacts are shown below:
<ul>
{% for key, value in editor.items %}
<li>{{ key }}:{{ value }}</li>
{% endfor %}
</ul>
</p>""" 

# создаем объект шаблон
t = Template(raw_template)

# задаем значения различных контекстных переменных (далее будут переданы в виде словаря python):
person_name = 'John'
editor = {
	'name': 'Mike', 
	'email': 'mike@msc.ru'
	}
music_score = {
	'composer': 'J.S.Bach', 
	'title': 'D-moll prelude', 
	'num_of_pages': '5', 
	'date_of_creation': datetime.date(1720, 1, 1)
	}

# создаем объект контекст (в качестве параметра передается словарь python со значениями для заполнения шаблона)
c = Context({'editor': editor, 'music_score': music_score, 'person_name': person_name})

# рендерим объект шаблон, передавая в качестве параметра объект контекст
t.render(c)