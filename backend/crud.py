from sqlalchemy.orm import Session
from sqlalchemy import select, or_, desc, asc
import models, schemas

def get_employee(db: Session, employee_id: int):
    return db.get(models.Employee, employee_id)

def get_employee_by_email(db: Session, email: str):
    return db.execute(select(models.Employee).where(models.Employee.email == email)).scalar_one_or_none()

def list_employees(db: Session, page: int = 1, page_size: int = 10, q: str | None = None,
                   department: str | None = None, status: str | None = None,
                   sort: str | None = None):
    stmt = select(models.Employee)
    if q:
        like = f"%{q.lower()}%"
        stmt = stmt.where(or_(models.Employee.name.ilike(like),
                              models.Employee.email.ilike(like),
                              models.Employee.phone.ilike(like)))
    if department:
        stmt = stmt.where(models.Employee.department == department)
    if status:
        stmt = stmt.where(models.Employee.status == status)

    if sort:
        direction = asc
        field = sort
        if sort.startswith("-"):
            direction = desc
            field = sort[1:]
        if hasattr(models.Employee, field):
            stmt = stmt.order_by(direction(getattr(models.Employee, field)))
    else:
        stmt = stmt.order_by(desc(models.Employee.id))

    total = db.execute(stmt).scalars().all()
    count = len(total)
    start = (page - 1) * page_size
    end = start + page_size
    items = total[start:end]
    return items, count

def create_employee(db: Session, data: schemas.EmployeeCreate):
    emp = models.Employee(**data.model_dump())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

def update_employee(db: Session, db_emp: models.Employee, updates: schemas.EmployeeUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_emp, field, value)
    db.commit()
    db.refresh(db_emp)
    return db_emp

def delete_employee(db: Session, db_emp: models.Employee):
    db.delete(db_emp)
    db.commit()

def bulk_delete(db: Session, ids: list[int]):
    rows = db.query(models.Employee).filter(models.Employee.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    return rows
