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
import json
import logging
import os
import datetime
import threading
from bstack_utils.helper import bstack11l1111l11_opy_, bstack11l11l1ll1_opy_, bstack1ll1llllll_opy_, bstack11l1lll111_opy_, bstack111111l111_opy_, bstack111l1111l1_opy_, bstack1111ll1111_opy_, bstack111lll1l_opy_
from bstack_utils.bstack1lll1111l11_opy_ import bstack1lll11111ll_opy_
import bstack_utils.bstack1l11l11111_opy_ as bstack1ll11l1l1_opy_
from bstack_utils.bstack1111lll11_opy_ import bstack11lll1lll_opy_
import bstack_utils.bstack1lllllll1l_opy_ as bstack11l11l111_opy_
from bstack_utils.bstack1l1lll1l_opy_ import bstack1l1lll1l_opy_
from bstack_utils.bstack11lll1111l_opy_ import bstack11l1ll1l1l_opy_
bstack1ll1l11llll_opy_ = bstack1111ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᙖ")
logger = logging.getLogger(__name__)
class bstack1l1111l11_opy_:
    bstack1lll1111l11_opy_ = None
    bs_config = None
    bstack111l11l1l_opy_ = None
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def launch(cls, bs_config, bstack111l11l1l_opy_):
        cls.bs_config = bs_config
        cls.bstack111l11l1l_opy_ = bstack111l11l1l_opy_
        try:
            cls.bstack1ll1l111lll_opy_()
            bstack11l111lll1_opy_ = bstack11l1111l11_opy_(bs_config)
            bstack11l1111l1l_opy_ = bstack11l11l1ll1_opy_(bs_config)
            data = bstack1ll11l1l1_opy_.bstack1ll1l1l11l1_opy_(bs_config, bstack111l11l1l_opy_)
            config = {
                bstack1111ll1_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᙗ"): (bstack11l111lll1_opy_, bstack11l1111l1l_opy_),
                bstack1111ll1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᙘ"): cls.default_headers()
            }
            response = bstack1ll1llllll_opy_(bstack1111ll1_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᙙ"), cls.request_url(bstack1111ll1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠴࠲ࡦࡺ࡯࡬ࡥࡵࠪᙚ")), data, config)
            if response.status_code != 200:
                bstack1ll1l11l1ll_opy_ = response.json()
                if bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᙛ")] == False:
                    cls.bstack1ll1l1ll1l1_opy_(bstack1ll1l11l1ll_opy_)
                    return
                cls.bstack1ll1l11l11l_opy_(bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᙜ")])
                cls.bstack1ll1l1l1ll1_opy_(bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᙝ")])
                return None
            bstack1ll1ll11111_opy_ = cls.bstack1ll1l1l1l11_opy_(response)
            return bstack1ll1ll11111_opy_
        except Exception as error:
            logger.error(bstack1111ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁࠧᙞ").format(str(error)))
            return None
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def stop(cls, bstack1ll1l1lll11_opy_=None):
        if not bstack11lll1lll_opy_.on() and not bstack11l11l111_opy_.on():
            return
        if os.environ.get(bstack1111ll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᙟ")) == bstack1111ll1_opy_ (u"ࠤࡱࡹࡱࡲࠢᙠ") or os.environ.get(bstack1111ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᙡ")) == bstack1111ll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᙢ"):
            logger.error(bstack1111ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᙣ"))
            return {
                bstack1111ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᙤ"): bstack1111ll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᙥ"),
                bstack1111ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᙦ"): bstack1111ll1_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧᙧ")
            }
        try:
            cls.bstack1lll1111l11_opy_.shutdown()
            data = {
                bstack1111ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᙨ"): bstack111lll1l_opy_()
            }
            if not bstack1ll1l1lll11_opy_ is None:
                data[bstack1111ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠨᙩ")] = [{
                    bstack1111ll1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᙪ"): bstack1111ll1_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫᙫ"),
                    bstack1111ll1_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧᙬ"): bstack1ll1l1lll11_opy_
                }]
            config = {
                bstack1111ll1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ᙭"): cls.default_headers()
            }
            bstack1111lll1l1_opy_ = bstack1111ll1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪ᙮").format(os.environ[bstack1111ll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣᙯ")])
            bstack1ll1l11l1l1_opy_ = cls.request_url(bstack1111lll1l1_opy_)
            response = bstack1ll1llllll_opy_(bstack1111ll1_opy_ (u"ࠫࡕ࡛ࡔࠨᙰ"), bstack1ll1l11l1l1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1111ll1_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦᙱ"))
        except Exception as error:
            logger.error(bstack1111ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺࠻ࠢࠥᙲ") + str(error))
            return {
                bstack1111ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᙳ"): bstack1111ll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᙴ"),
                bstack1111ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᙵ"): str(error)
            }
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def bstack1ll1l1l1l11_opy_(cls, response):
        bstack1ll1l11l1ll_opy_ = response.json()
        bstack1ll1ll11111_opy_ = {}
        if bstack1ll1l11l1ll_opy_.get(bstack1111ll1_opy_ (u"ࠪ࡮ࡼࡺࠧᙶ")) is None:
            os.environ[bstack1111ll1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᙷ")] = bstack1111ll1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᙸ")
        else:
            os.environ[bstack1111ll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᙹ")] = bstack1ll1l11l1ll_opy_.get(bstack1111ll1_opy_ (u"ࠧ࡫ࡹࡷࠫᙺ"), bstack1111ll1_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᙻ"))
        os.environ[bstack1111ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᙼ")] = bstack1ll1l11l1ll_opy_.get(bstack1111ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᙽ"), bstack1111ll1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᙾ"))
        if bstack11lll1lll_opy_.bstack1ll1l11ll1l_opy_(cls.bs_config, cls.bstack111l11l1l_opy_.get(bstack1111ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ᙿ"), bstack1111ll1_opy_ (u"࠭ࠧ "))) is True:
            bstack1ll1l1llll1_opy_, bstack1ll1l111ll1_opy_, bstack1ll1l1ll11l_opy_ = cls.bstack1ll1l1lllll_opy_(bstack1ll1l11l1ll_opy_)
            if bstack1ll1l1llll1_opy_ != None and bstack1ll1l111ll1_opy_ != None:
                bstack1ll1ll11111_opy_[bstack1111ll1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᚁ")] = {
                    bstack1111ll1_opy_ (u"ࠨ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠫᚂ"): bstack1ll1l1llll1_opy_,
                    bstack1111ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᚃ"): bstack1ll1l111ll1_opy_,
                    bstack1111ll1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᚄ"): bstack1ll1l1ll11l_opy_
                }
            else:
                bstack1ll1ll11111_opy_[bstack1111ll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᚅ")] = {}
        else:
            bstack1ll1ll11111_opy_[bstack1111ll1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᚆ")] = {}
        if bstack11l11l111_opy_.bstack11l11111l1_opy_(cls.bs_config) is True:
            bstack1ll1l1l1l1l_opy_, bstack1ll1l111ll1_opy_ = cls.bstack1ll1l1111ll_opy_(bstack1ll1l11l1ll_opy_)
            if bstack1ll1l1l1l1l_opy_ != None and bstack1ll1l111ll1_opy_ != None:
                bstack1ll1ll11111_opy_[bstack1111ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚇ")] = {
                    bstack1111ll1_opy_ (u"ࠧࡢࡷࡷ࡬ࡤࡺ࡯࡬ࡧࡱࠫᚈ"): bstack1ll1l1l1l1l_opy_,
                    bstack1111ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᚉ"): bstack1ll1l111ll1_opy_,
                }
            else:
                bstack1ll1ll11111_opy_[bstack1111ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᚊ")] = {}
        else:
            bstack1ll1ll11111_opy_[bstack1111ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚋ")] = {}
        if bstack1ll1ll11111_opy_[bstack1111ll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᚌ")].get(bstack1111ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᚍ")) != None or bstack1ll1ll11111_opy_[bstack1111ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚎ")].get(bstack1111ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᚏ")) != None:
            cls.bstack1ll1l1l111l_opy_(bstack1ll1l11l1ll_opy_.get(bstack1111ll1_opy_ (u"ࠨ࡬ࡺࡸࠬᚐ")), bstack1ll1l11l1ll_opy_.get(bstack1111ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᚑ")))
        return bstack1ll1ll11111_opy_
    @classmethod
    def bstack1ll1l1lllll_opy_(cls, bstack1ll1l11l1ll_opy_):
        if bstack1ll1l11l1ll_opy_.get(bstack1111ll1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᚒ")) == None:
            cls.bstack1ll1l11l11l_opy_()
            return [None, None, None]
        if bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᚓ")][bstack1111ll1_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᚔ")] != True:
            cls.bstack1ll1l11l11l_opy_(bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᚕ")])
            return [None, None, None]
        logger.debug(bstack1111ll1_opy_ (u"ࠧࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫᚖ"))
        os.environ[bstack1111ll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧᚗ")] = bstack1111ll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᚘ")
        if bstack1ll1l11l1ll_opy_.get(bstack1111ll1_opy_ (u"ࠪ࡮ࡼࡺࠧᚙ")):
            os.environ[bstack1111ll1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᚚ")] = bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"ࠬࡰࡷࡵࠩ᚛")]
            os.environ[bstack1111ll1_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪ᚜")] = json.dumps({
                bstack1111ll1_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ᚝"): bstack11l1111l11_opy_(cls.bs_config),
                bstack1111ll1_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪ᚞"): bstack11l11l1ll1_opy_(cls.bs_config)
            })
        if bstack1ll1l11l1ll_opy_.get(bstack1111ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ᚟")):
            os.environ[bstack1111ll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᚠ")] = bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᚡ")]
        if bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᚢ")].get(bstack1111ll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᚣ"), {}).get(bstack1111ll1_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᚤ")):
            os.environ[bstack1111ll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩᚥ")] = str(bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᚦ")][bstack1111ll1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᚧ")][bstack1111ll1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᚨ")])
        return [bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"ࠬࡰࡷࡵࠩᚩ")], bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᚪ")], os.environ[bstack1111ll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᚫ")]]
    @classmethod
    def bstack1ll1l1111ll_opy_(cls, bstack1ll1l11l1ll_opy_):
        if bstack1ll1l11l1ll_opy_.get(bstack1111ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᚬ")) == None:
            cls.bstack1ll1l1l1ll1_opy_()
            return [None, None]
        if bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᚭ")][bstack1111ll1_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᚮ")] != True:
            cls.bstack1ll1l1l1ll1_opy_(bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᚯ")])
            return [None, None]
        if bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚰ")].get(bstack1111ll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᚱ")):
            logger.debug(bstack1111ll1_opy_ (u"ࠧࡕࡧࡶࡸࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫᚲ"))
            parsed = json.loads(os.getenv(bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᚳ"), bstack1111ll1_opy_ (u"ࠩࡾࢁࠬᚴ")))
            capabilities = bstack1ll11l1l1_opy_.bstack1ll1l1l1111_opy_(bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚵ")][bstack1111ll1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᚶ")][bstack1111ll1_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᚷ")], bstack1111ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᚸ"), bstack1111ll1_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ᚹ"))
            bstack1ll1l1l1l1l_opy_ = capabilities[bstack1111ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭ᚺ")]
            os.environ[bstack1111ll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᚻ")] = bstack1ll1l1l1l1l_opy_
            parsed[bstack1111ll1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᚼ")] = capabilities[bstack1111ll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᚽ")]
            os.environ[bstack1111ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᚾ")] = json.dumps(parsed)
            scripts = bstack1ll11l1l1_opy_.bstack1ll1l1l1111_opy_(bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚿ")][bstack1111ll1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨᛀ")][bstack1111ll1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᛁ")], bstack1111ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᛂ"), bstack1111ll1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࠫᛃ"))
            bstack1l1lll1l_opy_.bstack111lllll1l_opy_(scripts)
            commands = bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᛄ")][bstack1111ll1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᛅ")][bstack1111ll1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠧᛆ")].get(bstack1111ll1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᛇ"))
            bstack1l1lll1l_opy_.bstack11l111ll1l_opy_(commands)
            bstack1l1lll1l_opy_.store()
        return [bstack1ll1l1l1l1l_opy_, bstack1ll1l11l1ll_opy_[bstack1111ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᛈ")]]
    @classmethod
    def bstack1ll1l11l11l_opy_(cls, response=None):
        os.environ[bstack1111ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᛉ")] = bstack1111ll1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᛊ")
        os.environ[bstack1111ll1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪᛋ")] = bstack1111ll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᛌ")
        os.environ[bstack1111ll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᛍ")] = bstack1111ll1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᛎ")
        os.environ[bstack1111ll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᛏ")] = bstack1111ll1_opy_ (u"ࠩࡱࡹࡱࡲࠧᛐ")
        os.environ[bstack1111ll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᛑ")] = bstack1111ll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᛒ")
        os.environ[bstack1111ll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᛓ")] = bstack1111ll1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᛔ")
        cls.bstack1ll1l1ll1l1_opy_(response, bstack1111ll1_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢᛕ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l1l1ll1_opy_(cls, response=None):
        os.environ[bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᛖ")] = bstack1111ll1_opy_ (u"ࠩࡱࡹࡱࡲࠧᛗ")
        os.environ[bstack1111ll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᛘ")] = bstack1111ll1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᛙ")
        os.environ[bstack1111ll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᛚ")] = bstack1111ll1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᛛ")
        cls.bstack1ll1l1ll1l1_opy_(response, bstack1111ll1_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢᛜ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l1l111l_opy_(cls, bstack1ll1l11lll1_opy_, bstack1ll1l111ll1_opy_):
        os.environ[bstack1111ll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᛝ")] = bstack1ll1l11lll1_opy_
        os.environ[bstack1111ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᛞ")] = bstack1ll1l111ll1_opy_
    @classmethod
    def bstack1ll1l1ll1l1_opy_(cls, response=None, product=bstack1111ll1_opy_ (u"ࠥࠦᛟ")):
        if response == None:
            logger.error(product + bstack1111ll1_opy_ (u"ࠦࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠨᛠ"))
        for error in response[bstack1111ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬᛡ")]:
            bstack111l111111_opy_ = error[bstack1111ll1_opy_ (u"࠭࡫ࡦࡻࠪᛢ")]
            error_message = error[bstack1111ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᛣ")]
            if error_message:
                if bstack111l111111_opy_ == bstack1111ll1_opy_ (u"ࠣࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊࠢᛤ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1111ll1_opy_ (u"ࠤࡇࡥࡹࡧࠠࡶࡲ࡯ࡳࡦࡪࠠࡵࡱࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࠥᛥ") + product + bstack1111ll1_opy_ (u"ࠥࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᛦ"))
    @classmethod
    def bstack1ll1l111lll_opy_(cls):
        if cls.bstack1lll1111l11_opy_ is not None:
            return
        cls.bstack1lll1111l11_opy_ = bstack1lll11111ll_opy_(cls.bstack1ll1l1l1lll_opy_)
        cls.bstack1lll1111l11_opy_.start()
    @classmethod
    def bstack11l1ll1lll_opy_(cls):
        if cls.bstack1lll1111l11_opy_ is None:
            return
        cls.bstack1lll1111l11_opy_.shutdown()
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def bstack1ll1l1l1lll_opy_(cls, bstack11l1ll1l11_opy_, bstack1ll1l11l111_opy_=bstack1111ll1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᛧ")):
        config = {
            bstack1111ll1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᛨ"): cls.default_headers()
        }
        response = bstack1ll1llllll_opy_(bstack1111ll1_opy_ (u"࠭ࡐࡐࡕࡗࠫᛩ"), cls.request_url(bstack1ll1l11l111_opy_), bstack11l1ll1l11_opy_, config)
        bstack111llll11l_opy_ = response.json()
    @classmethod
    def bstack11l1llll1l_opy_(cls, bstack11l1ll1l11_opy_, bstack1ll1l11l111_opy_=bstack1111ll1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᛪ")):
        if not bstack1ll11l1l1_opy_.bstack1ll1l1ll1ll_opy_(bstack11l1ll1l11_opy_[bstack1111ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ᛫")]):
            return
        bstack1ll1llll1l_opy_ = bstack1ll11l1l1_opy_.bstack1ll1l1l11ll_opy_(bstack11l1ll1l11_opy_[bstack1111ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭᛬")], bstack11l1ll1l11_opy_.get(bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ᛭")))
        if bstack1ll1llll1l_opy_ != None:
            if bstack11l1ll1l11_opy_.get(bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᛮ")) != None:
                bstack11l1ll1l11_opy_[bstack1111ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᛯ")][bstack1111ll1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫᛰ")] = bstack1ll1llll1l_opy_
            else:
                bstack11l1ll1l11_opy_[bstack1111ll1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬᛱ")] = bstack1ll1llll1l_opy_
        if bstack1ll1l11l111_opy_ == bstack1111ll1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᛲ"):
            cls.bstack1ll1l111lll_opy_()
            cls.bstack1lll1111l11_opy_.add(bstack11l1ll1l11_opy_)
        elif bstack1ll1l11l111_opy_ == bstack1111ll1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᛳ"):
            cls.bstack1ll1l1l1lll_opy_([bstack11l1ll1l11_opy_], bstack1ll1l11l111_opy_)
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def bstack1l1111l1_opy_(cls, bstack11ll11ll11_opy_):
        bstack1ll1l111l11_opy_ = []
        for log in bstack11ll11ll11_opy_:
            bstack1ll1l111l1l_opy_ = {
                bstack1111ll1_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᛴ"): bstack1111ll1_opy_ (u"࡙ࠫࡋࡓࡕࡡࡏࡓࡌ࠭ᛵ"),
                bstack1111ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᛶ"): log[bstack1111ll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᛷ")],
                bstack1111ll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᛸ"): log[bstack1111ll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ᛹")],
                bstack1111ll1_opy_ (u"ࠩ࡫ࡸࡹࡶ࡟ࡳࡧࡶࡴࡴࡴࡳࡦࠩ᛺"): {},
                bstack1111ll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᛻"): log[bstack1111ll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᛼")],
            }
            if bstack1111ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᛽") in log:
                bstack1ll1l111l1l_opy_[bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭᛾")] = log[bstack1111ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᛿")]
            elif bstack1111ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᜀ") in log:
                bstack1ll1l111l1l_opy_[bstack1111ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᜁ")] = log[bstack1111ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᜂ")]
            bstack1ll1l111l11_opy_.append(bstack1ll1l111l1l_opy_)
        cls.bstack11l1llll1l_opy_({
            bstack1111ll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᜃ"): bstack1111ll1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᜄ"),
            bstack1111ll1_opy_ (u"࠭࡬ࡰࡩࡶࠫᜅ"): bstack1ll1l111l11_opy_
        })
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def bstack1ll1ll1111l_opy_(cls, steps):
        bstack1ll1l11ll11_opy_ = []
        for step in steps:
            bstack1ll1l1ll111_opy_ = {
                bstack1111ll1_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᜆ"): bstack1111ll1_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡕࡇࡓࠫᜇ"),
                bstack1111ll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᜈ"): step[bstack1111ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᜉ")],
                bstack1111ll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᜊ"): step[bstack1111ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᜋ")],
                bstack1111ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᜌ"): step[bstack1111ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᜍ")],
                bstack1111ll1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᜎ"): step[bstack1111ll1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᜏ")]
            }
            if bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᜐ") in step:
                bstack1ll1l1ll111_opy_[bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᜑ")] = step[bstack1111ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᜒ")]
            elif bstack1111ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᜓ") in step:
                bstack1ll1l1ll111_opy_[bstack1111ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪ᜔ࠧ")] = step[bstack1111ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᜕")]
            bstack1ll1l11ll11_opy_.append(bstack1ll1l1ll111_opy_)
        cls.bstack11l1llll1l_opy_({
            bstack1111ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭᜖"): bstack1111ll1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ᜗"),
            bstack1111ll1_opy_ (u"ࠫࡱࡵࡧࡴࠩ᜘"): bstack1ll1l11ll11_opy_
        })
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def bstack1ll111lll1_opy_(cls, screenshot):
        cls.bstack11l1llll1l_opy_({
            bstack1111ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ᜙"): bstack1111ll1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ᜚"),
            bstack1111ll1_opy_ (u"ࠧ࡭ࡱࡪࡷࠬ᜛"): [{
                bstack1111ll1_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭᜜"): bstack1111ll1_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠫ᜝"),
                bstack1111ll1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭᜞"): datetime.datetime.utcnow().isoformat() + bstack1111ll1_opy_ (u"ࠫ࡟࠭ᜟ"),
                bstack1111ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᜠ"): screenshot[bstack1111ll1_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬᜡ")],
                bstack1111ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᜢ"): screenshot[bstack1111ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᜣ")]
            }]
        }, bstack1ll1l11l111_opy_=bstack1111ll1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᜤ"))
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def bstack1ll111l11_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l1llll1l_opy_({
            bstack1111ll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᜥ"): bstack1111ll1_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨᜦ"),
            bstack1111ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᜧ"): {
                bstack1111ll1_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᜨ"): cls.current_test_uuid(),
                bstack1111ll1_opy_ (u"ࠢࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸࠨᜩ"): cls.bstack11ll1llll1_opy_(driver)
            }
        })
    @classmethod
    def bstack11lll11111_opy_(cls, event: str, bstack11l1ll1l11_opy_: bstack11l1ll1l1l_opy_):
        bstack11ll1lll11_opy_ = {
            bstack1111ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᜪ"): event,
            bstack11l1ll1l11_opy_.bstack11ll1l1lll_opy_(): bstack11l1ll1l11_opy_.bstack11l1lll11l_opy_(event)
        }
        cls.bstack11l1llll1l_opy_(bstack11ll1lll11_opy_)
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1111ll1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᜫ"), None) is None or os.environ[bstack1111ll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᜬ")] == bstack1111ll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᜭ")) and (os.environ.get(bstack1111ll1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᜮ"), None) is None or os.environ[bstack1111ll1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᜯ")] == bstack1111ll1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᜰ")):
            return False
        return True
    @staticmethod
    def bstack1ll1l1lll1l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1111l11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1111ll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᜱ"): bstack1111ll1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᜲ"),
            bstack1111ll1_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭ᜳ"): bstack1111ll1_opy_ (u"ࠫࡹࡸࡵࡦ᜴ࠩ")
        }
        if os.environ.get(bstack1111ll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭᜵"), None):
            headers[bstack1111ll1_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭᜶")] = bstack1111ll1_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ᜷").format(os.environ[bstack1111ll1_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠤ᜸")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1111ll1_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨ᜹").format(bstack1ll1l11llll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1111ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ᜺"), None)
    @staticmethod
    def bstack11ll1llll1_opy_(driver):
        return {
            bstack111111l111_opy_(): bstack111l1111l1_opy_(driver)
        }
    @staticmethod
    def bstack1ll1ll111l1_opy_(exception_info, report):
        return [{bstack1111ll1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ᜻"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11l11ll1ll_opy_(typename):
        if bstack1111ll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ᜼") in typename:
            return bstack1111ll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ᜽")
        return bstack1111ll1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ᜾")