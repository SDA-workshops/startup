import datetime

from sqlalchemy import (
    Column,
    DECIMAL,
    String,
    Integer,
    Date,
    create_engine,
    ForeignKey,
    Table
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine(
    "mysql+pymysql://root:qwerty@127.0.0.1:33061/startup"
)
Base = declarative_base(bind=engine)


employees_departments = Table(
    "employees_departments",
    Base.metadata,
    Column("pesel", ForeignKey("employees.pesel"), primary_key=True),
    Column("department_id", ForeignKey("departments.id"), primary_key=True),
    Column("date", Date, default=datetime.datetime.now)
)


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    amount = Column(DECIMAL(precision=10, scale=2), nullable=False)

    def __repr__(self) -> str:
        return f"Position({self.id}, {self.name}, {self.amount})"


class Salary(Base):
    __tablename__ = "salaries"

    id = Column(Integer, primary_key=True)
    amount = Column(DECIMAL(precision=10, scale=2), nullable=False)
    pesel = Column(String(20), ForeignKey("employees.pesel"), nullable=False)
    date = Column(Date, nullable=False, default=datetime.datetime.now)

    employee = relationship("Employee", back_populates="salaries")

    def __repr__(self) -> str:
        return f"Salary({self.pesel}, {self.amount}, {self.date})"


class Employee(Base):
    __tablename__ = "employees"

    pesel = Column(String(20), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    birth = Column(Date, nullable=False)
    phone = Column(String(20), nullable=False)
    home_address = Column(String(100), nullable=False)

    salaries = relationship("Salary")
    departments = relationship(
        "Department",
        secondary=employees_departments,
        back_populates="employees"
    )

    def pay(self, amount: float, date: str = None) -> None:
        self.salaries.append(
            Salary(amount=amount, date=date, pesel=self.pesel)
        )

    def __repr__(self) -> str:
        return f"Employee({self.first_name}, {self.last_name})"


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    address = Column(String(50))
    manager_id = Column(Integer, nullable=False)

    employees = relationship(
        "Employee",
        secondary=employees_departments,
        back_populates="departments"
    )

    def __repr__(self) -> str:
        return f"Department({self.name}, {self.manager_id})"


if __name__ == "__main__":
    Base.metadata.create_all()
