from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from pydantic import BaseModel, constr, confloat
from typing import List, Optional

#$ uvicorn main:app --reload -через это запускается программа


SQLALCHEMY_DATABASE_URL = "sqlite:///./stores.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Модели
class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    products = relationship("Product", back_populates="store", cascade="all, delete")
    __table_args__ = (UniqueConstraint('name', 'address', name='_store_name_address_uc'),)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    store = relationship("Store", back_populates="products")

Base.metadata.create_all(bind=engine)

#схемы
class StoreBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    address: constr(strip_whitespace=True, min_length=1)

class StoreCreate(StoreBase):
    pass

class StoreResponse(StoreBase):
    id: int

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    price: confloat(gt=0)
    store_id: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True

# фастапи
app = FastAPI()

# здесь сессии для БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#эндпоинты для магазинов
@app.get("/stores", response_model=List[StoreResponse])
def get_stores(db: Session = Depends(get_db)):
    return db.query(Store).all()

@app.post("/stores", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
def create_store(store: StoreCreate, db: Session = Depends(get_db)):
    db_store = Store(**store.dict())
    try:
        db.add(db_store)
        db.commit()
        db.refresh(db_store)
        return db_store
    except:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="магазин с таким именем и адресом уже существует"
        )

@app.get("/stores/{store_id}/products", response_model=List[ProductResponse])
def get_store_products(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Магазин не найден"
        )
    return store.products

@app.put("/stores/{store_id}", response_model=StoreResponse)
def update_store(store_id: int, store: StoreCreate, db: Session = Depends(get_db)):
    db_store = db.query(Store).filter(Store.id == store_id).first()
    if not db_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Магазин не найден"
        )
    try:
        db_store.name = store.name
        db_store.address = store.address
        db.commit()
        db.refresh(db_store)
        return db_store
    except:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="магазин с таким именем и адресом уже существует"
        )

#Эндпоинты для товаров
@app.get("/products", response_model=List[ProductResponse])
def get_products(store_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Product)
    if store_id is not None:
        query = query.filter(Product.store_id == store_id)
    return query.all()

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == product.store_id).first()
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="магазин не найден"
        )
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="товар не найден"
        )
    db.delete(product)
    db.commit()
