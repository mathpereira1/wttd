from ast import Subscript
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscriptionFormTest(TestCase):
    def test_has_fields(self):
        """Form must have 4 fields."""
        form = SubscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digit(self):
        """CPF must only accepts digits"""
        # 12345678901 ABCD5678901 quality
        form = self.make_validated_form(cpf='ABCD5678901')
        self.assertFormErrorCode(form, 'cpf', 'digits')
    
    def test_cpf_has_11_digits(self):
        """CPF must have 11 digits."""
        # 12345678901 1234 quantity   
        form = self.make_validated_form(cpf='1234')     
        self.assertFormErrorCode(form, 'cpf', 'length')
    
    def test_name_must_be_capitalized(self):
        """Name must be capitaqlized."""
        # MATHEUS pereira -> Matheus Pereira
        form = self.make_validated_form(name='MATHEUS pereira')
        self.assertEqual('Matheus Pereira', form.cleaned_data['name'])
    
    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)
    
    def make_validated_form(self, **kwargs):
        valid = dict(name='Matheus Pereira', cpf='12345678901',
                    email='matheusps3110@gmail.com', phone='11-983222522')
        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form