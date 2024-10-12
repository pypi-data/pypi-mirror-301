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
import re
bstack1ll1ll1111_opy_ = {
	bstack1111ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࿜"): bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࠬ࿝"),
  bstack1111ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ࿞"): bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡮ࡩࡾ࠭࿟"),
  bstack1111ll1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ࿠"): bstack1111ll1_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࿡"),
  bstack1111ll1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭࿢"): bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡢࡻ࠸ࡩࠧ࿣"),
  bstack1111ll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭࿤"): bstack1111ll1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࠪ࿥"),
  bstack1111ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭࿦"): bstack1111ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࠪ࿧"),
  bstack1111ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ࿨"): bstack1111ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ࿩"),
  bstack1111ll1_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭࿪"): bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥࡧࡥࡹ࡬࠭࿫"),
  bstack1111ll1_opy_ (u"ࠩࡦࡳࡳࡹ࡯࡭ࡧࡏࡳ࡬ࡹࠧ࿬"): bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡳࡹ࡯࡭ࡧࠪ࿭"),
  bstack1111ll1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩ࿮"): bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩ࿯"),
  bstack1111ll1_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪ࿰"): bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪ࿱"),
  bstack1111ll1_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࠧ࿲"): bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡸ࡬ࡨࡪࡵࠧ࿳"),
  bstack1111ll1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩ࿴"): bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩ࿵"),
  bstack1111ll1_opy_ (u"ࠬࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬ࿶"): bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬ࿷"),
  bstack1111ll1_opy_ (u"ࠧࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬ࿸"): bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬ࿹"),
  bstack1111ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫ࿺"): bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫ࿻"),
  bstack1111ll1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭࿼"): bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ࿽"),
  bstack1111ll1_opy_ (u"࠭࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬ࿾"): bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬ࿿"),
  bstack1111ll1_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭က"): bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ခ"),
  bstack1111ll1_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪဂ"): bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪဃ"),
  bstack1111ll1_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧင"): bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡯ࡦࡎࡩࡾࡹࠧစ"),
  bstack1111ll1_opy_ (u"ࠧࡢࡷࡷࡳ࡜ࡧࡩࡵࠩဆ"): bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡷࡷࡳ࡜ࡧࡩࡵࠩဇ"),
  bstack1111ll1_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨဈ"): bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡫ࡳࡸࡺࡳࠨဉ"),
  bstack1111ll1_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬည"): bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧ࡬ࡣࡢࡥ࡫ࡩࠬဋ"),
  bstack1111ll1_opy_ (u"࠭ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧဌ"): bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧဍ"),
  bstack1111ll1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫဎ"): bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫဏ"),
  bstack1111ll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧတ"): bstack1111ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫထ"),
  bstack1111ll1_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩဒ"): bstack1111ll1_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫဓ"),
  bstack1111ll1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧန"): bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨပ"),
  bstack1111ll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩဖ"): bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩဗ"),
  bstack1111ll1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬဘ"): bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬမ"),
  bstack1111ll1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬယ"): bstack1111ll1_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࡳࠨရ"),
  bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪလ"): bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪဝ"),
  bstack1111ll1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪသ"): bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡴࡻࡲࡤࡧࠪဟ"),
  bstack1111ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧဠ"): bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧအ"),
  bstack1111ll1_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩဢ"): bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡓࡧ࡭ࡦࠩဣ"),
  bstack1111ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬဤ"): bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬဥ"),
  bstack1111ll1_opy_ (u"ࠫࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨဦ"): bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨဧ"),
  bstack1111ll1_opy_ (u"࠭ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫဨ"): bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫဩ")
}
bstack111ll111ll_opy_ = [
  bstack1111ll1_opy_ (u"ࠨࡱࡶࠫဪ"),
  bstack1111ll1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬါ"),
  bstack1111ll1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬာ"),
  bstack1111ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩိ"),
  bstack1111ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩီ"),
  bstack1111ll1_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪု"),
  bstack1111ll1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧူ"),
]
bstack1ll11lll11_opy_ = {
  bstack1111ll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪေ"): [bstack1111ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪဲ"), bstack1111ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘ࡟ࡏࡃࡐࡉࠬဳ")],
  bstack1111ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧဴ"): bstack1111ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨဵ"),
  bstack1111ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩံ"): bstack1111ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇ့ࠪ"),
  bstack1111ll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭း"): bstack1111ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋ္ࠧ"),
  bstack1111ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ်ࠬ"): bstack1111ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ျ"),
  bstack1111ll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬြ"): bstack1111ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡁࡓࡃࡏࡐࡊࡒࡓࡠࡒࡈࡖࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧွ"),
  bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫှ"): bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑ࠭ဿ"),
  bstack1111ll1_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭၀"): bstack1111ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧ၁"),
  bstack1111ll1_opy_ (u"ࠫࡦࡶࡰࠨ၂"): [bstack1111ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡖࡐࡠࡋࡇࠫ၃"), bstack1111ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡐࡑࠩ၄")],
  bstack1111ll1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ၅"): bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡔࡆࡎࡣࡑࡕࡇࡍࡇ࡙ࡉࡑ࠭၆"),
  bstack1111ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭၇"): bstack1111ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭၈"),
  bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ၉"): bstack1111ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡒࡆࡘࡋࡒࡗࡃࡅࡍࡑࡏࡔ࡚ࠩ၊")
}
bstack1l111ll111_opy_ = {
  bstack1111ll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ။"): [bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡵࡣࡳࡧ࡭ࡦࠩ၌"), bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ၍")],
  bstack1111ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ၎"): [bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡡ࡮ࡩࡾ࠭၏"), bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ၐ")],
  bstack1111ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨၑ"): bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨၒ"),
  bstack1111ll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬၓ"): bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬၔ"),
  bstack1111ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫၕ"): bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫၖ"),
  bstack1111ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫၗ"): [bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡶࡰࠨၘ"), bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬၙ")],
  bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫၚ"): bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ၛ"),
  bstack1111ll1_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ၜ"): bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ၝ"),
  bstack1111ll1_opy_ (u"ࠫࡦࡶࡰࠨၞ"): bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࠨၟ"),
  bstack1111ll1_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨၠ"): bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨၡ"),
  bstack1111ll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬၢ"): bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬၣ")
}
bstack1l1l1111ll_opy_ = {
  bstack1111ll1_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ၤ"): bstack1111ll1_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨၥ"),
  bstack1111ll1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧၦ"): [bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨၧ"), bstack1111ll1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪၨ")],
  bstack1111ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ၩ"): bstack1111ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧၪ"),
  bstack1111ll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧၫ"): bstack1111ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫၬ"),
  bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪၭ"): [bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧၮ"), bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ၯ")],
  bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩၰ"): bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫၱ"),
  bstack1111ll1_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧၲ"): bstack1111ll1_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩၳ"),
  bstack1111ll1_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬၴ"): [bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ၵ"), bstack1111ll1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨၶ")],
  bstack1111ll1_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧၷ"): [bstack1111ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵࠪၸ"), bstack1111ll1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࠪၹ")]
}
bstack11llllll11_opy_ = [
  bstack1111ll1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪၺ"),
  bstack1111ll1_opy_ (u"ࠬࡶࡡࡨࡧࡏࡳࡦࡪࡓࡵࡴࡤࡸࡪ࡭ࡹࠨၻ"),
  bstack1111ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬၼ"),
  bstack1111ll1_opy_ (u"ࠧࡴࡧࡷ࡛࡮ࡴࡤࡰࡹࡕࡩࡨࡺࠧၽ"),
  bstack1111ll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡵࡵࡵࡵࠪၾ"),
  bstack1111ll1_opy_ (u"ࠩࡶࡸࡷ࡯ࡣࡵࡈ࡬ࡰࡪࡏ࡮ࡵࡧࡵࡥࡨࡺࡡࡣ࡫࡯࡭ࡹࡿࠧၿ"),
  bstack1111ll1_opy_ (u"ࠪࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡖࡲࡰ࡯ࡳࡸࡇ࡫ࡨࡢࡸ࡬ࡳࡷ࠭ႀ"),
  bstack1111ll1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩႁ"),
  bstack1111ll1_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪႂ"),
  bstack1111ll1_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧႃ"),
  bstack1111ll1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ႄ"),
  bstack1111ll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩႅ"),
]
bstack1l1l1l1111_opy_ = [
  bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ႆ"),
  bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧႇ"),
  bstack1111ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪႈ"),
  bstack1111ll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬႉ"),
  bstack1111ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩႊ"),
  bstack1111ll1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩႋ"),
  bstack1111ll1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫႌ"),
  bstack1111ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾႍ࠭"),
  bstack1111ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ႎ"),
  bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩႏ"),
  bstack1111ll1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ႐"),
  bstack1111ll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨ႑"),
  bstack1111ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡔࡢࡩࠪ႒"),
  bstack1111ll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ႓"),
  bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ႔"),
  bstack1111ll1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧ႕"),
  bstack1111ll1_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠳ࠪ႖"),
  bstack1111ll1_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠵ࠫ႗"),
  bstack1111ll1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠷ࠬ႘"),
  bstack1111ll1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠹࠭႙"),
  bstack1111ll1_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠻ࠧႚ"),
  bstack1111ll1_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠶ࠨႛ"),
  bstack1111ll1_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠸ࠩႜ"),
  bstack1111ll1_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠺ࠪႝ"),
  bstack1111ll1_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠼ࠫ႞"),
  bstack1111ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ႟"),
  bstack1111ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭Ⴀ"),
  bstack1111ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫႡ"),
  bstack1111ll1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫႢ")
]
bstack111l1lll1l_opy_ = [
  bstack1111ll1_opy_ (u"ࠪࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨႣ"),
  bstack1111ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭Ⴄ"),
  bstack1111ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨႥ"),
  bstack1111ll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫႦ"),
  bstack1111ll1_opy_ (u"ࠧࡵࡧࡶࡸࡕࡸࡩࡰࡴ࡬ࡸࡾ࠭Ⴇ"),
  bstack1111ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫႨ"),
  bstack1111ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡕࡣࡪࠫႩ"),
  bstack1111ll1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨႪ"),
  bstack1111ll1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ⴋ"),
  bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪႬ"),
  bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧႭ"),
  bstack1111ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭Ⴎ"),
  bstack1111ll1_opy_ (u"ࠨࡱࡶࠫႯ"),
  bstack1111ll1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬႰ"),
  bstack1111ll1_opy_ (u"ࠪ࡬ࡴࡹࡴࡴࠩႱ"),
  bstack1111ll1_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭Ⴒ"),
  bstack1111ll1_opy_ (u"ࠬࡸࡥࡨ࡫ࡲࡲࠬႳ"),
  bstack1111ll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨႴ"),
  bstack1111ll1_opy_ (u"ࠧ࡮ࡣࡦ࡬࡮ࡴࡥࠨႵ"),
  bstack1111ll1_opy_ (u"ࠨࡴࡨࡷࡴࡲࡵࡵ࡫ࡲࡲࠬႶ"),
  bstack1111ll1_opy_ (u"ࠩ࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧႷ"),
  bstack1111ll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧႸ"),
  bstack1111ll1_opy_ (u"ࠫࡻ࡯ࡤࡦࡱࠪႹ"),
  bstack1111ll1_opy_ (u"ࠬࡴ࡯ࡑࡣࡪࡩࡑࡵࡡࡥࡖ࡬ࡱࡪࡵࡵࡵࠩႺ"),
  bstack1111ll1_opy_ (u"࠭ࡢࡧࡥࡤࡧ࡭࡫ࠧႻ"),
  bstack1111ll1_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭Ⴜ"),
  bstack1111ll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬႽ"),
  bstack1111ll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡨࡲࡩࡑࡥࡺࡵࠪႾ"),
  bstack1111ll1_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧႿ"),
  bstack1111ll1_opy_ (u"ࠫࡳࡵࡐࡪࡲࡨࡰ࡮ࡴࡥࠨჀ"),
  bstack1111ll1_opy_ (u"ࠬࡩࡨࡦࡥ࡮࡙ࡗࡒࠧჁ"),
  bstack1111ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨჂ"),
  bstack1111ll1_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡃࡰࡱ࡮࡭ࡪࡹࠧჃ"),
  bstack1111ll1_opy_ (u"ࠨࡥࡤࡴࡹࡻࡲࡦࡅࡵࡥࡸ࡮ࠧჄ"),
  bstack1111ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭Ⴥ"),
  bstack1111ll1_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ჆"),
  bstack1111ll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡗࡧࡵࡷ࡮ࡵ࡮ࠨჇ"),
  bstack1111ll1_opy_ (u"ࠬࡴ࡯ࡃ࡮ࡤࡲࡰࡖ࡯࡭࡮࡬ࡲ࡬࠭჈"),
  bstack1111ll1_opy_ (u"࠭࡭ࡢࡵ࡮ࡗࡪࡴࡤࡌࡧࡼࡷࠬ჉"),
  bstack1111ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡌࡰࡩࡶࠫ჊"),
  bstack1111ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡊࡦࠪ჋"),
  bstack1111ll1_opy_ (u"ࠩࡧࡩࡩ࡯ࡣࡢࡶࡨࡨࡉ࡫ࡶࡪࡥࡨࠫ჌"),
  bstack1111ll1_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡓࡥࡷࡧ࡭ࡴࠩჍ"),
  bstack1111ll1_opy_ (u"ࠫࡵ࡮࡯࡯ࡧࡑࡹࡲࡨࡥࡳࠩ჎"),
  bstack1111ll1_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࠪ჏"),
  bstack1111ll1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡓࡵࡺࡩࡰࡰࡶࠫა"),
  bstack1111ll1_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬბ"),
  bstack1111ll1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨგ"),
  bstack1111ll1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭დ"),
  bstack1111ll1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡅ࡭ࡴࡳࡥࡵࡴ࡬ࡧࠬე"),
  bstack1111ll1_opy_ (u"ࠫࡻ࡯ࡤࡦࡱ࡙࠶ࠬვ"),
  bstack1111ll1_opy_ (u"ࠬࡳࡩࡥࡕࡨࡷࡸ࡯࡯࡯ࡋࡱࡷࡹࡧ࡬࡭ࡃࡳࡴࡸ࠭ზ"),
  bstack1111ll1_opy_ (u"࠭ࡥࡴࡲࡵࡩࡸࡹ࡯ࡔࡧࡵࡺࡪࡸࠧთ"),
  bstack1111ll1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ი"),
  bstack1111ll1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡆࡨࡵ࠭კ"),
  bstack1111ll1_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩლ"),
  bstack1111ll1_opy_ (u"ࠪࡷࡾࡴࡣࡕ࡫ࡰࡩ࡜࡯ࡴࡩࡐࡗࡔࠬმ"),
  bstack1111ll1_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩნ"),
  bstack1111ll1_opy_ (u"ࠬ࡭ࡰࡴࡎࡲࡧࡦࡺࡩࡰࡰࠪო"),
  bstack1111ll1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧპ"),
  bstack1111ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧჟ"),
  bstack1111ll1_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࡃࡩࡣࡱ࡫ࡪࡐࡡࡳࠩრ"),
  bstack1111ll1_opy_ (u"ࠩࡻࡱࡸࡐࡡࡳࠩს"),
  bstack1111ll1_opy_ (u"ࠪࡼࡲࡾࡊࡢࡴࠪტ"),
  bstack1111ll1_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪუ"),
  bstack1111ll1_opy_ (u"ࠬࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬფ"),
  bstack1111ll1_opy_ (u"࠭ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧქ"),
  bstack1111ll1_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡄࡱࡵࡷࡗ࡫ࡳࡵࡴ࡬ࡧࡹ࡯࡯࡯ࡵࠪღ"),
  bstack1111ll1_opy_ (u"ࠨࡣࡳࡴ࡛࡫ࡲࡴ࡫ࡲࡲࠬყ"),
  bstack1111ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨშ"),
  bstack1111ll1_opy_ (u"ࠪࡶࡪࡹࡩࡨࡰࡄࡴࡵ࠭ჩ"),
  bstack1111ll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡩ࡮ࡣࡷ࡭ࡴࡴࡳࠨც"),
  bstack1111ll1_opy_ (u"ࠬࡩࡡ࡯ࡣࡵࡽࠬძ"),
  bstack1111ll1_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧწ"),
  bstack1111ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧჭ"),
  bstack1111ll1_opy_ (u"ࠨ࡫ࡨࠫხ"),
  bstack1111ll1_opy_ (u"ࠩࡨࡨ࡬࡫ࠧჯ"),
  bstack1111ll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪჰ"),
  bstack1111ll1_opy_ (u"ࠫࡶࡻࡥࡶࡧࠪჱ"),
  bstack1111ll1_opy_ (u"ࠬ࡯࡮ࡵࡧࡵࡲࡦࡲࠧჲ"),
  bstack1111ll1_opy_ (u"࠭ࡡࡱࡲࡖࡸࡴࡸࡥࡄࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠧჳ"),
  bstack1111ll1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡃࡢ࡯ࡨࡶࡦࡏ࡭ࡢࡩࡨࡍࡳࡰࡥࡤࡶ࡬ࡳࡳ࠭ჴ"),
  bstack1111ll1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡋࡸࡤ࡮ࡸࡨࡪࡎ࡯ࡴࡶࡶࠫჵ"),
  bstack1111ll1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡉ࡯ࡥ࡯ࡹࡩ࡫ࡈࡰࡵࡷࡷࠬჶ"),
  bstack1111ll1_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡄࡴࡵ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧჷ"),
  bstack1111ll1_opy_ (u"ࠫࡷ࡫ࡳࡦࡴࡹࡩࡉ࡫ࡶࡪࡥࡨࠫჸ"),
  bstack1111ll1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬჹ"),
  bstack1111ll1_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡳࠨჺ"),
  bstack1111ll1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡢࡵࡶࡧࡴࡪࡥࠨ჻"),
  bstack1111ll1_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡊࡱࡶࡈࡪࡼࡩࡤࡧࡖࡩࡹࡺࡩ࡯ࡩࡶࠫჼ"),
  bstack1111ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡸࡨ࡮ࡵࡉ࡯࡬ࡨࡧࡹ࡯࡯࡯ࠩჽ"),
  bstack1111ll1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡴࡵࡲࡥࡑࡣࡼࠫჾ"),
  bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬჿ"),
  bstack1111ll1_opy_ (u"ࠬࡽࡤࡪࡱࡖࡩࡷࡼࡩࡤࡧࠪᄀ"),
  bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᄁ"),
  bstack1111ll1_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡄࡴࡲࡷࡸ࡙ࡩࡵࡧࡗࡶࡦࡩ࡫ࡪࡰࡪࠫᄂ"),
  bstack1111ll1_opy_ (u"ࠨࡪ࡬࡫࡭ࡉ࡯࡯ࡶࡵࡥࡸࡺࠧᄃ"),
  bstack1111ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡒࡵࡩ࡫࡫ࡲࡦࡰࡦࡩࡸ࠭ᄄ"),
  bstack1111ll1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡖ࡭ࡲ࠭ᄅ"),
  bstack1111ll1_opy_ (u"ࠫࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨᄆ"),
  bstack1111ll1_opy_ (u"ࠬࡸࡥ࡮ࡱࡹࡩࡎࡕࡓࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࡑࡵࡣࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪᄇ"),
  bstack1111ll1_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨᄈ"),
  bstack1111ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᄉ"),
  bstack1111ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᄊ"),
  bstack1111ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᄋ"),
  bstack1111ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᄌ"),
  bstack1111ll1_opy_ (u"ࠫࡵࡧࡧࡦࡎࡲࡥࡩ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠧᄍ"),
  bstack1111ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫᄎ"),
  bstack1111ll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡳࡺࡺࡳࠨᄏ"),
  bstack1111ll1_opy_ (u"ࠧࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡓࡶࡴࡳࡰࡵࡄࡨ࡬ࡦࡼࡩࡰࡴࠪᄐ")
]
bstack1ll1llll_opy_ = {
  bstack1111ll1_opy_ (u"ࠨࡸࠪᄑ"): bstack1111ll1_opy_ (u"ࠩࡹࠫᄒ"),
  bstack1111ll1_opy_ (u"ࠪࡪࠬᄓ"): bstack1111ll1_opy_ (u"ࠫ࡫࠭ᄔ"),
  bstack1111ll1_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫᄕ"): bstack1111ll1_opy_ (u"࠭ࡦࡰࡴࡦࡩࠬᄖ"),
  bstack1111ll1_opy_ (u"ࠧࡰࡰ࡯ࡽࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᄗ"): bstack1111ll1_opy_ (u"ࠨࡱࡱࡰࡾࡇࡵࡵࡱࡰࡥࡹ࡫ࠧᄘ"),
  bstack1111ll1_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭ᄙ"): bstack1111ll1_opy_ (u"ࠪࡪࡴࡸࡣࡦ࡮ࡲࡧࡦࡲࠧᄚ"),
  bstack1111ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻ࡫ࡳࡸࡺࠧᄛ"): bstack1111ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨᄜ"),
  bstack1111ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡵࡵࡲࡵࠩᄝ"): bstack1111ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪᄞ"),
  bstack1111ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫᄟ"): bstack1111ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᄠ"),
  bstack1111ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭ᄡ"): bstack1111ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᄢ"),
  bstack1111ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭ᄣ"): bstack1111ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡋࡳࡸࡺࠧᄤ"),
  bstack1111ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨᄥ"): bstack1111ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡵࡲࡵࠩᄦ"),
  bstack1111ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪᄧ"): bstack1111ll1_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬᄨ"),
  bstack1111ll1_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭ᄩ"): bstack1111ll1_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧᄪ"),
  bstack1111ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧᄫ"): bstack1111ll1_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩᄬ"),
  bstack1111ll1_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪᄭ"): bstack1111ll1_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫᄮ"),
  bstack1111ll1_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧᄯ"): bstack1111ll1_opy_ (u"ࠫࡧ࡯࡮ࡢࡴࡼࡴࡦࡺࡨࠨᄰ"),
  bstack1111ll1_opy_ (u"ࠬࡶࡡࡤࡨ࡬ࡰࡪ࠭ᄱ"): bstack1111ll1_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᄲ"),
  bstack1111ll1_opy_ (u"ࠧࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᄳ"): bstack1111ll1_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᄴ"),
  bstack1111ll1_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᄵ"): bstack1111ll1_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᄶ"),
  bstack1111ll1_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬᄷ"): bstack1111ll1_opy_ (u"ࠬࡲ࡯ࡨࡨ࡬ࡰࡪ࠭ᄸ"),
  bstack1111ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᄹ"): bstack1111ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᄺ"),
}
bstack111ll1l11l_opy_ = bstack1111ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡪ࡭ࡹ࡮ࡵࡣ࠰ࡦࡳࡲ࠵ࡰࡦࡴࡦࡽ࠴ࡩ࡬ࡪ࠱ࡵࡩࡱ࡫ࡡࡴࡧࡶ࠳ࡱࡧࡴࡦࡵࡷ࠳ࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᄻ")
bstack111ll11111_opy_ = bstack1111ll1_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠱࡫ࡩࡦࡲࡴࡩࡥ࡫ࡩࡨࡱࠢᄼ")
bstack1l1l1l111_opy_ = bstack1111ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡼࡪ࠯ࡩࡷࡥࠫᄽ")
bstack1lll11l1_opy_ = bstack1111ll1_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠧᄾ")
bstack11lll1l11_opy_ = bstack1111ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴࠩᄿ")
bstack111ll11l1l_opy_ = {
  bstack1111ll1_opy_ (u"࠭ࡣࡳ࡫ࡷ࡭ࡨࡧ࡬ࠨᅀ"): 50,
  bstack1111ll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᅁ"): 40,
  bstack1111ll1_opy_ (u"ࠨࡹࡤࡶࡳ࡯࡮ࡨࠩᅂ"): 30,
  bstack1111ll1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᅃ"): 20,
  bstack1111ll1_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᅄ"): 10
}
bstack1l1l1l1ll1_opy_ = bstack111ll11l1l_opy_[bstack1111ll1_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᅅ")]
bstack11l11lll_opy_ = bstack1111ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᅆ")
bstack1l1l1l11l1_opy_ = bstack1111ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᅇ")
bstack1l11l111l1_opy_ = bstack1111ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭ᅈ")
bstack1l1ll111l1_opy_ = bstack1111ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᅉ")
bstack1l11l111ll_opy_ = bstack1111ll1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶࠣࡥࡳࡪࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡳࡥࡨࡱࡡࡨࡧࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡦࠧᅊ")
bstack111l1ll1l1_opy_ = [bstack1111ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫᅋ"), bstack1111ll1_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫᅌ")]
bstack111l1lllll_opy_ = [bstack1111ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨᅍ"), bstack1111ll1_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨᅎ")]
bstack11ll1ll1_opy_ = re.compile(bstack1111ll1_opy_ (u"ࠧ࡟࡝࡟ࡠࡼ࠳࡝ࠬ࠼࠱࠮ࠩ࠭ᅏ"))
bstack1ll11l111_opy_ = [
  bstack1111ll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡓࡧ࡭ࡦࠩᅐ"),
  bstack1111ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᅑ"),
  bstack1111ll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᅒ"),
  bstack1111ll1_opy_ (u"ࠫࡳ࡫ࡷࡄࡱࡰࡱࡦࡴࡤࡕ࡫ࡰࡩࡴࡻࡴࠨᅓ"),
  bstack1111ll1_opy_ (u"ࠬࡧࡰࡱࠩᅔ"),
  bstack1111ll1_opy_ (u"࠭ࡵࡥ࡫ࡧࠫᅕ"),
  bstack1111ll1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᅖ"),
  bstack1111ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࠨᅗ"),
  bstack1111ll1_opy_ (u"ࠩࡲࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧᅘ"),
  bstack1111ll1_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࠨᅙ"),
  bstack1111ll1_opy_ (u"ࠫࡳࡵࡒࡦࡵࡨࡸࠬᅚ"), bstack1111ll1_opy_ (u"ࠬ࡬ࡵ࡭࡮ࡕࡩࡸ࡫ࡴࠨᅛ"),
  bstack1111ll1_opy_ (u"࠭ࡣ࡭ࡧࡤࡶࡘࡿࡳࡵࡧࡰࡊ࡮ࡲࡥࡴࠩᅜ"),
  bstack1111ll1_opy_ (u"ࠧࡦࡸࡨࡲࡹ࡚ࡩ࡮࡫ࡱ࡫ࡸ࠭ᅝ"),
  bstack1111ll1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡑࡧࡵࡪࡴࡸ࡭ࡢࡰࡦࡩࡑࡵࡧࡨ࡫ࡱ࡫ࠬᅞ"),
  bstack1111ll1_opy_ (u"ࠩࡲࡸ࡭࡫ࡲࡂࡲࡳࡷࠬᅟ"),
  bstack1111ll1_opy_ (u"ࠪࡴࡷ࡯࡮ࡵࡒࡤ࡫ࡪ࡙࡯ࡶࡴࡦࡩࡔࡴࡆࡪࡰࡧࡊࡦ࡯࡬ࡶࡴࡨࠫᅠ"),
  bstack1111ll1_opy_ (u"ࠫࡦࡶࡰࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩᅡ"), bstack1111ll1_opy_ (u"ࠬࡧࡰࡱࡒࡤࡧࡰࡧࡧࡦࠩᅢ"), bstack1111ll1_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨᅣ"), bstack1111ll1_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡑࡣࡦ࡯ࡦ࡭ࡥࠨᅤ"), bstack1111ll1_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡆࡸࡶࡦࡺࡩࡰࡰࠪᅥ"),
  bstack1111ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧᅦ"),
  bstack1111ll1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡨࡷࡹࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧᅧ"),
  bstack1111ll1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪ࠭ᅨ"), bstack1111ll1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࡅ࡯ࡦࡌࡲࡹ࡫࡮ࡵࠩᅩ"),
  bstack1111ll1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡄࡦࡸ࡬ࡧࡪࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫᅪ"),
  bstack1111ll1_opy_ (u"ࠧࡢࡦࡥࡔࡴࡸࡴࠨᅫ"),
  bstack1111ll1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡔࡱࡦ࡯ࡪࡺࠧᅬ"),
  bstack1111ll1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡗ࡭ࡲ࡫࡯ࡶࡶࠪᅭ"),
  bstack1111ll1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡔࡦࡺࡨࠨᅮ"),
  bstack1111ll1_opy_ (u"ࠫࡦࡼࡤࠨᅯ"), bstack1111ll1_opy_ (u"ࠬࡧࡶࡥࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨᅰ"), bstack1111ll1_opy_ (u"࠭ࡡࡷࡦࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨᅱ"), bstack1111ll1_opy_ (u"ࠧࡢࡸࡧࡅࡷ࡭ࡳࠨᅲ"),
  bstack1111ll1_opy_ (u"ࠨࡷࡶࡩࡐ࡫ࡹࡴࡶࡲࡶࡪ࠭ᅳ"), bstack1111ll1_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡺࡨࠨᅴ"), bstack1111ll1_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡳࡴࡹࡲࡶࡩ࠭ᅵ"),
  bstack1111ll1_opy_ (u"ࠫࡰ࡫ࡹࡂ࡮࡬ࡥࡸ࠭ᅶ"), bstack1111ll1_opy_ (u"ࠬࡱࡥࡺࡒࡤࡷࡸࡽ࡯ࡳࡦࠪᅷ"),
  bstack1111ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨᅸ"), bstack1111ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡇࡲࡨࡵࠪᅹ"), bstack1111ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࡇ࡭ࡷ࠭ᅺ"), bstack1111ll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡄࡪࡵࡳࡲ࡫ࡍࡢࡲࡳ࡭ࡳ࡭ࡆࡪ࡮ࡨࠫᅻ"), bstack1111ll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡗࡶࡩࡘࡿࡳࡵࡧࡰࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧᅼ"),
  bstack1111ll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࠧᅽ"), bstack1111ll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࡴࠩᅾ"),
  bstack1111ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡉ࡯ࡳࡢࡤ࡯ࡩࡇࡻࡩ࡭ࡦࡆ࡬ࡪࡩ࡫ࠨᅿ"),
  bstack1111ll1_opy_ (u"ࠧࡢࡷࡷࡳ࡜࡫ࡢࡷ࡫ࡨࡻ࡙࡯࡭ࡦࡱࡸࡸࠬᆀ"),
  bstack1111ll1_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡂࡥࡷ࡭ࡴࡴࠧᆁ"), bstack1111ll1_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡅࡤࡸࡪ࡭࡯ࡳࡻࠪᆂ"), bstack1111ll1_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡉࡰࡦ࡭ࡳࠨᆃ"), bstack1111ll1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡥࡱࡏ࡮ࡵࡧࡱࡸࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᆄ"),
  bstack1111ll1_opy_ (u"ࠬࡪ࡯࡯ࡶࡖࡸࡴࡶࡁࡱࡲࡒࡲࡗ࡫ࡳࡦࡶࠪᆅ"),
  bstack1111ll1_opy_ (u"࠭ࡵ࡯࡫ࡦࡳࡩ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨᆆ"), bstack1111ll1_opy_ (u"ࠧࡳࡧࡶࡩࡹࡑࡥࡺࡤࡲࡥࡷࡪࠧᆇ"),
  bstack1111ll1_opy_ (u"ࠨࡰࡲࡗ࡮࡭࡮ࠨᆈ"),
  bstack1111ll1_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࡗࡱ࡭ࡲࡶ࡯ࡳࡶࡤࡲࡹ࡜ࡩࡦࡹࡶࠫᆉ"),
  bstack1111ll1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳࡪࡲࡰ࡫ࡧ࡛ࡦࡺࡣࡩࡧࡵࡷࠬᆊ"),
  bstack1111ll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᆋ"),
  bstack1111ll1_opy_ (u"ࠬࡸࡥࡤࡴࡨࡥࡹ࡫ࡃࡩࡴࡲࡱࡪࡊࡲࡪࡸࡨࡶࡘ࡫ࡳࡴ࡫ࡲࡲࡸ࠭ᆌ"),
  bstack1111ll1_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬᆍ"),
  bstack1111ll1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࡔࡦࡺࡨࠨᆎ"),
  bstack1111ll1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡕࡳࡩࡪࡪࠧᆏ"),
  bstack1111ll1_opy_ (u"ࠩࡪࡴࡸࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ᆐ"),
  bstack1111ll1_opy_ (u"ࠪ࡭ࡸࡎࡥࡢࡦ࡯ࡩࡸࡹࠧᆑ"),
  bstack1111ll1_opy_ (u"ࠫࡦࡪࡢࡆࡺࡨࡧ࡙࡯࡭ࡦࡱࡸࡸࠬᆒ"),
  bstack1111ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡩࡘࡩࡲࡪࡲࡷࠫᆓ"),
  bstack1111ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡈࡪࡼࡩࡤࡧࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪᆔ"),
  bstack1111ll1_opy_ (u"ࠧࡢࡷࡷࡳࡌࡸࡡ࡯ࡶࡓࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹࠧᆕ"),
  bstack1111ll1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡐࡤࡸࡺࡸࡡ࡭ࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ᆖ"),
  bstack1111ll1_opy_ (u"ࠩࡶࡽࡸࡺࡥ࡮ࡒࡲࡶࡹ࠭ᆗ"),
  bstack1111ll1_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡨࡧࡎ࡯ࡴࡶࠪᆘ"),
  bstack1111ll1_opy_ (u"ࠫࡸࡱࡩࡱࡗࡱࡰࡴࡩ࡫ࠨᆙ"), bstack1111ll1_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯࡙ࡿࡰࡦࠩᆚ"), bstack1111ll1_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰࡑࡥࡺࠩᆛ"),
  bstack1111ll1_opy_ (u"ࠧࡢࡷࡷࡳࡑࡧࡵ࡯ࡥ࡫ࠫᆜ"),
  bstack1111ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡥࡤࡸࡈࡧࡰࡵࡷࡵࡩࠬᆝ"),
  bstack1111ll1_opy_ (u"ࠩࡸࡲ࡮ࡴࡳࡵࡣ࡯ࡰࡔࡺࡨࡦࡴࡓࡥࡨࡱࡡࡨࡧࡶࠫᆞ"),
  bstack1111ll1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨ࡛࡮ࡴࡤࡰࡹࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࠬᆟ"),
  bstack1111ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡳࡴࡲࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᆠ"),
  bstack1111ll1_opy_ (u"ࠬ࡫࡮ࡧࡱࡵࡧࡪࡇࡰࡱࡋࡱࡷࡹࡧ࡬࡭ࠩᆡ"),
  bstack1111ll1_opy_ (u"࠭ࡥ࡯ࡵࡸࡶࡪ࡝ࡥࡣࡸ࡬ࡩࡼࡹࡈࡢࡸࡨࡔࡦ࡭ࡥࡴࠩᆢ"), bstack1111ll1_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࡅࡧࡹࡸࡴࡵ࡬ࡴࡒࡲࡶࡹ࠭ᆣ"), bstack1111ll1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡘࡧࡥࡺ࡮࡫ࡷࡅࡧࡷࡥ࡮ࡲࡳࡄࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠫᆤ"),
  bstack1111ll1_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡳࡴࡸࡉࡡࡤࡪࡨࡐ࡮ࡳࡩࡵࠩᆥ"),
  bstack1111ll1_opy_ (u"ࠪࡧࡦࡲࡥ࡯ࡦࡤࡶࡋࡵࡲ࡮ࡣࡷࠫᆦ"),
  bstack1111ll1_opy_ (u"ࠫࡧࡻ࡮ࡥ࡮ࡨࡍࡩ࠭ᆧ"),
  bstack1111ll1_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬᆨ"),
  bstack1111ll1_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡇࡱࡥࡧࡲࡥࡥࠩᆩ"), bstack1111ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡩࡩ࠭ᆪ"),
  bstack1111ll1_opy_ (u"ࠨࡣࡸࡸࡴࡇࡣࡤࡧࡳࡸࡆࡲࡥࡳࡶࡶࠫᆫ"), bstack1111ll1_opy_ (u"ࠩࡤࡹࡹࡵࡄࡪࡵࡰ࡭ࡸࡹࡁ࡭ࡧࡵࡸࡸ࠭ᆬ"),
  bstack1111ll1_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧࡌࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡹࡌࡪࡤࠪᆭ"),
  bstack1111ll1_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨ࡛ࡪࡨࡔࡢࡲࠪᆮ"),
  bstack1111ll1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡎࡴࡩࡵ࡫ࡤࡰ࡚ࡸ࡬ࠨᆯ"), bstack1111ll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡇ࡬࡭ࡱࡺࡔࡴࡶࡵࡱࡵࠪᆰ"), bstack1111ll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉࡨࡰࡲࡶࡪࡌࡲࡢࡷࡧ࡛ࡦࡸ࡮ࡪࡰࡪࠫᆱ"), bstack1111ll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡨࡲࡑ࡯࡮࡬ࡵࡌࡲࡇࡧࡣ࡬ࡩࡵࡳࡺࡴࡤࠨᆲ"),
  bstack1111ll1_opy_ (u"ࠩ࡮ࡩࡪࡶࡋࡦࡻࡆ࡬ࡦ࡯࡮ࡴࠩᆳ"),
  bstack1111ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡽࡥࡧࡲࡥࡔࡶࡵ࡭ࡳ࡭ࡳࡅ࡫ࡵࠫᆴ"),
  bstack1111ll1_opy_ (u"ࠫࡵࡸ࡯ࡤࡧࡶࡷࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᆵ"),
  bstack1111ll1_opy_ (u"ࠬ࡯࡮ࡵࡧࡵࡏࡪࡿࡄࡦ࡮ࡤࡽࠬᆶ"),
  bstack1111ll1_opy_ (u"࠭ࡳࡩࡱࡺࡍࡔ࡙ࡌࡰࡩࠪᆷ"),
  bstack1111ll1_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡔࡶࡵࡥࡹ࡫ࡧࡺࠩᆸ"),
  bstack1111ll1_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡓࡧࡶࡴࡴࡴࡳࡦࡖ࡬ࡱࡪࡵࡵࡵࠩᆹ"), bstack1111ll1_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࡝ࡡࡪࡶࡗ࡭ࡲ࡫࡯ࡶࡶࠪᆺ"),
  bstack1111ll1_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡇࡩࡧࡻࡧࡑࡴࡲࡼࡾ࠭ᆻ"),
  bstack1111ll1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡸࡿ࡮ࡤࡇࡻࡩࡨࡻࡴࡦࡈࡵࡳࡲࡎࡴࡵࡲࡶࠫᆼ"),
  bstack1111ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡏࡳ࡬ࡉࡡࡱࡶࡸࡶࡪ࠭ᆽ"),
  bstack1111ll1_opy_ (u"࠭ࡷࡦࡤ࡮࡭ࡹࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭ᆾ"),
  bstack1111ll1_opy_ (u"ࠧࡧࡷ࡯ࡰࡈࡵ࡮ࡵࡧࡻࡸࡑ࡯ࡳࡵࠩᆿ"),
  bstack1111ll1_opy_ (u"ࠨࡹࡤ࡭ࡹࡌ࡯ࡳࡃࡳࡴࡘࡩࡲࡪࡲࡷࠫᇀ"),
  bstack1111ll1_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡆࡳࡳࡴࡥࡤࡶࡕࡩࡹࡸࡩࡦࡵࠪᇁ"),
  bstack1111ll1_opy_ (u"ࠪࡥࡵࡶࡎࡢ࡯ࡨࠫᇂ"),
  bstack1111ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡘࡒࡃࡦࡴࡷࠫᇃ"),
  bstack1111ll1_opy_ (u"ࠬࡺࡡࡱ࡙࡬ࡸ࡭࡙ࡨࡰࡴࡷࡔࡷ࡫ࡳࡴࡆࡸࡶࡦࡺࡩࡰࡰࠪᇄ"),
  bstack1111ll1_opy_ (u"࠭ࡳࡤࡣ࡯ࡩࡋࡧࡣࡵࡱࡵࠫᇅ"),
  bstack1111ll1_opy_ (u"ࠧࡸࡦࡤࡐࡴࡩࡡ࡭ࡒࡲࡶࡹ࠭ᇆ"),
  bstack1111ll1_opy_ (u"ࠨࡵ࡫ࡳࡼ࡞ࡣࡰࡦࡨࡐࡴ࡭ࠧᇇ"),
  bstack1111ll1_opy_ (u"ࠩ࡬ࡳࡸࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡶࡵࡨࠫᇈ"),
  bstack1111ll1_opy_ (u"ࠪࡼࡨࡵࡤࡦࡅࡲࡲ࡫࡯ࡧࡇ࡫࡯ࡩࠬᇉ"),
  bstack1111ll1_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡴࡵࡺࡳࡷࡪࠧᇊ"),
  bstack1111ll1_opy_ (u"ࠬࡻࡳࡦࡒࡵࡩࡧࡻࡩ࡭ࡶ࡚ࡈࡆ࠭ᇋ"),
  bstack1111ll1_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡗࡅࡃࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠧᇌ"),
  bstack1111ll1_opy_ (u"ࠧࡸࡧࡥࡈࡷ࡯ࡶࡦࡴࡄ࡫ࡪࡴࡴࡖࡴ࡯ࠫᇍ"),
  bstack1111ll1_opy_ (u"ࠨ࡭ࡨࡽࡨ࡮ࡡࡪࡰࡓࡥࡹ࡮ࠧᇎ"),
  bstack1111ll1_opy_ (u"ࠩࡸࡷࡪࡔࡥࡸ࡙ࡇࡅࠬᇏ"),
  bstack1111ll1_opy_ (u"ࠪࡻࡩࡧࡌࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᇐ"), bstack1111ll1_opy_ (u"ࠫࡼࡪࡡࡄࡱࡱࡲࡪࡩࡴࡪࡱࡱࡘ࡮ࡳࡥࡰࡷࡷࠫᇑ"),
  bstack1111ll1_opy_ (u"ࠬࡾࡣࡰࡦࡨࡓࡷ࡭ࡉࡥࠩᇒ"), bstack1111ll1_opy_ (u"࠭ࡸࡤࡱࡧࡩࡘ࡯ࡧ࡯࡫ࡱ࡫ࡎࡪࠧᇓ"),
  bstack1111ll1_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡘࡆࡄࡆࡺࡴࡤ࡭ࡧࡌࡨࠬᇔ"),
  bstack1111ll1_opy_ (u"ࠨࡴࡨࡷࡪࡺࡏ࡯ࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡷࡺࡏ࡯࡮ࡼࠫᇕ"),
  bstack1111ll1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࡶࠫᇖ"),
  bstack1111ll1_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵ࡭ࡪࡹࠧᇗ"), bstack1111ll1_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶࡾࡏ࡮ࡵࡧࡵࡺࡦࡲࠧᇘ"),
  bstack1111ll1_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹࡎࡡࡳࡦࡺࡥࡷ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨᇙ"),
  bstack1111ll1_opy_ (u"࠭࡭ࡢࡺࡗࡽࡵ࡯࡮ࡨࡈࡵࡩࡶࡻࡥ࡯ࡥࡼࠫᇚ"),
  bstack1111ll1_opy_ (u"ࠧࡴ࡫ࡰࡴࡱ࡫ࡉࡴࡘ࡬ࡷ࡮ࡨ࡬ࡦࡅ࡫ࡩࡨࡱࠧᇛ"),
  bstack1111ll1_opy_ (u"ࠨࡷࡶࡩࡈࡧࡲࡵࡪࡤ࡫ࡪ࡙ࡳ࡭ࠩᇜ"),
  bstack1111ll1_opy_ (u"ࠩࡶ࡬ࡴࡻ࡬ࡥࡗࡶࡩࡘ࡯࡮ࡨ࡮ࡨࡸࡴࡴࡔࡦࡵࡷࡑࡦࡴࡡࡨࡧࡵࠫᇝ"),
  bstack1111ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡋ࡚ࡈࡕ࠭ᇞ"),
  bstack1111ll1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡳࡺࡩࡨࡊࡦࡈࡲࡷࡵ࡬࡭ࠩᇟ"),
  bstack1111ll1_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࡍ࡯ࡤࡥࡧࡱࡅࡵ࡯ࡐࡰ࡮࡬ࡧࡾࡋࡲࡳࡱࡵࠫᇠ"),
  bstack1111ll1_opy_ (u"࠭࡭ࡰࡥ࡮ࡐࡴࡩࡡࡵ࡫ࡲࡲࡆࡶࡰࠨᇡ"),
  bstack1111ll1_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡰࡴࡰࡥࡹ࠭ᇢ"), bstack1111ll1_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇ࡫࡯ࡸࡪࡸࡓࡱࡧࡦࡷࠬᇣ"),
  bstack1111ll1_opy_ (u"ࠩࡤࡰࡱࡵࡷࡅࡧ࡯ࡥࡾࡇࡤࡣࠩᇤ"),
  bstack1111ll1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡍࡩࡒ࡯ࡤࡣࡷࡳࡷࡇࡵࡵࡱࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳ࠭ᇥ")
]
bstack11ll1lll1_opy_ = bstack1111ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪᇦ")
bstack1l11l11ll1_opy_ = [bstack1111ll1_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪᇧ"), bstack1111ll1_opy_ (u"࠭࠮ࡢࡣࡥࠫᇨ"), bstack1111ll1_opy_ (u"ࠧ࠯࡫ࡳࡥࠬᇩ")]
bstack1l11ll1l_opy_ = [bstack1111ll1_opy_ (u"ࠨ࡫ࡧࠫᇪ"), bstack1111ll1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᇫ"), bstack1111ll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ᇬ"), bstack1111ll1_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪᇭ")]
bstack1111l1ll_opy_ = {
  bstack1111ll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᇮ"): bstack1111ll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᇯ"),
  bstack1111ll1_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨᇰ"): bstack1111ll1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ᇱ"),
  bstack1111ll1_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᇲ"): bstack1111ll1_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫᇳ"),
  bstack1111ll1_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᇴ"): bstack1111ll1_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫᇵ"),
  bstack1111ll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭ᇶ"): bstack1111ll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨᇷ")
}
bstack1lllll1lll_opy_ = [
  bstack1111ll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᇸ"),
  bstack1111ll1_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧᇹ"),
  bstack1111ll1_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫᇺ"),
  bstack1111ll1_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᇻ"),
  bstack1111ll1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᇼ"),
]
bstack1l11ll11l1_opy_ = bstack1l1l1l1111_opy_ + bstack111l1lll1l_opy_ + bstack1ll11l111_opy_
bstack1lll111111_opy_ = [
  bstack1111ll1_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫᇽ"),
  bstack1111ll1_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨᇾ"),
  bstack1111ll1_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧᇿ"),
  bstack1111ll1_opy_ (u"ࠩࡡ࠵࠵࠴ࠧሀ"),
  bstack1111ll1_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩሁ"),
  bstack1111ll1_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪሂ"),
  bstack1111ll1_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫሃ"),
  bstack1111ll1_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩሄ")
]
bstack111ll1l111_opy_ = bstack1111ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨህ")
bstack11l1lll1l_opy_ = bstack1111ll1_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧሆ")
bstack1ll1l1l111_opy_ = [ bstack1111ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫሇ") ]
bstack1ll1111111_opy_ = [ bstack1111ll1_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩለ") ]
bstack1llllllll1_opy_ = [ bstack1111ll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫሉ") ]
bstack1l1l111111_opy_ = bstack1111ll1_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧሊ")
bstack1l1l1l1l1_opy_ = bstack1111ll1_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩላ")
bstack111ll1l1l_opy_ = bstack1111ll1_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫሌ")
bstack1lll11l111_opy_ = bstack1111ll1_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧል")
bstack1111ll1l1_opy_ = [
  bstack1111ll1_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭ሎ"),
  bstack1111ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪሏ"),
  bstack1111ll1_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬሐ"),
  bstack1111ll1_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫሑ"),
  bstack1111ll1_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪሒ"),
  bstack1111ll1_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨሓ"),
  bstack1111ll1_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨሔ"),
  bstack1111ll1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫሕ"),
  bstack1111ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬሖ"),
  bstack1111ll1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬሗ"),
  bstack1111ll1_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭መ"),
  bstack1111ll1_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬሙ"),
  bstack1111ll1_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪሚ"),
  bstack1111ll1_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩማ"),
  bstack1111ll1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ሜ"),
  bstack1111ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪም"),
  bstack1111ll1_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧሞ"),
  bstack1111ll1_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬሟ"),
  bstack1111ll1_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧሠ"),
  bstack1111ll1_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ሡ"),
  bstack1111ll1_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧሢ"),
]
bstack1lll1l1lll_opy_ = bstack1111ll1_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧሣ")
bstack111111lll_opy_ = os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠪࢂࠬሤ")), bstack1111ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫሥ"), bstack1111ll1_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫሦ"))
bstack111llllll1_opy_ = bstack1111ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵ࡯ࠧሧ")
bstack111l1ll1ll_opy_ = [ bstack1111ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧረ"), bstack1111ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧሩ"), bstack1111ll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨሪ"), bstack1111ll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪራ")]
bstack1l1lllll_opy_ = [ bstack1111ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫሬ"), bstack1111ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫር"), bstack1111ll1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬሮ"), bstack1111ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧሯ") ]
bstack11l1ll11l1_opy_ = {
  bstack1111ll1_opy_ (u"ࠨࡒࡄࡗࡘ࠭ሰ"): bstack1111ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩሱ"),
  bstack1111ll1_opy_ (u"ࠪࡊࡆࡏࡌࠨሲ"): bstack1111ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫሳ"),
  bstack1111ll1_opy_ (u"࡙ࠬࡋࡊࡒࠪሴ"): bstack1111ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧስ")
}
bstack1l1l11ll1l_opy_ = [
  bstack1111ll1_opy_ (u"ࠢࡨࡧࡷࠦሶ"),
  bstack1111ll1_opy_ (u"ࠣࡩࡲࡆࡦࡩ࡫ࠣሷ"),
  bstack1111ll1_opy_ (u"ࠤࡪࡳࡋࡵࡲࡸࡣࡵࡨࠧሸ"),
  bstack1111ll1_opy_ (u"ࠥࡶࡪ࡬ࡲࡦࡵ࡫ࠦሹ"),
  bstack1111ll1_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥሺ"),
  bstack1111ll1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤሻ"),
  bstack1111ll1_opy_ (u"ࠨࡳࡶࡤࡰ࡭ࡹࡋ࡬ࡦ࡯ࡨࡲࡹࠨሼ"),
  bstack1111ll1_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦሽ"),
  bstack1111ll1_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦሾ"),
  bstack1111ll1_opy_ (u"ࠤࡦࡰࡪࡧࡲࡆ࡮ࡨࡱࡪࡴࡴࠣሿ"),
  bstack1111ll1_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࡶࠦቀ"),
  bstack1111ll1_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠦቁ"),
  bstack1111ll1_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࡇࡳࡺࡰࡦࡗࡨࡸࡩࡱࡶࠥቂ"),
  bstack1111ll1_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧቃ"),
  bstack1111ll1_opy_ (u"ࠢࡲࡷ࡬ࡸࠧቄ"),
  bstack1111ll1_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡖࡲࡹࡨ࡮ࡁࡤࡶ࡬ࡳࡳࠨቅ"),
  bstack1111ll1_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡐࡹࡱࡺࡩࡕࡱࡸࡧ࡭ࠨቆ"),
  bstack1111ll1_opy_ (u"ࠥࡷ࡭ࡧ࡫ࡦࠤቇ"),
  bstack1111ll1_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࡄࡴࡵࠨቈ")
]
bstack111l1llll1_opy_ = [
  bstack1111ll1_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦ቉"),
  bstack1111ll1_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥቊ"),
  bstack1111ll1_opy_ (u"ࠢࡢࡷࡷࡳࠧቋ"),
  bstack1111ll1_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣቌ"),
  bstack1111ll1_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦቍ")
]
bstack1lll1l111_opy_ = {
  bstack1111ll1_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤ቎"): [bstack1111ll1_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ቏")],
  bstack1111ll1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤቐ"): [bstack1111ll1_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥቑ")],
  bstack1111ll1_opy_ (u"ࠢࡢࡷࡷࡳࠧቒ"): [bstack1111ll1_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧቓ"), bstack1111ll1_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧቔ"), bstack1111ll1_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢቕ"), bstack1111ll1_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥቖ")],
  bstack1111ll1_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧ቗"): [bstack1111ll1_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨቘ")],
  bstack1111ll1_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ቙"): [bstack1111ll1_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥቚ")],
}
bstack111ll11l11_opy_ = {
  bstack1111ll1_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࡆ࡮ࡨࡱࡪࡴࡴࠣቛ"): bstack1111ll1_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤቜ"),
  bstack1111ll1_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣቝ"): bstack1111ll1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ቞"),
  bstack1111ll1_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡈࡰࡪࡳࡥ࡯ࡶࠥ቟"): bstack1111ll1_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࠤበ"),
  bstack1111ll1_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦቡ"): bstack1111ll1_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦቢ"),
  bstack1111ll1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧባ"): bstack1111ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨቤ")
}
bstack11ll11l11l_opy_ = {
  bstack1111ll1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩብ"): bstack1111ll1_opy_ (u"࠭ࡓࡶ࡫ࡷࡩ࡙ࠥࡥࡵࡷࡳࠫቦ"),
  bstack1111ll1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪቧ"): bstack1111ll1_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡕࡧࡤࡶࡩࡵࡷ࡯ࠩቨ"),
  bstack1111ll1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧቩ"): bstack1111ll1_opy_ (u"ࠪࡘࡪࡹࡴࠡࡕࡨࡸࡺࡶࠧቪ"),
  bstack1111ll1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨቫ"): bstack1111ll1_opy_ (u"࡚ࠬࡥࡴࡶࠣࡘࡪࡧࡲࡥࡱࡺࡲࠬቬ")
}
bstack111ll11lll_opy_ = 65536
bstack111l1lll11_opy_ = bstack1111ll1_opy_ (u"࠭࠮࠯࠰࡞ࡘࡗ࡛ࡎࡄࡃࡗࡉࡉࡣࠧቭ")
bstack111ll111l1_opy_ = [
      bstack1111ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩቮ"), bstack1111ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫቯ"), bstack1111ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬተ"), bstack1111ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧቱ"), bstack1111ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭ቲ"),
      bstack1111ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨታ"), bstack1111ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩቴ"), bstack1111ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨት"), bstack1111ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩቶ"),
      bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡔࡡ࡮ࡧࠪቷ"), bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬቸ"), bstack1111ll1_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧቹ")
    ]
