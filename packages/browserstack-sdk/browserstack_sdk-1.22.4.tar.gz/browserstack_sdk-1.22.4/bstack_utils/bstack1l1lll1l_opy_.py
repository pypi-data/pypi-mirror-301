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
class bstack111lll1ll1_opy_(object):
  bstack1l1l111l1_opy_ = os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠬࢄࠧྰ")), bstack1111ll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ྱ"))
  bstack111lll11l1_opy_ = os.path.join(bstack1l1l111l1_opy_, bstack1111ll1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴ࠰࡭ࡷࡴࡴࠧྲ"))
  bstack111lll11ll_opy_ = None
  perform_scan = None
  bstack1l11l111_opy_ = None
  bstack1ll11ll1l1_opy_ = None
  bstack111llll111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1111ll1_opy_ (u"ࠨ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠪླ")):
      cls.instance = super(bstack111lll1ll1_opy_, cls).__new__(cls)
      cls.instance.bstack111lll1l11_opy_()
    return cls.instance
  def bstack111lll1l11_opy_(self):
    try:
      with open(self.bstack111lll11l1_opy_, bstack1111ll1_opy_ (u"ࠩࡵࠫྴ")) as bstack1lll1lll11_opy_:
        bstack111lll1lll_opy_ = bstack1lll1lll11_opy_.read()
        data = json.loads(bstack111lll1lll_opy_)
        if bstack1111ll1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬྵ") in data:
          self.bstack11l111ll1l_opy_(data[bstack1111ll1_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ྶ")])
        if bstack1111ll1_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ྷ") in data:
          self.bstack111lllll1l_opy_(data[bstack1111ll1_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧྸ")])
    except:
      pass
  def bstack111lllll1l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1111ll1_opy_ (u"ࠧࡴࡥࡤࡲࠬྐྵ")]
      self.bstack1l11l111_opy_ = scripts[bstack1111ll1_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬྺ")]
      self.bstack1ll11ll1l1_opy_ = scripts[bstack1111ll1_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ྻ")]
      self.bstack111llll111_opy_ = scripts[bstack1111ll1_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨྼ")]
  def bstack11l111ll1l_opy_(self, bstack111lll11ll_opy_):
    if bstack111lll11ll_opy_ != None and len(bstack111lll11ll_opy_) != 0:
      self.bstack111lll11ll_opy_ = bstack111lll11ll_opy_
  def store(self):
    try:
      with open(self.bstack111lll11l1_opy_, bstack1111ll1_opy_ (u"ࠫࡼ࠭྽")) as file:
        json.dump({
          bstack1111ll1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࠢ྾"): self.bstack111lll11ll_opy_,
          bstack1111ll1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࡹࠢ྿"): {
            bstack1111ll1_opy_ (u"ࠢࡴࡥࡤࡲࠧ࿀"): self.perform_scan,
            bstack1111ll1_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧ࿁"): self.bstack1l11l111_opy_,
            bstack1111ll1_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨ࿂"): self.bstack1ll11ll1l1_opy_,
            bstack1111ll1_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣ࿃"): self.bstack111llll111_opy_
          }
        }, file)
    except:
      pass
  def bstack11llllll_opy_(self, bstack111lll1l1l_opy_):
    try:
      return any(command.get(bstack1111ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ࿄")) == bstack111lll1l1l_opy_ for command in self.bstack111lll11ll_opy_)
    except:
      return False
bstack1l1lll1l_opy_ = bstack111lll1ll1_opy_()