import customtkinter as ctk
import random
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

sentences = [
    "the quick brown fox jumps over the lazy dog",
    "python is a powerful programming language",
    "practice makes a person perfect",
    "coding improves problem solving skills",
    "success comes from consistent hard work"
]

class TypeMasterPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TypeMaster Pro")
        self.geometry("1000x650")
        self.minsize(900, 600)

        self.start_time = 0
        self.running = False
        self.sentence = ""

        self.create_ui()

    def create_ui(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=25)
        self.main_frame.pack(padx=40, pady=40, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="⌨ TypeMaster Pro",
            font=("Arial", 34, "bold")
        )
        self.title_label.pack(pady=25)

        self.sentence_label = ctk.CTkLabel(
            self.main_frame,
            text="Click Start Test to begin",
            font=("Arial", 20),
            wraplength=800
        )
        self.sentence_label.pack(pady=20)

        self.text_box = ctk.CTkTextbox(
            self.main_frame,
            width=800,
            height=150,
            font=("Arial", 18),
            corner_radius=15
        )
        self.text_box.pack(pady=20)
        self.text_box.configure(state="disabled")

        self.stats_frame = ctk.CTkFrame(self.main_frame, corner_radius=20)
        self.stats_frame.pack(pady=15)

        self.time_label = ctk.CTkLabel(
            self.stats_frame,
            text="⏱ Time: 0.00s",
            font=("Arial", 16, "bold"),
            width=180
        )
        self.time_label.grid(row=0, column=0, padx=15, pady=15)

        self.wpm_label = ctk.CTkLabel(
            self.stats_frame,
            text="⚡ WPM: 0",
            font=("Arial", 16, "bold"),
            width=180
        )
        self.wpm_label.grid(row=0, column=1, padx=15, pady=15)

        self.accuracy_label = ctk.CTkLabel(
            self.stats_frame,
            text="🎯 Accuracy: 0%",
            font=("Arial", 16, "bold"),
            width=180
        )
        self.accuracy_label.grid(row=0, column=2, padx=15, pady=15)

        self.mistake_label = ctk.CTkLabel(
            self.stats_frame,
            text="❌ Mistakes: 0",
            font=("Arial", 16, "bold"),
            width=180
        )
        self.mistake_label.grid(row=0, column=3, padx=15, pady=15)

        self.progress = ctk.CTkProgressBar(self.main_frame, width=800)
        self.progress.pack(pady=15)
        self.progress.set(0)

        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="Start Test",
            font=("Arial", 16, "bold"),
            width=160,
            height=45,
            corner_radius=15,
            command=self.start_test
        )
        self.start_button.grid(row=0, column=0, padx=15)

        self.submit_button = ctk.CTkButton(
            self.button_frame,
            text="Submit",
            font=("Arial", 16, "bold"),
            width=160,
            height=45,
            corner_radius=15,
            command=self.submit_test,
            state="disabled"
        )
        self.submit_button.grid(row=0, column=1, padx=15)

        self.reset_button = ctk.CTkButton(
            self.button_frame,
            text="Reset",
            font=("Arial", 16, "bold"),
            width=160,
            height=45,
            corner_radius=15,
            fg_color="#E53935",
            hover_color="#B71C1C",
            command=self.reset_test
        )
        self.reset_button.grid(row=0, column=2, padx=15)

        self.result_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 18, "bold")
        )
        self.result_label.pack(pady=15)

        self.text_box.bind("<KeyRelease>", self.live_update)

    def calculate_accuracy(self, original, typed):
        if len(original) == 0:
            return 0

        correct = 0
        for i in range(min(len(original), len(typed))):
            if original[i] == typed[i]:
                correct += 1

        return (correct / len(original)) * 100

    def count_mistakes(self, original, typed):
        mistakes = 0

        for i in range(min(len(original), len(typed))):
            if original[i] != typed[i]:
                mistakes += 1

        if len(typed) > len(original):
            mistakes += len(typed) - len(original)

        return mistakes

    def start_test(self):
        self.sentence = random.choice(sentences)
        self.sentence_label.configure(text=self.sentence)

        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", "end")
        self.text_box.focus()

        self.start_time = time.time()
        self.running = True

        self.start_button.configure(state="disabled")
        self.submit_button.configure(state="normal")
        self.result_label.configure(text="")

        self.update_timer()

    def update_timer(self):
        if self.running:
            time_taken = time.time() - self.start_time
            self.time_label.configure(text=f"⏱ Time: {time_taken:.2f}s")
            self.after(100, self.update_timer)

    def live_update(self, event=None):
        if not self.running:
            return

        typed = self.text_box.get("1.0", "end").strip()
        time_taken = time.time() - self.start_time

        words = len(typed.split())
        wpm = (words * 60) / time_taken if time_taken > 0 else 0
        accuracy = self.calculate_accuracy(self.sentence, typed)
        mistakes = self.count_mistakes(self.sentence, typed)

        progress_value = min(len(typed) / len(self.sentence), 1)

        self.wpm_label.configure(text=f"⚡ WPM: {wpm:.2f}")
        self.accuracy_label.configure(text=f"🎯 Accuracy: {accuracy:.2f}%")
        self.mistake_label.configure(text=f"❌ Mistakes: {mistakes}")
        self.progress.set(progress_value)

    def submit_test(self):
        self.running = False

        typed = self.text_box.get("1.0", "end").strip()
        time_taken = time.time() - self.start_time

        if typed == "":
            self.result_label.configure(text="Please type something first.")
            self.running = True
            self.update_timer()
            return

        words = len(typed.split())
        wpm = (words * 60) / time_taken
        accuracy = self.calculate_accuracy(self.sentence, typed)
        mistakes = self.count_mistakes(self.sentence, typed)

        self.result_label.configure(
            text=f"Result: {wpm:.2f} WPM | {accuracy:.2f}% Accuracy | {mistakes} Mistakes"
        )

        self.text_box.configure(state="disabled")
        self.submit_button.configure(state="disabled")
        self.start_button.configure(state="normal")

    def reset_test(self):
        self.running = False

        self.sentence = ""
        self.sentence_label.configure(text="Click Start Test to begin")

        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", "end")
        self.text_box.configure(state="disabled")

        self.time_label.configure(text="⏱ Time: 0.00s")
        self.wpm_label.configure(text="⚡ WPM: 0")
        self.accuracy_label.configure(text="🎯 Accuracy: 0%")
        self.mistake_label.configure(text="❌ Mistakes: 0")
        self.progress.set(0)

        self.result_label.configure(text="")
        self.start_button.configure(state="normal")
        self.submit_button.configure(state="disabled")


if __name__ == "__main__":
    app = TypeMasterPro()
    app.mainloop()