import sqlite3


DATABASE = "database/memory.db"


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    conn = sqlite3.connect(
        DATABASE
    )

    conn.row_factory = sqlite3.Row

    return conn



# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()


    # --------------------------
    # Users table
    # --------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,

            password TEXT

        )
        """
    )


    # --------------------------
    # Chats table
    # --------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chats(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            title TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )


    # --------------------------
    # Messages table
    # --------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            chat_id INTEGER,

            role TEXT,

            content TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )


    conn.commit()

    conn.close()



# ==========================================================
# CREATE CHAT
# ==========================================================

def create_chat(title, user_id):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO chats
        (
            user_id,
            title
        )

        VALUES
        (
            ?,
            ?
        )
        """,

        (
            user_id,
            title
        )
    )


    conn.commit()


    chat_id = cursor.lastrowid


    conn.close()


    return chat_id



# ==========================================================
# LOAD USER CHATS
# ==========================================================

def load_chats(user_id):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM chats

        WHERE user_id=?

        ORDER BY id DESC
        """,

        (
            user_id,
        )
    )


    chats = cursor.fetchall()


    conn.close()


    return chats



# ==========================================================
# SAVE MESSAGE
# ==========================================================

def save_message(
        chat_id,
        role,
        content
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO messages
        (
            chat_id,
            role,
            content
        )

        VALUES
        (
            ?,
            ?,
            ?
        )
        """,

        (
            chat_id,
            role,
            content
        )
    )


    conn.commit()

    conn.close()



# ==========================================================
# LOAD CHAT MESSAGES
# ==========================================================

def load_messages(chat_id):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *

        FROM messages

        WHERE chat_id=?

        ORDER BY id ASC
        """,

        (
            chat_id,
        )
    )


    messages = cursor.fetchall()


    conn.close()


    return messages



# ==========================================================
# DELETE CHAT
# ==========================================================

def delete_chat(chat_id):

    conn = get_connection()

    cursor = conn.cursor()


    # Delete messages

    cursor.execute(
        """
        DELETE FROM messages

        WHERE chat_id=?
        """,

        (
            chat_id,
        )
    )


    # Delete chat

    cursor.execute(
        """
        DELETE FROM chats

        WHERE id=?
        """,

        (
            chat_id,
        )
    )


    conn.commit()

    conn.close()



# ==========================================================
# RENAME CHAT
# ==========================================================

def rename_chat(
        chat_id,
        new_title
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE chats

        SET title=?

        WHERE id=?
        """,

        (
            new_title,
            chat_id
        )
    )


    conn.commit()

    conn.close()