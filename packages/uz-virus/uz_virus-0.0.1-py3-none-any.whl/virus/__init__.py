import tkinter as tk

class Virus:
    def __init__(self):
        self.window = None  # Oyna

    def question(self, question_text):
        """Savolni o'rnatadi"""
        self.question_text = question_text

    def disable_event(self):
        """X tugmasini bosganda oynani yopmaslik"""
        pass

    def block_task_switching(self):
        """Boshqa ilovalarga o'tishni cheklash"""
        self.window.attributes("-fullscreen", True)  # Oynani butun ekran qilish
        self.window.attributes("-topmost", True)  # Oynani doim ustun qilish
        self.window.overrideredirect(True)  # Oynaning barcha tugmalarini (X, -, +) yo'qotish

    def run(self):
        """Oynani ochish"""
        self.window = tk.Tk()
        self.window.title("Warning!")
        self.window.geometry("600x400")  # Katta oyna
        self.window.protocol("WM_DELETE_WINDOW", self.disable_event)  # X tugmasi orqali oyna yopilmasligi uchun
        self.window.resizable(False, False)  # Oynaning hajmini o'zgartirib bo'lmaydi

        self.label = tk.Label(self.window, text=self.question_text, font=("Arial", 20))
        self.label.pack(pady=50)

        self.yes_button = tk.Button(self.window, text='Yes', font=("Arial", 16), command=self.close_window)
        self.yes_button.pack(side="left", padx=50)

        self.no_button = tk.Button(self.window, text='No', font=("Arial", 16), command=self.reopen_window)
        self.no_button.pack(side="right", padx=50)

        self.block_task_switching()  # Boshqa ilovalarga o'tishni bloklash va oynani to'liq ekran qilish

        self.window.mainloop()

    def close_window(self):
        """Yes tugmasi bosilganda dasturni to'xtatish"""
        self.window.overrideredirect(False)  # Oynani normal holatga qaytarish
        self.window.attributes("-fullscreen", False)  # To'liq ekranni o'chirish
        self.window.quit()  # Tkinter siklini to'xtatish va oyna yopilishi uchun

    def reopen_window(self):
        """No tugmasi bosilganda oyna qayta ochiladi"""
        self.window.destroy()  # Oynani yopish
        self.run()  # Yangi oyna qayta ochiladi


# Kutubxona ishlatilishi
if __name__ == '__main__':
    virus = Virus()
    virus.question('Are you gay?')  # Savol
    virus.run()
    