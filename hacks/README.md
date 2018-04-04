This folder contains necessary hacks that will require some manual effort and amendments to the installation instructions.

# views.py

This is a modified version of the library `django-notification` 0.2.0's `views.py`.  The original attempts to import `django.contrib.syndication.views.feed`, which does not exist in Django 1.4.22, which is required for the NRP to function.  Only `notification.views.feed_for_user()` uses the missing function, and the NRP doesn't use that.  Thus, the import is replaced by a function that throws a `NotImplementedError`.  To implement this change, after installing `django-notification` through `requirements.txt`, move this `views.py` to `path_to_your_env/lib/python2.7/site-packages/notification/` overwriting the original.

# init.sh

The installation instructions specify a series of commands that you may need to enter every time you log into your terminal.  Once you have installed `pip`, `virtualenv`, and `virtualenvwrapper`, and created your `virtualenv`, you can use init.sh to do all of that for you via:

    source path_to_init_sh/init.sh

You will have to modify the script to reflect the name of your `virtualenv` and the path to your project, and you may move the file wherever you wish.  It will hasten any troubleshooting a lot.

# fixtures.html and fixtures.js

These were used to generate the file `fixtures/verdun.json`.  The original NRP created most or all of the instances of `UseCase`, `EventType`, `AgentType`, `AgentAssociationType`, and `UseCaseEventType` in `post_migrate` callbacks in `models.py`.  Some of these instances, however, are necessary for the tests to function, and all non-fixture rows in the DB are wiped before testing.  Thus, they needed to go into a fixture file that would be loaded as a prerequisite for those tests.

There is no UI to `fixtures.html`; in order to re-use it, you must edit either `fixtures.js` or add a `<script>` at the bottom of `fixtures.html`.  The JavaScript builds a simple environment into which you can copy and paste `ModelClass.create` calls that will generate the JSON fixture.  The code that is specific to the fixtures in `verdun.json` are surrounded by toggle comments; to replace them for your fixture (if you are editing `fixtures.js`) find the follwing:

    //* VERDUN.JSON

and delete the first `/` character so it looks like this:

    /* VERDUN.JSON

then find:

    /*/
    // YOUR CODE
    /**/

and replace the `// YOUR CODE` with your code as follows.

For each class you need to adapt to a fixture, add the following:

    const NameOfClass = new ModelClass('full_python_path_of_class', []);
    
Go back to your python and copy the `NameOfClass.create`'s parameters, excluding the `cls` parameter.  If the parameters of the `create` function directly correspond with the field names of the model, paste them between the `[]` in that line of JS and surround each with `''` like so:

    const NameOfClass = new ModelClass('full_python_path_of_class', ['param', 'another_param', 'yet_another_param', 'etc']);

If they don't correspond (like the `UseCaseEventType` model already in the JS) you will need to provide the field names instead:

    const NameOfClass = new ModelClass(
      'full_python_path_of_class', 
      ['actual_field', 'another_field', 'yet_another_field', 'etc']
    );

and add a function that will map the parameters to the fields.  Start with this:

    NameOfClass.override(function setupFunction(uber) {
      return function mapper() {
        return uber.call(this,
        
        );
      };
    });

and paste the parameters you copied from the python into the `mapper`'s `()`.  Then, in the parameters to `uber.call` after `this,`, specify how the parameters map to the actual fields in the order you gave above.  It should look like this:

    NameOfClass.override(function setupFunction(uber) {
      return function mapper(param, another_param, yet_another_param, etc) {
        return uber.call(this,
          mapParam(param),
          mapAnother(another_param),
          mapYetAnother(yet_another_param),
          mapEtc(etc)
        );
      };
    });
    
where the `mapX` functions are replaced with whatever transformation you need to do.  Chances are good that what you need to do is retrieve an instance's primary key to refer to it, and to that end, every instance of `ModelClass` has a set of `Map` objects whose names correspond to the names you gave for their fields in the constructor where you can search for objects.  Following our example above, you can get an instance of `NameOfClass` whose `actual_field` is `'some-unique-value'` as follows:

    const modelInstance = NameOfClass.actual_field.get('some-unique-value');

