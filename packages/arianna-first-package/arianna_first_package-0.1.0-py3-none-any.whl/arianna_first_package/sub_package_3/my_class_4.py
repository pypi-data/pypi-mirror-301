# -*- coding: utf-8 -*-
"""
Copyright Arianna Bonazza
ariannabonazza28@gmail.com

This file is part of Arianna's first package.
"""


class MyClass4:
    """A whatever-you-are-doing.

    Parameters
    ----------
    a : str
        The `a` of the system.

    Examples
    --------
        >>> my_object = MyClass4(a = 'Arianna')
    """

    def __init__(self, a: str):
        self.a = a

    def greeting(self) -> str:
        """Print `a` and `says hello to the world!`.

        Returns
        -------
        Str
            'a' and 'says hello to the world!'.

        Examples
        --------
            >>> my_object = MyClass4(a='Arianna')
            >>> my_object.greeting()
            Arianna says hello to the world!
        """
        print(f"{self.a} says hello to the world!")
