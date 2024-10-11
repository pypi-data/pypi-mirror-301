from typing import Any



__ver__ = '0.0.2'

__any__ = [
    [str, int, float, bool, dict, list, tuple, set],
    {'+': 1, '-': -1, 1: 1, -1: -1},
    'Different element types', 'Type Error of {}',
    'Type Error of {}', 'The rules are unclear',
    'Data type error', '{} type does not support conversion to stack'
]

__all__ = ['stack', 'iters', 'stksum', 'update', 'clear', 'ssort', 'move', 'seek', 'isstack']


class StackError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def detection_stack(func):
    def wrapper(self, *args, **kwargs):
        if hasattr(stack, 'detection') and self.detection:
            self.detection()
            return func(self, *args, **kwargs)
        else:
            raise PermissionError('No permission')
    return wrapper


class stack:
    """
    Stack is a type developed based on lists.

    You can create a stack like this:
    _var = stack(typing)

    The available types of typing are:
    str, int, float, bool, list, dict, tuple, set, stack...

    If you view the stack, it will be returned in the form of a set:
    Empty stack {}
    Int stack {1, 2, 3, 4, 5}...

    Based on C++ -> Python.
    """

    def __new__(cls, *args, **kwargs):
        """ Create a new stack. """
        return super().__new__(cls)


    def __init__(self, typing=None):
        """ Initialize stack. """
        if (typing not in __any__[0]) and not isinstance(typing, tuple(__any__[0])) and typing not in ['any', None]:
            raise StackError(__any__[6])

        self.__typing = typing
        self.__stack: list[typing] = []

        if isinstance(typing, tuple(__any__[0][5:9])):
            try:
                self.__stack = list(typing)
                self.__typing = None
            except (TypeError):
                raise StackError(__any__[7].format(type(typing).__name__))


    def __str__(self):
        """ Convert stack to string. """
        from re import sub
        return sub(r'\[', '{', sub(']', '}', str(self.__stack)))


    def __repr__(self):
        """ Output Stack """
        from re import sub
        return sub(r'\[', '{', sub(']', '}', str(self.__stack)))


    def detection(self) -> None:
        """
        Check if the element types of the stack are consistent.

        In the class, the decorator 'detection_stack' can detect in real-time:
        @detection_stack
        def size(self) -> int: ...

        This function will not return anything.
        """

        if self.__typing in ['any', None]:
            return

        if len(self.__stack) > 0:
            for item in self.__stack:
                if not isinstance(item, self.__typing):
                    raise StackError(__any__[2])
        return


    @property
    @detection_stack
    def size(self) -> int:
        """ Return the number of elements in the stack. """
        return len(self.__stack)


    @detection_stack
    def pop(self) -> None:
        """ Pop up the top element of the stack. """
        if len(self.__stack) <= 0:
            return
        del self.__stack[-1]


    @property
    @detection_stack
    def top(self) -> Any:
        """ Get the top element of the stack. """
        if len(self.__stack) <= 0:
            return None
        return self.__stack[-1]


    @property
    @detection_stack
    def empty(self) -> bool:
        """ Check if the stack is empty. """
        return len(self.__stack) == 0


    @detection_stack
    def push(self, _obj) -> None:
        """ Push elements onto the stack. """
        self.__stack.append(_obj)


    @detection_stack
    def swap(self, other) -> None:
        """ Swap the two stacks. """
        if not isinstance(other, stack):
            raise StackError(__any__[3].format(type(other).__name__))
        _T, _C = stack(int), self.__stack[:]
        while not other.empty:
            _T.push(other.top)
            other.pop()
        while _C:
            other.push(_C[-1])
            _C.pop()
        self.__stack = iters(_T)


    @detection_stack
    def _copy(self) -> Any:
        """ Save your stack as a copy """
        _stack = stack(self.__typing)
        for item in reversed(self.__stack):
            _stack.push(item)
        return _stack


def isstack(*args) -> bool:
    """ Check if one or more variables are on the stack. """
    global stack, __any__
    for arg in args:
        if not isinstance(arg, stack):
            return False
    return True


def clear(_Stack) -> None:
    """ Pop up all elements of the stack. """
    global stack, __any__
    if not isstack(_Stack):
        raise StackError(__any__[4].format(type(_Stack).__name__))

    while not _Stack.empty:
        _Stack.pop()


def iters(_Stack, typing=list) -> list | tuple:
    """ Convert the stack into an iterable list. """
    global stack, __any__
    if not isstack(_Stack):
        raise StackError(__any__[4].format(type(_Stack).__name__))

    if typing not in [tuple, list]:
        raise StackError(__any__[4].format(type(typing).__name__))

    _StackIter, _T = [], _Stack._copy()

    while not _T.empty:
        _StackIter.append(_T.top)
        _T.pop()

    return typing(_StackIter)


def move(_Stack, other) -> None:
    """ Move elements from one stack to another stack. """
    global stack, __any__
    if not isstack(_Stack, other):
        raise StackError(__any__[4].format(type(_Stack).__name__))

    while not _Stack.empty:
        other.push(_Stack.top)
        _Stack.pop()


def seek(_Stack, *args) -> int | tuple[int, ...]:
    """ Find the position of an element from the stack. """
    global stack, __any__
    if not isstack(_Stack):
        raise StackError(__any__[4].format(type(_Stack).__name__))
    tup = []

    try:
        for s in args:
            if len(args) == 1:
                return iters(_Stack).index(s)
            tup.append(iters(_Stack).index(s))
        return tuple(tup)

    except Exception:
        return -1


def stksum(_Stack) -> int:
    """ Calculate the sum of elements in an int stack. """
    global stack, __any__
    if not isstack(_Stack):
        raise StackError(__any__[4].format(type(_Stack).__name__))
    result, _T = 0, _Stack._copy()

    while not _T.empty:
        if not isinstance(_T.top, int):
            return -1
        result += _T.top
        _T.pop()

    return result


def ssort(_Stack, rule=1) -> None:
    """ Stack ascending or descending sorting. """
    global stack, __any__

    if not isstack(_Stack):
        raise StackError(__any__[4].format(type(_Stack).__name__))

    if rule not in __any__[1]:
        raise StackError(__any__[5])

    _it = iters(_Stack)
    for i in range(len(_it)):
        for j in range(len(_it) - i - 1):
            if _it[j] > _it[j + 1]:
                _it[j], _it[j + 1] = _it[j + 1], _it[j]

    clear(_Stack)
    for item in _it[::__any__[1][rule]]:
        _Stack.push(item)


def update(_Stack, *args) -> None:
    """ Combine multiple stacks into one """
    global stack, __any__
    if not isstack(_Stack):
        raise StackError(__any__[4].format(type(_Stack).__name__))

    for s in args:
        if isstack(s):
            raise StackError(__any__[4].format(type(_Stack).__name__))
        while not s.empty:
            _Stack.push(s.top)
            s.pop()



if __name__ == '__main__':
    examstack_int = stack(int)                          # An int stack
    examstack_any = stack()                             # An arbitrary stack

    for i in range(1, 11):
        examstack_int.push(int(i))                      # Add elements to the stack

    print(isstack(examstack_int, examstack_any))  # Check if it is a stack
    print(examstack_int, stksum(examstack_int))         # Printing stack and summing stack elements