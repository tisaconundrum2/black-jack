import dill


class Foo(object):         # setup up a class
    def __init__(self):    #
        self.y = 1         # giving an arbitrary value for y
                           #
    def bar(self, x):      # give it a function
        return x + self.y  # return x + 1
                           #
                           #
f = Foo()                  # instantiate our Foo() object into f
_Foo = dill.dumps(Foo)     # pickle Foo() into a string and put it into _Foo
_f = dill.dumps(f)         # pickle f into a string and put it into _f
                           #
f_ = dill.loads(_f)        # unpickle _f from earlier and put it into f_
f_.y                       # call the .y variable.
                           #
f_.bar(1)                  # call the function bar from f_
                           #
Foo_ = dill.loads(_Foo)    # unpickle _Foo from earlier
g = Foo_()                 # Foo_ is an object, let's assign it to g
g.bar(1)                   # call Foo_().bar(1)
