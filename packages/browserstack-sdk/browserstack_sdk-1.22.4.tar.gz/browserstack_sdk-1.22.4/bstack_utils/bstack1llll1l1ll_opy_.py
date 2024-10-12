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
from browserstack_sdk.bstack1l111111_opy_ import bstack11llll1l_opy_
from browserstack_sdk.bstack11ll11111l_opy_ import RobotHandler
def bstack11llll111_opy_(framework):
    if framework.lower() == bstack1111ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨኮ"):
        return bstack11llll1l_opy_.version()
    elif framework.lower() == bstack1111ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨኯ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1111ll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪኰ"):
        import behave
        return behave.__version__
    else:
        return bstack1111ll1_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࠬ኱")