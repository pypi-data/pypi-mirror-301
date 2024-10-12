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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1lllll11l_opy_ = {}
        bstack11lllll111_opy_ = os.environ.get(bstack1111ll1_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩඟ"), bstack1111ll1_opy_ (u"ࠩࠪච"))
        if not bstack11lllll111_opy_:
            return bstack1lllll11l_opy_
        try:
            bstack11lllll11l_opy_ = json.loads(bstack11lllll111_opy_)
            if bstack1111ll1_opy_ (u"ࠥࡳࡸࠨඡ") in bstack11lllll11l_opy_:
                bstack1lllll11l_opy_[bstack1111ll1_opy_ (u"ࠦࡴࡹࠢජ")] = bstack11lllll11l_opy_[bstack1111ll1_opy_ (u"ࠧࡵࡳࠣඣ")]
            if bstack1111ll1_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥඤ") in bstack11lllll11l_opy_ or bstack1111ll1_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥඥ") in bstack11lllll11l_opy_:
                bstack1lllll11l_opy_[bstack1111ll1_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦඦ")] = bstack11lllll11l_opy_.get(bstack1111ll1_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨට"), bstack11lllll11l_opy_.get(bstack1111ll1_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨඨ")))
            if bstack1111ll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧඩ") in bstack11lllll11l_opy_ or bstack1111ll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥඪ") in bstack11lllll11l_opy_:
                bstack1lllll11l_opy_[bstack1111ll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦණ")] = bstack11lllll11l_opy_.get(bstack1111ll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣඬ"), bstack11lllll11l_opy_.get(bstack1111ll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨත")))
            if bstack1111ll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦථ") in bstack11lllll11l_opy_ or bstack1111ll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦද") in bstack11lllll11l_opy_:
                bstack1lllll11l_opy_[bstack1111ll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧධ")] = bstack11lllll11l_opy_.get(bstack1111ll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢන"), bstack11lllll11l_opy_.get(bstack1111ll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ඲")))
            if bstack1111ll1_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢඳ") in bstack11lllll11l_opy_ or bstack1111ll1_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧප") in bstack11lllll11l_opy_:
                bstack1lllll11l_opy_[bstack1111ll1_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨඵ")] = bstack11lllll11l_opy_.get(bstack1111ll1_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥබ"), bstack11lllll11l_opy_.get(bstack1111ll1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣභ")))
            if bstack1111ll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢම") in bstack11lllll11l_opy_ or bstack1111ll1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧඹ") in bstack11lllll11l_opy_:
                bstack1lllll11l_opy_[bstack1111ll1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨය")] = bstack11lllll11l_opy_.get(bstack1111ll1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥර"), bstack11lllll11l_opy_.get(bstack1111ll1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ඼")))
            if bstack1111ll1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨල") in bstack11lllll11l_opy_ or bstack1111ll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ඾") in bstack11lllll11l_opy_:
                bstack1lllll11l_opy_[bstack1111ll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ඿")] = bstack11lllll11l_opy_.get(bstack1111ll1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤව"), bstack11lllll11l_opy_.get(bstack1111ll1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤශ")))
            if bstack1111ll1_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥෂ") in bstack11lllll11l_opy_:
                bstack1lllll11l_opy_[bstack1111ll1_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦස")] = bstack11lllll11l_opy_[bstack1111ll1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧහ")]
        except Exception as error:
            logger.error(bstack1111ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡦࡺࡡ࠻ࠢࠥළ") +  str(error))
        return bstack1lllll11l_opy_