from django.core.management.base import BaseCommand
from reviews import models

from . import _common


class Command(BaseCommand):

    def get_path(self, file_name):
        return f'C:/Dev/api_yamdb/api_yamdb/static/data/{file_name}.csv'

    def handle(self, *args, **options):

        _common.create_items(
            self.get_path('category'),
            models.Category.objects,
        )

        _common.create_items(
            self.get_path('genre'),
            models.Genre.objects,
        )

        _common.create_items(
            self.get_path('users'),
            models.User.objects,
        )

        _common.create_items(
            self.get_path('titles'),
            models.Title.objects,
        )

        _common.create_items(
            self.get_path('review'),
            models.Review.objects,
        )

        _common.create_items(
            self.get_path('comments'),
            models.Comment.objects,
            None,
            ';'
        )
