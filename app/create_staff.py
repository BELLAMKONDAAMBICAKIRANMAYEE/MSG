
from getpass import getpass

from sqlalchemy import select

from app.database import SessionLocal
from app.models import User
from app.security import hash_password


def main():
    role = input("Role (admin/trainer): ").strip().lower()

    if role not in {"admin", "trainer"}:
        print("Invalid role. Choose admin or trainer.")
        return

    name = input("Name: ").strip()
    email = input("Email: ").strip().lower()
    password = getpass("Password (minimum 8 characters): ")

    if len(name) < 2 or len(password) < 8:
        print("Name must contain at least 2 characters and password 8.")
        return

    with SessionLocal() as db:
        existing = db.scalar(select(User).where(User.email == email))

        if existing:
            print("This email already exists.")
            return

        user = User(
            name=name,
            email=email,
            hashed_password=hash_password(password),
            role=role,
            is_active=True,
        )

        db.add(user)
        db.commit()

        print(f"{role.title()} account created successfully.")


if __name__ == "__main__":
    main()
