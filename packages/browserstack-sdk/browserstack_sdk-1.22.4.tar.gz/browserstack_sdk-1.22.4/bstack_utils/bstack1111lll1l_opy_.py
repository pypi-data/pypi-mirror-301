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
from collections import deque
from bstack_utils.constants import *
class bstack1llll1111l_opy_:
    def __init__(self):
        self._1lll1l1l1l1_opy_ = deque()
        self._1lll1l111ll_opy_ = {}
        self._1lll1l1ll11_opy_ = False
    def bstack1lll1l1l11l_opy_(self, test_name, bstack1lll1l11l11_opy_):
        bstack1lll1l1111l_opy_ = self._1lll1l111ll_opy_.get(test_name, {})
        return bstack1lll1l1111l_opy_.get(bstack1lll1l11l11_opy_, 0)
    def bstack1lll1l11111_opy_(self, test_name, bstack1lll1l11l11_opy_):
        bstack1lll1l11lll_opy_ = self.bstack1lll1l1l11l_opy_(test_name, bstack1lll1l11l11_opy_)
        self.bstack1lll1l1l111_opy_(test_name, bstack1lll1l11l11_opy_)
        return bstack1lll1l11lll_opy_
    def bstack1lll1l1l111_opy_(self, test_name, bstack1lll1l11l11_opy_):
        if test_name not in self._1lll1l111ll_opy_:
            self._1lll1l111ll_opy_[test_name] = {}
        bstack1lll1l1111l_opy_ = self._1lll1l111ll_opy_[test_name]
        bstack1lll1l11lll_opy_ = bstack1lll1l1111l_opy_.get(bstack1lll1l11l11_opy_, 0)
        bstack1lll1l1111l_opy_[bstack1lll1l11l11_opy_] = bstack1lll1l11lll_opy_ + 1
    def bstack11l11111_opy_(self, bstack1lll1l1ll1l_opy_, bstack1lll1l1l1ll_opy_):
        bstack1lll11lllll_opy_ = self.bstack1lll1l11111_opy_(bstack1lll1l1ll1l_opy_, bstack1lll1l1l1ll_opy_)
        bstack1lll1l11l1l_opy_ = bstack111ll11l11_opy_[bstack1lll1l1l1ll_opy_]
        bstack1lll1l111l1_opy_ = bstack1111ll1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦᖇ").format(bstack1lll1l1ll1l_opy_, bstack1lll1l11l1l_opy_, bstack1lll11lllll_opy_)
        self._1lll1l1l1l1_opy_.append(bstack1lll1l111l1_opy_)
    def bstack1lll1l1111_opy_(self):
        return len(self._1lll1l1l1l1_opy_) == 0
    def bstack1lll111l_opy_(self):
        bstack1lll1l11ll1_opy_ = self._1lll1l1l1l1_opy_.popleft()
        return bstack1lll1l11ll1_opy_
    def capturing(self):
        return self._1lll1l1ll11_opy_
    def bstack11ll11ll1_opy_(self):
        self._1lll1l1ll11_opy_ = True
    def bstack1l11ll1l11_opy_(self):
        self._1lll1l1ll11_opy_ = False