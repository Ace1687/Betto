import sys
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
import math

# ---------------------------
# Signal bridge (thread-safe UI updates)
# ---------------------------
class BettoSignals(QObject):
    message_received = pyqtSignal(str, str)  # sender, text
    set_state = pyqtSignal(str)              # sleeping / listening / thinking / speaking

signals = BettoSignals()

# ---------------------------
# Robot Face Widget
# ---------------------------
class RobotFace(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 200)
        self.state = "sleeping"   # sleeping | listening | thinking | speaking
        self.blink_open = True
        self.mouth_frame = 0
        self.pulse = 0.0

        # Blink timer
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self._blink)
        self.blink_timer.start(3000)

        # Animation timer
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self._animate)
        self.anim_timer.start(80)

    def set_state(self, state):
        self.state = state
        self.update()

    def _blink(self):
        if self.state == "sleeping":
            return
        self.blink_open = False
        self.update()
        QTimer.singleShot(150, self._open_eyes)

    def _open_eyes(self):
        self.blink_open = True
        self.update()

    def _animate(self):
        self.pulse = (self.pulse + 0.15) % (2 * math.pi)
        self.mouth_frame = (self.mouth_frame + 1) % 8
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        size = min(w, h)
        scale = size / 220

        # State colors
        state_colors = {
            "sleeping":  QColor(80, 80, 100),
            "listening": QColor(40, 180, 140),
            "thinking":  QColor(120, 80, 200),
            "speaking":  QColor(220, 100, 60),
        }
        accent = state_colors.get(self.state, QColor(80, 80, 100))

        # Head
        head_r = int(80 * scale)
        p.setPen(QPen(accent, 3 * scale))
        p.setBrush(QColor(30, 32, 40))
        p.drawEllipse(cx - head_r, cy - head_r, head_r * 2, head_r * 2)

        # Glow ring (listening / speaking)
        if self.state in ("listening", "speaking"):
            glow_r = head_r + int(8 * scale + 4 * scale * math.sin(self.pulse))
            glow_color = QColor(accent)
            glow_color.setAlpha(60)
            p.setPen(QPen(glow_color, 4 * scale))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawEllipse(cx - glow_r, cy - glow_r, glow_r * 2, glow_r * 2)

        # Eyes
        eye_y = cy - int(20 * scale)
        eye_x_off = int(25 * scale)
        eye_w = int(22 * scale)
        eye_h = int(14 * scale) if self.blink_open else int(3 * scale)

        if self.state == "sleeping":
            # Closed/squinted eyes
            for ex in [cx - eye_x_off, cx + eye_x_off]:
                p.setPen(QPen(accent, 2 * scale))
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.drawLine(int(ex - eye_w//2), eye_y, int(ex + eye_w//2), eye_y)
        else:
            for ex in [cx - eye_x_off, cx + eye_x_off]:
                # Eye white
                p.setPen(Qt.PenStyle.NoPen)
                p.setBrush(QColor(220, 230, 255))
                p.drawEllipse(int(ex - eye_w//2), int(eye_y - eye_h//2), eye_w, eye_h)
                # Pupil
                pupil_size = int(7 * scale)
                p.setBrush(QColor(20, 20, 30))
                p.drawEllipse(int(ex - pupil_size//2), int(eye_y - pupil_size//2), pupil_size, pupil_size)
                # Glint
                p.setBrush(QColor(255, 255, 255, 180))
                g = int(2 * scale)
                p.drawEllipse(int(ex + 2*scale), int(eye_y - 3*scale), g*2, g*2)

        # Thinking dots
        if self.state == "thinking":
            for i in range(3):
                dot_x = cx - int(18 * scale) + i * int(18 * scale)
                dot_y = cy + int(35 * scale)
                alpha = int(120 + 120 * math.sin(self.pulse + i * 1.0))
                c = QColor(accent)
                c.setAlpha(alpha)
                p.setBrush(c)
                p.setPen(Qt.PenStyle.NoPen)
                r = int(5 * scale)
                p.drawEllipse(dot_x - r, dot_y - r, r*2, r*2)

        # Mouth
        mouth_y = cy + int(30 * scale)
        mouth_w = int(40 * scale)
        p.setPen(QPen(accent, 2.5 * scale))
        p.setBrush(Qt.BrushStyle.NoBrush)

        if self.state == "sleeping":
            # Flat line
            p.drawLine(cx - mouth_w//2, mouth_y, cx + mouth_w//2, mouth_y)
        elif self.state == "speaking":
            # Animated open/close mouth
            open_h = int(6 * scale * (1 + math.sin(self.pulse * 3)))
            p.setBrush(QColor(20, 20, 30))
            p.drawEllipse(cx - mouth_w//2, mouth_y - open_h//2, mouth_w, max(4, open_h))
        elif self.state == "listening":
            # Slight smile
            from PyQt6.QtCore import QRect
            p.drawArc(QRect(cx - mouth_w//2, mouth_y - int(8*scale), mouth_w, int(16*scale)), 200*16, 140*16)
        else:
            # Neutral
            p.drawLine(cx - mouth_w//2, mouth_y, cx + mouth_w//2, mouth_y)

        # Ears / side panels
        ear_w = int(10 * scale)
        ear_h = int(24 * scale)
        p.setPen(QPen(accent, 1.5 * scale))
        p.setBrush(QColor(50, 52, 65))
        p.drawRect(cx - head_r - ear_w, cy - ear_h//2, ear_w, ear_h)
        p.drawRect(cx + head_r, cy - ear_h//2, ear_w, ear_h)

        # State label
        p.setPen(QPen(accent, 1))
        font = QFont("Consolas", max(8, int(9 * scale)))
        p.setFont(font)
        p.drawText(0, h - 20, w, 20, Qt.AlignmentFlag.AlignCenter, f"[ {self.state.upper()} ]")

# ---------------------------
# Main App Window
# ---------------------------
class BettoWindow(QMainWindow):
    def __init__(self, on_user_message=None):
        super().__init__()
        self.on_user_message = on_user_message
        self.setWindowTitle("Betto")
        self.setMinimumSize(420, 620)
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1b22; }
            QWidget { background-color: #1a1b22; color: #e0e0e0; }
            QTextEdit {
                background-color: #12131a;
                color: #d0d0d0;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 8px;
                font-family: Consolas, monospace;
                font-size: 13px;
            }
            QLineEdit {
                background-color: #12131a;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #5060c0; }
            QPushButton {
                background-color: #3a3dc0;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #4a4dd0; }
            QPushButton:pressed { background-color: #2a2da0; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Robot face
        self.face = RobotFace()
        self.face.setFixedHeight(200)
        layout.addWidget(self.face)

        # Status label
        self.status_label = QLabel("Say 'Hey Betto' or press Ctrl+B to activate")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(self.status_label)

        # Chat log
        self.chat_log = QTextEdit()
        self.chat_log.setReadOnly(True)
        self.chat_log.setMinimumHeight(200)
        layout.addWidget(self.chat_log)

        # Input row
        input_row = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type a message to Betto...")
        self.input_box.returnPressed.connect(self._send_message)
        input_row.addWidget(self.input_box)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self._send_message)
        input_row.addWidget(send_btn)
        layout.addLayout(input_row)

        # Connect signals
        signals.message_received.connect(self._append_message)
        signals.set_state.connect(self.face.set_state)
        signals.set_state.connect(self._update_status)

    def _send_message(self):
        text = self.input_box.text().strip()
        if not text:
            return
        self.input_box.clear()
        self._append_message("You", text)
        if self.on_user_message:
            threading.Thread(target=self.on_user_message, args=(text,), daemon=True).start()

    def _append_message(self, sender, text):
        if sender == "You":
            color = "#7eb8f7"
        elif sender == "Betto":
            color = "#7ef7b0"
        else:
            color = "#aaa"
        self.chat_log.append(f'<span style="color:{color}"><b>{sender}:</b></span> {text}<br>')

    def _update_status(self, state):
        messages = {
            "sleeping":  "Say 'Hey Betto' or press Ctrl+B to activate",
            "listening": "Listening...",
            "thinking":  "Betto is thinking...",
            "speaking":  "Betto is speaking...",
        }
        self.status_label.setText(messages.get(state, ""))

    def activate(self):
        """Called when wake word or hotkey fires."""
        signals.set_state.emit("listening")
        self.raise_()
        self.activateWindow()
        self.input_box.setFocus()

def run_app(on_user_message=None):
    app = QApplication(sys.argv)
    app.setApplicationName("Betto")
    window = BettoWindow(on_user_message=on_user_message)
    window.show()
    return app, window
