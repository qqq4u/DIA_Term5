from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from django.utils import timezone


class Parking(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(default="Парковка возле главного здания", verbose_name="Название")
    address = models.TextField(default="2-я Бауманская ул., 5, стр. 4, Москва", verbose_name="Адресс")
    places_count = models.IntegerField(default=50, verbose_name="Количество мест")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(upload_to="parkings", verbose_name="Фото")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Парковка"
        verbose_name_plural = "Парковки"


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('name', name)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_moderator = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Ticket(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )

    PRICE_STATUS_CHOICES = (
        (1, "Не вычислена"),
        (2, "Вычисляется"),
        (3, "Не удалось вычислить"),
        (4, "Вычислена")
    )

    time = models.IntegerField(default=2, verbose_name="Время (часов)")

    parkings = models.ManyToManyField(Parking, verbose_name="Парковки", null=True)

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания", blank=True, null=True)
    date_of_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    price = models.CharField(default=0, verbose_name="Стоимость", blank=True)
    price_status = models.IntegerField(default=1, verbose_name="Статус стоимости")

    owner = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Создатель", related_name='owner', null=True)
    moderator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Модератор", related_name='moderator', blank=True, null=True)

    def __str__(self):
        return "Абонемент №" + str(self.pk)

    class Meta:
        verbose_name = "Абонемент"
        verbose_name_plural = "Абонементы"