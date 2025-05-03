import time
import pytest
from sqlalchemy.orm import Session
from shared.database import SessionLocal
from shared.models import Product

@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_query_execution_time(db: Session):
    start = time.perf_counter()
    products = db.query(Product).all()
    end = time.perf_counter()
    duration = end - start
    print(f"Query execution time: {duration:.6f} seconds")
    assert duration < 0.5  # exemplo: queremos que rode em menos de 500ms
