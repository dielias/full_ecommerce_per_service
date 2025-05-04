# services/orders/app.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from services.orders.database import SessionLocal, engine
from services.orders.models import Base, Order
from pydantic import BaseModel

app = FastAPI()

# Cria as tabelas no banco de dados do serviço de pedidos
Base.metadata.create_all(bind=engine)

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schemas Pydantic
class OrderCreate(BaseModel):
    user_id: int
    product_id: int

class OrderUpdate(BaseModel):
    user_id: int
    product_id: int

@app.post("/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(user_id=order.user_id, product_id=order.product_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders")
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@app.put("/orders/{order_id}")
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    db_order.user_id = order_update.user_id
    db_order.product_id = order_update.product_id
    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    db.delete(db_order)
    db.commit()
    return {"message": "Pedido deletado com sucesso"}

@app.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return db_order
