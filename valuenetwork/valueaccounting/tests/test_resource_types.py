# Verify that the response's new resource form contains no quantity field

from django.test import TestCase, Client
from valuenetwork.valueaccounting.models import EconomicResourceType
from django_webtest import WebTest
from exceptions import Exception


class NoQuantityTest(WebTest):

    fixtures = ['verdun']

    def setUp(self):
        self.rt = EconomicResourceType(
            name='Spam',
            slug='test-rt-spam'
        )
        self.rt.save()

    def tearDown(self):
        self.rt.delete()

    def test_no_quantity(self):
        """
        Resource Type creation form should not take a quantity
        """
        resp = self.app.get(
            '/accounting/resource-type/%s/' % self.rt.id
        ).follow()
        res_form = None
        field = None
        try:
            res_form = resp.forms['resourceForm']
        except:
            pass
        self.assertIsNotNone(res_form, msg='form#resourceForm not found')

        try:
            field = res_form.fields['quantity']
        except:
            pass

        self.assertIsNone(field, msg='found (form#resourceForm).quantity')
