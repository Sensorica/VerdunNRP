import datetime
from decimal import *

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client

from webtest import AppError, TestApp

from django_webtest import WebTest

#WebTest doc: http://webtest.pythonpaste.org/en/latest/index.html

from valuenetwork.valueaccounting.models import *
from valuenetwork.valueaccounting.views import *
from valuenetwork.valueaccounting.utils import *
from valuenetwork.valueaccounting.tests.objects_for_testing import *

class OrderTest(WebTest):

    """Testing customer orders
    """

    def setUp(self):

        self.user = User.objects.create_user('alice', 'alice@whatever.com', 'password')

        facets = Facets()
        self.electronic_pattern = facets.electronic_pattern
        self.full_pattern = facets.full_pattern
        electronic_domain = facets.domain.values.get(value="Electronical")
        source_us = facets.source.values.get(value="Us")
        #
        atype = AgentType(
            name='Network',
            party_type='network',
            is_context=True)
        atype.save()
        self.project = EconomicAgent(
            name="Test Project",
            nick="TP",
            agent_type=atype)
        self.project.save()
        recipe = Recipe()
        self.parent = recipe.parent
        self.child = recipe.child
        self.grandchild = recipe.grandchild

        self.wf_recipe = WorkFlowRecipe()
        self.changeable = self.wf_recipe.changeable
        self.another_changeable = self.wf_recipe.another_changeable

        sellable = Facet(
            name="Sellable",
        )
        sellable.save()

        sellable_sellable = FacetValue(
            facet=sellable,
            value="sellable"
        )
        sellable_sellable.save()

        order_pattern = ProcessPattern(
            name="Order pattern",
        )
        order_pattern.save()

        use_case = UseCase.objects.get(identifier="cust_orders")

        puc = PatternUseCase(
            pattern=order_pattern,
            use_case=use_case,
        )
        puc.save()

        sale_pattern = ProcessPattern(
            name="Sale pattern",
        )
        #order_pattern.save() # huh?
        sale_pattern.save()

        use_case = UseCase.objects.get(identifier="sale")

        puc = PatternUseCase(
            pattern=order_pattern,
            use_case=use_case,
        )
        puc.save()

        event_type_sale = EventType(
            name="Sale",
            label="sells",
            relationship="output",
            related_to="agent",
            resource_effect="=",
        )
        event_type_sale.save()

        pfv = PatternFacetValue(
            pattern=order_pattern,
            facet_value=sellable_sellable,
            event_type=event_type_sale,
        )
        pfv.save()

        rtfv = ResourceTypeFacetValue(
            resource_type=self.parent,
            facet_value=sellable_sellable,
        )
        rtfv.save()

        rtfv = ResourceTypeFacetValue(
            resource_type=self.changeable,
            facet_value=sellable_sellable,
        )
        rtfv.save()

        rtfv = ResourceTypeFacetValue(
            resource_type=self.another_changeable,
            facet_value=sellable_sellable,
        )
        rtfv.save()

    def test_create_order(self):
        """Test create_order view

            and subsequent dependent demand explosion

        """

        response = self.app.get('/accounting/create-order/' , user='alice')
        form = response.form
        #import pdb; pdb.set_trace()
        due_date = datetime.date.today().strftime('%Y-%m-%d')
        form["due_date"] = due_date
        form["RT-6-quantity"] = 3
        response = form.submit("submit1").follow()
        process = self.parent.producing_commitments()[0].process
        incoming = process.incoming_commitments()
        child_input = incoming.filter(resource_type=self.child)[0]
        self.assertEqual(child_input.quantity, Decimal("6"))
        rt = child_input.resource_type
        child_output=rt.producing_commitments()[0]
        child_process=child_output.process
        grandchild_input = child_process.incoming_commitments()[0]
        self.assertEqual(grandchild_input.quantity, Decimal("18"))


    def test_order_validation(self):
        """Test fix for #510 Create order blows up
            at least one item must have quantity > 0
        """
        # probably don't need this, but it can't hurt
        Commitment.objects.filter(resource_type=self.child).delete()
        try:
            response = self.app.get('/accounting/create-order/' , user='alice')
            form = response.form
            #import pdb; pdb.set_trace()
            due_date = datetime.date.today().strftime('%Y-%m-%d')
            form["due_date"] = due_date
            form["RT-6-quantity"] = 0
            response = form.submit("submit1").follow()
        except Exception as e:
            raise AssertionError((_('an empty order should not throw, but threw %s' % str(e)),))

        coms = Commitment.objects.filter(resource_type=self.child)
        self.assertFalse(coms)

    def test_create_workflow_order(self):
        """Test create_order for a workflow item

            and subsequent dependent demand explosion

        """

        response = self.app.get('/accounting/create-order/' , user='alice')
        form = response.form
        #import pdb; pdb.set_trace()
        due_date = datetime.date.today().strftime('%Y-%m-%d')
        form["due_date"] = due_date
        form["RT-9-quantity"] = 2000
        response = form.submit("submit1").follow()
        #import pdb; pdb.set_trace()
        pcs = self.changeable.producing_commitments()
        count = pcs.count()
        self.assertEqual(count, 2)
        first_pc = pcs[0]
        self.assertEqual(first_pc.quantity, Decimal("2000"))
        last_pc = pcs[count - 1]
        #import pdb; pdb.set_trace()
        self.assertTrue(last_pc.order_item.exchange)
        order = last_pc.order_item.order
        processes = order.all_processes()
        self.assertEqual(len(processes), 2)
        first_process = processes[0]
        last_process = processes[count - 1]
        nexts = first_process.next_processes()
        prevs = last_process.previous_processes()
        self.assertTrue(first_process in prevs)
        self.assertTrue(last_process in nexts)


    def test_two_workflow_item_order(self):
        """Test create_order for two workflow items

            and subsequent dependent demand explosion

        """

        response = self.app.get('/accounting/create-order/' , user='alice')
        form = response.form
        #import pdb; pdb.set_trace()
        due_date = datetime.date.today().strftime('%Y-%m-%d')
        form["due_date"] = due_date
        form["RT-9-quantity"] = 2000
        form["RT-10-quantity"] = 4000
        response = form.submit("submit1").follow()
        #import pdb; pdb.set_trace()

        pcs = self.changeable.producing_commitments()
        count = pcs.count()
        self.assertEqual(count, 2)
        first_pc = pcs[0]
        self.assertEqual(first_pc.quantity, Decimal("2000"))
        last_pc = pcs[count - 1]
        #import pdb; pdb.set_trace()
        self.assertTrue(last_pc.order_item.exchange)
        first_process = first_pc.process
        last_process = last_pc.process
        nexts = first_process.next_processes()
        prevs = last_process.previous_processes()
        self.assertTrue(first_process in prevs)
        self.assertTrue(last_process in nexts)

        pcs = self.another_changeable.producing_commitments()
        count = pcs.count()
        self.assertEqual(count, 2)
        first_pc = pcs[0]
        self.assertEqual(first_pc.quantity, Decimal("4000"))
        last_pc = pcs[count - 1]
        #import pdb; pdb.set_trace()
        self.assertEqual(first_pc.order_item, last_pc.order_item)
        first_process = first_pc.process
        last_process = last_pc.process
        nexts = first_process.next_processes()
        prevs = last_process.previous_processes()
        self.assertTrue(first_process in prevs)
        self.assertTrue(last_process in nexts)

        order = last_pc.order_item.order
        processes = order.all_processes()
        self.assertEqual(len(processes), 4)

    def test_two_order_items_with_same_resource_type(self):
        due_date = datetime.date.today()
        order = Order(
            name="test",
            due_date=due_date,
        )
        order.save()
        unit = self.wf_recipe.unit
        et = self.wf_recipe.change_event_type
        stages, inheritance = self.changeable.staged_process_type_sequence()
        stage = stages[-1]
        commitment1 = order.add_commitment(
            resource_type=self.changeable,
            context_agent=None,
            quantity=Decimal("2000"),
            event_type=et,
            unit=unit,
            description="Test",
            stage=stage,
        )
        commitment1.generate_producing_process(self.user, [], explode=True)
        due = due_date + datetime.timedelta(days=10)
        commitment2 = order.add_commitment(
            resource_type=self.changeable,
            context_agent=None,
            quantity=Decimal("4000"),
            event_type=et,
            unit=unit,
            description="Test",
            stage=stage,
            due=due,
        )
        commitment2.generate_producing_process(self.user, [], explode=True)

        process1 = commitment1.process
        process2 = commitment2.process
        processes = order.all_processes()
        self.assertEqual(len(processes), 4)
        self.assertEqual(len(process1.previous_processes()), 1)
        self.assertEqual(len(process2.previous_processes()), 1)
        chain = commitment1.process_chain()
        self.assertEqual(len(chain), 2)
        chain = commitment2.process_chain()
        self.assertEqual(len(chain), 2)
        #import pdb; pdb.set_trace()

    def test_create_order_item(self):
        due_date = datetime.date.today()
        order = Order(
            name="test",
            due_date=due_date,
        )
        order.save()
        oi = order.create_order_item(
            resource_type=self.parent,
            quantity=Decimal("1.0"),
            user=self.user,
        )
        #import pdb; pdb.set_trace()
        self.assertEqual(order.order_items().count(), 1)

    def test_create_order_item_using_inherited_recipe(self):
        due_date = datetime.date.today()
        shipment_et = EventType.create('Shipment', 'ships', 'shipped by', 'shipment', 'exchange', '-', 'quantity')
        order = Order(
            order_type="rand",
            name="test",
            due_date=due_date,
        )
        order.save()
        heir = EconomicResourceType(
            name="heir",
            parent=self.parent,
        )
        heir.save()
        oi = order.create_order_item(
            resource_type=heir,
            quantity=Decimal("1.0"),
            user=self.user,
        )
        #import pdb; pdb.set_trace()
        self.assertEqual(order.order_items().count(), 1)
        rt = order.order_items()[0].resource_type
        self.assertEqual(rt, heir)
        self.assertEqual(len(order.all_processes()), 2)

    def test_create_order_item_using_inherited_workflow_recipe(self):
        due_date = datetime.date.today()
        shipment_et = EventType.create('Shipment', 'ships', 'shipped by', 'shipment', 'exchange', '-', 'quantity')
        order = Order(
            order_type="rand",
            name="test",
            due_date=due_date,
        )
        order.save()
        heir = EconomicResourceType(
            name="heir",
            parent=self.changeable,
        )
        heir.save()
        oi = order.create_order_item(
            resource_type=heir,
            quantity=Decimal("1.0"),
            user=self.user,
        )
        #import pdb; pdb.set_trace()
        self.assertEqual(order.order_items().count(), 1)
        rt = order.order_items()[0].resource_type
        self.assertEqual(rt, heir)
        self.assertEqual(len(order.all_processes()), 2)
        #import pdb; pdb.set_trace()
        p = order.all_processes()[1]
        rt = p.incoming_commitments()[0].resource_type
        #self.assertEqual(rt, heir)
        #AssertionError: <EconomicResourceType: changeable> != <EconomicResourceType: heir>
        p = order.all_processes()[0]
        rt = p.output_resource_types()[0]
        self.assertEqual(rt, heir)

    def create_3_process_order(self):
        #add another process to self.wf_recipe
        package_pt = ProcessType(
            name="package",
            estimated_duration=7200,
        )
        package_pt.save()

        to_be_event_type = self.wf_recipe.to_be_event_type
        change_event_type = self.wf_recipe.change_event_type
        change_pt = self.wf_recipe.change_pt
        unit = self.wf_recipe.unit

        package_input = ProcessTypeResourceType(
            process_type=package_pt,
            resource_type=self.changeable,
            stage=change_pt,
            event_type=to_be_event_type,
            quantity=Decimal("1000"),
            unit_of_quantity=unit,
        )
        package_input.save()

        package_output = ProcessTypeResourceType(
            process_type=package_pt,
            stage=package_pt,
            resource_type=self.changeable,
            event_type=change_event_type,
            quantity=Decimal("1000"),
            unit_of_quantity=unit,
        )
        package_output.save()

        due_date = datetime.date.today()
        order = Order(
            name="test",
            due_date=due_date,
        )
        order.save()

        stages, inheritance = self.changeable.staged_process_type_sequence()
        stage = stages[-1]
        order_item = order.add_commitment(
            resource_type=self.changeable,
            context_agent=None,
            quantity=Decimal("2000"),
            event_type=change_event_type,
            unit=unit,
            description="Test",
            stage=stage,
        )
        order_item.generate_producing_process(self.user, [], explode=True)
        return order

    def test_order_process_sequence(self):
        """ Test sequencing when processes have same dates.

            This was a bug, test failed before code fix.
        """
        order = self.create_3_process_order()
        order_item = order.order_items()[0]

        processes_b4 = order.all_processes()
        oi_processes_b4 = order_item.all_processes_in_my_order_item()
        #import pdb; pdb.set_trace()
        for p in processes_b4:
            p.start_date = order.due_date
            p.end_date = order.due_date
            p.save()
        processes_after = order.all_processes()
        #import pdb; pdb.set_trace()
        oi_processes_after = order_item.all_processes_in_my_order_item()
        self.assertEqual(processes_b4, processes_after)
        self.assertEqual(oi_processes_b4, oi_processes_after)

    def test_delete_last_order_process(self):
        order = self.create_3_process_order()
        order_item = order.order_items()[0]
        #delete last process
        last_process = order.last_process_in_order()
        order_item.adjust_workflow_commitments_process_deleted(process=last_process, user=self.user)
        last_process.delete()
        processes = order.all_processes()
        self.assertFalse(last_process in processes)
        self.assertEqual(len(processes), 2)
        new_last_process = order.last_process_in_order()
        self.assertEqual(new_last_process.name, "change")

    def test_delete_middle_order_process(self):
        order = self.create_3_process_order()
        order_item = order.order_items()[0]
        #delete middle process
        processes = order.all_processes()
        middle_process = processes[1]
        order_item.adjust_workflow_commitments_process_deleted(process=middle_process, user=self.user)
        middle_process.delete()
        processes = order.all_processes()
        self.assertFalse(middle_process in processes)
        self.assertEqual(len(processes), 2)
        last_process = order.last_process_in_order()
        self.assertEqual(last_process.name, "package")
