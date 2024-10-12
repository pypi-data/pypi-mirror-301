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
class bstack1l1l1l1lll_opy_:
    def __init__(self, handler):
        self._1ll1lllll11_opy_ = None
        self.handler = handler
        self._1ll1llll1ll_opy_ = self.bstack1ll1llll1l1_opy_()
        self.patch()
    def patch(self):
        self._1ll1lllll11_opy_ = self._1ll1llll1ll_opy_.execute
        self._1ll1llll1ll_opy_.execute = self.bstack1ll1lllll1l_opy_()
    def bstack1ll1lllll1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1111ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣᗡ"), driver_command, None, this, args)
            response = self._1ll1lllll11_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1111ll1_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣᗢ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1llll1ll_opy_.execute = self._1ll1lllll11_opy_
    @staticmethod
    def bstack1ll1llll1l1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver