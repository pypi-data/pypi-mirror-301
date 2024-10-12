# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack1111111_opy_ = 2048
bstack11ll1ll_opy_ = 7
def bstack1111ll1_opy_ (bstack1l11l1l_opy_):
    global bstack11ll_opy_
    bstack1111ll_opy_ = ord (bstack1l11l1l_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1l11l1l_opy_ [:-1]
    bstack11111l1_opy_ = bstack1111ll_opy_ % len (bstack1l11ll1_opy_)
    bstack111l1_opy_ = bstack1l11ll1_opy_ [:bstack11111l1_opy_] + bstack1l11ll1_opy_ [bstack11111l1_opy_:]
    if bstack1lll_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1111111_opy_ - (bstack111l11l_opy_ + bstack1111ll_opy_) % bstack11ll1ll_opy_) for bstack111l11l_opy_, char in enumerate (bstack111l1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack1111111_opy_ - (bstack111l11l_opy_ + bstack1111ll_opy_) % bstack11ll1ll_opy_) for bstack111l11l_opy_, char in enumerate (bstack111l1_opy_)])
    return eval (bstack1lllll1l_opy_)
import threading
bstack1lll1111lll_opy_ = 1000
bstack1lll111l11l_opy_ = 5
bstack1lll111111l_opy_ = 30
bstack1lll111l111_opy_ = 2
class bstack1lll11111ll_opy_:
    def __init__(self, handler, bstack1ll1lllllll_opy_=bstack1lll1111lll_opy_, bstack1ll1llllll1_opy_=bstack1lll111l11l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1ll1lllllll_opy_ = bstack1ll1lllllll_opy_
        self.bstack1ll1llllll1_opy_ = bstack1ll1llllll1_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1lll1111111_opy_()
    def bstack1lll1111111_opy_(self):
        self.timer = threading.Timer(self.bstack1ll1llllll1_opy_, self.bstack1lll1111ll1_opy_)
        self.timer.start()
    def bstack1lll11111l1_opy_(self):
        self.timer.cancel()
    def bstack1lll1111l1l_opy_(self):
        self.bstack1lll11111l1_opy_()
        self.bstack1lll1111111_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1ll1lllllll_opy_:
                t = threading.Thread(target=self.bstack1lll1111ll1_opy_)
                t.start()
                self.bstack1lll1111l1l_opy_()
    def bstack1lll1111ll1_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1ll1lllllll_opy_]
        del self.queue[:self.bstack1ll1lllllll_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1lll11111l1_opy_()
        while len(self.queue) > 0:
            self.bstack1lll1111ll1_opy_()