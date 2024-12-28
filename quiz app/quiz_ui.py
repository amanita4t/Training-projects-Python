import json
import random
from copy import deepcopy
from tkinter import Tk, Label, Button, StringVar, Radiobutton, Canvas

# Load questions from the JSON file
def read_data():
    with open("question.json", "r") as file:
        data = json.load(file)
    return data

# Quiz Application Class
class QuizApp:
    def __init__(self, master, data):
        self.master = master
        self.master.title("Quiz App")
        self.master.geometry("500x400")
        self.master.configure(bg="#2c3e50")  # Dark blue background
        self.data = deepcopy(data)  # Use deepcopy to avoid altering original data
        self.current_question = 0
        self.score = 0
        self.selected_answer = StringVar()
        self.timer_id = None
        self.time_left = 10

        # GUI Elements
        self.question_label = Label(
            master, text="", wraplength=400, justify="center", font=("Arial", 16, "bold"), bg="#2c3e50", fg="#ecf0f1"
        )
        self.question_label.pack(pady=20)

        self.options = []
        for i in range(4):  # Create 4 radio buttons for choices
            btn = Radiobutton(
                master, text="", variable=self.selected_answer, value="", font=("Arial", 14),
                bg="#503E2C", fg="#ecf0f1", indicatoron=0, width=25, padx=10, pady=5, relief="ridge", selectcolor="#6D543C"
            )
            btn.pack(anchor="center", pady=5)
            self.options.append(btn)

        self.submit_button = Button(master, text="Next", command=self.next_with_click, font=("Arial", 14), bg="#3498db", fg="white", relief="ridge")
        self.submit_button.pack(pady=20)

        self.feedback_label = Label(master, text="", font=("Arial", 14), bg="#2c3e50", fg="#e67e22")  # Feedback for answers
        self.feedback_label.pack()

        self.timer_canvas = Canvas(master, width=400, height=20, bg="#ecf0f1", highlightthickness=0)
        self.timer_canvas.pack(pady=10)

        # Display the first question
        self.display_question()

    def display_question(self):
        # Get the current question data
        question_data = self.data[self.current_question]

        # Update question text
        self.question_label.config(text=f"Question {question_data['id']}: {question_data['question']}")

        # Update options
        for i, choice in enumerate(question_data["choices"]):
            self.options[i].config(text=choice, value=choice)

        # Reset the selected answer and feedback label
        self.selected_answer.set("")
        self.feedback_label.config(text="")

        # Change the button text for the last question
        if self.current_question == len(self.data) - 1:
            self.submit_button.config(text="Submit", bg="#e74c3c")
        else:
            self.submit_button.config(text="Next", bg="#3498db")

        # Start the timer
        self.start_timer()

    def start_timer(self):
        self.time_left = 10
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            # Update the loading bar
            self.timer_canvas.delete("all")
            bar_width = (400 / 10) * (10 - self.time_left)
            self.timer_canvas.create_rectangle(0, 0, bar_width, 20, fill="#2ecc71", outline="")

            self.time_left -= 1
            self.timer_id = self.master.after(1000, self.update_timer)
        else:
            self.timer_canvas.delete("all")
            if not self.selected_answer.get():
                self.next_question()
            elif self.selected_answer.get():
                self.next_question()

    def stop_timer(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

    def check_answer(self):
        # Stop the timer
        self.stop_timer()

        # Get the current question data
        question_data = self.data[self.current_question]
        selected = self.selected_answer.get()

        # Check if the answer is correct
        if selected == str(question_data["answer"]) or selected.lower() == str(question_data["answer"]).lower():
            self.score += 1
            self.feedback_label.config(text="Correct!", fg="#2ecc71")
        else:
            self.feedback_label.config(
                text=f"Incorrect! The correct answer is: {question_data['answer']}", fg="#e74c3c"
            )

        # Pause for 2 seconds to display feedback before moving to the next question
        self.master.after(2000, self.next_question)

    def next_with_click(self):
        # Handle the "Next" button explicitly
        if self.timer_id:
            self.stop_timer()
        self.check_answer()

    def next_question(self):
        # Move to the next question or finish the quiz
        self.stop_timer()
        self.current_question += 1
        if self.current_question < len(self.data):
            self.display_question()
        else:
            self.show_score()

    def show_score(self):
        # Clear the screen and show the final score
        self.question_label.pack_forget()
        for option in self.options:
            option.pack_forget()
        self.submit_button.pack_forget()
        self.feedback_label.pack_forget()
        self.timer_canvas.pack_forget()

        Label(
            self.master,
            text=f"You scored {self.score} out of {len(self.data)}!",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
        ).pack(pady=20)

        Button(self.master, text="Close", command=self.master.destroy, font=("Arial", 14), bg="#e74c3c", fg="white").pack(pady=10)

# Run the Quiz App using main function
def main():
    data = read_data()
    root = Tk()
    app = QuizApp(root, data)
    root.mainloop()

main()
