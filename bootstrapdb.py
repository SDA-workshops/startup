from random import choice, choices
from string import digits

from faker import Faker
from sqlalchemy.exc import IntegrityError

from models import Employee, Department
from session import Session


def generate_pesel():
    return "".join([choice(digits) for _ in range(11)])


def create_employee():
    faker = Faker()
    return Employee(
        pesel=generate_pesel(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
        home_address=faker.address(),
        phone=faker.phone_number(),
        birth=faker.date_of_birth(minimum_age=18, maximum_age=65)
    )


def create_employees(session: Session, count: int = 20):
    total_employees = 0
    while total_employees < count:
        employee = create_employee()
        session.add(employee)
        try:
            session.commit()
        except IntegrityError:
            print(f"Duplicate appeared {employee} / {total_employees}")
            session.rollback()
        else:
            total_employees += 1
    print(f"Total employees generated {total_employees}")


def pay_salaries(session: Session):
    employees = session.query(Employee).all()
    for employee in employees:
        employee.pay(amount=5000)
    session.commit()


def create_departments(session: Session):
    departments = [
        "HR", "HQ", "Sales", "IT", "Marketing", "Supply",
        "Law", "Reclamation", "Support", "PR"
    ]
    for department in departments:
        session.add(
            Department(
                name=department,
                address="Wiejska 1, Warszawa"
            )
        )
        try:
            session.commit()
        except IntegrityError:
            session.rollback()


def shuffle_employees(session: Session):
    employees = session.query(Employee).all()
    departments = choices(session.query(Department).all(), k=5)
    for department in departments:
        department.employees.extend(
            choices(employees, k=20)
        )
        try:
            session.commit()
        except IntegrityError:
            session.rollback()


if __name__ == "__main__":
    session = Session()

    create_employees(session)
    pay_salaries(session)

    create_departments(session)
    shuffle_employees(session)
