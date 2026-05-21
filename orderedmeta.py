#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC, abstractmethod
from collections import OrderedDict


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

    def __init__(self, kind):
        self.kind = kind


if __name__ == "__main__":
    lot1 = Lot("metal")
    print(lot1.kind)
    try:
        lot2 = Lot("paper")
    except ValueError as exc:
        print(str(exc))
