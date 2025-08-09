# core/pet_window.py (Final Corrected Version)
import sys, random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMenu
from PyQt6.QtGui import QPixmap, QTransform, QAction
from PyQt6.QtCore import Qt, QTimer, QPoint, pyqtSignal

import config
from utils import asset_loader
from features.reminder_manager import ReminderManager
from features.event_manager import EventManager
from features.bubble_window import BubbleWindow

class PetWindow(QWidget):
    moved = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.pet_cfg, self.animations = asset_loader.load_pet(config.CURRENT_PET)
        self.state = 'standing'
        self.is_dragging, self.is_interacting, self.is_staying, self.flipped, self.frame = False, False, False, False, 0
        self.click_timer = QTimer(self); self.click_timer.setSingleShot(True); self.click_timer.timeout.connect(self.trigger_interaction)
        
        self.init_ui()
        self.reminders = ReminderManager(self)
        self.events = EventManager(self)
        self.setup_timers()
        self.show()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SubWindow)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.screen = QApplication.primaryScreen().geometry()
        
        self.pet_label = QLabel(self)
        pixmap = self.animations[self.state][0]
        self.pet_label.setPixmap(pixmap)
        self.setFixedSize(pixmap.size())
        self.pet_label.setGeometry(0, 0, self.width(), self.height())
        self.move(random.randint(0, self.screen.width() - self.width()), self.screen.height() - self.height() - 40)
        
    def setup_timers(self):
        self.anim_timer = QTimer(self, timeout=self.next_frame); self.anim_timer.start(self.pet_cfg.get("animation_interval", 33))
        self.logic_timer = QTimer(self, timeout=self.update_logic); self.logic_timer.start(5000)
        self.move_timer = QTimer(self, timeout=self.move_pet); self.vx = 2
        
    def move(self, *args):
        super().move(*args); self.moved.emit()
        
    def next_frame(self):
        frames = self.animations.get(self.state)
        if not frames: return
        if self.frame >= len(frames): self.frame = 0
        pixmap = frames[self.frame]
        if self.flipped: pixmap = pixmap.transformed(QTransform().scale(-1, 1))
        self.pet_label.setPixmap(pixmap)
        self.frame += 1

    def update_logic(self):
        if self.is_busy(): return
        next_state = random.choices(['standing', 'running', 'sleeping'], weights=[0.6, 0.3, 0.1])[0]
        self.change_state(next_state)
    
    def change_state(self, new_state):
        if self.state == new_state or new_state not in self.animations: return
        self.state, self.frame = new_state, 0
        self.move_timer.start(30) if new_state == 'running' else self.move_timer.stop()
        
    def move_pet(self):
        if self.is_busy(): return
        x, y = self.pos().x() + self.vx, self.pos().y()
        if x <= 0: self.vx *= -1; self.flipped = False
        elif x >= self.screen.width() - self.width(): self.vx *= -1; self.flipped = True
        self.move(x, y)
        
    def show_message_and_interact(self, msg, duration=8000, interact=True):
        BubbleWindow.show_message(self, msg, duration)
        if interact: self.trigger_interaction()

    def trigger_interaction(self):
        if 'interacting' in self.animations and not self.is_interacting:
            self.is_interacting = True
            original_state = 'standing' if self.state == 'interacting' else self.state
            self.change_state('interacting')
            duration = 2000 # Simplified
            QTimer.singleShot(duration, lambda: (self.change_state(original_state), setattr(self, 'is_interacting', False)))

    def is_busy(self): return self.is_dragging or self.is_interacting or self.is_staying
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True; self.start_pos = event.globalPosition()

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            if (event.globalPosition() - self.start_pos).manhattanLength() > QApplication.startDragDistance(): self.click_timer.stop()
            delta = event.globalPosition() - self.start_pos
            self.move(self.pos() + delta.toPoint()); self.start_pos = event.globalPosition()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_dragging and (event.globalPosition() - self.start_pos).manhattanLength() < QApplication.startDragDistance():
                self.click_timer.start(QApplication.doubleClickInterval())
            self.is_dragging = False

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.click_timer.stop(); 
            BubbleWindow.show_message(self, "汪！汪！( >ω< )")
            
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        stay = QAction("原地待命", self, checkable=True, checked=self.is_staying, triggered=self.toggle_stay)
        reminders = QAction("开启提醒", self, checkable=True, checked=config.REMINDERS_ENABLED, triggered=self.toggle_reminders)
        menu.addAction(stay); menu.addAction(reminders); menu.addSeparator(); menu.addAction("再见", self.close)
        menu.exec(event.globalPos())
        
    def toggle_stay(self, checked):
        self.is_staying = checked
        if not checked: self.update_logic()
        else: self.change_state('standing')
        
    def toggle_reminders(self, checked):
        config.REMINDERS_ENABLED = checked
        # --- 修复：调用 self.show_message_and_interact ---
        self.show_message_and_interact("提醒功能已开启！" if checked else "提醒功能已关闭。", interact=False)
        if checked:
            self.reminders.minute_timer.start(60000)
            self.reminders.rest_timer.start(config.REST_REMINDER_INTERVAL)
        else:
            self.reminders.minute_timer.stop()
            self.reminders.rest_timer.stop()