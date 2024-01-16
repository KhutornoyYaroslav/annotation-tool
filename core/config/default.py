from core.utils.basicconfig import Config, DictNode, ListNode


cfg_ = Config()
cfg_.ui = DictNode()
cfg_.ui.wnd = DictNode()
cfg_.ui.wnd.fullscreen = False
cfg_.ui.wnd.maximized = False
cfg_.ui.wnd.size = [800, 600]
