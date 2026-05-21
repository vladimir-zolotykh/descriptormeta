#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC, abstractmethod
from collections import OrderedDict
from numbers import Number


class Validator(ABC):
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self._name] = value

    @abstractmethod
    def validate(self, value):
        pass


class OneOf(Validator):
    def __init__(self, *choices):
        self.choices = choices

    def validate(self, value):
        if value not in self.choices:
            raise ValueError(f"{value!r} must be one of {self.choices}")


class Number(Validator):
    def __init__(self, min: Number, max: Number):
        self._val: tuple[Number, Number] = (min, max)

    def validate(self, val):
        if isinstance(val, Number):
            raise TypeError(f"{val!r} must be of type Number")
        if val < self._value[0] or self._val[1] <= val:
            raise ValueError(
                f"{val!r} must be in range [{self._val[0]}, {self._val[1]}("
            )


class String(Validator):
    def __init__(self, size: tuple[int, int], predicate: callable = str.upper):
        self.size = size  # (mix, max)
        self.predicate = predicate

    def validate(self, val):
        if not isinstance(val, str):
            raise TypeError(f"{val!r} must be str")
        if len(val) < self.size[0] or self.size[1] < len(val):
            raise ValueError(
                f"{val!r} must have from {self.size[0]} to {self.size[1]} chars"
            )


class OrderedMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        fields = clsdict.get("_fields", [])
        if fields:
            for key, value in clsdict.items():
                if isinstance(value, Validator):
                    fields.append(value)
            clsdict["_fields"] = fields
        return super().__new__(mcls, clsname, bases, clsdict)

    def __prepare__(clsname, bases, **kwds):
        return OrderedDict()


class Drawer(metaclass=OrderedMeta):
    pass


class Lot(Drawer):
    kind = OneOf("metal", "wood", "plastic")
    quantity = Number(0.3, 10.2)

    def __init__(self, kind, quantity):
        self.kind = kind
        self.quantity = quantity


if __name__ == "__main__":
    lot1 = Lot("metal", 7.2)
    print(lot1.kind)
    try:
        lot2 = Lot("paper")
    except ValueError as exc:
        print(str(exc))
