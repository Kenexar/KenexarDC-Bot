class Testing:
    def __init__(self, **kwargs):
        self.options = kwargs.get('options')
        self.no_pm = None

    def print_options(self):
        return self.options if self.options else None

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return self


class MoreTesting(Testing):
    def __init__(self, **kwargs):
        super(MoreTesting, self).__init__(**kwargs)
        self.no_pm = True


if __name__ == '__main__':
    tester = Testing()
    test = MoreTesting()

    print(tester.no_pm)
    print(test.no_pm)

    with tester as runner:
        print(runner.print_options())
