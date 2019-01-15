# -*- coding: utf-8 -*-

from django import forms
import re


class RrnField(forms.CharField):
    def validate(self, value):
        super(RrnField, self).validate(value)
        if not value:
            return
        try:
            if (97 - int(value[:9]) % 97) != int(value[-2:]):
                raise ValueError()
        except ValueError:
            raise forms.ValidationError("Format invalide")


class NumHouseField(forms.CharField):
    def validate(self, value):
        super(NumHouseField, self).validate(value)
        if not value:
            return
        try:
            if not re.match("[1-9][0-9]*", value):
                raise ValueError()
        except ValueError:
            raise forms.ValidationError("Format invalide")

class NumPhoneField(forms.CharField):
    def validate(self, value):
        super(NumPhoneField, self).validate(value)
        if not value:
            return
        try:
            if not re.match("^(0|\\+|00)(\d{8,})", value):
                raise ValueError()
        except ValueError:
            raise forms.ValidationError("Format invalide")



A2_ATTRIBUTE_KINDS = [
        {
            'label': u'Numéro de registre national',
            'name': 'rrn',
            'field_class': RrnField,
        },
        {
            'label': u'Numéro de maison',
            'name': 'num_house',
            'field_class': NumHouseField,
        },
        {
            'label': u'Numéro de téléphone',
            'name': 'phone',
            'field_class': NumPhoneField,
        }
]
