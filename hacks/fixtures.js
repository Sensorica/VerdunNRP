/**
 * Consumes Django models and Python initialization code (within reason) to
 * produce a JSON fixture format that you can use with manage.py loaddata
 */

// was going to have model classes extend a Model class, but, nah.
function modelFactory(cls, flds) {

  function createFields(...args) {
  	let obj = {};
    flds.forEach((fieldName, i, arr) => {
    	let fieldVal = args[i];

      if (typeof fieldVal === "object") {
      	fieldVal = fieldVal.pk;
      }
      obj[fieldName] = fieldVal;
    });

    return obj;
  }

	function make(...args) {
  	const obj = {
      model: cls.model,
      pk: cls.all.size + 1,
      fields: createFields(...args)
    }
    fixtures.push(obj);
    return cls.add(obj);
  }

  return make;
}

const fixtures = [];

class ModelClass {
	constructor(name, fields) {
  	this.model = `valueaccounting.${name.toLowerCase()}`;
    this.create = modelFactory(this, fields);
    this.all = new Map();
    this.fields = fields;
    let field;
    for (field of fields) {
    	this[field] = new Map();
    }
  }
  add(obj) {
  	let field;
    for (field of Object.keys(obj.fields)) {
    	this[field].set(obj.fields[field], obj);
    }
    this.all.set(obj, obj.pk);
    return obj;
  }
  override(fn) {
  	this.create = fn(this.create);
  }
}

function _(str) {
	return str;
}

const True = true, False = false;

//* VERDUN.JSON

const AgentType = new ModelClass(
		'AgentType', ['name', 'party_type', 'is_context']
  ),
  AgentAssociationType = new ModelClass(
  	'AgentAssociationType',
    [
    	'identifier',
      'name',
      'plural_name',
      'association_behavior',
      'label',
      'inverse_label'
    ]
  ),
  UseCase = new ModelClass(
  	'UseCase',
    [
    	'identifier',
      'name',
      'restrict_to_one_pattern'
    ]
  ),
  EventType = new ModelClass(
  	'EventType',
    [
    	'name',
      'label',
      'inverse_label',
      'relationship',
      'related_to',
      'resource_effect',
      'unit_type'
    ]
  ),
  UseCaseEventType = new ModelClass(
  	'UseCaseEventType',
    [
    	'use_case',
      'event_type'
    ]
  );

UseCaseEventType.override(function (uber) {
	return function (use_case_identifier, event_type_name) {
  	return uber.call(this,
    	UseCase.identifier.get(use_case_identifier),
      EventType.name.get(event_type_name)
    );
  };
});


AgentType.create('Individual', 'individual', False);
AgentType.create('Organization', 'org', False);
AgentType.create('Network', 'network', True);

AgentAssociationType.create('child', 'Child', 'Children', 'child', 'is child of', 'has child');
AgentAssociationType.create('member', 'Member', 'Members', 'member', 'is member of', 'has member');
AgentAssociationType.create('supplier', 'Supplier', 'Suppliers', 'supplier', 'is supplier of', 'has supplier');
AgentAssociationType.create('customer', 'Customer', 'Customers', 'customer', 'is customer of', 'has customer');

UseCase.create('cash_contr', _('Cash Contribution'), True);
UseCase.create('non_prod', _('Non-production Logging'), True);
UseCase.create('rand', _('Manufacturing Recipes/Logging'));
UseCase.create('recipe', _('Workflow Recipes/Logging'));
UseCase.create('todo', _('Todos'), True);
UseCase.create('cust_orders', _('Customer Orders'));
UseCase.create('purchasing', _('Purchasing'));
UseCase.create('res_contr', _('Material Contribution'));
UseCase.create('purch_contr', _('Purchase Contribution'));
UseCase.create('exp_contr', _('Expense Contribution'), True);
UseCase.create('sale', _('Sale'));
UseCase.create('distribution', _('Distribution'), True);
UseCase.create('val_equation', _('Value Equation'), True);
UseCase.create('payout', _('Payout'), True);
UseCase.create('transfer', _('Transfer'));
UseCase.create('available', _('Make Available'), True);
UseCase.create('intrnl_xfer', _('Internal Exchange'));
UseCase.create('supply_xfer', _('Incoming Exchange'));
UseCase.create('demand_xfer', _('Outgoing Exchange'));

