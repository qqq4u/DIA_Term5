from django.core.management import BaseCommand

from app.models import CustomUser


def add_users():
    CustomUser.objects.create_user(name='user1', email='user1@user.com', password='1234')
    CustomUser.objects.create_user(name='user2', email='user2@user.com', password='1234')
    CustomUser.objects.create_user(name='user3', email='user3@user.com', password='1234')
    CustomUser.objects.create_superuser(name='root', email='root@root.com', password='1234')
    CustomUser.objects.create_superuser(name='root2', email='root2@root.com', password='1234')
    CustomUser.objects.create_superuser(name='root3', email='root3@root.com', password='1234')

    print("Пользователи созданы")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()

