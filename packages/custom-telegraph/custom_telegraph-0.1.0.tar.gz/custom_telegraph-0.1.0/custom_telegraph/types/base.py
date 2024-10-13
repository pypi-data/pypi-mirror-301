from abc import ABC


class Type(ABC):
    def __repr__(self):
        attrs = ", ".join(f"{key}={value!r}" for key, value in vars(self).items())
        return f'{self.__class__.__name__}({attrs})'
