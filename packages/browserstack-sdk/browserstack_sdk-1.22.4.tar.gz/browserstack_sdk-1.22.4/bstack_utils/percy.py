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
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1ll1lll1l1_opy_, bstack1ll1llllll_opy_
class bstack111lll11_opy_:
  working_dir = os.getcwd()
  bstack11l11l1l1_opy_ = False
  config = {}
  binary_path = bstack1111ll1_opy_ (u"࠭ࠧᔔ")
  bstack1lll1lll1ll_opy_ = bstack1111ll1_opy_ (u"ࠧࠨᔕ")
  bstack111l1l11_opy_ = False
  bstack1lllll111l1_opy_ = None
  bstack1llll1l111l_opy_ = {}
  bstack1llll11l1l1_opy_ = 300
  bstack1llll111lll_opy_ = False
  logger = None
  bstack1lll1ll1l1l_opy_ = False
  bstack1ll1111l1l_opy_ = False
  bstack1l1l1111l_opy_ = None
  bstack1llll1ll1ll_opy_ = bstack1111ll1_opy_ (u"ࠨࠩᔖ")
  bstack1lll1ll1lll_opy_ = {
    bstack1111ll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᔗ") : 1,
    bstack1111ll1_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫᔘ") : 2,
    bstack1111ll1_opy_ (u"ࠫࡪࡪࡧࡦࠩᔙ") : 3,
    bstack1111ll1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬᔚ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1llll1l1111_opy_(self):
    bstack1llll1l1l11_opy_ = bstack1111ll1_opy_ (u"࠭ࠧᔛ")
    bstack1llll1l1ll1_opy_ = sys.platform
    bstack1llll1lll1l_opy_ = bstack1111ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᔜ")
    if re.match(bstack1111ll1_opy_ (u"ࠣࡦࡤࡶࡼ࡯࡮ࡽ࡯ࡤࡧࠥࡵࡳࠣᔝ"), bstack1llll1l1ll1_opy_) != None:
      bstack1llll1l1l11_opy_ = bstack111ll1l11l_opy_ + bstack1111ll1_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡲࡷࡽ࠴ࡺࡪࡲࠥᔞ")
      self.bstack1llll1ll1ll_opy_ = bstack1111ll1_opy_ (u"ࠪࡱࡦࡩࠧᔟ")
    elif re.match(bstack1111ll1_opy_ (u"ࠦࡲࡹࡷࡪࡰࡿࡱࡸࡿࡳࡽ࡯࡬ࡲ࡬ࡽࡼࡤࡻࡪࡻ࡮ࡴࡼࡣࡥࡦࡻ࡮ࡴࡼࡸ࡫ࡱࡧࡪࢂࡥ࡮ࡥࡿࡻ࡮ࡴ࠳࠳ࠤᔠ"), bstack1llll1l1ll1_opy_) != None:
      bstack1llll1l1l11_opy_ = bstack111ll1l11l_opy_ + bstack1111ll1_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡽࡩ࡯࠰ࡽ࡭ࡵࠨᔡ")
      bstack1llll1lll1l_opy_ = bstack1111ll1_opy_ (u"ࠨࡰࡦࡴࡦࡽ࠳࡫ࡸࡦࠤᔢ")
      self.bstack1llll1ll1ll_opy_ = bstack1111ll1_opy_ (u"ࠧࡸ࡫ࡱࠫᔣ")
    else:
      bstack1llll1l1l11_opy_ = bstack111ll1l11l_opy_ + bstack1111ll1_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮࡮࡬ࡲࡺࡾ࠮ࡻ࡫ࡳࠦᔤ")
      self.bstack1llll1ll1ll_opy_ = bstack1111ll1_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨᔥ")
    return bstack1llll1l1l11_opy_, bstack1llll1lll1l_opy_
  def bstack1lll1lllll1_opy_(self):
    try:
      bstack1lll1llllll_opy_ = [os.path.join(expanduser(bstack1111ll1_opy_ (u"ࠥࢂࠧᔦ")), bstack1111ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᔧ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1lll1llllll_opy_:
        if(self.bstack1lll1lll111_opy_(path)):
          return path
      raise bstack1111ll1_opy_ (u"࡛ࠧ࡮ࡢ࡮ࡥࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤᔨ")
    except Exception as e:
      self.logger.error(bstack1111ll1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠱ࠥࢁࡽࠣᔩ").format(e))
  def bstack1lll1lll111_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1lll1l1llll_opy_(self, bstack1llll1l1l11_opy_, bstack1llll1lll1l_opy_):
    try:
      bstack1llll11l11l_opy_ = self.bstack1lll1lllll1_opy_()
      bstack1lll1ll1l11_opy_ = os.path.join(bstack1llll11l11l_opy_, bstack1111ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴ࡺࡪࡲࠪᔪ"))
      bstack1llll1ll11l_opy_ = os.path.join(bstack1llll11l11l_opy_, bstack1llll1lll1l_opy_)
      if os.path.exists(bstack1llll1ll11l_opy_):
        self.logger.info(bstack1111ll1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᔫ").format(bstack1llll1ll11l_opy_))
        return bstack1llll1ll11l_opy_
      if os.path.exists(bstack1lll1ll1l11_opy_):
        self.logger.info(bstack1111ll1_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡼ࡬ࡴࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡺࡴࡺࡪࡲࡳ࡭ࡳ࡭ࠢᔬ").format(bstack1lll1ll1l11_opy_))
        return self.bstack1llll11ll11_opy_(bstack1lll1ll1l11_opy_, bstack1llll1lll1l_opy_)
      self.logger.info(bstack1111ll1_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱࠥࢁࡽࠣᔭ").format(bstack1llll1l1l11_opy_))
      response = bstack1ll1llllll_opy_(bstack1111ll1_opy_ (u"ࠫࡌࡋࡔࠨᔮ"), bstack1llll1l1l11_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1lll1ll1l11_opy_, bstack1111ll1_opy_ (u"ࠬࡽࡢࠨᔯ")) as file:
          file.write(response.content)
        self.logger.info(bstack1111ll1_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡤࡲࡩࠦࡳࡢࡸࡨࡨࠥࡧࡴࠡࡽࢀࠦᔰ").format(bstack1lll1ll1l11_opy_))
        return self.bstack1llll11ll11_opy_(bstack1lll1ll1l11_opy_, bstack1llll1lll1l_opy_)
      else:
        raise(bstack1111ll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠡࡕࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪࡀࠠࡼࡿࠥᔱ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1111ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽ࠿ࠦࡻࡾࠤᔲ").format(e))
  def bstack1llll1lll11_opy_(self, bstack1llll1l1l11_opy_, bstack1llll1lll1l_opy_):
    try:
      retry = 2
      bstack1llll1ll11l_opy_ = None
      bstack1llll11llll_opy_ = False
      while retry > 0:
        bstack1llll1ll11l_opy_ = self.bstack1lll1l1llll_opy_(bstack1llll1l1l11_opy_, bstack1llll1lll1l_opy_)
        bstack1llll11llll_opy_ = self.bstack1lllll1111l_opy_(bstack1llll1l1l11_opy_, bstack1llll1lll1l_opy_, bstack1llll1ll11l_opy_)
        if bstack1llll11llll_opy_:
          break
        retry -= 1
      return bstack1llll1ll11l_opy_, bstack1llll11llll_opy_
    except Exception as e:
      self.logger.error(bstack1111ll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡲࡤࡸ࡭ࠨᔳ").format(e))
    return bstack1llll1ll11l_opy_, False
  def bstack1lllll1111l_opy_(self, bstack1llll1l1l11_opy_, bstack1llll1lll1l_opy_, bstack1llll1ll11l_opy_, bstack1lll1lll1l1_opy_ = 0):
    if bstack1lll1lll1l1_opy_ > 1:
      return False
    if bstack1llll1ll11l_opy_ == None or os.path.exists(bstack1llll1ll11l_opy_) == False:
      self.logger.warn(bstack1111ll1_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡷ࡫ࡴࡳࡻ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣᔴ"))
      return False
    bstack1llll11ll1l_opy_ = bstack1111ll1_opy_ (u"ࠦࡣ࠴ࠪࡁࡲࡨࡶࡨࡿ࡜࠰ࡥ࡯࡭ࠥࡢࡤ࠯࡞ࡧ࠯࠳ࡢࡤࠬࠤᔵ")
    command = bstack1111ll1_opy_ (u"ࠬࢁࡽࠡ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫᔶ").format(bstack1llll1ll11l_opy_)
    bstack1lll1ll11l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1llll11ll1l_opy_, bstack1lll1ll11l1_opy_) != None:
      return True
    else:
      self.logger.error(bstack1111ll1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡣࡩࡧࡦ࡯ࠥ࡬ࡡࡪ࡮ࡨࡨࠧᔷ"))
      return False
  def bstack1llll11ll11_opy_(self, bstack1lll1ll1l11_opy_, bstack1llll1lll1l_opy_):
    try:
      working_dir = os.path.dirname(bstack1lll1ll1l11_opy_)
      shutil.unpack_archive(bstack1lll1ll1l11_opy_, working_dir)
      bstack1llll1ll11l_opy_ = os.path.join(working_dir, bstack1llll1lll1l_opy_)
      os.chmod(bstack1llll1ll11l_opy_, 0o755)
      return bstack1llll1ll11l_opy_
    except Exception as e:
      self.logger.error(bstack1111ll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡹࡳࢀࡩࡱࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣᔸ"))
  def bstack1llll1lllll_opy_(self):
    try:
      bstack1llll111ll1_opy_ = self.config.get(bstack1111ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᔹ"))
      bstack1llll1lllll_opy_ = bstack1llll111ll1_opy_ or (bstack1llll111ll1_opy_ is None and self.bstack11l11l1l1_opy_)
      if not bstack1llll1lllll_opy_ or self.config.get(bstack1111ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᔺ"), None) not in bstack111ll1111l_opy_:
        return False
      self.bstack111l1l11_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1111ll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᔻ").format(e))
  def bstack1lll1ll1111_opy_(self):
    try:
      bstack1lll1ll1111_opy_ = self.bstack1llll111l11_opy_
      return bstack1lll1ll1111_opy_
    except Exception as e:
      self.logger.error(bstack1111ll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾࠦࡣࡢࡲࡷࡹࡷ࡫ࠠ࡮ࡱࡧࡩ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᔼ").format(e))
  def init(self, bstack11l11l1l1_opy_, config, logger):
    self.bstack11l11l1l1_opy_ = bstack11l11l1l1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1llll1lllll_opy_():
      return
    self.bstack1llll1l111l_opy_ = config.get(bstack1111ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫᔽ"), {})
    self.bstack1llll111l11_opy_ = config.get(bstack1111ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᔾ"))
    try:
      bstack1llll1l1l11_opy_, bstack1llll1lll1l_opy_ = self.bstack1llll1l1111_opy_()
      bstack1llll1ll11l_opy_, bstack1llll11llll_opy_ = self.bstack1llll1lll11_opy_(bstack1llll1l1l11_opy_, bstack1llll1lll1l_opy_)
      if bstack1llll11llll_opy_:
        self.binary_path = bstack1llll1ll11l_opy_
        thread = Thread(target=self.bstack1lllll11111_opy_)
        thread.start()
      else:
        self.bstack1lll1ll1l1l_opy_ = True
        self.logger.error(bstack1111ll1_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾ࠮࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡖࡥࡳࡥࡼࠦᔿ").format(bstack1llll1ll11l_opy_))
    except Exception as e:
      self.logger.error(bstack1111ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᕀ").format(e))
  def bstack1llll1ll111_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1111ll1_opy_ (u"ࠩ࡯ࡳ࡬࠭ᕁ"), bstack1111ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰࡯ࡳ࡬࠭ᕂ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1111ll1_opy_ (u"ࠦࡕࡻࡳࡩ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࡴࠢࡤࡸࠥࢁࡽࠣᕃ").format(logfile))
      self.bstack1lll1lll1ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1111ll1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࠡࡲࡤࡸ࡭࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᕄ").format(e))
  def bstack1lllll11111_opy_(self):
    bstack1lll1ll1ll1_opy_ = self.bstack1lll1l1lll1_opy_()
    if bstack1lll1ll1ll1_opy_ == None:
      self.bstack1lll1ll1l1l_opy_ = True
      self.logger.error(bstack1111ll1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠤᕅ"))
      return False
    command_args = [bstack1111ll1_opy_ (u"ࠢࡢࡲࡳ࠾ࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠣᕆ") if self.bstack11l11l1l1_opy_ else bstack1111ll1_opy_ (u"ࠨࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠬᕇ")]
    bstack1lll1ll111l_opy_ = self.bstack1llll1l1l1l_opy_()
    if bstack1lll1ll111l_opy_ != None:
      command_args.append(bstack1111ll1_opy_ (u"ࠤ࠰ࡧࠥࢁࡽࠣᕈ").format(bstack1lll1ll111l_opy_))
    env = os.environ.copy()
    env[bstack1111ll1_opy_ (u"ࠥࡔࡊࡘࡃ࡚ࡡࡗࡓࡐࡋࡎࠣᕉ")] = bstack1lll1ll1ll1_opy_
    env[bstack1111ll1_opy_ (u"࡙ࠦࡎ࡟ࡃࡗࡌࡐࡉࡥࡕࡖࡋࡇࠦᕊ")] = os.environ.get(bstack1111ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᕋ"), bstack1111ll1_opy_ (u"࠭ࠧᕌ"))
    bstack1llll11l1ll_opy_ = [self.binary_path]
    self.bstack1llll1ll111_opy_()
    self.bstack1lllll111l1_opy_ = self.bstack1llll1111ll_opy_(bstack1llll11l1ll_opy_ + command_args, env)
    self.logger.debug(bstack1111ll1_opy_ (u"ࠢࡔࡶࡤࡶࡹ࡯࡮ࡨࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠣᕍ"))
    bstack1lll1lll1l1_opy_ = 0
    while self.bstack1lllll111l1_opy_.poll() == None:
      bstack1llll1l1lll_opy_ = self.bstack1llll111l1l_opy_()
      if bstack1llll1l1lll_opy_:
        self.logger.debug(bstack1111ll1_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠦᕎ"))
        self.bstack1llll111lll_opy_ = True
        return True
      bstack1lll1lll1l1_opy_ += 1
      self.logger.debug(bstack1111ll1_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡔࡨࡸࡷࡿࠠ࠮ࠢࡾࢁࠧᕏ").format(bstack1lll1lll1l1_opy_))
      time.sleep(2)
    self.logger.error(bstack1111ll1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡋࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࠦࡡࡵࡶࡨࡱࡵࡺࡳࠣᕐ").format(bstack1lll1lll1l1_opy_))
    self.bstack1lll1ll1l1l_opy_ = True
    return False
  def bstack1llll111l1l_opy_(self, bstack1lll1lll1l1_opy_ = 0):
    if bstack1lll1lll1l1_opy_ > 10:
      return False
    try:
      bstack1llll11l111_opy_ = os.environ.get(bstack1111ll1_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡗࡊࡘࡖࡆࡔࡢࡅࡉࡊࡒࡆࡕࡖࠫᕑ"), bstack1111ll1_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴ࠻࠷࠶࠷࠽࠭ᕒ"))
      bstack1lll1lll11l_opy_ = bstack1llll11l111_opy_ + bstack111ll11111_opy_
      response = requests.get(bstack1lll1lll11l_opy_)
      data = response.json()
      self.bstack1l1l1111l_opy_ = data.get(bstack1111ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬᕓ"), {}).get(bstack1111ll1_opy_ (u"ࠧࡪࡦࠪᕔ"), None)
      return True
    except:
      self.logger.debug(bstack1111ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢࡺ࡬࡮ࡲࡥࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢ࡮ࡷ࡬ࠥࡩࡨࡦࡥ࡮ࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨᕕ"))
      return False
  def bstack1lll1l1lll1_opy_(self):
    bstack1lll1llll11_opy_ = bstack1111ll1_opy_ (u"ࠩࡤࡴࡵ࠭ᕖ") if self.bstack11l11l1l1_opy_ else bstack1111ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᕗ")
    bstack1lll1llll1l_opy_ = bstack1111ll1_opy_ (u"ࠦࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠢᕘ") if self.config.get(bstack1111ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᕙ")) is None else True
    bstack1111lll1l1_opy_ = bstack1111ll1_opy_ (u"ࠨࡡࡱ࡫࠲ࡥࡵࡶ࡟ࡱࡧࡵࡧࡾ࠵ࡧࡦࡶࡢࡴࡷࡵࡪࡦࡥࡷࡣࡹࡵ࡫ࡦࡰࡂࡲࡦࡳࡥ࠾ࡽࢀࠪࡹࡿࡰࡦ࠿ࡾࢁࠫࡶࡥࡳࡥࡼࡁࢀࢃࠢᕚ").format(self.config[bstack1111ll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᕛ")], bstack1lll1llll11_opy_, bstack1lll1llll1l_opy_)
    if self.bstack1llll111l11_opy_:
      bstack1111lll1l1_opy_ += bstack1111ll1_opy_ (u"ࠣࠨࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫࠽ࡼࡿࠥᕜ").format(self.bstack1llll111l11_opy_)
    uri = bstack1ll1lll1l1_opy_(bstack1111lll1l1_opy_)
    try:
      response = bstack1ll1llllll_opy_(bstack1111ll1_opy_ (u"ࠩࡊࡉ࡙࠭ᕝ"), uri, {}, {bstack1111ll1_opy_ (u"ࠪࡥࡺࡺࡨࠨᕞ"): (self.config[bstack1111ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᕟ")], self.config[bstack1111ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᕠ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack111l1l11_opy_ = data.get(bstack1111ll1_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᕡ"))
        self.bstack1llll111l11_opy_ = data.get(bstack1111ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࠬᕢ"))
        os.environ[bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭ᕣ")] = str(self.bstack111l1l11_opy_)
        os.environ[bstack1111ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ᕤ")] = str(self.bstack1llll111l11_opy_)
        if bstack1lll1llll1l_opy_ == bstack1111ll1_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨᕥ") and str(self.bstack111l1l11_opy_).lower() == bstack1111ll1_opy_ (u"ࠦࡹࡸࡵࡦࠤᕦ"):
          self.bstack1ll1111l1l_opy_ = True
        if bstack1111ll1_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦᕧ") in data:
          return data[bstack1111ll1_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧᕨ")]
        else:
          raise bstack1111ll1_opy_ (u"ࠧࡕࡱ࡮ࡩࡳࠦࡎࡰࡶࠣࡊࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠧᕩ").format(data)
      else:
        raise bstack1111ll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡴࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡸࡺࡡࡵࡷࡶࠤ࠲ࠦࡻࡾ࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡈ࡯ࡥࡻࠣ࠱ࠥࢁࡽࠣᕪ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1111ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡳࡶࡴࡰࡥࡤࡶࠥᕫ").format(e))
  def bstack1llll1l1l1l_opy_(self):
    bstack1llll1111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111ll1_opy_ (u"ࠥࡴࡪࡸࡣࡺࡅࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳࠨᕬ"))
    try:
      if bstack1111ll1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᕭ") not in self.bstack1llll1l111l_opy_:
        self.bstack1llll1l111l_opy_[bstack1111ll1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ᕮ")] = 2
      with open(bstack1llll1111l1_opy_, bstack1111ll1_opy_ (u"࠭ࡷࠨᕯ")) as fp:
        json.dump(self.bstack1llll1l111l_opy_, fp)
      return bstack1llll1111l1_opy_
    except Exception as e:
      self.logger.error(bstack1111ll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡧࡷ࡫ࡡࡵࡧࠣࡴࡪࡸࡣࡺࠢࡦࡳࡳ࡬ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᕰ").format(e))
  def bstack1llll1111ll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1llll1ll1ll_opy_ == bstack1111ll1_opy_ (u"ࠨࡹ࡬ࡲࠬᕱ"):
        bstack1llll11111l_opy_ = [bstack1111ll1_opy_ (u"ࠩࡦࡱࡩ࠴ࡥࡹࡧࠪᕲ"), bstack1111ll1_opy_ (u"ࠪ࠳ࡨ࠭ᕳ")]
        cmd = bstack1llll11111l_opy_ + cmd
      cmd = bstack1111ll1_opy_ (u"ࠫࠥ࠭ᕴ").join(cmd)
      self.logger.debug(bstack1111ll1_opy_ (u"ࠧࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻࡾࠤᕵ").format(cmd))
      with open(self.bstack1lll1lll1ll_opy_, bstack1111ll1_opy_ (u"ࠨࡡࠣᕶ")) as bstack1lll1ll11ll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1lll1ll11ll_opy_, text=True, stderr=bstack1lll1ll11ll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1lll1ll1l1l_opy_ = True
      self.logger.error(bstack1111ll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠡࡹ࡬ࡸ࡭ࠦࡣ࡮ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᕷ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1llll111lll_opy_:
        self.logger.info(bstack1111ll1_opy_ (u"ࠣࡕࡷࡳࡵࡶࡩ࡯ࡩࠣࡔࡪࡸࡣࡺࠤᕸ"))
        cmd = [self.binary_path, bstack1111ll1_opy_ (u"ࠤࡨࡼࡪࡩ࠺ࡴࡶࡲࡴࠧᕹ")]
        self.bstack1llll1111ll_opy_(cmd)
        self.bstack1llll111lll_opy_ = False
    except Exception as e:
      self.logger.error(bstack1111ll1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡱࡳࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡧࡴࡳ࡭ࡢࡰࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᕺ").format(cmd, e))
  def bstack1ll1l1111_opy_(self):
    if not self.bstack111l1l11_opy_:
      return
    try:
      bstack1llll1l11ll_opy_ = 0
      while not self.bstack1llll111lll_opy_ and bstack1llll1l11ll_opy_ < self.bstack1llll11l1l1_opy_:
        if self.bstack1lll1ll1l1l_opy_:
          self.logger.info(bstack1111ll1_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡩࡥ࡮ࡲࡥࡥࠤᕻ"))
          return
        time.sleep(1)
        bstack1llll1l11ll_opy_ += 1
      os.environ[bstack1111ll1_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡇࡋࡓࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫᕼ")] = str(self.bstack1llll1llll1_opy_())
      self.logger.info(bstack1111ll1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠢᕽ"))
    except Exception as e:
      self.logger.error(bstack1111ll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᕾ").format(e))
  def bstack1llll1llll1_opy_(self):
    if self.bstack11l11l1l1_opy_:
      return
    try:
      bstack1llll111111_opy_ = [platform[bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᕿ")].lower() for platform in self.config.get(bstack1111ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᖀ"), [])]
      bstack1llll11lll1_opy_ = sys.maxsize
      bstack1llll1ll1l1_opy_ = bstack1111ll1_opy_ (u"ࠪࠫᖁ")
      for browser in bstack1llll111111_opy_:
        if browser in self.bstack1lll1ll1lll_opy_:
          bstack1llll1l11l1_opy_ = self.bstack1lll1ll1lll_opy_[browser]
        if bstack1llll1l11l1_opy_ < bstack1llll11lll1_opy_:
          bstack1llll11lll1_opy_ = bstack1llll1l11l1_opy_
          bstack1llll1ll1l1_opy_ = browser
      return bstack1llll1ll1l1_opy_
    except Exception as e:
      self.logger.error(bstack1111ll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡨࡥࡴࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᖂ").format(e))
  @classmethod
  def bstack111111ll1_opy_(self):
    return os.getenv(bstack1111ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪᖃ"), bstack1111ll1_opy_ (u"࠭ࡆࡢ࡮ࡶࡩࠬᖄ")).lower()
  @classmethod
  def bstack1l11ll11_opy_(self):
    return os.getenv(bstack1111ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫᖅ"), bstack1111ll1_opy_ (u"ࠨࠩᖆ"))