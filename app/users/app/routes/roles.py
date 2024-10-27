from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.users.app.models.models import Role
from app.users.app.schemas.role import RoleCreate, RoleUpdate
from app.database import get_db

router = APIRouter()

# Endpoint para crear un nuevo rol
@router.post("/roles/create", response_model=RoleCreate)
async def create_role(role_data: RoleCreate, db: Session = Depends(get_db)):
    existing_role = db.query(Role).filter(Role.name == role_data.name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="El rol ya existe")
    
    new_role = Role(name=role_data.name, description=role_data.description)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

# Endpoint para actualizar un rol
@router.put("/roles/update/{role_id}", response_model=RoleUpdate)
async def update_role(role_id: int, role_data: RoleUpdate, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    if role_data.name:
        role.name = role_data.name
    if role_data.description:
        role.description = role_data.description

    db.commit()
    db.refresh(role)
    return role

# Endpoint para eliminar un rol
@router.delete("/roles/delete/{role_id}")
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    db.delete(role)
    db.commit()
    return {"message": "Rol eliminado exitosamente"}
