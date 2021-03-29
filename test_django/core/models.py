from django.db import models
import datetime
from django.utils import timezone
import pytz
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import IntegrityError

# Create your models here.
# МОДЕЛИ (=классы):


# константы:
USER_TYPE_ADMIN = 1
USER_TYPE_COMPOSER = 2


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
		ordering = ["id"]


class InnerUserManager(BaseUserManager):

	def create_user(self, email, password=None):
		if not email:
			raise ValueError('user must have an email')

		user = self.model(
			email = self.normalize_email(email)
		)

		user.type_of = USER_TYPE_COMPOSER 
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		user = self.create_user(email, password)
		user.type_of = USER_TYPE_ADMIN
		user.is_admin = True
		user.is_staff = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser, PermissionsMixin):
# класс Композитор - переименовали его в User (соотв-но поменяли знач-е аттрибута composer в классе ComposerScore)
# class Composer(models.Model):
	first_name = models.CharField(max_length=20, null=False, \
		blank=False, unique=False, verbose_name="Имя")
	last_name = models.CharField(max_length=30, null=True, \
		blank=True, unique=False, verbose_name="Фамилия")
	pen_name = models.CharField(max_length=50, null=True, \
		blank=False, unique=True) # уникальное имя (псевдоним), null=True - означает, означает, что джанго при создании таблицы укажет не доп. ограничение NOT NULL
	email = models.EmailField(null=False, blank=False, unique=True) # email уникален, но пустое значение (blank) допускается
	headshot = models.ImageField(null=True, blank=True, unique=False, upload_to='tmp', verbose_name="фотография")
	website = models.URLField(null=True, blank=True, unique=False, verbose_name="Веб-страница")
	type_of = models.PositiveIntegerField(default=USER_TYPE_COMPOSER, \
		blank=False, null=False, unique=False)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	objects = InnerUserManager()
	USERNAME_FIELD = 'email'  # поэтому в аттрибуте email запретил true-значения blank и null
	REQUIRED_FIELDS = []


	def __str__(self):
		if self.pen_name is not None:
			return "%s %s (known as %s)" % (self.first_name, self.last_name, self.pen_name)
		return self.first_name

	@property
	def full_name(self):
		return self.__str__()
	

	class Meta:
		db_table = 'users'
		verbose_name = "Пользователь"
		verbose_name_plural = "Пользователи"
		ordering = ["first_name"]


# класс Композиторы_и_Ноты (связь нот с из композиторами - связь вида ManyToMany (задана в классе Score))
class ComposerScore(models.Model):
	composer = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, db_column='composer_id', null=False, blank=False, unique=False)
	score = models.ForeignKey('Score', to_field='id', on_delete=models.CASCADE, db_column='score_id', null=False, blank=False, unique=False)

	def save(self,*args, **kwargs):
		if self.composer.type_of != USER_TYPE_COMPOSER:
			raise ValueError('Composer has wrong type_of field value!')

		return super(ComposerScore, self).save(*args, **kwargs)

	class Meta:
		db_table = 'composers_scores'
		


#класс Ноты
class Score(models.Model):
	title = models.CharField(max_length=100, null=False, blank=False, verbose_name="Ноты")
	publisher = models.ForeignKey('Publisher', to_field='id', \
		db_column='publisher_id', on_delete=models.CASCADE, blank=True, \
		null=True, unique=False, verbose_name='Издатель') # ключ id в таблице Publisher создается 
	                                                      # django автоматически (см. миграцию 0001_initial.py)
	creation_date = models.DateField(null=True, blank=True, verbose_name='Дата создания муз. произведения')
	publication_date = models.DateField(default=timezone.now, null=True, verbose_name='Дата публикации нот')
	composers = models.ManyToManyField('User', through='ComposerScore') # !!!!!!!!!!

	def starred(self):
		pass

	def to_json(self):
		scores_obj = {}
		if not self.id: # проверка, сохранено ли в базу
			return {}

		scores_obj.update({'title': self.title})
		scores_obj.update({'publisher': self.publisher})
		scores_obj.update({'publication_date': self.publication_date})
		if len(self.composers.all()) > 0:
			scores_obj.update({'composers': [c.__str__() for c in self.composers.all()]})
		else:
			scores_obj.update({'composers': []})
		return scores_obj

	# пример встраивания логики в модель (правильно с т.з. MVC):
	@property # <-позволяет манипулировать функцией как свойством
	def published_recently(self):
		return self.publication_date >= timezone.now() - datetime.timedelta(days=1)

	def __str__(self):
		composers_str = '; '.join([x.__str__() for x in self.composers.all()])
		return "Title: %s, published: %s, by %s, from: %s" % (self.title, \
			self.publication_date, composers_str, self.publisher)


	class Meta:
		db_table = 'scores'
		ordering = ["publisher_id"]
