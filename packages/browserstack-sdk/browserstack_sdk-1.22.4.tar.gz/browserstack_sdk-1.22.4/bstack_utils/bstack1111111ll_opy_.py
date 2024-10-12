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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack111ll11l1l_opy_, bstack111ll111l1_opy_
import tempfile
import json
bstack1llllll111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠩᒥ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1111ll1_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ᒦ"),
      datefmt=bstack1111ll1_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫᒧ"),
      stream=sys.stdout
    )
  return logger
def bstack1llllll11ll_opy_():
  global bstack1llllll111l_opy_
  if os.path.exists(bstack1llllll111l_opy_):
    os.remove(bstack1llllll111l_opy_)
def bstack1111l111l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11ll11l1_opy_(config, log_level):
  bstack1lllll1l111_opy_ = log_level
  if bstack1111ll1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᒨ") in config and config[bstack1111ll1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᒩ")] in bstack111ll11l1l_opy_:
    bstack1lllll1l111_opy_ = bstack111ll11l1l_opy_[config[bstack1111ll1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᒪ")]]
  if config.get(bstack1111ll1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᒫ"), False):
    logging.getLogger().setLevel(bstack1lllll1l111_opy_)
    return bstack1lllll1l111_opy_
  global bstack1llllll111l_opy_
  bstack1111l111l_opy_()
  bstack1lllll1ll1l_opy_ = logging.Formatter(
    fmt=bstack1111ll1_opy_ (u"ࠧ࡝ࡰࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬᒬ"),
    datefmt=bstack1111ll1_opy_ (u"ࠨࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪᒭ")
  )
  bstack1lllll1l1l1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1llllll111l_opy_)
  file_handler.setFormatter(bstack1lllll1ll1l_opy_)
  bstack1lllll1l1l1_opy_.setFormatter(bstack1lllll1ll1l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lllll1l1l1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1111ll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫᒮ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lllll1l1l1_opy_.setLevel(bstack1lllll1l111_opy_)
  logging.getLogger().addHandler(bstack1lllll1l1l1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lllll1l111_opy_
def bstack1lllll1ll11_opy_(config):
  try:
    bstack1llllll1111_opy_ = set(bstack111ll111l1_opy_)
    bstack1llllll11l1_opy_ = bstack1111ll1_opy_ (u"ࠪࠫᒯ")
    with open(bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧᒰ")) as bstack1llllll1l11_opy_:
      bstack1lllll1llll_opy_ = bstack1llllll1l11_opy_.read()
      bstack1llllll11l1_opy_ = re.sub(bstack1111ll1_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠣ࠯ࠬࠧࡠࡳ࠭ᒱ"), bstack1111ll1_opy_ (u"࠭ࠧᒲ"), bstack1lllll1llll_opy_, flags=re.M)
      bstack1llllll11l1_opy_ = re.sub(
        bstack1111ll1_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠪࠪᒳ") + bstack1111ll1_opy_ (u"ࠨࡾࠪᒴ").join(bstack1llllll1111_opy_) + bstack1111ll1_opy_ (u"ࠩࠬ࠲࠯ࠪࠧᒵ"),
        bstack1111ll1_opy_ (u"ࡵࠫࡡ࠸࠺ࠡ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬᒶ"),
        bstack1llllll11l1_opy_, flags=re.M | re.I
      )
    def bstack1lllll1lll1_opy_(dic):
      bstack1lllll1l11l_opy_ = {}
      for key, value in dic.items():
        if key in bstack1llllll1111_opy_:
          bstack1lllll1l11l_opy_[key] = bstack1111ll1_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᒷ")
        else:
          if isinstance(value, dict):
            bstack1lllll1l11l_opy_[key] = bstack1lllll1lll1_opy_(value)
          else:
            bstack1lllll1l11l_opy_[key] = value
      return bstack1lllll1l11l_opy_
    bstack1lllll1l11l_opy_ = bstack1lllll1lll1_opy_(config)
    return {
      bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᒸ"): bstack1llllll11l1_opy_,
      bstack1111ll1_opy_ (u"࠭ࡦࡪࡰࡤࡰࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᒹ"): json.dumps(bstack1lllll1l11l_opy_)
    }
  except Exception as e:
    return {}
def bstack1l1111l1_opy_(config):
  global bstack1llllll111l_opy_
  try:
    if config.get(bstack1111ll1_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩᒺ"), False):
      return
    uuid = os.getenv(bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᒻ"))
    if not uuid or uuid == bstack1111ll1_opy_ (u"ࠩࡱࡹࡱࡲࠧᒼ"):
      return
    bstack1lllll1l1ll_opy_ = [bstack1111ll1_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡱࡪࡴࡴࡴ࠰ࡷࡼࡹ࠭ᒽ"), bstack1111ll1_opy_ (u"ࠫࡕ࡯ࡰࡧ࡫࡯ࡩࠬᒾ"), bstack1111ll1_opy_ (u"ࠬࡶࡹࡱࡴࡲ࡮ࡪࡩࡴ࠯ࡶࡲࡱࡱ࠭ᒿ"), bstack1llllll111l_opy_]
    bstack1111l111l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1111ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡬ࡰࡩࡶ࠱ࠬᓀ") + uuid + bstack1111ll1_opy_ (u"ࠧ࠯ࡶࡤࡶ࠳࡭ࡺࠨᓁ"))
    with tarfile.open(output_file, bstack1111ll1_opy_ (u"ࠣࡹ࠽࡫ࡿࠨᓂ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lllll1l1ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lllll1ll11_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1llllll1l1l_opy_ = data.encode()
        tarinfo.size = len(bstack1llllll1l1l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1llllll1l1l_opy_))
    bstack1l1l1lll1_opy_ = MultipartEncoder(
      fields= {
        bstack1111ll1_opy_ (u"ࠩࡧࡥࡹࡧࠧᓃ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1111ll1_opy_ (u"ࠪࡶࡧ࠭ᓄ")), bstack1111ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࠱࡬ࢀࡩࡱࠩᓅ")),
        bstack1111ll1_opy_ (u"ࠬࡩ࡬ࡪࡧࡱࡸࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᓆ"): uuid
      }
    )
    response = requests.post(
      bstack1111ll1_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡶࡲ࡯ࡳࡦࡪ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡧࡱ࡯ࡥ࡯ࡶ࠰ࡰࡴ࡭ࡳ࠰ࡷࡳࡰࡴࡧࡤࠣᓇ"),
      data=bstack1l1l1lll1_opy_,
      headers={bstack1111ll1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᓈ"): bstack1l1l1lll1_opy_.content_type},
      auth=(config[bstack1111ll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᓉ")], config[bstack1111ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᓊ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1111ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡸࡴࡱࡵࡡࡥࠢ࡯ࡳ࡬ࡹ࠺ࠡࠩᓋ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1111ll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡱࡵࡧࡴ࠼ࠪᓌ") + str(e))
  finally:
    try:
      bstack1llllll11ll_opy_()
    except:
      pass