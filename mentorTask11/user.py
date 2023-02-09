import attr
from camel_to_snake_converter import change_case


@attr.s
class User:
    user_id: str = attr.ib(default="uid2000")
    transactions: list[str] = attr.ib(default=[])

    def __setattr__(self, __name: str, __value) -> None:
        __name = change_case(__name)
        if __name == "user_id":
            self.__dict__[__name] = __value
        elif __name == "transactions":
            self.__dict__[__name] = __value
