
from django.test import TestCase
from valuenetwork.valueaccounting.models import Transfer, EventType, EconomicEvent, EconomicResourceType
from datetime import date
from decimal import Decimal
from exceptions import Exception, AssertionError

class NoThrowTransferText(TestCase):
    """
    Tests fix for the issue wherein fetching a transfer's event text would throw
    """

    fixtures = ['verdun']
    
    def setUp(self):
        self.transfer = Transfer(
            created_date=date.today(),
            slug='test-xfer-xfer',
            transfer_date=date.today()
        )
        self.transfer.save()

        self.et_give = EventType.objects.get(name='Give') or EventType(
            name='Give',
            label='do not care',
            resource_effect='=',    # don't care
            slug='test-xfer-et-give'
        )
        self.et_give.save()

        self.et_recv = EventType.objects.get(name='Receive') or EventType(
            name='Receive',
            label='do not care',
            resource_effect='=',    # don't care
            slug='test-xfer-et-recv'
        )
        self.et_recv.save()

        self.rt_spam = EconomicResourceType(
            name='Spam',
            slug='test-xfer-rt-spam'
        )
        self.rt_spam.save()

        self.rt_eggs = EconomicResourceType(
            name='Eggs',
            slug='test-xfer-rt-eggs'
        )
        self.rt_eggs.save()

        # both events should have null agents so that there is no extra
        # assignment to give_text or receive_text
        self.ev_give = EconomicEvent(
            event_type=self.et_give,
            event_date=date.today(),
            resource_type=self.rt_spam,
            quantity=Decimal('1.0'),
            transfer=self.transfer,
            slug='test-xfer-ev-give'
        )
        self.ev_give.save()

        self.ev_recv = EconomicEvent(
            event_type=self.et_recv,
            event_date=date.today(),
            resource_type=self.rt_eggs,
            quantity=Decimal('1.0'),
            transfer=self.transfer,
            slug='test-xfer-ev-recv'
        )
        self.ev_recv.save()

    def tearDown(self):
        self.ev_recv.delete()
        self.ev_give.delete()
        self.rt_eggs.delete()
        self.rt_spam.delete()
        self.et_give.delete()
        self.et_recv.delete()
        self.transfer.delete()

    def test_xfer_throw(self):
        try:
            dont_care = self.transfer.event_text()
        except Exception as e:
            raise AssertionError((_('Transfer raised an exception: ' + str(e)),))
