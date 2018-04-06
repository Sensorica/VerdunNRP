# Verify that the response's new resource form contains no quantity field

from django.test import TestCase, Client
from django.contrib.auth.models import User
from valuenetwork.valueaccounting.models import EconomicResourceType, EconomicAgent, AgentType, AgentUser
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

        self.the_best_user = User.objects.create_user('david', 'moc.liamg@gmail.com', 'my actual secret password in real life')
        self.the_best_user.save()

        self.mi6 = AgentType(
            name='MI6 Spy',
            party_type='org',
            #is_context=True
        )
        self.mi6.save()

        self.secret_agent = EconomicAgent(
            name='bond, james bond',
            nick='007',
            agent_type=self.mi6,
            #is_context=True,
            slug='bond-james-bond'
        )
        self.secret_agent.save()

        self.queen = AgentUser(
            agent=self.secret_agent,
            user=self.the_best_user
        )
        self.queen.save()

        self.app.set_user(self.the_best_user)

    def tearDown(self):
        self.rt.delete()
        self.queen.delete()
        self.secret_agent.delete()
        self.mi6.delete()
        self.the_best_user.delete()
        self.app.set_user(None)

    def test_no_quantity(self):
        """Resource Type creation form should not take a quantity
        """
        resp = self.app.get(
            '/accounting/resource-type/%s/' % (self.rt.id,)
        )#.follow()#again if resp requires a redirect some day.
        self.assertIn('agent', resp.context, msg='agent is not in context')
        self.assertEqual(self.the_best_user.agent.agent, self.secret_agent,
            msg="This is not the agent we're looking for, it's %s" % (resp.context['agent'],)
        )

        res_form = None
        field = None
        try:
            res_form = resp.forms['resourceForm']
        except:
            pass
        self.assertIsNotNone(res_form, msg='form#resourceForm not found')

        try:
            field = res_form.fields['quantity']
            print resp.context.items()
        except:
            pass

        self.assertIsNone(field, msg='found (form#resourceForm).quantity')
