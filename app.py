import streamlit as st
import os
from auth import (
    initialize_users,
    register_user,
    login_user
)
from chatbot import ask_groq
from document_reader import read_document
from rag import add_document, search_document
from voice import listen_voice, speak_text
from memory import (
    initialize_database,
    create_chat,
    load_chats,
    load_messages,
    save_message,
    delete_chat,
    rename_chat
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# DATABASE
# ==========================================================

initialize_database()
initialize_users()

# ==========================================================
# UPLOAD FOLDER
# ==========================================================
UPLOAD_FOLDER = "uploads"
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# ==========================================================
# LOGIN SYSTEM
# ==========================================================

if "user_id" not in st.session_state:
    st.title("🤖 AI Assistant Login")

    choice = st.selectbox(
        "Select Option",
        [
            "Login",
            "Register"
        ]
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if choice == "Register":
        if st.button("Create Account"):
            result = register_user(
                username,
                password
            )

            if result:
                st.success(
                    "Account created successfully. Login now."
                )
            else:
                st.error(
                    "Username already exists"
                )

    else:
        if st.button("Login"):
            user = login_user(
                username,
                password
            )

            if user:
                st.session_state.user_id = user
                st.session_state.username = username
                st.success(
                    "Login successful"
                )
                st.rerun()
            else:
                st.error(
                    "Wrong username or password"
                )

    st.stop()

# ==========================================================
# SESSION STATE
# ==========================================================

if "chat_id" not in st.session_state:
    chats = load_chats(
        st.session_state.user_id
    )

    if len(chats) == 0:
        st.session_state.chat_id = create_chat(
            "New Chat",
            st.session_state.user_id
        )
    else:
        st.session_state.chat_id = chats[0]["id"]


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

    rows = load_messages(st.session_state.chat_id)

    for row in rows:
        st.session_state.messages.append(
            {
                "role": row["role"],
                "content": row["content"]
            }
        )

# ==========================================================
# SIDEBAR HEADER
# ==========================================================

with st.sidebar:
    st.title("🤖 AI Assistant")
    
    st.write(
        f"Welcome {st.session_state.username} 👋"
    )
    
    st.markdown("---")
    
    model = st.selectbox(
        "Groq Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ]
    )
    
    st.markdown("---")
    
    st.subheader("💬 Chat History")

    if st.button("➕ New Chat", use_container_width=True):
        chat_id = create_chat(
            "New Chat",
            st.session_state.user_id
        )
        st.session_state.chat_id = chat_id
        st.session_state.messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            }
        ]
        st.rerun()
        
    chats = load_chats(
        st.session_state.user_id
    )

    if len(chats) == 0:
        st.info("No chats available.")

    for chat in chats:
        col1, col2 = st.columns([5, 1])

        # -------------------------
        # Open Chat
        # -------------------------
        with col1:
            if st.button(
                chat["title"],
                key=f"chat_{chat['id']}",
                use_container_width=True
            ):
                st.session_state.chat_id = chat["id"]
                rows = load_messages(chat["id"])
                
                st.session_state.messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant."
                    }
                ]

                for row in rows:
                    st.session_state.messages.append(
                        {
                            "role": row["role"],
                            "content": row["content"]
                        }
                    )

                st.rerun()

        # -------------------------
        # Delete Chat
        # -------------------------
        with col2:
            if st.button(
                "🗑️",
                key=f"delete_{chat['id']}"
            ):
                delete_chat(chat["id"])
                chats = load_chats(
                    st.session_state.user_id
                )

                if len(chats) > 0:
                    st.session_state.chat_id = chats[0]["id"]
                else:
                    st.session_state.chat_id = create_chat(
                        "New Chat",
                        st.session_state.user_id
                    )

                st.session_state.messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant."
                    }
                ]

                st.rerun()

    # ==========================================================
    # DOCUMENT UPLOAD
    # ==========================================================
    st.markdown("---")
    st.subheader("📂 Upload Document")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=[
            "pdf",
            "docx",
            "txt",
            "xlsx"
        ]
    )
    
    if uploaded_file:
        file_path = os.path.join(
            UPLOAD_FOLDER,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Reading document..."):
            document_text = read_document(file_path)

        st.session_state.document = document_text
        
        # Add to vector database
        add_document(
            document_text
        )
        st.session_state.document_loaded = True
        
        st.success("✅ Document loaded")

    st.markdown("---")
    st.write("### 📊 Statistics")
    st.write(f"Chats : {len(load_chats(st.session_state.user_id))}")
    st.write(f"Messages : {len(st.session_state.messages)-1}")    

    # =====================================
    # EXPORT CHAT
    # =====================================
    st.markdown("---")
    if st.button(
        "📄 Export Conversation PDF",
        use_container_width=True
    ):
        from export_pdf import create_pdf
        pdf_file = create_pdf(
            st.session_state.messages
        )
        
        with open(
            pdf_file,
            "rb"
        ) as file:
            st.download_button(
                label="⬇ Download PDF",
                data=file,
                file_name="AI_Conversation.pdf",
                mime="application/pdf"
            )

    # =====================================
    # LOGOUT
    # =====================================
    st.markdown("---")
    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        # Remove login session
        del st.session_state.user_id
        del st.session_state.username

        # Clear chat memory
        if "chat_id" in st.session_state:
            del st.session_state.chat_id

        if "messages" in st.session_state:
            del st.session_state.messages

        st.rerun()

# ==========================================================
# MAIN CHAT WINDOW
# ==========================================================

st.title(f"🤖 Naveen AI Assistant - Welcome {st.session_state.username if 'username' in st.session_state else ''}")
st.caption("Powered by Groq • RAG • Vision • AI Generation")
st.markdown("---")
st.markdown("### Welcome to your AI Assistant")
st.markdown("---")

# ------------------------------------
# Display Previous Messages
# ------------------------------------

for message in st.session_state.messages:
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ------------------------------------
# Chat Input
# ------------------------------------

# ===============================
# Voice Input
# ===============================
if st.button("🎤 Speak"):
    voice_text = listen_voice()
    if voice_text:
        st.session_state.voice_prompt = voice_text
        st.success(
            voice_text
        )

prompt = st.chat_input("Ask anything, upload documents later...")

if prompt or "voice_prompt" in st.session_state:
    
    if "voice_prompt" in st.session_state:
        prompt = st.session_state.voice_prompt
        del st.session_state.voice_prompt

    # Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save User Message in Session
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Save User Message in Database
    save_message(
        st.session_state.chat_id,
        "user",
        prompt
    )

    # Automatically rename new chat
    chats = load_chats(
        st.session_state.user_id
    )
    current_title = None

    for chat in chats:
        if chat["id"] == st.session_state.chat_id:
            current_title = chat["title"]
            break

    if current_title == "New Chat":
        rename_chat(
            st.session_state.chat_id,
            prompt[:30]
        )

    # AI Response
    with st.chat_message("assistant"):
        with st.spinner("🤖 AI is thinking..."):
            
            # =====================================
            # RAG SEARCH
            # =====================================
            messages_for_ai = st.session_state.messages.copy()
            
            if "document_loaded" in st.session_state:
                relevant_chunks = search_document(
                    prompt
                )

                context = "\n\n".join(
                    relevant_chunks
                )

                document_message = {
                    "role": "system",
                    "content": f"""
You are an AI assistant.
Answer the user using the document information below.

DOCUMENT CONTEXT:{context}

If the answer is not available,
say:
'I cannot find this information in the uploaded document.'
"""
                }

                messages_for_ai.insert(
                    1,
                    document_message
                )
            
            # =====================================
            # TEXT RESPONSE
            # =====================================
            response = ask_groq(
                messages_for_ai,
                model
            )
            st.markdown(response)
            
            if st.sidebar.checkbox("🔊 Speak AI Response"):
                speak_text(
                    response
                )

    # Save AI Response in Session
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    # Save AI Response in Database
    save_message(
        st.session_state.chat_id,
        "assistant",
        response
    )

    st.rerun()