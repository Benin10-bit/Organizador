import customtkinter as ctk

ctk.set_appearance_mode("dark")      # "light", "dark", "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

app = ctk.CTk()
app.title("Organize Aí")
app.geometry("500x400")

label = ctk.CTkLabel(app, text="Olá Mundo!", font=("Inter", 20))
label.pack()

button = ctk.CTkButton(app, text="Clique", command=lambda: print("Oi"))
button.pack(pady=10)

frame = ctk.CTkFrame(app)
frame.pack(padx=20, pady=20)

ctk.CTkLabel(frame, text="Dentro do frame").pack()


def run():
    app.mainloop()