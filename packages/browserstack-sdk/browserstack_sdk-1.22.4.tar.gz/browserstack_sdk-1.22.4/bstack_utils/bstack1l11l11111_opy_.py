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
import datetime
import threading
from bstack_utils.helper import bstack11l11l11l1_opy_, bstack1l111111l_opy_, get_host_info, bstack111l111l11_opy_, \
 bstack1l111l1ll_opy_, bstack1llll1l11_opy_, bstack11l1lll111_opy_, bstack1111ll1111_opy_, bstack111lll1l_opy_
import bstack_utils.bstack1lllllll1l_opy_ as bstack11l11l111_opy_
from bstack_utils.bstack1111lll11_opy_ import bstack11lll1lll_opy_
from bstack_utils.percy import bstack111lll11_opy_
from bstack_utils.config import Config
bstack11l11l1ll_opy_ = Config.bstack1111l1lll_opy_()
logger = logging.getLogger(__name__)
percy = bstack111lll11_opy_()
@bstack11l1lll111_opy_(class_method=False)
def bstack1ll1l1l11l1_opy_(bs_config, bstack111l11l1l_opy_):
  try:
    data = {
        bstack1111ll1_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨ᜿"): bstack1111ll1_opy_ (u"ࠩ࡭ࡷࡴࡴࠧᝀ"),
        bstack1111ll1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩᝁ"): bs_config.get(bstack1111ll1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᝂ"), bstack1111ll1_opy_ (u"ࠬ࠭ᝃ")),
        bstack1111ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᝄ"): bs_config.get(bstack1111ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᝅ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1111ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᝆ"): bs_config.get(bstack1111ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᝇ")),
        bstack1111ll1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᝈ"): bs_config.get(bstack1111ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᝉ"), bstack1111ll1_opy_ (u"ࠬ࠭ᝊ")),
        bstack1111ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᝋ"): bstack111lll1l_opy_(),
        bstack1111ll1_opy_ (u"ࠧࡵࡣࡪࡷࠬᝌ"): bstack111l111l11_opy_(bs_config),
        bstack1111ll1_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫᝍ"): get_host_info(),
        bstack1111ll1_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪᝎ"): bstack1l111111l_opy_(),
        bstack1111ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᝏ"): os.environ.get(bstack1111ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪᝐ")),
        bstack1111ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪᝑ"): os.environ.get(bstack1111ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫᝒ"), False),
        bstack1111ll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩᝓ"): bstack11l11l11l1_opy_(),
        bstack1111ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᝔"): bstack1ll1l1111l1_opy_(),
        bstack1111ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭᝕"): bstack1ll11llll1l_opy_(bstack111l11l1l_opy_),
        bstack1111ll1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ᝖"): bstack11l1llll1_opy_(bs_config, bstack111l11l1l_opy_.get(bstack1111ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ᝗"), bstack1111ll1_opy_ (u"ࠬ࠭᝘"))),
        bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᝙"): bstack1l111l1ll_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1111ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ᝚").format(str(error)))
    return None
def bstack1ll11llll1l_opy_(framework):
  return {
    bstack1111ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ᝛"): framework.get(bstack1111ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ᝜"), bstack1111ll1_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ᝝")),
    bstack1111ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ᝞"): framework.get(bstack1111ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᝟")),
    bstack1111ll1_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᝠ"): framework.get(bstack1111ll1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᝡ")),
    bstack1111ll1_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪᝢ"): bstack1111ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᝣ"),
    bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᝤ"): framework.get(bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᝥ"))
  }
def bstack11l1llll1_opy_(bs_config, framework):
  bstack1ll1lll11_opy_ = False
  bstack1l11lll1l_opy_ = False
  if bstack1111ll1_opy_ (u"ࠬࡧࡰࡱࠩᝦ") in bs_config:
    bstack1ll1lll11_opy_ = True
  else:
    bstack1l11lll1l_opy_ = True
  bstack1ll1llll1l_opy_ = {
    bstack1111ll1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᝧ"): bstack11lll1lll_opy_.bstack1ll11llll11_opy_(bs_config, framework),
    bstack1111ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᝨ"): bstack11l11l111_opy_.bstack11l11111l1_opy_(bs_config),
    bstack1111ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᝩ"): bs_config.get(bstack1111ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᝪ"), False),
    bstack1111ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᝫ"): bstack1l11lll1l_opy_,
    bstack1111ll1_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪᝬ"): bstack1ll1lll11_opy_
  }
  return bstack1ll1llll1l_opy_
@bstack11l1lll111_opy_(class_method=False)
def bstack1ll1l1111l1_opy_():
  try:
    bstack1ll1l111111_opy_ = json.loads(os.getenv(bstack1111ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭᝭"), bstack1111ll1_opy_ (u"࠭ࡻࡾࠩᝮ")))
    return {
        bstack1111ll1_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩᝯ"): bstack1ll1l111111_opy_
    }
  except Exception as error:
    logger.error(bstack1111ll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢᝰ").format(str(error)))
    return {}
def bstack1ll1l1l1111_opy_(array, bstack1ll11lll1ll_opy_, bstack1ll11llllll_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll11lll1ll_opy_]
    result[key] = o[bstack1ll11llllll_opy_]
  return result
def bstack1ll1l1ll1ll_opy_(bstack1l111111ll_opy_=bstack1111ll1_opy_ (u"ࠩࠪ᝱")):
  bstack1ll11lll1l1_opy_ = bstack11l11l111_opy_.on()
  bstack1ll11lll11l_opy_ = bstack11lll1lll_opy_.on()
  bstack1ll11lllll1_opy_ = percy.bstack111111ll1_opy_()
  if bstack1ll11lllll1_opy_ and not bstack1ll11lll11l_opy_ and not bstack1ll11lll1l1_opy_:
    return bstack1l111111ll_opy_ not in [bstack1111ll1_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧᝲ"), bstack1111ll1_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᝳ")]
  elif bstack1ll11lll1l1_opy_ and not bstack1ll11lll11l_opy_:
    return bstack1l111111ll_opy_ not in [bstack1111ll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭᝴"), bstack1111ll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ᝵"), bstack1111ll1_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ᝶")]
  return bstack1ll11lll1l1_opy_ or bstack1ll11lll11l_opy_ or bstack1ll11lllll1_opy_
@bstack11l1lll111_opy_(class_method=False)
def bstack1ll1l1l11ll_opy_(bstack1l111111ll_opy_, test=None):
  bstack1ll1l11111l_opy_ = bstack11l11l111_opy_.on()
  if not bstack1ll1l11111l_opy_ or bstack1l111111ll_opy_ not in [bstack1111ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ᝷")] or test == None:
    return None
  return {
    bstack1111ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᝸"): bstack1ll1l11111l_opy_ and bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᝹"), None) == True and bstack11l11l111_opy_.bstack1l111l11_opy_(test[bstack1111ll1_opy_ (u"ࠫࡹࡧࡧࡴࠩ᝺")])
  }