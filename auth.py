import sqlite3
import bcrypt


DATABASE = "database/memory.db"



# ===============================
# Create User Table
# ===============================

def initialize_users():

    conn = sqlite3.connect(
        DATABASE
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,

            password TEXT

        )
        """
    )


    conn.commit()

    conn.close()



# ===============================
# Register User
# ===============================

def register_user(
    username,
    password
):

    conn = sqlite3.connect(
        DATABASE
    )

    cursor = conn.cursor()


    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )


    try:

        cursor.execute(
            """
            INSERT INTO users
            (username,password)

            VALUES (?,?)
            """,

            (
                username,
                hashed_password
            )
        )


        conn.commit()

        return True


    except:

        return False


    finally:

        conn.close()



# ===============================
# Login User
# ===============================

def login_user(
    username,
    password
):

    conn = sqlite3.connect(
        DATABASE
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT id,password
        FROM users
        WHERE username=?
        """,

        (username,)
    )


    user = cursor.fetchone()


    conn.close()


    if user:

        user_id = user[0]

        saved_password = user[1]


        if bcrypt.checkpw(
            password.encode(),
            saved_password
        ):

            return user_id


    return None