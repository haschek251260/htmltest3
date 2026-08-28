import random
import tkinter as tk
from tkinter import messagebox

# 50 häufige spanische Verben mit klarer Hauptübersetzung
VERBS = [
    {"es": "ser", "de": "sein"},
    {"es": "estar", "de": "sein (befinden)"},
    {"es": "tener", "de": "haben"},
    {"es": "hacer", "de": "machen"},
    {"es": "poder", "de": "können"},
    {"es": "decir", "de": "sagen"},
    {"es": "ir", "de": "gehen"},
    {"es": "ver", "de": "sehen"},
    {"es": "dar", "de": "geben"},
    {"es": "saber", "de": "wissen"},
    {"es": "querer", "de": "wollen"},
    {"es": "llegar", "de": "ankommen"},
    {"es": "pasar", "de": "passieren"},
    {"es": "deber", "de": "müssen"},
    {"es": "poner", "de": "setzen"},
    {"es": "parecer", "de": "scheinen"},
    {"es": "quedar", "de": "bleiben"},
    {"es": "creer", "de": "glauben"},
    {"es": "hablar", "de": "sprechen"},
    {"es": "llevar", "de": "tragen"},
    {"es": "dejar", "de": "lassen"},
    {"es": "seguir", "de": "folgen"},
    {"es": "encontrar", "de": "finden"},
    {"es": "llamar", "de": "rufen"},
    {"es": "venir", "de": "kommen"},
    {"es": "pensar", "de": "denken"},
    {"es": "salir", "de": "verlassen"},
    {"es": "volver", "de": "zurückkehren"},
    {"es": "tomar", "de": "nehmen"},
    {"es": "conocer", "de": "kennen"},
    {"es": "vivir", "de": "leben"},
    {"es": "sentir", "de": "fühlen"},
    {"es": "tratar", "de": "behandeln"},
    {"es": "mirar", "de": "schauen"},
    {"es": "contar", "de": "erzählen"},
    {"es": "empezar", "de": "anfangen"},
    {"es": "esperar", "de": "warten"},
    {"es": "buscar", "de": "suchen"},
    {"es": "existir", "de": "existieren"},
    {"es": "entrar", "de": "eintreten"},
    {"es": "trabajar", "de": "arbeiten"},
    {"es": "escribir", "de": "schreiben"},
    {"es": "perder", "de": "verlieren"},
    {"es": "producir", "de": "produzieren"},
    {"es": "ocurrir", "de": "geschehen"},
    {"es": "entender", "de": "verstehen"},
    {"es": "pedir", "de": "bitten"},
    {"es": "recibir", "de": "erhalten"},
    {"es": "recordar", "de": "erinnern"},
    {"es": "terminar", "de": "beenden"},
]

class VerbQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spanische Verben – Quiz (Deutsch ↔ Spanisch)")
        self.root.geometry("600x420")
        self.root.resizable(False, False)

        # State
        self.direction_es_to_de = True  # True: ES→DE, False: DE→ES
        self.remaining_indices = list(range(len(VERBS)))
        random.shuffle(self.remaining_indices)
        self.current_index = None
        self.correct_answer = None
        self.score = 0
        self.total = 0
        self.answered = False  # prevents double scoring

        # UI
        self.build_ui()
        self.next_question()

    def build_ui(self):
        # Header frame
        header = tk.Frame(self.root, padx=12, pady=8)
        header.pack(fill="x")

        self.direction_btn = tk.Button(
            header,
            text="Richtung: ES → DE",
            command=self.toggle_direction
        )
        self.direction_btn.pack(side="left")

        self.score_label = tk.Label(header, text="Punkte: 0/0")
        self.score_label.pack(side="right")

        # Question frame
        qframe = tk.Frame(self.root, padx=12, pady=12)
        qframe.pack(fill="x")

        self.prompt_label = tk.Label(qframe, text="Frage", font=("Arial", 16))
        self.prompt_label.pack(anchor="w")

        # Options frame
        oframe = tk.Frame(self.root, padx=12, pady=8)
        oframe.pack(fill="x")

        self.choice_var = tk.StringVar(value="")
        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(
                oframe,
                text=f"Option {i+1}",
                variable=self.choice_var,
                value=f"opt{i}",
                anchor="w",
                justify="left",
                font=("Arial", 13)
            )
            rb.pack(fill="x", pady=3)
            self.radio_buttons.append(rb)

        # Feedback frame
        fframe = tk.Frame(self.root, padx=12, pady=8)
        fframe.pack(fill="x")

        self.feedback_label = tk.Label(fframe, text="", fg="#333")
        self.feedback_label.pack(anchor="w")

        # Controls frame
        cframe = tk.Frame(self.root, padx=12, pady=12)
        cframe.pack(fill="x")

        self.check_btn = tk.Button(cframe, text="Antwort prüfen", command=self.check_answer)
        self.check_btn.pack(side="left", padx=6)

        self.next_btn = tk.Button(cframe, text="Nächste Frage", command=self.next_question)
        self.next_btn.pack(side="left", padx=6)

        self.reset_btn = tk.Button(cframe, text="Neu starten", command=self.reset_quiz)
        self.reset_btn.pack(side="right", padx=6)

    def toggle_direction(self):
        self.direction_es_to_de = not self.direction_es_to_de
        self.direction_btn.config(text="Richtung: ES → DE" if self.direction_es_to_de else "Richtung: DE → ES")
        # reset feedback for clarity
        self.feedback_label.config(text="")
        # keep current question but regenerate options for new direction
        self.generate_question(self.current_index)

    def next_question(self):
        self.feedback_label.config(text="")
        self.choice_var.set("")
        self.answered = False

        if not self.remaining_indices:
            messagebox.showinfo("Geschafft", "Alle 50 Verben wurden abgefragt. Du kannst neu starten.")
            return

        self.current_index = self.remaining_indices.pop()
        self.generate_question(self.current_index)

    def reset_quiz(self):
        self.remaining_indices = list(range(len(VERBS)))
        random.shuffle(self.remaining_indices)
        self.score = 0
        self.total = 0
        self.update_score()
        self.next_question()

    def update_score(self):
        self.score_label.config(text=f"Punkte: {self.score}/{self.total}")

    def generate_question(self, idx):
        verb = VERBS[idx]
        source = verb["es"] if self.direction_es_to_de else verb["de"]
        target = verb["de"] if self.direction_es_to_de else verb["es"]
        self.correct_answer = target

        # Prompt text
        if self.direction_es_to_de:
            self.prompt_label.config(text=f"Was bedeutet: „{source}“ (Spanisch → Deutsch)?")
        else:
            self.prompt_label.config(text=f"Wie lautet auf Spanisch: „{source}“ (Deutsch → Spanisch)?")

        # Build options: correct + 3 distractors
        all_targets = [v["de"] if self.direction_es_to_de else v["es"] for v in VERBS]
        distractors = [t for t in all_targets if t != target]
        options = random.sample(distractors, 3) + [target]
        random.shuffle(options)

        # Assign radio buttons
        for i, rb in enumerate(self.radio_buttons):
            rb.config(text=options[i])
            rb.config(value=options[i])

    def check_answer(self):
        if self.answered:
            return  # prevent double counting

        selected = self.choice_var.get()
        if not selected:
            self.feedback_label.config(text="Bitte wähle eine Option aus.")
            return

        self.total += 1
        if selected == self.correct_answer:
            self.score += 1
            self.feedback_label.config(text="Richtig! ✅")
        else:
            direction_hint = "(ES → DE)" if self.direction_es_to_de else "(DE → ES)"
            self.feedback_label.config(
                text=f"Leider falsch. Richtige Antwort: {self.correct_answer} {direction_hint}"
            )
        self.update_score()
        self.answered = True

if __name__ == "__main__":
    root = tk.Tk()
    app = VerbQuizApp(root)
    root.mainloop()
