# -*- coding: utf-8 -*-
from django.db import models

class PositiveBigIntegerField(models.PositiveIntegerField):
    """Represents MySQL's unsigned BIGINT data type (works with MySQL only!)"""
    empty_strings_allowed = False

    def get_internal_type(self):
        return "PositiveBigIntegerField"

    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            # This is how MySQL defines 64 bit unsigned integer data types
            return "BIGINT UNSIGNED"
        return super(PositiveBigIntegerField, self).db_type(connection)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['bawebauth\.fields\.PositiveBigIntegerField'])
except ImportError:
    pass
