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
import logging
import os
import threading
from bstack_utils.helper import bstack1l11l1ll11_opy_
from bstack_utils.constants import bstack111l1ll1ll_opy_
logger = logging.getLogger(__name__)
class bstack11lll1lll_opy_:
    bstack1lll1111l11_opy_ = None
    @classmethod
    def bstack1l1lllllll_opy_(cls):
        if cls.on():
            logger.info(
                bstack1111ll1_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨ᝻").format(os.environ[bstack1111ll1_opy_ (u"ࠨࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠧ᝼")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1111ll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨ᝽"), None) is None or os.environ[bstack1111ll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩ᝾")] == bstack1111ll1_opy_ (u"ࠤࡱࡹࡱࡲࠢ᝿"):
            return False
        return True
    @classmethod
    def bstack1ll11llll11_opy_(cls, bs_config, framework=bstack1111ll1_opy_ (u"ࠥࠦក")):
        if framework == bstack1111ll1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫខ"):
            return bstack1l11l1ll11_opy_(bs_config.get(bstack1111ll1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩគ")))
        bstack1ll11ll1ll1_opy_ = framework in bstack111l1ll1ll_opy_
        return bstack1l11l1ll11_opy_(bs_config.get(bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪឃ"), bstack1ll11ll1ll1_opy_))
    @classmethod
    def bstack1ll11ll1l11_opy_(cls, framework):
        return framework in bstack111l1ll1ll_opy_
    @classmethod
    def bstack1ll1l11ll1l_opy_(cls, bs_config, framework):
        return cls.bstack1ll11llll11_opy_(bs_config, framework) is True and cls.bstack1ll11ll1l11_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1111ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫង"), None)
    @staticmethod
    def bstack11llll1l1l_opy_():
        if getattr(threading.current_thread(), bstack1111ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬច"), None):
            return {
                bstack1111ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧឆ"): bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࠨជ"),
                bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫឈ"): getattr(threading.current_thread(), bstack1111ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩញ"), None)
            }
        if getattr(threading.current_thread(), bstack1111ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪដ"), None):
            return {
                bstack1111ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬឋ"): bstack1111ll1_opy_ (u"ࠨࡪࡲࡳࡰ࠭ឌ"),
                bstack1111ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩឍ"): getattr(threading.current_thread(), bstack1111ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧណ"), None)
            }
        return None
    @staticmethod
    def bstack1ll11ll1lll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11lll1lll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11ll111111_opy_(test, hook_name=None):
        bstack1ll11ll11ll_opy_ = test.parent
        if hook_name in [bstack1111ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩត"), bstack1111ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ថ"), bstack1111ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬទ"), bstack1111ll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩធ")]:
            bstack1ll11ll11ll_opy_ = test
        scope = []
        while bstack1ll11ll11ll_opy_ is not None:
            scope.append(bstack1ll11ll11ll_opy_.name)
            bstack1ll11ll11ll_opy_ = bstack1ll11ll11ll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll11lll111_opy_(hook_type):
        if hook_type == bstack1111ll1_opy_ (u"ࠣࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍࠨន"):
            return bstack1111ll1_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡪࡲࡳࡰࠨប")
        elif hook_type == bstack1111ll1_opy_ (u"ࠥࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠢផ"):
            return bstack1111ll1_opy_ (u"࡙ࠦ࡫ࡡࡳࡦࡲࡻࡳࠦࡨࡰࡱ࡮ࠦព")
    @staticmethod
    def bstack1ll11ll1l1l_opy_(bstack1lllllll11_opy_):
        try:
            if not bstack11lll1lll_opy_.on():
                return bstack1lllllll11_opy_
            if os.environ.get(bstack1111ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠥភ"), None) == bstack1111ll1_opy_ (u"ࠨࡴࡳࡷࡨࠦម"):
                tests = os.environ.get(bstack1111ll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠦយ"), None)
                if tests is None or tests == bstack1111ll1_opy_ (u"ࠣࡰࡸࡰࡱࠨរ"):
                    return bstack1lllllll11_opy_
                bstack1lllllll11_opy_ = tests.split(bstack1111ll1_opy_ (u"ࠩ࠯ࠫល"))
                return bstack1lllllll11_opy_
        except Exception as exc:
            print(bstack1111ll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡩࡷࡻ࡮ࠡࡪࡤࡲࡩࡲࡥࡳ࠼ࠣࠦវ"), str(exc))
        return bstack1lllllll11_opy_