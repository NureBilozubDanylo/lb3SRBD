from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.exc import NoResultFound
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from passlib.hash import bcrypt
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy import text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "url"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)  # связь с родительской категорией

    subcategories = relationship("Category", backref='parent', remote_side=[id])
    

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    image_url = Column(String, nullable=True)
    
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    category = relationship("Category", backref='products')

Base.metadata.create_all(engine)

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    username:  str
    access_token: str
    token_type: str = "bearer"

class Settings(BaseModel):
    authjwt_secret_key: str = "korm"

@AuthJWT.load_config
def get_config():
    return Settings()

@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, Authorize: AuthJWT = Depends()):
    try:
        user = session.query(User).filter_by(username=request.username).one()
        
        if not bcrypt.verify(request.password, user.password):
            raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")

        if not bcrypt.verify(request.password, user.password):
            raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")
        
        access_token = Authorize.create_access_token(subject=user.username)
        return LoginResponse(username=user.username,access_token=access_token)

    except NoResultFound:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    


class RegisterRequest(BaseModel):
    username: str
    password: str

class RegisterResponse(BaseModel):
    message: str

@app.post("/register", response_model=LoginResponse)
def register(request: RegisterRequest, Authorize: AuthJWT = Depends()):
    if session.query(User).filter_by(username=request.username).first():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    hashed_password = bcrypt.hash(request.password)
    new_user = User(username=request.username, password=hashed_password)
    session.add(new_user)
    session.commit()
    access_token = Authorize.create_access_token(subject=request.username)
    return LoginResponse(username=request.username,access_token=access_token)

@app.get("/categories/{category_id}/products")
def get_products_by_category(category_id: int):
    category = session.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    all_categories = [category] + get_all_subcategories(category.id, session)

    category_ids = [cat.id for cat in all_categories]

    products = session.query(Product).filter(Product.category_id.in_(category_ids)).all()

    return products

def get_all_subcategories(category_id, db):
    """ Рекурсивная функция для получения всех дочерних категорий """
    subcategories = []
    
    # Запрашиваем подкатегории для данной категории
    child_categories = db.query(Category).filter(Category.parent_id == category_id).all()
    
    for subcategory in child_categories:
        subcategories.append(subcategory)
        # Рекурсивно добавляем подкатегории
        subcategories += get_all_subcategories(subcategory.id, db)
    
    return subcategories

@app.get("/categories/{parent_id}")
def get_subcategories(parent_id: int):
    # Получение всех категорий, у которых parent_id равен переданному значению
    subcategories = session.query(Category).filter(Category.parent_id == parent_id).all()

    # Если категории не найдены, возвращаем ошибку
    if not subcategories:
        raise HTTPException(status_code=404, detail="No subcategories found")

    return subcategories

@app.get("/allCategories")
def get_all_categories():
    categories = session.query(Category).all()

    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")

    return categories

class AddRequest(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    image_url: str
    category_id: int

class RegisterResponse(BaseModel):
    message: str

@app.post("/add")
def add_new_product(request: AddRequest):
    try:
        session.execute(
            text("""
                CALL add_product(
                    :name,
                    :description,
                    :price,
                    :category_id,
                    :stock_quantity,
                    :image_url
                )
            """),
            {
                "name": request.name,
                "description": request.description,
                "price": request.price,
                "category_id": request.category_id,
                "stock_quantity": request.stock_quantity,
                "image_url": request.image_url
            }
        )
        session.commit()
        
        return {"message": "Product added successfully"}
    
    except Exception as e:
        session.rollback()
        if "Product with name" in str(e):
            raise HTTPException(status_code=400, detail="Name nust be unique")
        else:
            raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.get("/category-totals")
def get_category_totals():
    result = session.execute(text("SELECT * FROM get_category_totals2()")).fetchall()

    category_totals = [
        {
            "category_id": row[0],
            "category_name": row[1],
            "total_value": row[2]   
        }
        for row in result
    ]

    return category_totals

class CountRequest(BaseModel):
    category_id: int

@app.post("/product-count")
def get_product_count(request: CountRequest):
        result = session.execute(
            text("SELECT count_products_in_category1(:category_id) AS product_count"),
            {"category_id": request.category_id}
        ).fetchone()
        
        product_count = result[0] if result else 0 

        return {"category_id": request.category_id, "product_count": product_count}

