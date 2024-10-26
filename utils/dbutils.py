from typing import Any

def init_db(db:Any)->None:
    from entity.user import User
    db.metadata.create_all(bind=db.engine)
    
    print("Init Database:")
    print(db)
    db.session.add(
        User(
            username = "thuannv10",
            password = "937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244",
            role = "user"
        )
    )
    db.session.add(
        User(
            username = "administrator",
            password = "617ae1b5dd6fecfc587eb83fba6302109c0c036160da116c191d32b1a7dd336c",
            role = "admin"
        )
    )
    db.session.add(
        User(
            username = "thuan",
            password = "937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244",
            role = "admin"
        )
    )
    db.session.commit()
    return None

def drop_db(db:Any)->None:
    print("Drop Database:")
    print(db)
    try:
        db.metadata.drop_all(bind=db.engine)
    except Exception as e:
        print(f"Error dropping tables: {e}")