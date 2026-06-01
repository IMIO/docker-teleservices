# this file derive from django-tenant-schemas
#   Author: Bernardo Pires Carneiro
#   Email: carneiro.be@gmail.com
#   License: MIT license
#   Home-page: http://github.com/bcarneiro/django-tenant-schemas
from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.migrate import Command as DjangoMigrateCommand
from tenant_schemas.utils import django_is_in_test_mode


class Command(BaseCommand):
    # Django 5.2+ checks that migrate and makemigrations share the same autodetector
    autodetector = getattr(DjangoMigrateCommand, 'autodetector', None)

    def handle(self, *args, **options):
        database = options.get('database', 'default')
        raise CommandError(
            "migrate has been disabled, for database '{}'. Use migrate_schemas "
            "instead. Please read the documentation if you don't know why you "
            "shouldn't call migrate directly!".format(database)
        )


if django_is_in_test_mode():
    from .migrate_schemas import MigrateSchemasCommand

    Command = MigrateSchemasCommand