EventType.create('Citation', _('cites'), _('cited by'), 'cite', 'process', '=', '');
EventType.create('Resource Consumption', _('consumes'), _('consumed by'), 'consume', 'process', '-', 'quantity');
EventType.create('Cash Contribution', _('contributes cash'), _('cash contributed by'), 'cash', 'exchange', '+', 'value');
EventType.create('Donation', _('donates cash'), _('cash donated by'), 'cash', 'exchange', '+', 'value');
EventType.create('Resource Contribution', _('contributes resource'), _('resource contributed by'), 'resource', 'exchange', '+', 'quantity');
EventType.create('Damage', _('damages'), _('damaged by'), 'out', 'agent', '-', 'value');
EventType.create('Expense', _('expense'), '', 'expense', 'exchange', '=', 'value');
EventType.create('Failed quantity', _('fails'), '', 'out', 'process', '<', 'quantity');
EventType.create('Payment', _('pays'), _('paid by'), 'pay', 'exchange', '-', 'value');
EventType.create('Resource Production', _('produces'), _('produced by'), 'out', 'process', '+', 'quantity');
EventType.create('Work Provision', _('provides'), _('provided by'), 'out', 'agent', '+', 'time');
EventType.create('Receipt', _('receives'), _('received by'), 'receive', 'exchange', '+', 'quantity');
EventType.create('Sale', _('sells'), _('sold by'), 'out', 'agent', '=', '');
EventType.create('Shipment', _('ships'), _('shipped by'), 'shipment', 'exchange', '-', 'quantity');
EventType.create('Supply', _('supplies'), _('supplied by'), 'out', 'agent', '=', '');
EventType.create('Todo', _('todo'), '', 'todo', 'agent', '=', '');
EventType.create('Resource use', _('uses'), _('used by'), 'use', 'process', '=', 'time');
EventType.create('Time Contribution', _('work'), '', 'work', 'process', '=', 'time');
EventType.create('Create Changeable', _('creates changeable'), 'changeable created', 'out', 'process', '+~', 'quantity');
EventType.create('To Be Changed', _('to be changed'), '', 'in', 'process', '>~', 'quantity');
EventType.create('Change', _('changes'), 'changed', 'out', 'process', '~>', 'quantity');
EventType.create('Adjust Quantity', _('adjusts'), 'adjusted', 'adjust', 'agent', '+-', 'quantity');
EventType.create('Cash Receipt', _('receives cash'), _('cash received by'), 'receivecash', 'exchange', '+', 'value');
EventType.create('Distribution', _('distributes'), _('distributed by'), 'distribute', 'distribution', '+', 'value');
EventType.create('Cash Disbursement', _('disburses cash'), _('disbursed by'), 'disburse', 'distribution', '-', 'value');
EventType.create('Payout', _('pays out'), _('paid by'), 'payout', 'agent', '-', 'value');
EventType.create('Loan', _('loans'), _('loaned by'), 'cash', 'exchange', '+', 'value');
EventType.create('Transfer', _('transfers'), _('transfered by'), 'transfer', 'exchange', '=', 'quantity');
EventType.create('Reciprocal Transfer', _('reciprocal transfers'), _('transfered by'), 'transfer', 'exchange', '=', 'quantity');
EventType.create('Fee', _('fees'), _('charged by'), 'fee', 'exchange', '-', 'value');
EventType.create('Give', _('gives'), _('given by'), 'give', 'transfer', '-', 'quantity');
EventType.create('Receive', _('receives'), _('received by'), 'receive', 'exchange', '+', 'quantity');

UseCaseEventType.create('cash_contr', 'Time Contribution');
UseCaseEventType.create('cash_contr', 'Cash Contribution');
UseCaseEventType.create('cash_contr', 'Donation');
UseCaseEventType.create('non_prod', 'Time Contribution');
UseCaseEventType.create('rand', 'Citation');
UseCaseEventType.create('rand', 'Resource Consumption');
UseCaseEventType.create('rand', 'Resource Production');
UseCaseEventType.create('rand', 'Resource use');
UseCaseEventType.create('rand', 'Time Contribution');
UseCaseEventType.create('rand', 'To Be Changed');
UseCaseEventType.create('rand', 'Change');
UseCaseEventType.create('rand', 'Create Changeable');
UseCaseEventType.create('recipe','Citation');
UseCaseEventType.create('recipe', 'Resource Consumption');
UseCaseEventType.create('recipe', 'Resource Production');
UseCaseEventType.create('recipe', 'Resource use');
UseCaseEventType.create('recipe', 'Time Contribution');
UseCaseEventType.create('recipe', 'To Be Changed');
UseCaseEventType.create('recipe', 'Change');
UseCaseEventType.create('recipe', 'Create Changeable');
UseCaseEventType.create('todo', 'Todo');
UseCaseEventType.create('res_contr', 'Time Contribution');
UseCaseEventType.create('res_contr', 'Resource Contribution');
UseCaseEventType.create('purch_contr', 'Time Contribution');
UseCaseEventType.create('purch_contr', 'Expense');
UseCaseEventType.create('purch_contr', 'Payment');
UseCaseEventType.create('purch_contr', 'Receipt');
UseCaseEventType.create('exp_contr', 'Time Contribution');
UseCaseEventType.create('exp_contr', 'Expense');
UseCaseEventType.create('exp_contr', 'Payment');
UseCaseEventType.create('sale', 'Shipment');
UseCaseEventType.create('sale', 'Cash Receipt');
UseCaseEventType.create('sale', 'Time Contribution');
UseCaseEventType.create('distribution', 'Distribution');
UseCaseEventType.create('distribution', 'Time Contribution');
UseCaseEventType.create('distribution', 'Cash Disbursement');
UseCaseEventType.create('val_equation', 'Time Contribution');
UseCaseEventType.create('val_equation', 'Resource Production');
UseCaseEventType.create('payout', 'Payout');
UseCaseEventType.create('transfer', 'Transfer');
UseCaseEventType.create('transfer', 'Reciprocal Transfer');
UseCaseEventType.create('intrnl_xfer', 'Transfer');
UseCaseEventType.create('intrnl_xfer', 'Reciprocal Transfer');
UseCaseEventType.create('intrnl_xfer', 'Time Contribution');
UseCaseEventType.create('supply_xfer', 'Transfer');
UseCaseEventType.create('supply_xfer', 'Reciprocal Transfer');
UseCaseEventType.create('supply_xfer', 'Time Contribution');
UseCaseEventType.create('demand_xfer', 'Transfer');
UseCaseEventType.create('demand_xfer', 'Reciprocal Transfer');
UseCaseEventType.create('demand_xfer', 'Time Contribution');
/*/
// YOUR CODE
/**/

$("#out").text(JSON.stringify(fixtures));
