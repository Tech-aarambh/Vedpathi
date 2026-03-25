from app.database.db import engine, Base

# 👇 IMPORTANT: import models so SQLAlchemy knows them
from app.models.user import User

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Done!")

