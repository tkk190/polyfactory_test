from typing import Optional, List
from polyfactory import Use
from faker import Faker
from random import randint
from sqlmodel import SQLModel, Field, Relationship
from sqlmodel_factory import SQLModelFactory


class Address(SQLModel, table=True):
    __tablename__ = 'address'
    id: Optional[int] = Field(primary_key=True)
    street: str
    person_id: Optional[int] = Field(foreign_key="person.id")
    person: Optional["Person"] = Relationship(back_populates="addresses")

class Person(SQLModel, table=True):
    __tablename__ = 'person'
    id: Optional[int] = Field(primary_key=True)
    name: str
    age: Optional[int]
    height: float
    weight: float
    addresses: List[Address] = Relationship(back_populates="person")

def or_none(v):
    if randint(0,1) == 1:
        return None
    else:
        return v

class AddressFactory(SQLModelFactory[Address]):
    __faker__ = Faker(locale="de_DE")
    __set_relationships__ = True
    __allow_none_optionals___ = False
    @classmethod
    def street(cls) -> float:
        return cls.__faker__.street_name()


class PersonFactory(SQLModelFactory[Person]):
    __faker__ = Faker(locale="de_DE")
    __allow_none_optionals___ = False
    __set_relationships__ = True
    # __randomize_collection_length__=True
    # __random_seed__ = 10
    addresses = Use(AddressFactory.batch, size=2)


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
    print(person_instance.addresses)
    assert isinstance(person_instance, Person)
    assert isinstance(person_instance.name, str)
    assert isinstance(person_instance.age, (int, type(None)))
    assert isinstance(person_instance.height, float)
    assert isinstance(person_instance.weight, float)


if __name__ == '__main__':
    test_is_person()

