
class MyResource:
    def __enter__(self):
        print('Entering context.')
        return self

    def __exit__(self, *exc):
        print('EXITING context.')

    def try_me(self):
        print("I work")

def fun():
    with MyResource() as a:
        print('Returning inside with-statement.')
        return a
    print('Returning outside with-statement.')

t =fun()
t.try_me()