bstack111ll11ll1_opy_= {
  bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩቺ"): bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪቻ"),
  bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫቼ"): bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬች"),
  bstack1111ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨቾ"): bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧቿ"),
  bstack1111ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫኀ"): bstack1111ll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬኁ"),
  bstack1111ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩኂ"): bstack1111ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪኃ"),
  bstack1111ll1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪኄ"): bstack1111ll1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫኅ"),
  bstack1111ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ኆ"): bstack1111ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧኇ"),
  bstack1111ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩኈ"): bstack1111ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ኉"),
  bstack1111ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪኊ"): bstack1111ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫኋ"),
  bstack1111ll1_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧኌ"): bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨኍ"),
  bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ኎"): bstack1111ll1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ኏"),
  bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪነ"): bstack1111ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫኑ"),
  bstack1111ll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪኒ"): bstack1111ll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫና"),
  bstack1111ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧኔ"): bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ን"),
  bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧኖ"): bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨኗ"),
  bstack1111ll1_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫኘ"): bstack1111ll1_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬኙ"),
  bstack1111ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨኚ"): bstack1111ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩኛ"),
  bstack1111ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪኜ"): bstack1111ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫኝ"),
  bstack1111ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩኞ"): bstack1111ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪኟ"),
  bstack1111ll1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪአ"): bstack1111ll1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫኡ"),
  bstack1111ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪኢ"): bstack1111ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫኣ"),
  bstack1111ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬኤ"): bstack1111ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭እ"),
  bstack1111ll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫኦ"): bstack1111ll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬኧ"),
  bstack1111ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ከ"): bstack1111ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧኩ"),
  bstack1111ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫኪ"): bstack1111ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬካ")
}
bstack111ll1111l_opy_ = [bstack1111ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ኬ"), bstack1111ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ክ")]