import streamlit as st
import random

# ==============================
# SETUP
# ==============================
st.set_page_config(page_title="Tic Tac Toe AI", layout="centered")

# ==============================
# SESSION STATE
# ==============================
if "board" not in st.session_state:
    st.session_state.board = [" "] * 9
    st.session_state.turn = "X"
    st.session_state.game_over = False
    st.session_state.message = ""

board = st.session_state.board


# ==============================
# CEK PEMENANG
# ==============================
def winner(p):
    win = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in win:
        if board[a]==board[b]==board[c]==p:
            return True
    return False


def full():
    return " " not in board


# ==============================
# MINIMAX
# ==============================
def minimax(is_ai):

    if winner("O"):
        return 1
    if winner("X"):
        return -1
    if full():
        return 0

    if is_ai:
        best = -100
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(False)
                board[i] = " "
                best = max(best, score)
        return best

    else:
        best = 100
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(True)
                board[i] = " "
                best = min(best, score)
        return best


# ==============================
# AI MOVE
# ==============================
def ai_move():
    best_score = -100
    move = 0

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i

    return move


# ==============================
# RESET
# ==============================
def reset():
    st.session_state.board = [" "] * 9
    st.session_state.turn = "X"
    st.session_state.game_over = False
    st.session_state.message = ""


# ==============================
# UI
# ==============================
st.title("🎮 Tic Tac Toe AI")
st.write("Kamu = ❌ | AI = ⭕")

st.write("---")

# GRID
for i in range(3):
    cols = st.columns(3)

    for j in range(3):
        idx = i*3 + j

        if cols[j].button(
            board[idx] if board[idx] != " " else " ",
            key=idx,
            use_container_width=True
        ):

            if board[idx] == " " and not st.session_state.game_over:

                board[idx] = "X"

                if winner("X"):
                    st.session_state.game_over = True
                    st.session_state.message = "🎉 Kamu MENANG!"
                    st.rerun()

                if full():
                    st.session_state.game_over = True
                    st.session_state.message = "🤝 SERI!"
                    st.rerun()

                # AI TURN
                ai = ai_move()
                board[ai] = "O"

                alasan = [
                    "karena langkah ini membuka peluang menang.",
                    "untuk mencegah kekalahanmu.",
                    "karena ini langkah terbaik.",
                    "karena posisi ini menguntungkan.",
                    "karena analisis minimax."
                ]

                st.info(f"🤖 AI memilih kotak {ai+1} {random.choice(alasan)}")

                if winner("O"):
                    st.session_state.game_over = True
                    st.session_state.message = "🤖 AI MENANG!"
                    st.rerun()

                if full():
                    st.session_state.game_over = True
                    st.session_state.message = "🤝 SERI!"
                    st.rerun()


# ==============================
# STATUS
# ==============================
if st.session_state.message:
    st.success(st.session_state
