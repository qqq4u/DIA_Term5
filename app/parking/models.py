from datetime import datetime
from django.db import models, connection

from django.urls import reverse
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

    def get_absolute_url(self):
        return reverse("parking_details", kwargs={"parking_id": self.id})

    def get_delete_url(self):
        return reverse("parking_delete", kwargs={"parking_id": self.id})

    def delete(self):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE parking_parking SET status = 2 WHERE id = %s", [self.pk])


class Ticket(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )

    time = models.IntegerField(default=2, verbose_name="Время (часов)")

    parkings = models.ManyToManyField(Parking, verbose_name="Парковки", null=True)

    status = models.IntegerField(max_length=100, choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата создания")
    date_of_formation = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата формирования")
    date_complete = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата завершения")

    def __str__(self):
        return "Абонемент №" + str(self.pk)

    class Meta:
        verbose_name = "Абонемент"
        verbose_name_plural = "Абонементы"