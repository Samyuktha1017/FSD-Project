from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas, crud
import csv, io

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Magnus CRUD Demo", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/employees", response_model=schemas.EmployeeOut, status_code=201)
def create_employee(emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    exists = crud.get_employee_by_email(db, emp.email)
    if exists:
        raise HTTPException(status_code=409, detail="Email already exists")
    return crud.create_employee(db, emp)

@app.get("/api/employees/{employee_id}", response_model=schemas.EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Not found")
    return emp

@app.get("/api/employees", response_model=schemas.PaginatedEmployees)
def list_employees(page: int = 1, page_size: int = 10, q: str | None = None,
                   department: str | None = None, status: str | None = None, sort: str | None = None,
                   db: Session = Depends(get_db)):
    items, total = crud.list_employees(db, page, page_size, q, department, status, sort)
    return {"items": items, "total": total, "page": page, "page_size": page_size}

@app.patch("/api/employees/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee(employee_id: int, updates: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    emp = crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Not found")
    # prevent email conflicts
    if updates.email and crud.get_employee_by_email(db, updates.email) and updates.email != emp.email:
        raise HTTPException(status_code=409, detail="Email already exists")
    return crud.update_employee(db, emp, updates)

@app.delete("/api/employees/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Not found")
    crud.delete_employee(db, emp)
    return Response(status_code=204)

@app.post("/api/employees/bulk-delete")
def bulk_delete(ids: list[int] = Query(...), db: Session = Depends(get_db)):
    deleted = crud.bulk_delete(db, ids)
    return {"deleted": deleted}

@app.post("/api/employees/import")
async def import_employees(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    text = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    inserted = 0
    for row in reader:
        try:
            emp = schemas.EmployeeCreate(
                name=row.get("name") or row.get("Name"),
                email=row.get("email") or row.get("Email"),
                phone=row.get("phone") or row.get("Phone"),
                department=row.get("department") or row.get("Department"),
                status=row.get("status") or row.get("Status"),
            )
            if not crud.get_employee_by_email(db, emp.email):
                crud.create_employee(db, emp)
                inserted += 1
        except Exception:
            continue
    return {"inserted": inserted}

@app.get("/api/employees/export")
def export_employees(db: Session = Depends(get_db)):
    items, _ = crud.list_employees(db, page=1, page_size=10_000)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "email", "phone", "department", "status"])
    for e in items:
        writer.writerow([e.id, e.name, e.email, e.phone, e.department, e.status])
    return Response(content=output.getvalue(), media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=employees.csv"})
