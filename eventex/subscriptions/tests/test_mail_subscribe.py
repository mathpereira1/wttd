from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r

class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Matheus Pereira', cpf='12345678901',
            email='matheusps3110@gmail.com', phone='11-98322-2522')
        self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]
        
    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        
        self.assertEqual(expect, self.email.subject)
        
    def test_subscription_email_from(self):
        expect = 'matheusps3110@outlook.com'
        
        self.assertEqual(expect, self.email.from_email)
        
    def test_subscription_email_to(self):
        expect = ['matheusps3110@outlook.com', 'matheusps3110@gmail.com']
        
        self.assertEqual(expect, self.email.to)
        
    def test_subscription_email_body(self):
        contents = [ 
            'Matheus Pereira',
            '12345678901',
            'matheusps3110@gmail.com',
            '11-98322-2522',
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)