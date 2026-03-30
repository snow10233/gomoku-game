from .alart_dialog import AlartDialog


class WipDialog(AlartDialog):

    def __init__(self, parent=None):
        super().__init__("此模式暫未開放！",parent)
        self.setWindowTitle("系統提示")
