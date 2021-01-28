This directory contains code for testing a babynames.py module:

i) ./babynames_reference.py is the reference implementation
ii) ./test/ directory contains files needed to run unittests

To set this up:

1) drop a babynames.py module into this directory
2) create a PyCharm project based on this directory
3) set up a project configuration for performing unit tests
 - select a py.test configuration
 - set the target to the ./test directory
 - click run to run all the tests!

Once you have everything set up as above and can run all the 
tests, check the output carefully. Your code should pass all
the tests. If any do not pass, then you should investigate!
You may need to look at the source code of the test to 
understand what is required of your code, and thus why it is
failing.

In addition, look at the recording for how much time each test
takes to run.   Each should usually be less than ~100ms.  For 
comparison, it takes about 2 seconds in total to run *all* the
tests on the reference implementation.  If you find your code
is running significantly slower than that, you should look at
whether your code does something inefficient and then think how
you can streamline it.  If you're stuck, have a look through
the babynames_reference.py code itself for ideas about 
relatively efficient ways to implement the requirements of the 
task.


