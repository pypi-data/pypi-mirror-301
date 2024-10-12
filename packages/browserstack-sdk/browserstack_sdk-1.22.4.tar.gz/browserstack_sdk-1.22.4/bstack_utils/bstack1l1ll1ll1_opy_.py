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
import logging
import bstack_utils.bstack1lllllll1l_opy_ as bstack11l11l111_opy_
from bstack_utils.helper import bstack1llll1l11_opy_
logger = logging.getLogger(__name__)
def bstack1111lll1_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1l1l1l1ll_opy_(context, *args):
    tags = getattr(args[0], bstack1111ll1_opy_ (u"ࠬࡺࡡࡨࡵࠪ࿅"), [])
    bstack1ll1ll1l1l_opy_ = bstack11l11l111_opy_.bstack1l111l11_opy_(tags)
    threading.current_thread().isA11yTest = bstack1ll1ll1l1l_opy_
    try:
      bstack1ll11ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1111lll1_opy_(bstack1111ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶ࿆ࠬ")) else context.browser
      if bstack1ll11ll1_opy_ and bstack1ll11ll1_opy_.session_id and bstack1ll1ll1l1l_opy_ and bstack1llll1l11_opy_(
              threading.current_thread(), bstack1111ll1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭࿇"), None):
          threading.current_thread().isA11yTest = bstack11l11l111_opy_.bstack1lll1lllll_opy_(bstack1ll11ll1_opy_, bstack1ll1ll1l1l_opy_)
    except Exception as e:
       logger.debug(bstack1111ll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨ࿈").format(str(e)))
def bstack111l11l11_opy_(bstack1ll11ll1_opy_):
    if bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭࿉"), None) and bstack1llll1l11_opy_(
      threading.current_thread(), bstack1111ll1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ࿊"), None) and not bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧ࿋"), False):
      threading.current_thread().a11y_stop = True
      bstack11l11l111_opy_.bstack11l1l111_opy_(bstack1ll11ll1_opy_, name=bstack1111ll1_opy_ (u"ࠧࠨ࿌"), path=bstack1111ll1_opy_ (u"ࠨࠢ࿍"))