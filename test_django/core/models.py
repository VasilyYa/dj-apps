from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
# МОДЕЛИ (классы):

# класс Издатель
class Publisher(models.Model):
	name = models.CharField(max_length=30, null=False, \
		blank=False, unique=False, verbose_name="Имя")
	adress = models.CharField(max_length=50, null=True, \
	 	blank=True, unique=False, db_column="addr", verbose_name="Адрес")
	website = models.URLField(null=True, verbose_name="Веб-сайт")

	def __str__(self):
		return str(self.name)

	class Meta:
		db_table = 'publishers'

#класс Ноты
class Score(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Ноты")
	publisher = models.ForeignKey('Publisher', to_field='id', \
		db_column='publisher_id', on_delete=models.CASCADE, blank=True, \
		null=True, unique=False, verbose_name='Издатель') # ключ id в таблице Publisher создается 
	                                                      # django автоматически (см. миграцию 0001_initial.py)
	creation_date = models.DateField(null=True, blank=True, verbose_name='Дата создания муз. произведения')
	publication_date = models.DateField(default=timezone.now, null=True, verbose_name='Дата публикации нот')
	# composers = ... (связь типа "многие ко многим" будет разобрана на след. занятии № 5)

	def __str__(self):
		return "Title %s, published: %s, from %s" % (self.name, self.publication_date, self.publisher)
	class Meta:
		db_table = 'scores'

#класс Композитор
class Composer(models.Model):
	first_name = models.CharField(max_length=20, null=False, \
		blank=False, unique=False, verbose_name="Имя")
	last_name = models.CharField(max_length=30, null=True, \
		blank=True, unique=False, verbose_name="Фамилия")
	email = models.EmailField()
	headshot = models.ImageField(upload_to='tmp', verbose_name="фотография")
	website = models.URLField(null=True, blank=True, unique=False, verbose_name="Веб-страница")

	class Meta:
		db_table = 'composers'