Note that this is only going to work if the field is unique for each model instance and you have already generated the instance before you try to access its primary key.  You can get the primary key by `modelInstance.pk` if you want, but you don't have to.  The `NameOfClass.create` function will substitute any object with its primary key automatically.  As an example, suppose I have two instances of `ModelClass`:

    const Foo = new ModelClass('my_project.Foo', ['name']),
      Bar = new ModelClass('my_project.Bar', ['foo']);
      
and the `foo` field of my model `my_project.Bar` is supposed to be the primary key of a `my_project.Foo` instance, but the parameters of `Bar.create` are `cls, name_of_foo`.  I would then write my mapper as follows:

    Bar.override(function (uber) {
      return function (name_of_foo) {
        return uber.call(this,
          Foo.name.get(name_of_foo)
        );
      };
    });
    
Finally, copy all of the Python code that initializes the model instances and paste it below all of your `new ModelClass` and `NameOfClass.override` (where applicable).  Copy only `NameOfClass.create` calls.  If you are using `override` and need to fetch `Foo` instances for your `ModelClass` `Bar`, make sure the initializations of `Foo` objects are above the initializations of `Bar`.  Delete or comment out the Python comments (`#` and `"""`) and add semicolons at the ends of the lines.

If you have been editing `fixtures.js`, you are done.  If you are adding a tag to `fixtures.html`, add the following at the top of your code:

    fixtures = [];
    
and the following at the bottom of your code:

    $('#out').text(JSON.stringify(fixtures));

Save the file you edited and open `fixtures.html` in your favorite ES6+ compliant browser.  Click the JSON code you see.  Press Ctrl+A to select the code in its entirety, Ctrl+C to copy.  Get out your favorite text editor, create a new file, and paste the generated JSON into it.  Save the file as `whatever.json` in the folder `my_project/fixtures/`.

Finally, in each of your test classes, you'll need to have a static `fixtures` property that reflects the test's dependency on the fixture.  If there is no `fixtures` property on the class, add one:

    class MyTest(TestCase):
      fixtures = ['whatever']
      
If there is already a `fixtures`, append `'whatever'` to it:

    class MyTest(TestCase):
      fixtures = ['some_other_fixture', 'whatever']
      
Now your tests can run, and hopefully you can get rid of the hackish `post_migrate` calls, too.

# Other installation hacks

While installing the NRP on our server, I ran into a variety of issues that were not reflected in the original installation instructions.  Most of them were related to version clashes, and these *should* be fixed by this repository's `requirements.txt`.  Other things I had to do (and you probably will too):

* Our production server did not offer a Django 1.4.22 environment at all anymore.  If you start with a different version of Django, you will want to uninstall the existing Django *outside of your virtualenv*, or it can cause libraries that are not really set up right for Django 1.4.22 to succesfully import what they need from the other version.  Trust me, you want the dependencies to fail early if they're going to fail.
* Ensure that your server does not have Python 3+ installed for the same reason.
* Our production server did not support `sudo`/root privileges or `apt-get`.  Thus, I installed `pip` through the following command:
  * `python <(curl https://bootstrap.pypa.io/get-pip.py) --user`
* For the same reason, rather than installing the original image libraries, I had to use `pip install PIL`.
* No matter what I tried, the `django-corsheaders` library refused to install in a normal location using just `pip`.  You may need to manually move it from `lib/python2.7/home/lib/python2.7/` to `lib/python2.7` (or the equivalent in the `virtualenv`).
* The `django-user-accounts` library was installed previously by another library as its dependency, but the version of `django-user-accounts` was incompatible.  I've included the proper version in `requirements.txt`, but if you start seeing `ImportError`s it's possible that the dependent library went ahead and installed an incompatible version anyway.  To remedy:
  * `pip uninstall django-user-accounts`
  * `pip install django-user-accounts==1.0`
* Our production database did not support superusers or `CREATE` priveleges, which prevented our tests from creating a test database to play around in.  We had to install a "private database app" and reconfigure the `DATABASES` in `local_settings.py` to use it in order to get said priveleges and run our tests.
