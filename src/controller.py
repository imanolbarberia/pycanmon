from model import Model
from view import View


class Controller:
    def __init__(self, mdl: Model, vw: View):
        super(Controller, self).__init__()
        self.model = mdl
        self.view = vw

        self.view.onTestBtnClicked.connect(self.activate)

    def run(self):
        self.view.show()

    def activate(self):
        self.model.add_frame([5])
