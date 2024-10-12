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
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111l1l1111_opy_, bstack1l111llll_opy_, bstack1llll1l11_opy_, bstack11llllll1l_opy_, \
    bstack1111lll1ll_opy_
def bstack11lll1111_opy_(bstack1ll1llll111_opy_):
    for driver in bstack1ll1llll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1l1ll1_opy_(driver, status, reason=bstack1111ll1_opy_ (u"ࠪࠫᗣ")):
    bstack11l11l1ll_opy_ = Config.bstack1111l1lll_opy_()
    if bstack11l11l1ll_opy_.bstack11l1l111l1_opy_():
        return
    bstack1l11ll1ll1_opy_ = bstack1ll1ll111_opy_(bstack1111ll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᗤ"), bstack1111ll1_opy_ (u"ࠬ࠭ᗥ"), status, reason, bstack1111ll1_opy_ (u"࠭ࠧᗦ"), bstack1111ll1_opy_ (u"ࠧࠨᗧ"))
    driver.execute_script(bstack1l11ll1ll1_opy_)
def bstack11l1ll1ll_opy_(page, status, reason=bstack1111ll1_opy_ (u"ࠨࠩᗨ")):
    try:
        if page is None:
            return
        bstack11l11l1ll_opy_ = Config.bstack1111l1lll_opy_()
        if bstack11l11l1ll_opy_.bstack11l1l111l1_opy_():
            return
        bstack1l11ll1ll1_opy_ = bstack1ll1ll111_opy_(bstack1111ll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᗩ"), bstack1111ll1_opy_ (u"ࠪࠫᗪ"), status, reason, bstack1111ll1_opy_ (u"ࠫࠬᗫ"), bstack1111ll1_opy_ (u"ࠬ࠭ᗬ"))
        page.evaluate(bstack1111ll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᗭ"), bstack1l11ll1ll1_opy_)
    except Exception as e:
        print(bstack1111ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧᗮ"), e)
def bstack1ll1ll111_opy_(type, name, status, reason, bstack1ll1l1ll11_opy_, bstack1lll1l1l1l_opy_):
    bstack11ll1ll11_opy_ = {
        bstack1111ll1_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨᗯ"): type,
        bstack1111ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᗰ"): {}
    }
    if type == bstack1111ll1_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬᗱ"):
        bstack11ll1ll11_opy_[bstack1111ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᗲ")][bstack1111ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᗳ")] = bstack1ll1l1ll11_opy_
        bstack11ll1ll11_opy_[bstack1111ll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᗴ")][bstack1111ll1_opy_ (u"ࠧࡥࡣࡷࡥࠬᗵ")] = json.dumps(str(bstack1lll1l1l1l_opy_))
    if type == bstack1111ll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᗶ"):
        bstack11ll1ll11_opy_[bstack1111ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᗷ")][bstack1111ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨᗸ")] = name
    if type == bstack1111ll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᗹ"):
        bstack11ll1ll11_opy_[bstack1111ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᗺ")][bstack1111ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᗻ")] = status
        if status == bstack1111ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᗼ") and str(reason) != bstack1111ll1_opy_ (u"ࠣࠤᗽ"):
            bstack11ll1ll11_opy_[bstack1111ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᗾ")][bstack1111ll1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪᗿ")] = json.dumps(str(reason))
    bstack1llll1lll1_opy_ = bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩᘀ").format(json.dumps(bstack11ll1ll11_opy_))
    return bstack1llll1lll1_opy_
def bstack1111l1l11_opy_(url, config, logger, bstack1l1111l1l_opy_=False):
    hostname = bstack1l111llll_opy_(url)
    is_private = bstack11llllll1l_opy_(hostname)
    try:
        if is_private or bstack1l1111l1l_opy_:
            file_path = bstack111l1l1111_opy_(bstack1111ll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᘁ"), bstack1111ll1_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᘂ"), logger)
            if os.environ.get(bstack1111ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᘃ")) and eval(
                    os.environ.get(bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᘄ"))):
                return
            if (bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᘅ") in config and not config[bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᘆ")]):
                os.environ[bstack1111ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᘇ")] = str(True)
                bstack1ll1lll1ll1_opy_ = {bstack1111ll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧᘈ"): hostname}
                bstack1111lll1ll_opy_(bstack1111ll1_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᘉ"), bstack1111ll1_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬᘊ"), bstack1ll1lll1ll1_opy_, logger)
    except Exception as e:
        pass
def bstack1ll11lll_opy_(caps, bstack1ll1llll11l_opy_):
    if bstack1111ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᘋ") in caps:
        caps[bstack1111ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᘌ")][bstack1111ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩᘍ")] = True
        if bstack1ll1llll11l_opy_:
            caps[bstack1111ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᘎ")][bstack1111ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᘏ")] = bstack1ll1llll11l_opy_
    else:
        caps[bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫᘐ")] = True
        if bstack1ll1llll11l_opy_:
            caps[bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᘑ")] = bstack1ll1llll11l_opy_
def bstack1lll11l1ll1_opy_(bstack11ll11l111_opy_):
    bstack1ll1lll1lll_opy_ = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬᘒ"), bstack1111ll1_opy_ (u"ࠩࠪᘓ"))
    if bstack1ll1lll1lll_opy_ == bstack1111ll1_opy_ (u"ࠪࠫᘔ") or bstack1ll1lll1lll_opy_ == bstack1111ll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᘕ"):
        threading.current_thread().testStatus = bstack11ll11l111_opy_
    else:
        if bstack11ll11l111_opy_ == bstack1111ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᘖ"):
            threading.current_thread().testStatus = bstack11ll11l111_opy_