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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1lllllll1l_opy_ as bstack11l11l111_opy_
from browserstack_sdk.bstack1l1ll1ll11_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l11l111ll_opy_
class bstack11llll1l_opy_:
    def __init__(self, args, logger, bstack11l11lll11_opy_, bstack11l1l11ll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l11lll11_opy_ = bstack11l11lll11_opy_
        self.bstack11l1l11ll1_opy_ = bstack11l1l11ll1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1lllllll11_opy_ = []
        self.bstack11l1l11l1l_opy_ = None
        self.bstack111111l1l_opy_ = []
        self.bstack11l1l11111_opy_ = self.bstack1l11l1l1l_opy_()
        self.bstack1l111ll1_opy_ = -1
    def bstack1llll11l_opy_(self, bstack11l1l1ll11_opy_):
        self.parse_args()
        self.bstack11l1l111ll_opy_()
        self.bstack11l1l1l1ll_opy_(bstack11l1l1ll11_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11l1l11l11_opy_():
        import importlib
        if getattr(importlib, bstack1111ll1_opy_ (u"࠭ࡦࡪࡰࡧࡣࡱࡵࡡࡥࡧࡵࠫໟ"), False):
            bstack11l11lll1l_opy_ = importlib.find_loader(bstack1111ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ໠"))
        else:
            bstack11l11lll1l_opy_ = importlib.util.find_spec(bstack1111ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪ໡"))
    def bstack11l1l1l111_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l111ll1_opy_ = -1
        if self.bstack11l1l11ll1_opy_ and bstack1111ll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ໢") in self.bstack11l11lll11_opy_:
            self.bstack1l111ll1_opy_ = int(self.bstack11l11lll11_opy_[bstack1111ll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ໣")])
        try:
            bstack11l1l1111l_opy_ = [bstack1111ll1_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭໤"), bstack1111ll1_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨ໥"), bstack1111ll1_opy_ (u"࠭࠭ࡱࠩ໦")]
            if self.bstack1l111ll1_opy_ >= 0:
                bstack11l1l1111l_opy_.extend([bstack1111ll1_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ໧"), bstack1111ll1_opy_ (u"ࠨ࠯ࡱࠫ໨")])
            for arg in bstack11l1l1111l_opy_:
                self.bstack11l1l1l111_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11l1l111ll_opy_(self):
        bstack11l1l11l1l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11l1l11l1l_opy_ = bstack11l1l11l1l_opy_
        return bstack11l1l11l1l_opy_
    def bstack11lll1l1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11l1l11l11_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l11l111ll_opy_)
    def bstack11l1l1l1ll_opy_(self, bstack11l1l1ll11_opy_):
        bstack11l11l1ll_opy_ = Config.bstack1111l1lll_opy_()
        if bstack11l1l1ll11_opy_:
            self.bstack11l1l11l1l_opy_.append(bstack1111ll1_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭໩"))
            self.bstack11l1l11l1l_opy_.append(bstack1111ll1_opy_ (u"ࠪࡘࡷࡻࡥࠨ໪"))
        if bstack11l11l1ll_opy_.bstack11l1l111l1_opy_():
            self.bstack11l1l11l1l_opy_.append(bstack1111ll1_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ໫"))
            self.bstack11l1l11l1l_opy_.append(bstack1111ll1_opy_ (u"࡚ࠬࡲࡶࡧࠪ໬"))
        self.bstack11l1l11l1l_opy_.append(bstack1111ll1_opy_ (u"࠭࠭ࡱࠩ໭"))
        self.bstack11l1l11l1l_opy_.append(bstack1111ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠬ໮"))
        self.bstack11l1l11l1l_opy_.append(bstack1111ll1_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪ໯"))
        self.bstack11l1l11l1l_opy_.append(bstack1111ll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ໰"))
        if self.bstack1l111ll1_opy_ > 1:
            self.bstack11l1l11l1l_opy_.append(bstack1111ll1_opy_ (u"ࠪ࠱ࡳ࠭໱"))
            self.bstack11l1l11l1l_opy_.append(str(self.bstack1l111ll1_opy_))
    def bstack11l11llll1_opy_(self):
        bstack111111l1l_opy_ = []
        for spec in self.bstack1lllllll11_opy_:
            bstack11l11111l_opy_ = [spec]
            bstack11l11111l_opy_ += self.bstack11l1l11l1l_opy_
            bstack111111l1l_opy_.append(bstack11l11111l_opy_)
        self.bstack111111l1l_opy_ = bstack111111l1l_opy_
        return bstack111111l1l_opy_
    def bstack1l11l1l1l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11l1l11111_opy_ = True
            return True
        except Exception as e:
            self.bstack11l1l11111_opy_ = False
        return self.bstack11l1l11111_opy_
    def bstack11lllll1ll_opy_(self, bstack11l1l1l1l1_opy_, bstack1llll11l_opy_):
        bstack1llll11l_opy_[bstack1111ll1_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ໲")] = self.bstack11l11lll11_opy_
        multiprocessing.set_start_method(bstack1111ll1_opy_ (u"ࠬࡹࡰࡢࡹࡱࠫ໳"))
        bstack11ll111l_opy_ = []
        manager = multiprocessing.Manager()
        bstack111l1ll1_opy_ = manager.list()
        if bstack1111ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ໴") in self.bstack11l11lll11_opy_:
            for index, platform in enumerate(self.bstack11l11lll11_opy_[bstack1111ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ໵")]):
                bstack11ll111l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11l1l1l1l1_opy_,
                                                            args=(self.bstack11l1l11l1l_opy_, bstack1llll11l_opy_, bstack111l1ll1_opy_)))
            bstack11l11lllll_opy_ = len(self.bstack11l11lll11_opy_[bstack1111ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ໶")])
        else:
            bstack11ll111l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11l1l1l1l1_opy_,
                                                        args=(self.bstack11l1l11l1l_opy_, bstack1llll11l_opy_, bstack111l1ll1_opy_)))
            bstack11l11lllll_opy_ = 1
        i = 0
        for t in bstack11ll111l_opy_:
            os.environ[bstack1111ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ໷")] = str(i)
            if bstack1111ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭໸") in self.bstack11l11lll11_opy_:
                os.environ[bstack1111ll1_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ໹")] = json.dumps(self.bstack11l11lll11_opy_[bstack1111ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ໺")][i % bstack11l11lllll_opy_])
            i += 1
            t.start()
        for t in bstack11ll111l_opy_:
            t.join()
        return list(bstack111l1ll1_opy_)
    @staticmethod
    def bstack1ll11ll1ll_opy_(driver, bstack11l1l1l11l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1111ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ໻"), None)
        if item and getattr(item, bstack1111ll1_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࠩ໼"), None) and not getattr(item, bstack1111ll1_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࡤࡪ࡯࡯ࡧࠪ໽"), False):
            logger.info(
                bstack1111ll1_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠣ໾"))
            bstack11l1l11lll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11l11l111_opy_.bstack11l1l111_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)