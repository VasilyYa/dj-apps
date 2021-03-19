from django.db import models
import datetime
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
	composers = models.ManyToManyField('Composer', through='ComposerScore') # !!!!!!!!!!

	def to_json(self):
		pass

	# пример встраивания логики в модель (правильно с т.з. MVC):
	@property # <-позволяет манипулировать функцией как свойством
	def published_recently(self):
		return self.publication_date >= timezone.now() - datetime.timedelta(days=1)

	def __str__(self):
		composers_str = '; '.join([x.__str__() for x in self.composers.all()])
		return "Title(name): %s, published: %s, by %s, from: %s" % (self.name, \
			self.publication_date, composers_str, self.publisher)

	# def save(self):
	# 	#
	# 	return super(Score, self).save(*args, **kwargs)

	class Meta:
		db_table = 'scores'

#класс Композитор
class Composer(models.Model):
	first_name = models.CharField(max_length=20, null=False, \
		blank=False, unique=False, verbose_name="Имя")
	last_name = models.CharField(max_length=30, null=True, \
		blank=True, unique=False, verbose_name="Фамилия")
	pen_name = models.CharField(max_length=50, null=True, \
		blank=False, unique=True) # уникальное имя (псевдоним), либо допускается null
	email = models.EmailField(null=True, blank=True, unique=True) # email также уникален, либо отсутствует (null)
																  # значения null в БД становятся None!!!
	headshot = models.ImageField(upload_to='tmp', verbose_name="фотография")
	website = models.URLField(null=True, blank=True, unique=False, verbose_name="Веб-страница")

	def __str__(self):
		if self.pen_name is not None:
			return "%s %s (known as %s)." % (self.first_name, self.last_name, self.pen_name)
		return self.first_name

	class Meta:
		db_table = 'composers'



#класс Композиторы ))
class ComposerScore(models.Model):
	composer = models.ForeignKey('Composer', to_field='id', on_delete=models.CASCADE, db_column='composer_id', null=False, blank=False, unique=False)
	score = models.ForeignKey('Score', to_field='id', on_delete=models.CASCADE, db_column='score_id', null=False, blank=False, unique=False)

	class Meta:
		db_table = 'composers_scores'
		