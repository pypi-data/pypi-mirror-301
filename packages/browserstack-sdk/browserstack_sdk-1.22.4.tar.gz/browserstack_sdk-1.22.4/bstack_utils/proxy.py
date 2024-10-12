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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lllll111ll_opy_
bstack11l11l1ll_opy_ = Config.bstack1111l1lll_opy_()
def bstack1lll11ll111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll11lll1l_opy_(bstack1lll11lll11_opy_, bstack1lll11ll1ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll11lll11_opy_):
        with open(bstack1lll11lll11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll11ll111_opy_(bstack1lll11lll11_opy_):
        pac = get_pac(url=bstack1lll11lll11_opy_)
    else:
        raise Exception(bstack1111ll1_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪᖈ").format(bstack1lll11lll11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1111ll1_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧᖉ"), 80))
        bstack1lll11llll1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll11llll1_opy_ = bstack1111ll1_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ᖊ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll11ll1ll_opy_, bstack1lll11llll1_opy_)
    return proxy_url
def bstack1ll11111l_opy_(config):
    return bstack1111ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᖋ") in config or bstack1111ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᖌ") in config
def bstack1lll11llll_opy_(config):
    if not bstack1ll11111l_opy_(config):
        return
    if config.get(bstack1111ll1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᖍ")):
        return config.get(bstack1111ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᖎ"))
    if config.get(bstack1111ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᖏ")):
        return config.get(bstack1111ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᖐ"))
def bstack1lll1lll_opy_(config, bstack1lll11ll1ll_opy_):
    proxy = bstack1lll11llll_opy_(config)
    proxies = {}
    if config.get(bstack1111ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᖑ")) or config.get(bstack1111ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᖒ")):
        if proxy.endswith(bstack1111ll1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᖓ")):
            proxies = bstack11l1l1111_opy_(proxy, bstack1lll11ll1ll_opy_)
        else:
            proxies = {
                bstack1111ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᖔ"): proxy
            }
    bstack11l11l1ll_opy_.bstack11llllll1_opy_(bstack1111ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩᖕ"), proxies)
    return proxies
def bstack11l1l1111_opy_(bstack1lll11lll11_opy_, bstack1lll11ll1ll_opy_):
    proxies = {}
    global bstack1lll11ll1l1_opy_
    if bstack1111ll1_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭ᖖ") in globals():
        return bstack1lll11ll1l1_opy_
    try:
        proxy = bstack1lll11lll1l_opy_(bstack1lll11lll11_opy_, bstack1lll11ll1ll_opy_)
        if bstack1111ll1_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦᖗ") in proxy:
            proxies = {}
        elif bstack1111ll1_opy_ (u"ࠧࡎࡔࡕࡒࠥᖘ") in proxy or bstack1111ll1_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧᖙ") in proxy or bstack1111ll1_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨᖚ") in proxy:
            bstack1lll11ll11l_opy_ = proxy.split(bstack1111ll1_opy_ (u"ࠣࠢࠥᖛ"))
            if bstack1111ll1_opy_ (u"ࠤ࠽࠳࠴ࠨᖜ") in bstack1111ll1_opy_ (u"ࠥࠦᖝ").join(bstack1lll11ll11l_opy_[1:]):
                proxies = {
                    bstack1111ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᖞ"): bstack1111ll1_opy_ (u"ࠧࠨᖟ").join(bstack1lll11ll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1111ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᖠ"): str(bstack1lll11ll11l_opy_[0]).lower() + bstack1111ll1_opy_ (u"ࠢ࠻࠱࠲ࠦᖡ") + bstack1111ll1_opy_ (u"ࠣࠤᖢ").join(bstack1lll11ll11l_opy_[1:])
                }
        elif bstack1111ll1_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣᖣ") in proxy:
            bstack1lll11ll11l_opy_ = proxy.split(bstack1111ll1_opy_ (u"ࠥࠤࠧᖤ"))
            if bstack1111ll1_opy_ (u"ࠦ࠿࠵࠯ࠣᖥ") in bstack1111ll1_opy_ (u"ࠧࠨᖦ").join(bstack1lll11ll11l_opy_[1:]):
                proxies = {
                    bstack1111ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᖧ"): bstack1111ll1_opy_ (u"ࠢࠣᖨ").join(bstack1lll11ll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1111ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᖩ"): bstack1111ll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᖪ") + bstack1111ll1_opy_ (u"ࠥࠦᖫ").join(bstack1lll11ll11l_opy_[1:])
                }
        else:
            proxies = {
                bstack1111ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᖬ"): proxy
            }
    except Exception as e:
        print(bstack1111ll1_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤᖭ"), bstack1lllll111ll_opy_.format(bstack1lll11lll11_opy_, str(e)))
    bstack1lll11ll1l1_opy_ = proxies
    return proxies