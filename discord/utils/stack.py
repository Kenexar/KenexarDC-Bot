from typing import NewType

stack = NewType('Stack', list)


class Stack:
    def __init__(self, stack_name):
        self.stack_name = stack_name

        self.stacks = False

    def create_stack(self, pre_stack: list = None) -> stack:
        """ Create a Stack with content or without content

        :param pre_stack: Optional list of pre-stack elements
        :type pre_stack: List
        :return: A new stack object
        :rtype: stack
        """

        if self.stacks:
            raise OverflowError('Already created a stack')
        self.stacks = True

        ret = stack([])
        if pre_stack:
            ret = ret + pre_stack
        return ret

    def push(self: list, element):
        return self.append(element)

    def __repr__(self):
        return self.stack_name


if __name__ == '__main__':
    my_stack = Stack('My Stack')
    my_stack.create_stack()
    print(my_stack)
