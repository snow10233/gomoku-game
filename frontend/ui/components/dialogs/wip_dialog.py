from .alert_dialog import AlertDialog


class WipDialog(AlertDialog):

    def __init__(self, parent=None):
        super().__init__("此模式暫未開放！", parent)
        self.setWindowTitle("系統提示")
