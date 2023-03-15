from models import (
    Position,
    Salary,
    Employee,
    Department,
    engine,
)
from session import Session


def create_sample_positions(session: Session) -> None:
    session.add_all([
        Position(name="Payroll", amount=6000),
        Position(name="HR", amount=6500),
        Position(name="CTO", amount=8000),
        Position(name="CEO", amount=10000)
    ])
    session.commit()


def pay_to_employee(
    session: Session,
    pesel: str,
    amount: float
) -> None:
    employee = session.query(Employee).get(pesel)
    employee.salaries.append(
        Salary(amount=amount, pesel=pesel)
    )
    session.commit()


if __name__ == "__main__":
    session = Session(bind=engine)

    departments = session.query(Department).all()
    for department in departments:
        print(department, department.employees)

    print(10 * "=")

    employees = session.query(Employee).all()
    for employee in employees:
        print(employee, employee.departments)
