from math import inf
from numbers import Number
from pickledb import PickleDB


class Preferences(PickleDB):
    numerical_op_error = TypeError(
        "Numerical operations can only apply to int or float values"
    )

    def _numerical_op(self, key, direction, step, limit):
        value = self.get(key)

        if isinstance(value, Number):
            newvalue = (
                min(value + step, limit) if direction > 0 else max(value - step, limit)
            )
            return self.set(key, newvalue)
        else:
            raise self.numerical_op_error

    def increment(self, key, step=1, max=inf):
        return self._numerical_op(key, 1, step, max)

    def decrement(self, key, step=1, min=inf):
        return self._numerical_op(key, -1, step, min)

    def startswith(self, substring):
        return [k for k in self.getall() if k.startswith(substring)]

    def setall(self, dict):
        self.db.update(dict)
        self._autodumpdb()
        return True
