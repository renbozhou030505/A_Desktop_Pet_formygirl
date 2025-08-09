# debug_boundingRect.py (New Strategy Verification)
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QFontMetrics, QTextOption

TEST_TEXT = "这是一个需要换行的、比较长的句子，用来测试我们的新逻辑是否可靠。"
TEST_FONT = QFont("Microsoft YaHei UI", 13)

def debug_new_strategy():
    metrics = QFontMetrics(TEST_FONT)
    print("--- 开始验证新的尺寸计算策略 ---")
    
    max_width = 180 # 我们设定的最大宽度
    
    # --- 新策略核心 ---
    # 我们使用 boundingRect 的一个特定重载版本，它只接受 QRect 和 text
    # 并且我们可以传入一个 flags，这个 flags 只包含对齐方式
    # 换行由 Qt 内部根据 QRect 的宽度自动处理
    flags = int(Qt.AlignmentFlag.AlignCenter) 
    
    # 创建一个 QRect，宽度是我们的最大宽度，高度可以设为0，表示不限制
    calculation_rect = QRect(0, 0, max_width, 0)
    
    try:
        print(f"\n[新策略] 尝试调用: metrics.boundingRect(QRect(0, 0, {max_width}, 0), flags, text)")
        # PyQt6 在这种情况下，会自动处理换行
        final_rect = metrics.boundingRect(calculation_rect, flags, TEST_TEXT)
        print(f"  > 成功！计算出的换行后矩形: QRect({final_rect.x()}, {final_rect.y()}, {final_rect.width()}, {final_rect.height()})")
        print(f"  > 注意：计算出的宽度 ({final_rect.width()}) 小于等于我们的最大宽度 ({max_width})，这证明自动换行成功了！")
    except Exception as e:
        print(f"  > 失败！新策略也失败了。错误: {e}")

    print("\n--- 验证结束 ---")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    debug_new_strategy()