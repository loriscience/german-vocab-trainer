import csv
import random
from tkinter import *
from tkinter import ttk

class GermanTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("German Vocabulary Trainer")
        self.data = {'Noun': [], 'Verb': [], 'Adjektive': []}
        self.current_word = None
        self.score = 0
        self.total = 0
        self.false_answers = []
        self.false_answers_ids = []
        
        # Load data
        self.load_data()
        
        # Create type selection screen
        self.create_type_selection()

    def load_data(self):
        with open('german.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Type'] in self.data:
                    self.data[row['Type']].append(row)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_type_selection(self):
        self.clear_window()
        Label(self.root, text="Choose word type:", font=('Arial', 14)).pack(pady=10)
        
        for word_type in self.data.keys():
            ttk.Button(self.root, text=word_type, 
                      command=lambda t=word_type: self.start_training(t)).pack(pady=5)

    def start_training(self, word_type):
        self.clear_window()
        self.words = random.sample(self.data[word_type], len(self.data[word_type]))
        self.current_type = word_type
        self.show_next_word()

    def show_next_word(self):
        self.clear_window()
        if not self.words:
            self.show_results()
            return
            
        self.current_word = self.words.pop(0)
        self.total += 1
        
        main_frame = Frame(self.root)
        main_frame.pack(pady=20, padx=20)
        
        Label(main_frame, text=f"Word {self.total}/{len(self.data[self.current_type])}", 
              font=('Arial', 12)).pack()
        
        Label(main_frame, text=f"\nWord: {self.current_word['Word']}", 
              font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.create_question_fields(main_frame)
        
        ttk.Button(main_frame, text="Submit", command=self.check_answer).pack(pady=10)
        ttk.Button(self.root, text="Quit", command=self.create_type_selection).pack()

    def create_question_fields(self, parent):
        self.answer_entries = []
        
        if self.current_type == 'Noun':
            fields = [('Artikel', 'Artikel'), ('Plural', 'Plural')]
        elif self.current_type == 'Verb':
            fields = [('Konjugation', 'Konjugation'), 
                     ('Prateritum', 'Prateritum'), 
                     ('Perfekt', 'Perfekt')]
        else:  # Adjective
            fields = [('Komparativ', 'Komparativ'), 
                     ('Superlativ', 'Superlativ')]
            
        for field, key in fields:
            frame = Frame(parent)
            frame.pack(pady=5, fill=X)
            Label(frame, text=f"{field}:", width=12, anchor='w').pack(side=LEFT)
            entry = ttk.Entry(frame)
            entry.pack(side=LEFT, expand=True, fill=X)
            self.answer_entries.append((key, entry))

    def check_answer(self):
        correct = True
        results = []

        if not self.current_word:
            self.show_feedback("Error: No current word available", "red")
            self.root.after(1500, self.show_next_word)
            return
        
        for key, entry in self.answer_entries:
            user_answer = entry.get().strip()
            correct_answer = self.current_word[key].strip()
            
            # Special handling for adjectives with "keine komparativ"
            if correct_answer.lower() in ['keine komparativ', 'keine superlativ']:
                correct_answer = '-'
                
            if user_answer.lower() != correct_answer.lower():
                correct = False
                results.append(f"{key}: {correct_answer}")

        
        if correct:
            self.score += 1
            self.show_feedback("Correct!", "green")
            print(self.current_word)
        else:
            feedback = "Incorrect. Correct answers:\n" + "\n".join(results)
            self.show_feedback(feedback, "red")
            
            self.false_answers.append(self.current_word['Word'])
            self.false_answers_ids.append(self.current_word['wid'])
            print(self.current_word)
            print(self.false_answers)
        
        self.root.after(1500, self.show_next_word)

    def show_feedback(self, message, color):
        self.clear_window()
        Label(self.root, text=message, fg=color, font=('Arial', 12)).pack(pady=20)
        self.root.update()

    def show_results(self):
        self.clear_window()
        Label(self.root, text="Training Complete!", font=('Arial', 14)).pack(pady=10)
        Label(self.root, text=f"Score: {self.score}/{self.total}", 
              font=('Arial', 12)).pack(pady=10)
        ttk.Button(self.root, text="Start Over", 
                 command=self.create_type_selection).pack(pady=10)

if __name__ == "__main__":
    print("Starting German Vocabulary Trainer...")
    root = Tk()
    print("Initializing GUI...")
    app = GermanTrainer(root)
    root.mainloop()