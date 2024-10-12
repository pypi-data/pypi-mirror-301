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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11l11lll11_opy_, bstack11l1l11ll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l11lll11_opy_ = bstack11l11lll11_opy_
        self.bstack11l1l11ll1_opy_ = bstack11l1l11ll1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11ll111111_opy_(bstack11l11ll111_opy_):
        bstack11l11ll1l1_opy_ = []
        if bstack11l11ll111_opy_:
            tokens = str(os.path.basename(bstack11l11ll111_opy_)).split(bstack1111ll1_opy_ (u"ࠥࡣࠧ໿"))
            camelcase_name = bstack1111ll1_opy_ (u"ࠦࠥࠨༀ").join(t.title() for t in tokens)
            suite_name, bstack11l11ll11l_opy_ = os.path.splitext(camelcase_name)
            bstack11l11ll1l1_opy_.append(suite_name)
        return bstack11l11ll1l1_opy_
    @staticmethod
    def bstack11l11ll1ll_opy_(typename):
        if bstack1111ll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ༁") in typename:
            return bstack1111ll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ༂")
        return bstack1111ll1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ༃")