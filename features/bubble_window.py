# features/bubble_window.py (The Final, Deterministic Manual Calculation Fix)
import os
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QTimer, QPoint, QSize
from PyQt6.QtGui import QFontDatabase, QFont, QColor, QFontMetrics

class BubbleWindow(QWidget):
    _instance = None
    _font_family = "Microsoft YaHei UI"
    _font_loaded = False
    
    def __init__(self):
        super().__init__()
        if BubbleWindow._instance: return
        BubbleWindow._instance = self

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.parent_pet = None
        self.load_font()
        
        self.shadow_radius = 10
        layout = QVBoxLayout(self)
        layout.setContentsMargins(self.shadow_radius, self.shadow_radius, self.shadow_radius, self.shadow_radius)
        
        self.label = QLabel()
        self.label.setWordWrap(True)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(self.shadow_radius * 2)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(1, 2)
        self.label.setGraphicsEffect(shadow)
        
        # --- GEOMETRY CONSTANTS - The Single Source of Truth ---
        self.border_slice = 12
        self.bottom_border_slice = self.border_slice + 8
        self.padding = {'top': 8, 'right': 12, 'bottom': 8, 'left': 12}
        
        bg_path = "assets/bubble_background_template.png".replace("\\", "/")
        
        self.label.setStyleSheet(f"""
            QLabel {{
                border-image: url({bg_path}) {self.border_slice} {self.border_slice} {self.bottom_border_slice} {self.border_slice} stretch stretch;
                padding: {self.padding['top']}px {self.padding['right']}px {self.padding['bottom']}px {self.padding['left']}px;
                color: #3b3b3b; 
                font-size: 13px; 
                font-family: '{self._font_family}';
                qproperty-alignment: 'AlignCenter';
            }}
        """)
        
        layout.addWidget(self.label)
        
        self.hide_timer = QTimer(self); self.hide_timer.setSingleShot(True); self.hide_timer.timeout.connect(self.do_hide)

    def load_font(self):
        if not BubbleWindow._font_loaded:
            font_path = "assets/fonts/ZCOOLKuaiLe-Regular.ttf"
            if os.path.exists(font_path):
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1: self._font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            BubbleWindow._font_loaded = True

    def do_hide(self):
        if self.parent_pet:
            try: self.parent_pet.moved.disconnect(self.update_position)
            except TypeError: pass
        self.hide()

    def update_position(self, new_size=None):
        if not self.parent_pet: return
        window_size = new_size if new_size else self.size()
        if not window_size.isValid(): return

        pet_rect = self.parent_pet.geometry()
        screen_rect = QApplication.primaryScreen().availableGeometry()
        pet_anchor = self.parent_pet.mapToGlobal(QPoint(pet_rect.width() // 2, 0))
        
        bubble_tail_x = (window_size.width() - self.shadow_radius * 2) // 2
        
        pos_x = pet_anchor.x() - bubble_tail_x - self.shadow_radius
        pos_y = pet_anchor.y() - window_size.height() + self.shadow_radius
        
        offset_x = - (pet_rect.width() // 8) if self.parent_pet.flipped else (pet_rect.width() // 8)
        pos_x += offset_x

        if pos_x + window_size.width() > screen_rect.right(): pos_x = screen_rect.right() - window_size.width()
        if pos_x < screen_rect.left(): pos_x = screen_rect.left()
        if pos_y < screen_rect.top(): pos_y = pet_anchor.y() + 10
        
        self.move(int(pos_x), int(pos_y))
        
    @classmethod
    def show_message(cls, parent_pet, message, duration=4000):
        if cls._instance is None: cls._instance = cls()
        instance = cls._instance
        instance.parent_pet = parent_pet

        try: parent_pet.moved.disconnect(instance.update_position)
        except TypeError: pass
        parent_pet.moved.connect(instance.update_position)
        
        instance.label.setText(message)
        
        # --- FULL MANUAL CALCULATION - The only reliable way ---
        
        # 1. Define max width for the CONTENT area (text)
        max_content_width = 220 

        # 2. Get font metrics to calculate text size
        font_metrics = QFontMetrics(instance.label.font())
        
        # 3. Calculate the bounding rectangle for the word-wrapped text
        text_rect = font_metrics.boundingRect(0, 0, max_content_width, 9999, Qt.TextFlag.TextWordWrap, message)

        # 4. Calculate the total required size for the LABEL.
        # This is text size + padding + border spaces.
        label_width = text_rect.width() + instance.padding['left'] + instance.padding['right']
        label_height = text_rect.height() + instance.padding['top'] + instance.padding['bottom']

        # 5. Set this exact, calculated size to the label.
        instance.label.setFixedSize(label_width, label_height)
        
        # 6. Calculate the final WINDOW size (label size + shadow margins)
        final_width = label_width + instance.shadow_radius * 2
        final_height = label_height + instance.shadow_radius * 2
        final_size = QSize(final_width, final_height)
        
        # 7. Set the final, calculated size for the main window
        instance.setFixedSize(final_size)
        
        # 8. Position the window with its known, correct size
        instance.update_position(final_size)
        
        # 9. Show the window. It is now guaranteed to be correct.
        instance.show()
        
        instance.hide_timer.start(duration)