from typing import Optional, List
from dataclasses import dataclass
from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.factories import DataclassFactory
from pydantic import BaseModel
from faker import Faker
from random import randint


class Address(BaseModel):
    street: str

class Person(BaseModel):
    name: str
    age: Optional[int]
    height: float
    weight: float
    address: List[Address]
    address2: Address
    address3: List[Address]


def or_none(v):
    if randint(0,1) == 1:
        return None
    else:
        return v

class AddressFactory(ModelFactory[Address]):
    __faker__ = Faker(locale="de_DE")
    @classmethod
    def street(cls) -> float:
        return cls.__faker__.street_name()


class PersonFactory(ModelFactory[Person]):
    __faker__ = Faker(locale="de_DE")
    # __randomize_collection_length__=True
    # __random_seed__ = 10
    address = Use(AddressFactory.batch, size=2)
    address2 = AddressFactory
    address3 = Use(AddressFactory.batch, size=randint(0,3))


    @classmethod
    def name(cls) -> str:
        return cls.__faker__.name()

    @classmethod
    def age(cls) -> int or None:
        return or_none(randint(0, 120))

    @classmethod
    def height(cls) -> float:
        return randint(150, 220)/100

    @classmethod
    def weight(cls) -> float:
        return randint(4000, 16000)/100






def test_is_person() -> None:
    address_instance = AddressFactory.build()
    print(address_instance)
    person_instance = PersonFactory.build()
    print(person_instance)
    print(person_instance.address3)
    assert isinstance(person_instance, Person)
    assert isinstance(person_instance.name, str)
    assert isinstance(person_instance.age, (int, type(None)))
    assert isinstance(person_instance.height, float)
    assert isinstance(person_instance.weight, float)


if __name__ == '__main__':
    test_is_person()

