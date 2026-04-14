from app.db.session import engine
from app.models.entities import Base


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables created")
