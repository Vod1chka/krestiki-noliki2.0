import tkinter as tk
from tkinter import font

# Создаем главное окно
window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("400x600")
window.resizable(False, False)

# Настраиваем шрифты
header_font = font.Font(family="Helvetica", size=16, weight="bold")
button_font = font.Font(family="Arial", size=24, weight="bold")
status_font = font.Font(family="Helvetica", size=14)

current_player = "X"
buttons = []

# Счетчики побед для серии из 3 игр
player_x_wins = 0
player_o_wins = 0

# Метка для отображения текущего статуса и счета
status_label = tk.Label(window, text=f"Текущий ход: {current_player}\nСчет: X={player_x_wins} O={player_o_wins}", font=status_font)
status_label.pack(pady=10)

# Создаем отдельный Frame для сетки кнопок
buttons_frame = tk.Frame(window)
buttons_frame.pack()

def check_winner():
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return buttons[i][0]["text"]
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return buttons[0][i]["text"]
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return buttons[0][0]["text"]
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return buttons[0][2]["text"]
    return None

def check_draw():
    for row in buttons:
        for btn in row:
            if btn["text"] == "":
                return False
    return True

def disable_buttons():
    for row in buttons:
        for btn in row:
            btn.config(state="disabled")

def restart_game():
    global current_player
    current_player = "X"
    for row in buttons:
        for btn in row:
            btn.config(text="", state="normal")
    update_status()

def update_status():
    global current_player, player_x_wins, player_o_wins
    status_label.config(text=f"Текущий ход: {current_player}\nСчет: X={player_x_wins} O={player_o_wins}")

def show_result(message):
    result_window = tk.Toplevel()
    result_window.title("Результат")
    result_window.geometry("300x200")
    result_window.resizable(False, False)

    def on_result_close():
        result_window.destroy()
        start_new_series()

    result_window.protocol("WM_DELETE_WINDOW", on_result_close)
    result_label = tk.Label(result_window, text=message, font=("Helvetica", 16))
    result_label.pack(pady=20)

    def play_again():
        result_window.destroy()
        restart_game()

    play_button = tk.Button(result_window, text="Играть снова", font=("Arial", 14), command=play_again)
    play_button.pack(pady=10)

def start_new_series():
    global player_x_wins, player_o_wins
    player_x_wins = 0
    player_o_wins = 0
    restart_game()

def on_click(row, col):
    global current_player, player_x_wins, player_o_wins

    if buttons[row][col]['text'] != "" or all(btn["state"] == "disabled" for row in buttons for btn in row):
        return
    buttons[row][col]['text'] = current_player

    winner = check_winner()
    if winner:
        disable_buttons()
        if winner == "X":
            player_x_wins += 1
        else:
            player_o_wins += 1

        if player_x_wins >= 3:
            show_result("X выиграл серию из 3 игр!")
            start_new_series()
            return
        elif player_o_wins >= 3:
            show_result("O выиграл серию из 3 игр!")
            start_new_series()
            return
        else:
            update_status()
            show_result(f"Победил {winner}!\nСчет: X={player_x_wins} O={player_o_wins}")
        return

    if check_draw():
        disable_buttons()
        show_result("Ничья!")
        update_status()
        return

    current_player = "O" if current_player == "X" else "X"
    update_status()

# Создаем кнопки для сетки игры
for i in range(3):
    row_buttons = []
    for j in range(3):
        btn = tk.Button(
            buttons_frame,
            text="",
            font=button_font,
            width=5,
            height=2,
            bg="#f0f0f0",
            activebackground="#d9d9d9",
            relief="raised",
            bd=4,
            command=lambda r=i, c=j: on_click(r, c)
        )
        btn.grid(row=i, column=j, padx=5, pady=5)
        row_buttons.append(btn)
    buttons.append(row_buttons)

# Кнопка "Сбросить игру"
reset_button = tk.Button(
    window,
    text="Сбросить игру",
    font=("Arial", 14),
    bg="#ff6666",
    fg="white",
    command=lambda: [restart_game(), start_new_series()]
)
reset_button.pack(pady=20)

window.mainloop()