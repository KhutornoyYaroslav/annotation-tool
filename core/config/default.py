from core.utils.basicconfig import Config, DictNode, ListNode


cfg_ = Config()
# View settings
cfg_.view = DictNode()
cfg_.view.appearance = DictNode()
cfg_.view.appearance.fullscreen = False
cfg_.view.appearance.maximized = False
cfg_.view.appearance.wndsize = [800, 600]
# Control settings
cfg_.control = DictNode()
cfg_.control.zoom_factor = 1.25
# Annotation settings
cfg_.annotation = DictNode()
cfg_.annotation.classes = ListNode()
cfg_.annotation.classes.name = "default_class"
cfg_.annotation.classes.shapes = ["boundingrect"]
cfg_.annotation.classes.append()
# Files settings
cfg_.files = DictNode()
cfg_.files.valid_extensions = ['png', 'jpg', 'jpeg', 'bmp', 'JPG']
