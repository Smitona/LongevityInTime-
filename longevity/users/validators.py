import re
from django.core.exceptions import ValidationError


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'[A-Z]', password):
            raise ValidationError(
                'Your password must contain at least one uppercase character.'
            )

    def get_help_text(self):
        return 'Your password must contain at least one uppercase character.'


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'[a-z]', password):
            raise ValidationError(
                'Your password must contain at least one lowercase character.'
            )

    def get_help_text(self):
        return 'Your password must contain at least one lowercase character.'


class LatinCharValidator(object):
    def validate(self, password, user=None):
        if re.findall(r'[а-яА-яЁё] ', password):
            raise ValidationError(
                'Your password must use Latin characters only.'
            )

    def get_help_text(self):
        return 'Your password must use Latin characters only.'


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'\d', password):
            raise ValidationError(
                'Your password must contain at least one digit.'
            )

    def get_help_text(self):
        return 'Your password must contain at least one digit.'


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                'Your password must contain at least one symbol.'
            )

    def get_help_text(self):
        return 'Your password must contain at least one symbol.'
