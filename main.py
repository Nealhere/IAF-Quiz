
import sys, json, random, os
from PyQt5 import QtWidgets, QtGui, QtCore

APP_TITLE = "Indian Air Force — Quiz"

class QuizWindow(QtWidgets.QWidget):
    def __init__(self, questions_file="questions.json"):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100,100,1100,700)
        self.questions = self.load_questions(questions_file)
        if not self.questions:
            QtWidgets.QMessageBox.critical(None, "No questions", "questions.json is empty or invalid.")
            sys.exit(1)
        random.shuffle(self.questions)
        self.q_index = 0
        self.score = 0
        self.time_per_q = 180  # seconds per question
        self.remaining = self.time_per_q

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.build_ui()
        self.load_question()
        self.timer.start(1000)

    def load_questions(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            # validate minimally
            if not isinstance(data, list):
                return []
            return data
        except Exception as e:
            return []

    def build_ui(self):
        layout = QtWidgets.QVBoxLayout()
        header = QtWidgets.QHBoxLayout()
        self.title_label = QtWidgets.QLabel("<h1>Indian Air Force — Quiz</h1>")
        header.addWidget(self.title_label)
        header.addStretch()

        self.timer_label = QtWidgets.QLabel("Time: 00:00")
        self.timer_label.setStyleSheet("font-weight:bold; font-size:16px; padding-right:20px;")
        header.addWidget(self.timer_label)

        self.score_label = QtWidgets.QLabel("Score: 0")
        self.score_label.setStyleSheet("font-weight:bold; font-size:16px; padding-left:20px;")
        header.addWidget(self.score_label)

        layout.addLayout(header)

        self.question_box = QtWidgets.QGroupBox()
        q_layout = QtWidgets.QVBoxLayout()

        self.question_label = QtWidgets.QLabel("Question appears here", alignment=QtCore.Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size:20px;")
        q_layout.addWidget(self.question_label)

        self.options_layout = QtWidgets.QGridLayout()
        self.option_buttons = []
        for i in range(4):
            btn = QtWidgets.QPushButton("Option {}".format(i+1))
            btn.setFixedHeight(80)
            font = btn.font()
            font.setPointSize(14)
            btn.setFont(font)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            btn.clicked.connect(self.make_choice(i))
            self.option_buttons.append(btn)
            r = i//2; c = i%2
            self.options_layout.addWidget(btn, r, c)
        q_layout.addLayout(self.options_layout)

        self.question_box.setLayout(q_layout)
        layout.addWidget(self.question_box, stretch=1)

        footer = QtWidgets.QHBoxLayout()
        self.feedback_label = QtWidgets.QLabel("")
        footer.addWidget(self.feedback_label)
        footer.addStretch()
        self.prev_btn = QtWidgets.QPushButton("Previous")
        self.prev_btn.clicked.connect(self.prev_question)
        footer.addWidget(self.prev_btn)
        self.next_btn = QtWidgets.QPushButton("Next")
        self.next_btn.clicked.connect(self.next_question)
        footer.addWidget(self.next_btn)
        layout.addLayout(footer)

        self.setLayout(layout)

    def make_choice(self, i):
        def handler():
            self.check_answer(i)
        return handler

    def load_question(self):
        if self.q_index < 0:
            self.q_index = 0
        if self.q_index >= len(self.questions):
            self.end_quiz()
            return
        q = self.questions[self.q_index]
        self.question_label.setText(f"<b>{self.q_index+1}. {q.get('question')}</b>")
        opts = q.get('options', [])
        for i,btn in enumerate(self.option_buttons):
            text = opts[i] if i < len(opts) else ''
            btn.setText(text)
            btn.setEnabled(True)
            btn.setStyleSheet('')
        self.correct_index = q.get('answer', 0)
        self.feedback_label.setText('')
        self.remaining = self.time_per_q
        self.update_timer_label()

    def check_answer(self, idx):
        for b in self.option_buttons:
            b.setEnabled(False)
        if idx == self.correct_index:
            self.score += 100
            self.feedback_label.setText('<span style="color:green; font-weight:bold">Correct ✅ (+100)</span>')
            self.option_buttons[idx].setStyleSheet('background-color: lightgreen;')
        else:
            correct_text = self.option_buttons[self.correct_index].text() if 0 <= self.correct_index < len(self.option_buttons) else 'N/A'
            self.feedback_label.setText(f'<span style="color:red; font-weight:bold">Wrong ❌ — Correct: {correct_text}</span>')
            self.option_buttons[idx].setStyleSheet('background-color: salmon;')
            if 0 <= self.correct_index < len(self.option_buttons):
                self.option_buttons[self.correct_index].setStyleSheet('background-color: lightgreen;')
        self.score_label.setText(f"Score: {self.score}")

    def prev_question(self):
        if self.q_index > 0:
            self.q_index -= 1
            self.load_question()

    def next_question(self):
        self.q_index += 1
        if self.q_index < len(self.questions):
            self.load_question()
        else:
            self.end_quiz()

    def update_timer(self):
        if self.remaining > 0:
            self.remaining -= 1
            self.update_timer_label()
        else:
            self.feedback_label.setText('<span style="color:orange">Time up — moving to next question</span>')
            for b in self.option_buttons:
                b.setEnabled(False)
            QtCore.QTimer.singleShot(1200, self.next_question)

    def update_timer_label(self):
        mins = self.remaining // 60
        secs = self.remaining % 60
        self.timer_label.setText(f"Time: {mins:02d}:{secs:02d}")

    def end_quiz(self):
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Quiz finished")
        msg.setText(f"You have completed the quiz!\nFinal score: {self.score}\nQuestions attempted: {len(self.questions)}")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    base = os.path.dirname(__file__)
    qfile = os.path.join(base, "questions.json")
    if not os.path.exists(qfile):
        QtWidgets.QMessageBox.critical(None, "Missing file", "questions.json not found in the application folder.")
        return
    w = QuizWindow(questions_file=qfile)
    w.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
