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
import builtins
import logging
class bstack11lll11lll_opy_:
    def __init__(self, handler):
        self._111ll1lll1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111ll1llll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1111ll1_opy_ (u"ࠧࡪࡰࡩࡳࠬ࿎"), bstack1111ll1_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧ࿏"), bstack1111ll1_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪ࿐"), bstack1111ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ࿑")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111ll1ll11_opy_
        self._111lll1111_opy_()
    def _111ll1ll11_opy_(self, *args, **kwargs):
        self._111ll1lll1_opy_(*args, **kwargs)
        message = bstack1111ll1_opy_ (u"ࠫࠥ࠭࿒").join(map(str, args)) + bstack1111ll1_opy_ (u"ࠬࡢ࡮ࠨ࿓")
        self._log_message(bstack1111ll1_opy_ (u"࠭ࡉࡏࡈࡒࠫ࿔"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1111ll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭࿕"): level, bstack1111ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿖"): msg})
    def _111lll1111_opy_(self):
        for level, bstack111ll1ll1l_opy_ in self._111ll1llll_opy_.items():
            setattr(logging, level, self._111lll111l_opy_(level, bstack111ll1ll1l_opy_))
    def _111lll111l_opy_(self, level, bstack111ll1ll1l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111ll1ll1l_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111ll1lll1_opy_
        for level, bstack111ll1ll1l_opy_ in self._111ll1llll_opy_.items():
            setattr(logging, level, bstack111ll1ll1l_opy_)