# Verify that the response's new resource form contains no quantity field

from django.test import TestCase, Client
from valuenetwork.valueaccounting.models import EconomicResourceType
from xml.etree import ElementTree
from exceptions import Exception


class NoQuantityTest(TestCase):
    """
    Tests fix for issue of new resource types accepting a quantity on their
    form class (they shouldn't)
    """

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
        client = Client()
        resp = client.get(
            '/accounting/resource-type/%s/' % self.rt.id,
            follow=True
        )
        doc = ElementTree.fromstring(resp.content)

        res_form = None
        for form in doc.iter('form'):
            node_id = form.get('id')
            if node_id == 'resourceForm':
                res_form = form
                break

        if not res_form:
            raise Exception((_('Could not find resource form in resource type form'),))

        for inp in res_form.iter('input'):
            assert inp.get('name') != 'quantity'
