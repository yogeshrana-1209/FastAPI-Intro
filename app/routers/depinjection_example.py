from fastapi import APIRouter, Depends, HTTPException
router = APIRouter()

@router.get("/user/")
async def user(id: str, name: str, age: int):
   return {"id": id, "name": name, "age": age}

@router.get("/admin/")
async def admin(id: str, name: str, age: int):
   return {"id": id, "name": name, "age": age}

async def dependency(id: str, name: str, age: int):
   return {"id": id, "name": name, "age": age}

@router.get("/user/")
async def user(dep: dict = Depends(dependency)):
   return dep

#Validate Query params using Dependency Injection
async def validate(dep: dependency = Depends(dependency)):
   if dep["age"] > 18:
      raise HTTPException(status_code=400, detail="You are not eligible")

@router.get("/useragecheck/", dependencies=[Depends(validate)])
async def user():
   return {"message": "You are eligible"}