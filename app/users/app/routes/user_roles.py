from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.users.app.models.models import User, UserRole, Role
from app.database import get_db

router = APIRouter()

# Endpoint para asignar un rol a un usuario
@router.post("/users/{user_id}/assign-role/{role_id}")
async def assign_role_to_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.add(user_role)
    db.commit()
    return {"message": "Rol asignado exitosamente"}

# Endpoint para eliminar un rol de un usuario
@router.delete("/users/{user_id}/remove-role/{role_id}")
async def remove_role_from_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.user_id == user_id, UserRole.role_id == role_id).first()
    if not user_role:
        raise HTTPException(status_code=404, detail="Rol no asignado al usuario")

    db.delete(user_role)
    db.commit()
    return {"message": "Rol eliminado del usuario"}
