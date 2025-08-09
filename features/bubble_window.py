# features/bubble_window.py (The Final Error-Free Version)
import os
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer, QRect, QPoint
from PyQt6.QtGui import QFontDatabase, QFont, QFontMetrics

class BubbleWindow(QWidget):
    _instance = None; _font_family = "Microsoft YaHei UI"; _font_loaded = False
    
    def __init__(self):
        super().__init__()
        if BubbleWindow._instance: return
        BubbleWindow._instance = self

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.parent_pet = None
        self.load_font()
        
        layout = QVBoxLayout(self); layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel()
        
        self.border = {'top': 22, 'right': 22, 'bottom': 38, 'left': 22}
        self.padding = {'top': 5, 'right': 10, 'bottom': 5, 'left': 10}
        
        bg_path = "assets/bubble_background.png".replace("\\", "/")
        self.setStyleSheet(f"""
            QLabel {{
                border-image: url({bg_path}) {self.border['top']} {self.border['right']} {self.border['bottom']} {self.border['left']};
                border-width: {self.border['top']}px {self.border['right']}px {self.border['bottom']}px {self.border['left']}px;
                padding: {self.padding['top']}px {self.padding['right']}px {self.padding['bottom']}px {self.padding['left']}px;
                color: #3b3b3b; font-size: 13px; font-family: '{self._font_family}';
                /* 使用正确的对齐方式 */
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

    def update_position(self):
        if not (self.parent_pet and self.isVisible()): return
        pet_rect, screen_rect = self.parent_pet.geometry(), QApplication.primaryScreen().availableGeometry()
        anchors = {'top_right': QPoint(pet_rect.width()-20,-self.height()+15), 'top_left': QPoint(-self.width()+20,-self.height()+15)}
        priority = ['top_left', 'top_right'] if not self.parent_pet.flipped else ['top_right', 'top_left']
        for name in priority:
            pos = pet_rect.topLeft() + anchors[name]
            if screen_rect.contains(QRect(pos, self.size())):
                self.move(pos); return
        self.move(pet_rect.center().x() - self.width() // 2, pet_rect.top() - self.height())
        
    @classmethod
    def show_message(cls, parent_pet, message, duration=4000):
        if cls._instance is None: cls._instance = cls()
        instance = cls._instance; instance.parent_pet = parent_pet
        try: parent_pet.moved.connect(instance.update_position)
        except TypeError: pass
        
        instance.label.setText(message)
        font = QFont(cls._font_family, 13); metrics = QFontMetrics(font)
        
        # --- 最终的、绝对正确的计算逻辑 ---
        max_width = 180
        # 我们不再手动传递 flags，因为样式表已经处理了对齐
        # 并且 QLabel 的 setWordWrap 会自动处理换行
        
        instance.label.setWordWrap(True) # 总是允许换行
        # sizeHint 会根据内容、字体和换行策略，给出最佳尺寸
        ideal_size = instance.label.sizeHint() 
        
        # 如果宽度超过最大值，则限制宽度并让高度自适应
        if ideal_size.width() > max_width:
            instance.label.setFixedWidth(max_width)
        else:
            instance.label.setFixedWidth(ideal_size.width() + instance.padding['left'] + instance.padding['right'])
        
        # 根据最终的标签尺寸，重新调整整个窗口
        instance.adjustSize()
        
        instance.update_position(); instance.show()
        QApplication.processEvents()
        instance.hide_timer.start(duration)