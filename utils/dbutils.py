from typing import Any
import json
from sqlalchemy import text


def init_db(db: Any) -> None:
    from entity.user import User
    db.metadata.create_all(bind=db.engine)

    print("Init Database:")
    print(db)
    db.session.add(
        User(
            username="thuannv10",
            password="937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244",
            role="user"
        )
    )
    db.session.add(
        User(
            username="administrator",
            password="617ae1b5dd6fecfc587eb83fba6302109c0c036160da116c191d32b1a7dd336c",
            role="admin"
        )
    )
    db.session.add(
        User(
            username="thuan",
            password="937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244",
            role="admin"
        )
    )
    db.session.commit()
    return None


def drop_db(db: Any) -> None:
    print("Drop Database:")
    print(db)
    try:
        db.metadata.drop_all(bind=db.engine)
    except Exception as e:
        print(f"Error dropping tables: {e}")


def initdb_word_toeic(db: Any) -> None:
    from entity.word_toeic import WordToeic
    print("Init table word toeic:")
    print(db)
    list_word = []
    try:
        with open("data_word.json", 'r', encoding='utf-8') as file:
            list_words = json.load(file)["data"]
        words_to_add = []
        for word in list_words:
            words_to_add.append(
                WordToeic(
                    word=word[0],
                    transliteration=word[1],
                    mean1=word[2],
                    mean2=word[3],
                    mean3=word[4],
                    mean4=word[5],
                    mean5=word[6],
                )
            )
        db.session.add_all(words_to_add)
        db.session.commit()
    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
    except json.JSONDecodeError:
        print("Error decoding JSON. Please check if the file contains valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


def remove_table_word_toeic(db: Any) -> None:
    print("Drop table toeic:")
    print(db)
    db.session.execute(text("drop table word_toeic"))
    db.session.commit()
    return None
