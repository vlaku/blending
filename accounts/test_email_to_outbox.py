from django.core import mail
from django.urls import reverse
from django.test import TestCase


class EmailTest(TestCase):
    def test_no_email_sent(self):
        self.response = self.client.get(reverse('email_to_outbox'))
        self.assertEqual(len(mail.outbox), 0)

    def test_no_email_sent(self):
        self.response = self.client.get(reverse('email_to_outbox'))
        self.assertEqual(len(mail.outbox), 0)

    def test_email_sent(self):
        self.response = self.client.get(reverse('email_to_outbox'), {'email': 'test@example.com'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].body, 'This is a test message sent to test@example.com.')
