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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from uuid import uuid4
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1ll1111ll_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1111lll1l_opy_ import bstack1llll1111l_opy_
import time
import requests
def bstack1l1l11lll1_opy_():
  global CONFIG
  headers = {
        bstack1111ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1111ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1lll1lll_opy_(CONFIG, bstack11lll1l11_opy_)
  try:
    response = requests.get(bstack11lll1l11_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1llll11ll_opy_ = response.json()[bstack1111ll1_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l111l11ll_opy_.format(response.json()))
      return bstack1llll11ll_opy_
    else:
      logger.debug(bstack1ll1l111l1_opy_.format(bstack1111ll1_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1ll1l111l1_opy_.format(e))
def bstack1l1lll11l_opy_(hub_url):
  global CONFIG
  url = bstack1111ll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1111ll1_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1111ll1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1111ll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1lll1lll_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l111lll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1111ll111_opy_.format(hub_url, e))
def bstack1lllll1l1_opy_():
  try:
    global bstack1l1lll1lll_opy_
    bstack1llll11ll_opy_ = bstack1l1l11lll1_opy_()
    bstack1l1111llll_opy_ = []
    results = []
    for bstack1l1l1llll1_opy_ in bstack1llll11ll_opy_:
      bstack1l1111llll_opy_.append(bstack1lllll11l1_opy_(target=bstack1l1lll11l_opy_,args=(bstack1l1l1llll1_opy_,)))
    for t in bstack1l1111llll_opy_:
      t.start()
    for t in bstack1l1111llll_opy_:
      results.append(t.join())
    bstack1ll1l11lll_opy_ = {}
    for item in results:
      hub_url = item[bstack1111ll1_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1111ll1_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1ll1l11lll_opy_[hub_url] = latency
    bstack1l11l1l1ll_opy_ = min(bstack1ll1l11lll_opy_, key= lambda x: bstack1ll1l11lll_opy_[x])
    bstack1l1lll1lll_opy_ = bstack1l11l1l1ll_opy_
    logger.debug(bstack1ll111lll_opy_.format(bstack1l11l1l1ll_opy_))
  except Exception as e:
    logger.debug(bstack1l1llll1l1_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1111111ll_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack1ll1ll111l_opy_, bstack1ll1llllll_opy_, bstack1ll1lll1l1_opy_, bstack1llll1l11_opy_, bstack1l111l1ll_opy_, \
  Notset, bstack1lll1111l_opy_, \
  bstack111llll11_opy_, bstack11l1l11ll_opy_, bstack1l1l1l1l_opy_, bstack1l111111l_opy_, bstack1ll11l1lll_opy_, bstack1l1l11ll_opy_, \
  bstack111llllll_opy_, \
  bstack1lll11111l_opy_, bstack1ll1l1llll_opy_, bstack1l11llll_opy_, bstack1l11111lll_opy_, \
  bstack1ll1l1l11_opy_, bstack1llll11l1_opy_, bstack1l11l1ll11_opy_, bstack1lll11ll1l_opy_
from bstack_utils.bstack1llll1l1ll_opy_ import bstack11llll111_opy_
from bstack_utils.bstack1ll11l1l1l_opy_ import bstack1l1l1l1lll_opy_
from bstack_utils.bstack1ll1lll1_opy_ import bstack1ll1l1ll1_opy_, bstack11l1ll1ll_opy_
from bstack_utils.bstack1ll1lllll_opy_ import bstack1l1111l11_opy_
from bstack_utils.bstack1111lll11_opy_ import bstack11lll1lll_opy_
from bstack_utils.bstack1l1lll1l_opy_ import bstack1l1lll1l_opy_
from bstack_utils.proxy import bstack11l1l1111_opy_, bstack1lll1lll_opy_, bstack1lll11llll_opy_, bstack1ll11111l_opy_
import bstack_utils.bstack1lllllll1l_opy_ as bstack11l11l111_opy_
from browserstack_sdk.bstack1l111111_opy_ import *
from browserstack_sdk.bstack1l1ll1ll11_opy_ import *
from bstack_utils.bstack11ll11111_opy_ import bstack1lllll1ll_opy_
from browserstack_sdk.bstack1l1111ll1l_opy_ import *
import bstack_utils.bstack1l11l11111_opy_ as bstack1ll11l1l1_opy_
import bstack_utils.bstack1l1ll1ll1_opy_ as bstack1ll1111l11_opy_
bstack1lll11ll1_opy_ = bstack1111ll1_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack11ll111l1_opy_ = bstack1111ll1_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1lll1ll1ll_opy_ = None
CONFIG = {}
bstack111l1111l_opy_ = {}
bstack11ll1l11l_opy_ = {}
bstack11l111ll1_opy_ = None
bstack11lll1ll1_opy_ = None
bstack111111ll_opy_ = None
bstack1l1ll1l111_opy_ = -1
bstack1111ll1ll_opy_ = 0
bstack1l1111l1l1_opy_ = bstack1l1l1l1ll1_opy_
bstack1llll1ll1l_opy_ = 1
bstack111l1l11l_opy_ = False
bstack1l11l1llll_opy_ = False
bstack1ll1l11ll_opy_ = bstack1111ll1_opy_ (u"ࠨࠩࢂ")
bstack1l11l11lll_opy_ = bstack1111ll1_opy_ (u"ࠩࠪࢃ")
bstack1l1lll1111_opy_ = False
bstack1ll111ll_opy_ = True
bstack1l1llllll1_opy_ = bstack1111ll1_opy_ (u"ࠪࠫࢄ")
bstack111lll1ll_opy_ = []
bstack1l1lll1lll_opy_ = bstack1111ll1_opy_ (u"ࠫࠬࢅ")
bstack1l1l11l1ll_opy_ = False
bstack11111l1ll_opy_ = None
bstack111l1llll_opy_ = None
bstack11ll1llll_opy_ = None
bstack1lllll1ll1_opy_ = -1
bstack1l1ll11lll_opy_ = os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠬࢄࠧࢆ")), bstack1111ll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack1111ll1_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1lll111l1l_opy_ = 0
bstack11l1lll11_opy_ = 0
bstack1l1l111l1l_opy_ = []
bstack1ll1111l_opy_ = []
bstack11lll111l_opy_ = []
bstack1lll1l11ll_opy_ = []
bstack11ll1111_opy_ = bstack1111ll1_opy_ (u"ࠨࠩࢉ")
bstack1llll11l11_opy_ = bstack1111ll1_opy_ (u"ࠩࠪࢊ")
bstack1l1lll1l1l_opy_ = False
bstack111lllll_opy_ = False
bstack1l1111l111_opy_ = {}
bstack1lll11l1l1_opy_ = None
bstack1l111ll11l_opy_ = None
bstack1111ll1l_opy_ = None
bstack11111lll_opy_ = None
bstack1lll11l11l_opy_ = None
bstack1l11ll1ll_opy_ = None
bstack111111111_opy_ = None
bstack1ll1l1l1l1_opy_ = None
bstack111l11ll_opy_ = None
bstack1l111l1l1_opy_ = None
bstack1ll1l1lll_opy_ = None
bstack1lll1l1l1_opy_ = None
bstack1l11l1l11_opy_ = None
bstack1l1llll11_opy_ = None
bstack1l1ll1111_opy_ = None
bstack1ll1ll1l_opy_ = None
bstack1llll11111_opy_ = None
bstack1l1lllll1_opy_ = None
bstack1lll1lll1_opy_ = None
bstack1ll1ll1l11_opy_ = None
bstack11lllll1_opy_ = None
bstack1ll111l1l1_opy_ = None
bstack11lll111_opy_ = False
bstack1l111lll1_opy_ = bstack1111ll1_opy_ (u"ࠥࠦࢋ")
logger = bstack1111111ll_opy_.get_logger(__name__, bstack1l1111l1l1_opy_)
bstack11l11l1ll_opy_ = Config.bstack1111l1lll_opy_()
percy = bstack111lll11_opy_()
bstack111l1l11_opy_ = bstack1llll1111l_opy_()
bstack1ll1l11ll1_opy_ = bstack1l1111ll1l_opy_()
def bstack1l1l1l11_opy_():
  global CONFIG
  global bstack1l1lll1l1l_opy_
  global bstack11l11l1ll_opy_
  bstack1ll11ll11l_opy_ = bstack11111l111_opy_(CONFIG)
  if bstack1l111l1ll_opy_(CONFIG):
    if (bstack1111ll1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ࢌ") in bstack1ll11ll11l_opy_ and str(bstack1ll11ll11l_opy_[bstack1111ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ")]).lower() == bstack1111ll1_opy_ (u"࠭ࡴࡳࡷࡨࠫࢎ")):
      bstack1l1lll1l1l_opy_ = True
    bstack11l11l1ll_opy_.bstack11l1l1lll_opy_(bstack1ll11ll11l_opy_.get(bstack1111ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ࢏"), False))
  else:
    bstack1l1lll1l1l_opy_ = True
    bstack11l11l1ll_opy_.bstack11l1l1lll_opy_(True)
def bstack1l11llll1l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack111l11ll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack111ll111l_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1111ll1_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack1111ll1_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1llllll1_opy_
      bstack1l1llllll1_opy_ += bstack1111ll1_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack11111ll1l_opy_ = re.compile(bstack1111ll1_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack1ll1l1ll1l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11111ll1l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1111ll1_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack1111ll1_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack11111l1l1_opy_():
  bstack1111l11l1_opy_ = bstack111ll111l_opy_()
  if bstack1111l11l1_opy_ and os.path.exists(os.path.abspath(bstack1111l11l1_opy_)):
    fileName = bstack1111l11l1_opy_
  if bstack1111ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack1111ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack1111ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack1111ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack1l11111_opy_ = os.path.abspath(fileName)
  else:
    bstack1l11111_opy_ = bstack1111ll1_opy_ (u"࢛ࠬ࠭")
  bstack1l11llll11_opy_ = os.getcwd()
  bstack111l1ll11_opy_ = bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack1llllll1l1_opy_ = bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack1l11111_opy_)) and bstack1l11llll11_opy_ != bstack1111ll1_opy_ (u"ࠣࠤ࢞"):
    bstack1l11111_opy_ = os.path.join(bstack1l11llll11_opy_, bstack111l1ll11_opy_)
    if not os.path.exists(bstack1l11111_opy_):
      bstack1l11111_opy_ = os.path.join(bstack1l11llll11_opy_, bstack1llllll1l1_opy_)
    if bstack1l11llll11_opy_ != os.path.dirname(bstack1l11llll11_opy_):
      bstack1l11llll11_opy_ = os.path.dirname(bstack1l11llll11_opy_)
    else:
      bstack1l11llll11_opy_ = bstack1111ll1_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack1l11111_opy_):
    bstack1l11l1l1l1_opy_(
      bstack1ll1111lll_opy_.format(os.getcwd()))
  try:
    with open(bstack1l11111_opy_, bstack1111ll1_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack1111ll1_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack11111ll1l_opy_)
      yaml.add_constructor(bstack1111ll1_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack1ll1l1ll1l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1l11111_opy_, bstack1111ll1_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1l11l1l1l1_opy_(bstack1ll1ll1l1_opy_.format(str(exc)))
def bstack1ll11111l1_opy_(config):
  bstack11lll1l1l_opy_ = bstack1l111ll1ll_opy_(config)
  for option in list(bstack11lll1l1l_opy_):
    if option.lower() in bstack1ll1llll_opy_ and option != bstack1ll1llll_opy_[option.lower()]:
      bstack11lll1l1l_opy_[bstack1ll1llll_opy_[option.lower()]] = bstack11lll1l1l_opy_[option]
      del bstack11lll1l1l_opy_[option]
  return config
def bstack11lll11l1_opy_():
  global bstack11ll1l11l_opy_
  for key, bstack1lll1111ll_opy_ in bstack1ll11lll11_opy_.items():
    if isinstance(bstack1lll1111ll_opy_, list):
      for var in bstack1lll1111ll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11ll1l11l_opy_[key] = os.environ[var]
          break
    elif bstack1lll1111ll_opy_ in os.environ and os.environ[bstack1lll1111ll_opy_] and str(os.environ[bstack1lll1111ll_opy_]).strip():
      bstack11ll1l11l_opy_[key] = os.environ[bstack1lll1111ll_opy_]
  if bstack1111ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack11ll1l11l_opy_[bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack11ll1l11l_opy_[bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack1111ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack1111ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack1ll11l1l_opy_():
  global bstack111l1111l_opy_
  global bstack1l1llllll1_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1111ll1_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack111l1111l_opy_[bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack111l1111l_opy_[bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack1111ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1l1l11l1l1_opy_ in bstack1l111ll111_opy_.items():
    if isinstance(bstack1l1l11l1l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l1l11l1l1_opy_:
          if idx < len(sys.argv) and bstack1111ll1_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack111l1111l_opy_:
            bstack111l1111l_opy_[key] = sys.argv[idx + 1]
            bstack1l1llllll1_opy_ += bstack1111ll1_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack1111ll1_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1111ll1_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack1l1l11l1l1_opy_.lower() == val.lower() and not key in bstack111l1111l_opy_:
          bstack111l1111l_opy_[key] = sys.argv[idx + 1]
          bstack1l1llllll1_opy_ += bstack1111ll1_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack1l1l11l1l1_opy_ + bstack1111ll1_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l11ll11l_opy_(config):
  bstack1l1l11111_opy_ = config.keys()
  for bstack1l1ll11l1_opy_, bstack111l111l1_opy_ in bstack1ll1ll1111_opy_.items():
    if bstack111l111l1_opy_ in bstack1l1l11111_opy_:
      config[bstack1l1ll11l1_opy_] = config[bstack111l111l1_opy_]
      del config[bstack111l111l1_opy_]
  for bstack1l1ll11l1_opy_, bstack111l111l1_opy_ in bstack1l1l1111ll_opy_.items():
    if isinstance(bstack111l111l1_opy_, list):
      for bstack11l1111ll_opy_ in bstack111l111l1_opy_:
        if bstack11l1111ll_opy_ in bstack1l1l11111_opy_:
          config[bstack1l1ll11l1_opy_] = config[bstack11l1111ll_opy_]
          del config[bstack11l1111ll_opy_]
          break
    elif bstack111l111l1_opy_ in bstack1l1l11111_opy_:
      config[bstack1l1ll11l1_opy_] = config[bstack111l111l1_opy_]
      del config[bstack111l111l1_opy_]
  for bstack11l1111ll_opy_ in list(config):
    for bstack1ll111ll11_opy_ in bstack1l11ll11l1_opy_:
      if bstack11l1111ll_opy_.lower() == bstack1ll111ll11_opy_.lower() and bstack11l1111ll_opy_ != bstack1ll111ll11_opy_:
        config[bstack1ll111ll11_opy_] = config[bstack11l1111ll_opy_]
        del config[bstack11l1111ll_opy_]
  bstack1l1l1l11l_opy_ = [{}]
  if not config.get(bstack1111ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ")):
    config[bstack1111ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")] = [{}]
  bstack1l1l1l11l_opy_ = config[bstack1111ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࢵ")]
  for platform in bstack1l1l1l11l_opy_:
    for bstack11l1111ll_opy_ in list(platform):
      for bstack1ll111ll11_opy_ in bstack1l11ll11l1_opy_:
        if bstack11l1111ll_opy_.lower() == bstack1ll111ll11_opy_.lower() and bstack11l1111ll_opy_ != bstack1ll111ll11_opy_:
          platform[bstack1ll111ll11_opy_] = platform[bstack11l1111ll_opy_]
          del platform[bstack11l1111ll_opy_]
  for bstack1l1ll11l1_opy_, bstack111l111l1_opy_ in bstack1l1l1111ll_opy_.items():
    for platform in bstack1l1l1l11l_opy_:
      if isinstance(bstack111l111l1_opy_, list):
        for bstack11l1111ll_opy_ in bstack111l111l1_opy_:
          if bstack11l1111ll_opy_ in platform:
            platform[bstack1l1ll11l1_opy_] = platform[bstack11l1111ll_opy_]
            del platform[bstack11l1111ll_opy_]
            break
      elif bstack111l111l1_opy_ in platform:
        platform[bstack1l1ll11l1_opy_] = platform[bstack111l111l1_opy_]
        del platform[bstack111l111l1_opy_]
  for bstack1l1lll111_opy_ in bstack1111l1ll_opy_:
    if bstack1l1lll111_opy_ in config:
      if not bstack1111l1ll_opy_[bstack1l1lll111_opy_] in config:
        config[bstack1111l1ll_opy_[bstack1l1lll111_opy_]] = {}
      config[bstack1111l1ll_opy_[bstack1l1lll111_opy_]].update(config[bstack1l1lll111_opy_])
      del config[bstack1l1lll111_opy_]
  for platform in bstack1l1l1l11l_opy_:
    for bstack1l1lll111_opy_ in bstack1111l1ll_opy_:
      if bstack1l1lll111_opy_ in list(platform):
        if not bstack1111l1ll_opy_[bstack1l1lll111_opy_] in platform:
          platform[bstack1111l1ll_opy_[bstack1l1lll111_opy_]] = {}
        platform[bstack1111l1ll_opy_[bstack1l1lll111_opy_]].update(platform[bstack1l1lll111_opy_])
        del platform[bstack1l1lll111_opy_]
  config = bstack1ll11111l1_opy_(config)
  return config
def bstack1ll11111_opy_(config):
  global bstack1l11l11lll_opy_
  if bstack1l111l1ll_opy_(config) and bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ") in config and str(config[bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢷ")]).lower() != bstack1111ll1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࢸ"):
    if not bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ") in config:
      config[bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢺ")] = {}
    if not config[bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")].get(bstack1111ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧࢼ")) and not bstack1111ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢽ") in config[bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢾ")]:
      bstack111lll1l_opy_ = datetime.datetime.now()
      bstack1llll1ll11_opy_ = bstack111lll1l_opy_.strftime(bstack1111ll1_opy_ (u"࠭ࠥࡥࡡࠨࡦࡤࠫࡈࠦࡏࠪࢿ"))
      hostname = socket.gethostname()
      bstack1l11111ll_opy_ = bstack1111ll1_opy_ (u"ࠧࠨࣀ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1111ll1_opy_ (u"ࠨࡽࢀࡣࢀࢃ࡟ࡼࡿࠪࣁ").format(bstack1llll1ll11_opy_, hostname, bstack1l11111ll_opy_)
      config[bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣂ")][bstack1111ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣃ")] = identifier
    bstack1l11l11lll_opy_ = config[bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣄ")].get(bstack1111ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ"))
  return config
def bstack1l11l1111l_opy_():
  bstack1l1ll11111_opy_ =  bstack1l111111l_opy_()[bstack1111ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠬࣆ")]
  return bstack1l1ll11111_opy_ if bstack1l1ll11111_opy_ else -1
def bstack1l1ll1l1l1_opy_(bstack1l1ll11111_opy_):
  global CONFIG
  if not bstack1111ll1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣇ") in CONFIG[bstack1111ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣈ")]:
    return
  CONFIG[bstack1111ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")] = CONFIG[bstack1111ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")].replace(
    bstack1111ll1_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭࣋"),
    str(bstack1l1ll11111_opy_)
  )
def bstack1lll11l1ll_opy_():
  global CONFIG
  if not bstack1111ll1_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫ࣌") in CONFIG[bstack1111ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")]:
    return
  bstack111lll1l_opy_ = datetime.datetime.now()
  bstack1llll1ll11_opy_ = bstack111lll1l_opy_.strftime(bstack1111ll1_opy_ (u"ࠧࠦࡦ࠰ࠩࡧ࠳ࠥࡉ࠼ࠨࡑࠬ࣎"))
  CONFIG[bstack1111ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ")] = CONFIG[bstack1111ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")].replace(
    bstack1111ll1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾ࣑ࠩ"),
    bstack1llll1ll11_opy_
  )
def bstack1l111l1l11_opy_():
  global CONFIG
  if bstack1111ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG and not bool(CONFIG[bstack1111ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")]):
    del CONFIG[bstack1111ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]
    return
  if not bstack1111ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ") in CONFIG:
    CONFIG[bstack1111ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")] = bstack1111ll1_opy_ (u"ࠩࠦࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬࣗ")
  if bstack1111ll1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩࣘ") in CONFIG[bstack1111ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣙ")]:
    bstack1lll11l1ll_opy_()
    os.environ[bstack1111ll1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩࣚ")] = CONFIG[bstack1111ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣛ")]
  if not bstack1111ll1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣜ") in CONFIG[bstack1111ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣝ")]:
    return
  bstack1l1ll11111_opy_ = bstack1111ll1_opy_ (u"ࠩࠪࣞ")
  bstack1ll1l1ll_opy_ = bstack1l11l1111l_opy_()
  if bstack1ll1l1ll_opy_ != -1:
    bstack1l1ll11111_opy_ = bstack1111ll1_opy_ (u"ࠪࡇࡎࠦࠧࣟ") + str(bstack1ll1l1ll_opy_)
  if bstack1l1ll11111_opy_ == bstack1111ll1_opy_ (u"ࠫࠬ࣠"):
    bstack1ll1ll11l_opy_ = bstack1l1lll1l11_opy_(CONFIG[bstack1111ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࣡")])
    if bstack1ll1ll11l_opy_ != -1:
      bstack1l1ll11111_opy_ = str(bstack1ll1ll11l_opy_)
  if bstack1l1ll11111_opy_:
    bstack1l1ll1l1l1_opy_(bstack1l1ll11111_opy_)
    os.environ[bstack1111ll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ࣢")] = CONFIG[bstack1111ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")]
def bstack1ll1llll1_opy_(bstack1l1l1ll1l1_opy_, bstack1l1111l1ll_opy_, path):
  bstack1l1ll111l_opy_ = {
    bstack1111ll1_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣤ"): bstack1l1111l1ll_opy_
  }
  if os.path.exists(path):
    bstack11ll1111l_opy_ = json.load(open(path, bstack1111ll1_opy_ (u"ࠩࡵࡦࠬࣥ")))
  else:
    bstack11ll1111l_opy_ = {}
  bstack11ll1111l_opy_[bstack1l1l1ll1l1_opy_] = bstack1l1ll111l_opy_
  with open(path, bstack1111ll1_opy_ (u"ࠥࡻ࠰ࠨࣦ")) as outfile:
    json.dump(bstack11ll1111l_opy_, outfile)
def bstack1l1lll1l11_opy_(bstack1l1l1ll1l1_opy_):
  bstack1l1l1ll1l1_opy_ = str(bstack1l1l1ll1l1_opy_)
  bstack1l1l111l1_opy_ = os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠫࢃ࠭ࣧ")), bstack1111ll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬࣨ"))
  try:
    if not os.path.exists(bstack1l1l111l1_opy_):
      os.makedirs(bstack1l1l111l1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"࠭ࡾࠨࣩ")), bstack1111ll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ࣪"), bstack1111ll1_opy_ (u"ࠨ࠰ࡥࡹ࡮ࡲࡤ࠮ࡰࡤࡱࡪ࠳ࡣࡢࡥ࡫ࡩ࠳ࡰࡳࡰࡰࠪ࣫"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1111ll1_opy_ (u"ࠩࡺࠫ࣬")):
        pass
      with open(file_path, bstack1111ll1_opy_ (u"ࠥࡻ࠰ࠨ࣭")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1111ll1_opy_ (u"ࠫࡷ࣮࠭")) as bstack1lll1lll11_opy_:
      bstack1111ll11_opy_ = json.load(bstack1lll1lll11_opy_)
    if bstack1l1l1ll1l1_opy_ in bstack1111ll11_opy_:
      bstack1lll1111l1_opy_ = bstack1111ll11_opy_[bstack1l1l1ll1l1_opy_][bstack1111ll1_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ࣯ࠩ")]
      bstack11ll1l1ll_opy_ = int(bstack1lll1111l1_opy_) + 1
      bstack1ll1llll1_opy_(bstack1l1l1ll1l1_opy_, bstack11ll1l1ll_opy_, file_path)
      return bstack11ll1l1ll_opy_
    else:
      bstack1ll1llll1_opy_(bstack1l1l1ll1l1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1llll1l1l1_opy_.format(str(e)))
    return -1
def bstack11llll11l_opy_(config):
  if not config[bstack1111ll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࣰ")] or not config[bstack1111ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࣱࠪ")]:
    return True
  else:
    return False
def bstack1l1l11llll_opy_(config, index=0):
  global bstack1l1lll1111_opy_
  bstack1l1l1lll1l_opy_ = {}
  caps = bstack1l1l1l1111_opy_ + bstack11llllll11_opy_
  if bstack1l1lll1111_opy_:
    caps += bstack1ll11l111_opy_
  for key in config:
    if key in caps + [bstack1111ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣲࠫ")]:
      continue
    bstack1l1l1lll1l_opy_[key] = config[key]
  if bstack1111ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ") in config:
    for bstack11111l11_opy_ in config[bstack1111ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index]:
      if bstack11111l11_opy_ in caps:
        continue
      bstack1l1l1lll1l_opy_[bstack11111l11_opy_] = config[bstack1111ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index][bstack11111l11_opy_]
  bstack1l1l1lll1l_opy_[bstack1111ll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࣶࠧ")] = socket.gethostname()
  if bstack1111ll1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ") in bstack1l1l1lll1l_opy_:
    del (bstack1l1l1lll1l_opy_[bstack1111ll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨࣸ")])
  return bstack1l1l1lll1l_opy_
def bstack1l11111l1_opy_(config):
  global bstack1l1lll1111_opy_
  bstack1l11ll1l1l_opy_ = {}
  caps = bstack11llllll11_opy_
  if bstack1l1lll1111_opy_:
    caps += bstack1ll11l111_opy_
  for key in caps:
    if key in config:
      bstack1l11ll1l1l_opy_[key] = config[key]
  return bstack1l11ll1l1l_opy_
def bstack1l1l1llll_opy_(bstack1l1l1lll1l_opy_, bstack1l11ll1l1l_opy_):
  bstack1ll1111l1_opy_ = {}
  for key in bstack1l1l1lll1l_opy_.keys():
    if key in bstack1ll1ll1111_opy_:
      bstack1ll1111l1_opy_[bstack1ll1ll1111_opy_[key]] = bstack1l1l1lll1l_opy_[key]
    else:
      bstack1ll1111l1_opy_[key] = bstack1l1l1lll1l_opy_[key]
  for key in bstack1l11ll1l1l_opy_:
    if key in bstack1ll1ll1111_opy_:
      bstack1ll1111l1_opy_[bstack1ll1ll1111_opy_[key]] = bstack1l11ll1l1l_opy_[key]
    else:
      bstack1ll1111l1_opy_[key] = bstack1l11ll1l1l_opy_[key]
  return bstack1ll1111l1_opy_
def bstack1l1lll11_opy_(config, index=0):
  global bstack1l1lll1111_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1ll1llll11_opy_ = bstack1ll1ll111l_opy_(bstack11ll1ll1_opy_, config, logger)
  bstack1l11ll1l1l_opy_ = bstack1l11111l1_opy_(config)
  bstack11lllll1l1_opy_ = bstack11llllll11_opy_
  bstack11lllll1l1_opy_ += bstack1lllll1lll_opy_
  bstack1l11ll1l1l_opy_ = update(bstack1l11ll1l1l_opy_, bstack1ll1llll11_opy_)
  if bstack1l1lll1111_opy_:
    bstack11lllll1l1_opy_ += bstack1ll11l111_opy_
  if bstack1111ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ") in config:
    if bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࣺࠧ") in config[bstack1111ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")][index]:
      caps[bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩࣼ")] = config[bstack1111ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")][index][bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫࣾ")]
    if bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨࣿ") in config[bstack1111ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index]:
      caps[bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪँ")] = str(config[bstack1111ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ं")][index][bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬः")])
    bstack1ll1l111l_opy_ = bstack1ll1ll111l_opy_(bstack11ll1ll1_opy_, config[bstack1111ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऄ")][index], logger)
    bstack11lllll1l1_opy_ += list(bstack1ll1l111l_opy_.keys())
    for bstack1llllll11_opy_ in bstack11lllll1l1_opy_:
      if bstack1llllll11_opy_ in config[bstack1111ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index]:
        if bstack1llllll11_opy_ == bstack1111ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩआ"):
          try:
            bstack1ll1l111l_opy_[bstack1llllll11_opy_] = str(config[bstack1111ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack1llllll11_opy_] * 1.0)
          except:
            bstack1ll1l111l_opy_[bstack1llllll11_opy_] = str(config[bstack1111ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack1llllll11_opy_])
        else:
          bstack1ll1l111l_opy_[bstack1llllll11_opy_] = config[bstack1111ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1llllll11_opy_]
        del (config[bstack1111ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1llllll11_opy_])
    bstack1l11ll1l1l_opy_ = update(bstack1l11ll1l1l_opy_, bstack1ll1l111l_opy_)
  bstack1l1l1lll1l_opy_ = bstack1l1l11llll_opy_(config, index)
  for bstack11l1111ll_opy_ in bstack11llllll11_opy_ + list(bstack1ll1llll11_opy_.keys()):
    if bstack11l1111ll_opy_ in bstack1l1l1lll1l_opy_:
      bstack1l11ll1l1l_opy_[bstack11l1111ll_opy_] = bstack1l1l1lll1l_opy_[bstack11l1111ll_opy_]
      del (bstack1l1l1lll1l_opy_[bstack11l1111ll_opy_])
  if bstack1lll1111l_opy_(config):
    bstack1l1l1lll1l_opy_[bstack1111ll1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬऋ")] = True
    caps.update(bstack1l11ll1l1l_opy_)
    caps[bstack1111ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧऌ")] = bstack1l1l1lll1l_opy_
  else:
    bstack1l1l1lll1l_opy_[bstack1111ll1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧऍ")] = False
    caps.update(bstack1l1l1llll_opy_(bstack1l1l1lll1l_opy_, bstack1l11ll1l1l_opy_))
    if bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ऎ") in caps:
      caps[bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪए")] = caps[bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨऐ")]
      del (caps[bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")])
    if bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऒ") in caps:
      caps[bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨओ")] = caps[bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨऔ")]
      del (caps[bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")])
  return caps
def bstack1l11lllll1_opy_():
  global bstack1l1lll1lll_opy_
  if bstack111l11ll1_opy_() <= version.parse(bstack1111ll1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩख")):
    if bstack1l1lll1lll_opy_ != bstack1111ll1_opy_ (u"ࠪࠫग"):
      return bstack1111ll1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧघ") + bstack1l1lll1lll_opy_ + bstack1111ll1_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤङ")
    return bstack1lll11l1_opy_
  if bstack1l1lll1lll_opy_ != bstack1111ll1_opy_ (u"࠭ࠧच"):
    return bstack1111ll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤछ") + bstack1l1lll1lll_opy_ + bstack1111ll1_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤज")
  return bstack1l1l1l111_opy_
def bstack1l111l1l_opy_(options):
  return hasattr(options, bstack1111ll1_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪझ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1lll1l11l1_opy_(options, bstack1l1llllll_opy_):
  for bstack1llll11l1l_opy_ in bstack1l1llllll_opy_:
    if bstack1llll11l1l_opy_ in [bstack1111ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨञ"), bstack1111ll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨट")]:
      continue
    if bstack1llll11l1l_opy_ in options._experimental_options:
      options._experimental_options[bstack1llll11l1l_opy_] = update(options._experimental_options[bstack1llll11l1l_opy_],
                                                         bstack1l1llllll_opy_[bstack1llll11l1l_opy_])
    else:
      options.add_experimental_option(bstack1llll11l1l_opy_, bstack1l1llllll_opy_[bstack1llll11l1l_opy_])
  if bstack1111ll1_opy_ (u"ࠬࡧࡲࡨࡵࠪठ") in bstack1l1llllll_opy_:
    for arg in bstack1l1llllll_opy_[bstack1111ll1_opy_ (u"࠭ࡡࡳࡩࡶࠫड")]:
      options.add_argument(arg)
    del (bstack1l1llllll_opy_[bstack1111ll1_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")])
  if bstack1111ll1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण") in bstack1l1llllll_opy_:
    for ext in bstack1l1llllll_opy_[bstack1111ll1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त")]:
      options.add_extension(ext)
    del (bstack1l1llllll_opy_[bstack1111ll1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")])
def bstack1ll1l1lll1_opy_(options, bstack1l111l11l1_opy_):
  if bstack1111ll1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪद") in bstack1l111l11l1_opy_:
    for bstack11lllll11_opy_ in bstack1l111l11l1_opy_[bstack1111ll1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध")]:
      if bstack11lllll11_opy_ in options._preferences:
        options._preferences[bstack11lllll11_opy_] = update(options._preferences[bstack11lllll11_opy_], bstack1l111l11l1_opy_[bstack1111ll1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")][bstack11lllll11_opy_])
      else:
        options.set_preference(bstack11lllll11_opy_, bstack1l111l11l1_opy_[bstack1111ll1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack11lllll11_opy_])
  if bstack1111ll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭प") in bstack1l111l11l1_opy_:
    for arg in bstack1l111l11l1_opy_[bstack1111ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ")]:
      options.add_argument(arg)
def bstack1l1l11l1l_opy_(options, bstack1lll11111_opy_):
  if bstack1111ll1_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫब") in bstack1lll11111_opy_:
    options.use_webview(bool(bstack1lll11111_opy_[bstack1111ll1_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ")]))
  bstack1lll1l11l1_opy_(options, bstack1lll11111_opy_)
def bstack1l11l11ll_opy_(options, bstack1ll1lll1l_opy_):
  for bstack1ll1lll1ll_opy_ in bstack1ll1lll1l_opy_:
    if bstack1ll1lll1ll_opy_ in [bstack1111ll1_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩम"), bstack1111ll1_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      continue
    options.set_capability(bstack1ll1lll1ll_opy_, bstack1ll1lll1l_opy_[bstack1ll1lll1ll_opy_])
  if bstack1111ll1_opy_ (u"ࠧࡢࡴࡪࡷࠬर") in bstack1ll1lll1l_opy_:
    for arg in bstack1ll1lll1l_opy_[bstack1111ll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ")]:
      options.add_argument(arg)
  if bstack1111ll1_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल") in bstack1ll1lll1l_opy_:
    options.bstack1l11l111l_opy_(bool(bstack1ll1lll1l_opy_[bstack1111ll1_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ")]))
def bstack1111l1ll1_opy_(options, bstack1l1l11l11_opy_):
  for bstack11l1l111l_opy_ in bstack1l1l11l11_opy_:
    if bstack11l1l111l_opy_ in [bstack1111ll1_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऴ"), bstack1111ll1_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      continue
    options._options[bstack11l1l111l_opy_] = bstack1l1l11l11_opy_[bstack11l1l111l_opy_]
  if bstack1111ll1_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪश") in bstack1l1l11l11_opy_:
    for bstack1l1l111l11_opy_ in bstack1l1l11l11_opy_[bstack1111ll1_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष")]:
      options.bstack111l111ll_opy_(
        bstack1l1l111l11_opy_, bstack1l1l11l11_opy_[bstack1111ll1_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")][bstack1l1l111l11_opy_])
  if bstack1111ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह") in bstack1l1l11l11_opy_:
    for arg in bstack1l1l11l11_opy_[bstack1111ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ")]:
      options.add_argument(arg)
def bstack1l1l1111l1_opy_(options, caps):
  if not hasattr(options, bstack1111ll1_opy_ (u"ࠫࡐࡋ࡙ࠨऻ")):
    return
  if options.KEY == bstack1111ll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ़ࠪ") and options.KEY in caps:
    bstack1lll1l11l1_opy_(options, caps[bstack1111ll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ")])
  elif options.KEY == bstack1111ll1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬा") and options.KEY in caps:
    bstack1ll1l1lll1_opy_(options, caps[bstack1111ll1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि")])
  elif options.KEY == bstack1111ll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪी") and options.KEY in caps:
    bstack1l11l11ll_opy_(options, caps[bstack1111ll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु")])
  elif options.KEY == bstack1111ll1_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬू") and options.KEY in caps:
    bstack1l1l11l1l_opy_(options, caps[bstack1111ll1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ")])
  elif options.KEY == bstack1111ll1_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬॄ") and options.KEY in caps:
    bstack1111l1ll1_opy_(options, caps[bstack1111ll1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ")])
def bstack1ll1l111ll_opy_(caps):
  global bstack1l1lll1111_opy_
  if isinstance(os.environ.get(bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩॆ")), str):
    bstack1l1lll1111_opy_ = eval(os.getenv(bstack1111ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")))
  if bstack1l1lll1111_opy_:
    if bstack1l11llll1l_opy_() < version.parse(bstack1111ll1_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩै")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1111ll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॉ")
    if bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ") in caps:
      browser = caps[bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")]
    elif bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨौ") in caps:
      browser = caps[bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ")]
    browser = str(browser).lower()
    if browser == bstack1111ll1_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩॎ") or browser == bstack1111ll1_opy_ (u"ࠪ࡭ࡵࡧࡤࠨॏ"):
      browser = bstack1111ll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॐ")
    if browser == bstack1111ll1_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭॑"):
      browser = bstack1111ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ॒࠭")
    if browser not in [bstack1111ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓"), bstack1111ll1_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭॔"), bstack1111ll1_opy_ (u"ࠩ࡬ࡩࠬॕ"), bstack1111ll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪॖ"), bstack1111ll1_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬॗ")]:
      return None
    try:
      package = bstack1111ll1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧक़").format(browser)
      name = bstack1111ll1_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧख़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l111l1l_opy_(options):
        return None
      for bstack11l1111ll_opy_ in caps.keys():
        options.set_capability(bstack11l1111ll_opy_, caps[bstack11l1111ll_opy_])
      bstack1l1l1111l1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11l1l1ll1_opy_(options, bstack11l1llll_opy_):
  if not bstack1l111l1l_opy_(options):
    return
  for bstack11l1111ll_opy_ in bstack11l1llll_opy_.keys():
    if bstack11l1111ll_opy_ in bstack1lllll1lll_opy_:
      continue
    if bstack11l1111ll_opy_ in options._caps and type(options._caps[bstack11l1111ll_opy_]) in [dict, list]:
      options._caps[bstack11l1111ll_opy_] = update(options._caps[bstack11l1111ll_opy_], bstack11l1llll_opy_[bstack11l1111ll_opy_])
    else:
      options.set_capability(bstack11l1111ll_opy_, bstack11l1llll_opy_[bstack11l1111ll_opy_])
  bstack1l1l1111l1_opy_(options, bstack11l1llll_opy_)
  if bstack1111ll1_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ग़") in options._caps:
    if options._caps[bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ज़")] and options._caps[bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")].lower() != bstack1111ll1_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫढ़"):
      del options._caps[bstack1111ll1_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़")]
def bstack1l1l1lll11_opy_(proxy_config):
  if bstack1111ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩय़") in proxy_config:
    proxy_config[bstack1111ll1_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨॠ")] = proxy_config[bstack1111ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॡ")]
    del (proxy_config[bstack1111ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")])
  if bstack1111ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬॣ") in proxy_config and proxy_config[bstack1111ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।")].lower() != bstack1111ll1_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫ॥"):
    proxy_config[bstack1111ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ०")] = bstack1111ll1_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭१")
  if bstack1111ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ२") in proxy_config:
    proxy_config[bstack1111ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ३")] = bstack1111ll1_opy_ (u"ࠩࡳࡥࡨ࠭४")
  return proxy_config
def bstack11111ll11_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1111ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ५") in config:
    return proxy
  config[bstack1111ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६")] = bstack1l1l1lll11_opy_(config[bstack1111ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")])
  if proxy == None:
    proxy = Proxy(config[bstack1111ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  return proxy
def bstack111l1l1ll_opy_(self):
  global CONFIG
  global bstack1lll1l1l1_opy_
  try:
    proxy = bstack1lll11llll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1111ll1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ९")):
        proxies = bstack11l1l1111_opy_(proxy, bstack1l11lllll1_opy_())
        if len(proxies) > 0:
          protocol, bstack1llll111ll_opy_ = proxies.popitem()
          if bstack1111ll1_opy_ (u"ࠣ࠼࠲࠳ࠧ॰") in bstack1llll111ll_opy_:
            return bstack1llll111ll_opy_
          else:
            return bstack1111ll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack1llll111ll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1111ll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢॲ").format(str(e)))
  return bstack1lll1l1l1_opy_(self)
def bstack1ll111111l_opy_():
  global CONFIG
  return bstack1ll11111l_opy_(CONFIG) and bstack1l1l11ll_opy_() and bstack111l11ll1_opy_() >= version.parse(bstack1lll11l111_opy_)
def bstack1l1l1ll111_opy_():
  global CONFIG
  return (bstack1111ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧॳ") in CONFIG or bstack1111ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩॴ") in CONFIG) and bstack111llllll_opy_()
def bstack1l111ll1ll_opy_(config):
  bstack11lll1l1l_opy_ = {}
  if bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪॵ") in config:
    bstack11lll1l1l_opy_ = config[bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॶ")]
  if bstack1111ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॷ") in config:
    bstack11lll1l1l_opy_ = config[bstack1111ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॸ")]
  proxy = bstack1lll11llll_opy_(config)
  if proxy:
    if proxy.endswith(bstack1111ll1_opy_ (u"ࠪ࠲ࡵࡧࡣࠨॹ")) and os.path.isfile(proxy):
      bstack11lll1l1l_opy_[bstack1111ll1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧॺ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1111ll1_opy_ (u"ࠬ࠴ࡰࡢࡥࠪॻ")):
        proxies = bstack1lll1lll_opy_(config, bstack1l11lllll1_opy_())
        if len(proxies) > 0:
          protocol, bstack1llll111ll_opy_ = proxies.popitem()
          if bstack1111ll1_opy_ (u"ࠨ࠺࠰࠱ࠥॼ") in bstack1llll111ll_opy_:
            parsed_url = urlparse(bstack1llll111ll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1111ll1_opy_ (u"ࠢ࠻࠱࠲ࠦॽ") + bstack1llll111ll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack11lll1l1l_opy_[bstack1111ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫॾ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack11lll1l1l_opy_[bstack1111ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬॿ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack11lll1l1l_opy_[bstack1111ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ঀ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack11lll1l1l_opy_[bstack1111ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧঁ")] = str(parsed_url.password)
  return bstack11lll1l1l_opy_
def bstack11111l111_opy_(config):
  if bstack1111ll1_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪং") in config:
    return config[bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫঃ")]
  return {}
def bstack1ll11lll_opy_(caps):
  global bstack1l11l11lll_opy_
  if bstack1111ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ঄") in caps:
    caps[bstack1111ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ")][bstack1111ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨআ")] = True
    if bstack1l11l11lll_opy_:
      caps[bstack1111ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫই")][bstack1111ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ঈ")] = bstack1l11l11lll_opy_
  else:
    caps[bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪউ")] = True
    if bstack1l11l11lll_opy_:
      caps[bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧঊ")] = bstack1l11l11lll_opy_
def bstack1l1ll11ll1_opy_():
  global CONFIG
  if not bstack1l111l1ll_opy_(CONFIG):
    return
  if bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫঋ") in CONFIG and bstack1l11l1ll11_opy_(CONFIG[bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬঌ")]):
    if (
      bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍") in CONFIG
      and bstack1l11l1ll11_opy_(CONFIG[bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ঎")].get(bstack1111ll1_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨএ")))
    ):
      logger.debug(bstack1111ll1_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨঐ"))
      return
    bstack11lll1l1l_opy_ = bstack1l111ll1ll_opy_(CONFIG)
    bstack1ll1ll11_opy_(CONFIG[bstack1111ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack11lll1l1l_opy_)
def bstack1ll1ll11_opy_(key, bstack11lll1l1l_opy_):
  global bstack1lll1ll1ll_opy_
  logger.info(bstack1111111l1_opy_)
  try:
    bstack1lll1ll1ll_opy_ = Local()
    bstack1111llll_opy_ = {bstack1111ll1_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack1111llll_opy_.update(bstack11lll1l1l_opy_)
    logger.debug(bstack1l1l11lll_opy_.format(str(bstack1111llll_opy_)))
    bstack1lll1ll1ll_opy_.start(**bstack1111llll_opy_)
    if bstack1lll1ll1ll_opy_.isRunning():
      logger.info(bstack11ll11lll_opy_)
  except Exception as e:
    bstack1l11l1l1l1_opy_(bstack11l11ll1_opy_.format(str(e)))
def bstack1l11l1ll_opy_():
  global bstack1lll1ll1ll_opy_
  if bstack1lll1ll1ll_opy_.isRunning():
    logger.info(bstack11llll11_opy_)
    bstack1lll1ll1ll_opy_.stop()
  bstack1lll1ll1ll_opy_ = None
def bstack1lll1lll1l_opy_(bstack111ll1lll_opy_=[]):
  global CONFIG
  bstack111l11111_opy_ = []
  bstack11111111_opy_ = [bstack1111ll1_opy_ (u"ࠨࡱࡶࠫও"), bstack1111ll1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstack1111ll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstack1111ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack111ll1lll_opy_:
      bstack1l1ll11l11_opy_ = {}
      for k in bstack11111111_opy_:
        val = CONFIG[bstack1111ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstack1111ll1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack1l1ll11l11_opy_[k] = val
      if(err[bstack1111ll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")] != bstack1111ll1_opy_ (u"ࠪࠫজ")):
        bstack1l1ll11l11_opy_[bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪঝ")] = {
          err[bstack1111ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪঞ")]: err[bstack1111ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬট")]
        }
        bstack111l11111_opy_.append(bstack1l1ll11l11_opy_)
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩঠ") + str(e))
  finally:
    return bstack111l11111_opy_
def bstack1l111111l1_opy_(file_name):
  bstack1ll1l11l1l_opy_ = []
  try:
    bstack1l1111ll1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l1111ll1_opy_):
      with open(bstack1l1111ll1_opy_) as f:
        bstack1ll11l11l1_opy_ = json.load(f)
        bstack1ll1l11l1l_opy_ = bstack1ll11l11l1_opy_
      os.remove(bstack1l1111ll1_opy_)
    return bstack1ll1l11l1l_opy_
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪড") + str(e))
    return bstack1ll1l11l1l_opy_
def bstack11lll1111_opy_():
  global bstack1l111lll1_opy_
  global bstack111lll1ll_opy_
  global bstack1l1l111l1l_opy_
  global bstack1ll1111l_opy_
  global bstack11lll111l_opy_
  global bstack1llll11l11_opy_
  global CONFIG
  bstack11llllllll_opy_ = os.environ.get(bstack1111ll1_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪঢ"))
  if bstack11llllllll_opy_ in [bstack1111ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩণ"), bstack1111ll1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪত")]:
    bstack1ll11ll1l_opy_()
  percy.shutdown()
  if bstack1l111lll1_opy_:
    logger.warning(bstack1ll111l1ll_opy_.format(str(bstack1l111lll1_opy_)))
  else:
    try:
      bstack11ll1111l_opy_ = bstack111llll11_opy_(bstack1111ll1_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫথ"), logger)
      if bstack11ll1111l_opy_.get(bstack1111ll1_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")) and bstack11ll1111l_opy_.get(bstack1111ll1_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")).get(bstack1111ll1_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")):
        logger.warning(bstack1ll111l1ll_opy_.format(str(bstack11ll1111l_opy_[bstack1111ll1_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ঩")][bstack1111ll1_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬপ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1l1l111lll_opy_)
  global bstack1lll1ll1ll_opy_
  if bstack1lll1ll1ll_opy_:
    bstack1l11l1ll_opy_()
  try:
    for driver in bstack111lll1ll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1lll111ll1_opy_)
  if bstack1llll11l11_opy_ == bstack1111ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪফ"):
    bstack11lll111l_opy_ = bstack1l111111l1_opy_(bstack1111ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ব"))
  if bstack1llll11l11_opy_ == bstack1111ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ভ") and len(bstack1ll1111l_opy_) == 0:
    bstack1ll1111l_opy_ = bstack1l111111l1_opy_(bstack1111ll1_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬম"))
    if len(bstack1ll1111l_opy_) == 0:
      bstack1ll1111l_opy_ = bstack1l111111l1_opy_(bstack1111ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧয"))
  bstack1111lllll_opy_ = bstack1111ll1_opy_ (u"ࠩࠪর")
  if len(bstack1l1l111l1l_opy_) > 0:
    bstack1111lllll_opy_ = bstack1lll1lll1l_opy_(bstack1l1l111l1l_opy_)
  elif len(bstack1ll1111l_opy_) > 0:
    bstack1111lllll_opy_ = bstack1lll1lll1l_opy_(bstack1ll1111l_opy_)
  elif len(bstack11lll111l_opy_) > 0:
    bstack1111lllll_opy_ = bstack1lll1lll1l_opy_(bstack11lll111l_opy_)
  elif len(bstack1lll1l11ll_opy_) > 0:
    bstack1111lllll_opy_ = bstack1lll1lll1l_opy_(bstack1lll1l11ll_opy_)
  if bool(bstack1111lllll_opy_):
    bstack1lll1ll111_opy_(bstack1111lllll_opy_)
  else:
    bstack1lll1ll111_opy_()
  bstack11l1l11ll_opy_(bstack111111lll_opy_, logger)
  bstack1111111ll_opy_.bstack1l1111l1_opy_(CONFIG)
  if len(bstack11lll111l_opy_) > 0:
    sys.exit(len(bstack11lll111l_opy_))
def bstack1111l111_opy_(bstack1l11l11l_opy_, frame):
  global bstack11l11l1ll_opy_
  logger.error(bstack11lll11ll_opy_)
  bstack11l11l1ll_opy_.bstack11llllll1_opy_(bstack1111ll1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭঱"), bstack1l11l11l_opy_)
  if hasattr(signal, bstack1111ll1_opy_ (u"ࠫࡘ࡯ࡧ࡯ࡣ࡯ࡷࠬল")):
    bstack11l11l1ll_opy_.bstack11llllll1_opy_(bstack1111ll1_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ঳"), signal.Signals(bstack1l11l11l_opy_).name)
  else:
    bstack11l11l1ll_opy_.bstack11llllll1_opy_(bstack1111ll1_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭঴"), bstack1111ll1_opy_ (u"ࠧࡔࡋࡊ࡙ࡓࡑࡎࡐ࡙ࡑࠫ঵"))
  bstack11llllllll_opy_ = os.environ.get(bstack1111ll1_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩশ"))
  if bstack11llllllll_opy_ == bstack1111ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩষ"):
    bstack1l1111l11_opy_.stop(bstack11l11l1ll_opy_.get_property(bstack1111ll1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪস")))
  bstack11lll1111_opy_()
  sys.exit(1)
def bstack1l11l1l1l1_opy_(err):
  logger.critical(bstack1l1l1ll11l_opy_.format(str(err)))
  bstack1lll1ll111_opy_(bstack1l1l1ll11l_opy_.format(str(err)), True)
  atexit.unregister(bstack11lll1111_opy_)
  bstack1ll11ll1l_opy_()
  sys.exit(1)
def bstack111l11lll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1lll1ll111_opy_(message, True)
  atexit.unregister(bstack11lll1111_opy_)
  bstack1ll11ll1l_opy_()
  sys.exit(1)
def bstack1111l1l1l_opy_():
  global CONFIG
  global bstack111l1111l_opy_
  global bstack11ll1l11l_opy_
  global bstack1ll111ll_opy_
  CONFIG = bstack11111l1l1_opy_()
  load_dotenv(CONFIG.get(bstack1111ll1_opy_ (u"ࠫࡪࡴࡶࡇ࡫࡯ࡩࠬহ")))
  bstack11lll11l1_opy_()
  bstack1ll11l1l_opy_()
  CONFIG = bstack1l11ll11l_opy_(CONFIG)
  update(CONFIG, bstack11ll1l11l_opy_)
  update(CONFIG, bstack111l1111l_opy_)
  CONFIG = bstack1ll11111_opy_(CONFIG)
  bstack1ll111ll_opy_ = bstack1l111l1ll_opy_(CONFIG)
  os.environ[bstack1111ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ঺")] = bstack1ll111ll_opy_.__str__()
  bstack11l11l1ll_opy_.bstack11llllll1_opy_(bstack1111ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ঻"), bstack1ll111ll_opy_)
  if (bstack1111ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ়ࠪ") in CONFIG and bstack1111ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫঽ") in bstack111l1111l_opy_) or (
          bstack1111ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬা") in CONFIG and bstack1111ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ি") not in bstack11ll1l11l_opy_):
    if os.getenv(bstack1111ll1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨী")):
      CONFIG[bstack1111ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧু")] = os.getenv(bstack1111ll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪূ"))
    else:
      bstack1l111l1l11_opy_()
  elif (bstack1111ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪৃ") not in CONFIG and bstack1111ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪৄ") in CONFIG) or (
          bstack1111ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ৅") in bstack11ll1l11l_opy_ and bstack1111ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭৆") not in bstack111l1111l_opy_):
    del (CONFIG[bstack1111ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ে")])
  if bstack11llll11l_opy_(CONFIG):
    bstack1l11l1l1l1_opy_(bstack1ll1lll111_opy_)
  bstack1llllll111_opy_()
  bstack1ll1lllll1_opy_()
  if bstack1l1lll1111_opy_:
    CONFIG[bstack1111ll1_opy_ (u"ࠬࡧࡰࡱࠩৈ")] = bstack1l111l111_opy_(CONFIG)
    logger.info(bstack1l11l1ll1_opy_.format(CONFIG[bstack1111ll1_opy_ (u"࠭ࡡࡱࡲࠪ৉")]))
  if not bstack1ll111ll_opy_:
    CONFIG[bstack1111ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৊")] = [{}]
def bstack111ll11l_opy_(config, bstack11l11l1l1_opy_):
  global CONFIG
  global bstack1l1lll1111_opy_
  CONFIG = config
  bstack1l1lll1111_opy_ = bstack11l11l1l1_opy_
def bstack1ll1lllll1_opy_():
  global CONFIG
  global bstack1l1lll1111_opy_
  if bstack1111ll1_opy_ (u"ࠨࡣࡳࡴࠬো") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack111l11lll_opy_(e, bstack111111l11_opy_)
    bstack1l1lll1111_opy_ = True
    bstack11l11l1ll_opy_.bstack11llllll1_opy_(bstack1111ll1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨৌ"), True)
def bstack1l111l111_opy_(config):
  bstack1l1lll111l_opy_ = bstack1111ll1_opy_ (u"্ࠪࠫ")
  app = config[bstack1111ll1_opy_ (u"ࠫࡦࡶࡰࠨৎ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l11l11ll1_opy_:
      if os.path.exists(app):
        bstack1l1lll111l_opy_ = bstack1llll1111_opy_(config, app)
      elif bstack1l1111lll_opy_(app):
        bstack1l1lll111l_opy_ = app
      else:
        bstack1l11l1l1l1_opy_(bstack1ll111111_opy_.format(app))
    else:
      if bstack1l1111lll_opy_(app):
        bstack1l1lll111l_opy_ = app
      elif os.path.exists(app):
        bstack1l1lll111l_opy_ = bstack1llll1111_opy_(app)
      else:
        bstack1l11l1l1l1_opy_(bstack1lll11lll_opy_)
  else:
    if len(app) > 2:
      bstack1l11l1l1l1_opy_(bstack1l1111ll_opy_)
    elif len(app) == 2:
      if bstack1111ll1_opy_ (u"ࠬࡶࡡࡵࡪࠪ৏") in app and bstack1111ll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ৐") in app:
        if os.path.exists(app[bstack1111ll1_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ৑")]):
          bstack1l1lll111l_opy_ = bstack1llll1111_opy_(config, app[bstack1111ll1_opy_ (u"ࠨࡲࡤࡸ࡭࠭৒")], app[bstack1111ll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ৓")])
        else:
          bstack1l11l1l1l1_opy_(bstack1ll111111_opy_.format(app))
      else:
        bstack1l11l1l1l1_opy_(bstack1l1111ll_opy_)
    else:
      for key in app:
        if key in bstack1l11ll1l_opy_:
          if key == bstack1111ll1_opy_ (u"ࠪࡴࡦࡺࡨࠨ৔"):
            if os.path.exists(app[key]):
              bstack1l1lll111l_opy_ = bstack1llll1111_opy_(config, app[key])
            else:
              bstack1l11l1l1l1_opy_(bstack1ll111111_opy_.format(app))
          else:
            bstack1l1lll111l_opy_ = app[key]
        else:
          bstack1l11l1l1l1_opy_(bstack111ll1ll1_opy_)
  return bstack1l1lll111l_opy_
def bstack1l1111lll_opy_(bstack1l1lll111l_opy_):
  import re
  bstack1l1ll1l1_opy_ = re.compile(bstack1111ll1_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ৕"))
  bstack1l1llll1ll_opy_ = re.compile(bstack1111ll1_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ৖"))
  if bstack1111ll1_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬৗ") in bstack1l1lll111l_opy_ or re.fullmatch(bstack1l1ll1l1_opy_, bstack1l1lll111l_opy_) or re.fullmatch(bstack1l1llll1ll_opy_, bstack1l1lll111l_opy_):
    return True
  else:
    return False
def bstack1llll1111_opy_(config, path, bstack1l1l11ll1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1111ll1_opy_ (u"ࠧࡳࡤࠪ৘")).read()).hexdigest()
  bstack1l1llll1_opy_ = bstack1l1l1l1l1l_opy_(md5_hash)
  bstack1l1lll111l_opy_ = None
  if bstack1l1llll1_opy_:
    logger.info(bstack1llll1l11l_opy_.format(bstack1l1llll1_opy_, md5_hash))
    return bstack1l1llll1_opy_
  bstack1l1l1lll1_opy_ = MultipartEncoder(
    fields={
      bstack1111ll1_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭৙"): (os.path.basename(path), open(os.path.abspath(path), bstack1111ll1_opy_ (u"ࠩࡵࡦࠬ৚")), bstack1111ll1_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧ৛")),
      bstack1111ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧড়"): bstack1l1l11ll1_opy_
    }
  )
  response = requests.post(bstack11ll1lll1_opy_, data=bstack1l1l1lll1_opy_,
                           headers={bstack1111ll1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫঢ়"): bstack1l1l1lll1_opy_.content_type},
                           auth=(config[bstack1111ll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ৞")], config[bstack1111ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪয়")]))
  try:
    res = json.loads(response.text)
    bstack1l1lll111l_opy_ = res[bstack1111ll1_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩৠ")]
    logger.info(bstack11111ll1_opy_.format(bstack1l1lll111l_opy_))
    bstack111l111l_opy_(md5_hash, bstack1l1lll111l_opy_)
  except ValueError as err:
    bstack1l11l1l1l1_opy_(bstack1l111l11l_opy_.format(str(err)))
  return bstack1l1lll111l_opy_
def bstack1llllll111_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1llll1ll1l_opy_
  bstack1lllll11l_opy_ = 1
  bstack111ll11ll_opy_ = 1
  if bstack1111ll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩৡ") in CONFIG:
    bstack111ll11ll_opy_ = CONFIG[bstack1111ll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪৢ")]
  else:
    bstack111ll11ll_opy_ = bstack1l1111ll11_opy_(framework_name, args) or 1
  if bstack1111ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧৣ") in CONFIG:
    bstack1lllll11l_opy_ = len(CONFIG[bstack1111ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৤")])
  bstack1llll1ll1l_opy_ = int(bstack111ll11ll_opy_) * int(bstack1lllll11l_opy_)
def bstack1l1111ll11_opy_(framework_name, args):
  if framework_name == bstack1l1l1l11l1_opy_ and args and bstack1111ll1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ৥") in args:
      bstack1l1l1ll1ll_opy_ = args.index(bstack1111ll1_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ০"))
      return int(args[bstack1l1l1ll1ll_opy_ + 1]) or 1
  return 1
def bstack1l1l1l1l1l_opy_(md5_hash):
  bstack1l11lllll_opy_ = os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠨࢀࠪ১")), bstack1111ll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ২"), bstack1111ll1_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ৩"))
  if os.path.exists(bstack1l11lllll_opy_):
    bstack1l1lllll1l_opy_ = json.load(open(bstack1l11lllll_opy_, bstack1111ll1_opy_ (u"ࠫࡷࡨࠧ৪")))
    if md5_hash in bstack1l1lllll1l_opy_:
      bstack1l1lll11l1_opy_ = bstack1l1lllll1l_opy_[md5_hash]
      bstack1l111l1l1l_opy_ = datetime.datetime.now()
      bstack11l11lll1_opy_ = datetime.datetime.strptime(bstack1l1lll11l1_opy_[bstack1111ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ৫")], bstack1111ll1_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ৬"))
      if (bstack1l111l1l1l_opy_ - bstack11l11lll1_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l1lll11l1_opy_[bstack1111ll1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ৭")]):
        return None
      return bstack1l1lll11l1_opy_[bstack1111ll1_opy_ (u"ࠨ࡫ࡧࠫ৮")]
  else:
    return None
def bstack111l111l_opy_(md5_hash, bstack1l1lll111l_opy_):
  bstack1l1l111l1_opy_ = os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠩࢁࠫ৯")), bstack1111ll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪৰ"))
  if not os.path.exists(bstack1l1l111l1_opy_):
    os.makedirs(bstack1l1l111l1_opy_)
  bstack1l11lllll_opy_ = os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠫࢃ࠭ৱ")), bstack1111ll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ৲"), bstack1111ll1_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ৳"))
  bstack1ll1ll1ll_opy_ = {
    bstack1111ll1_opy_ (u"ࠧࡪࡦࠪ৴"): bstack1l1lll111l_opy_,
    bstack1111ll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ৵"): datetime.datetime.strftime(datetime.datetime.now(), bstack1111ll1_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭৶")),
    bstack1111ll1_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ৷"): str(__version__)
  }
  if os.path.exists(bstack1l11lllll_opy_):
    bstack1l1lllll1l_opy_ = json.load(open(bstack1l11lllll_opy_, bstack1111ll1_opy_ (u"ࠫࡷࡨࠧ৸")))
  else:
    bstack1l1lllll1l_opy_ = {}
  bstack1l1lllll1l_opy_[md5_hash] = bstack1ll1ll1ll_opy_
  with open(bstack1l11lllll_opy_, bstack1111ll1_opy_ (u"ࠧࡽࠫࠣ৹")) as outfile:
    json.dump(bstack1l1lllll1l_opy_, outfile)
def bstack1l1lll11ll_opy_(self):
  return
def bstack1lll1l11_opy_(self):
  return
def bstack1l1ll1l1l_opy_(self):
  global bstack1l11l1l11_opy_
  bstack1l11l1l11_opy_(self)
def bstack11111l1l_opy_():
  global bstack11ll1llll_opy_
  bstack11ll1llll_opy_ = True
def bstack11l1ll111_opy_(self):
  global bstack1ll1l11ll_opy_
  global bstack11l111ll1_opy_
  global bstack1l111ll11l_opy_
  try:
    if bstack1111ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭৺") in bstack1ll1l11ll_opy_ and self.session_id != None and bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ৻"), bstack1111ll1_opy_ (u"ࠨࠩৼ")) != bstack1111ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ৽"):
      bstack1ll11l1ll1_opy_ = bstack1111ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ৾") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1111ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ৿")
      if bstack1ll11l1ll1_opy_ == bstack1111ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ਀"):
        bstack1ll1l1l11_opy_(logger)
      if self != None:
        bstack1ll1l1ll1_opy_(self, bstack1ll11l1ll1_opy_, bstack1111ll1_opy_ (u"࠭ࠬࠡࠩਁ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1111ll1_opy_ (u"ࠧࠨਂ")
    if bstack1111ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਃ") in bstack1ll1l11ll_opy_ and getattr(threading.current_thread(), bstack1111ll1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ਄"), None):
      bstack11llll1l_opy_.bstack1ll11ll1ll_opy_(self, bstack1l1111l111_opy_, logger, wait=True)
    if bstack1111ll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪਅ") in bstack1ll1l11ll_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1ll1l1ll1_opy_(self, bstack1111ll1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦਆ"))
      bstack1ll1111l11_opy_.bstack111l11l11_opy_(self)
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨਇ") + str(e))
  bstack1l111ll11l_opy_(self)
  self.session_id = None
def bstack1lll11l1l_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack111llll1_opy_
    global bstack1ll1l11ll_opy_
    command_executor = kwargs.get(bstack1111ll1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩਈ"), bstack1111ll1_opy_ (u"ࠧࠨਉ"))
    bstack1l111ll1l1_opy_ = False
    if type(command_executor) == str and bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫਊ") in command_executor:
      bstack1l111ll1l1_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ਋") in str(getattr(command_executor, bstack1111ll1_opy_ (u"ࠪࡣࡺࡸ࡬ࠨ਌"), bstack1111ll1_opy_ (u"ࠫࠬ਍"))):
      bstack1l111ll1l1_opy_ = True
    else:
      return bstack1lll11l1l1_opy_(self, *args, **kwargs)
    if bstack1l111ll1l1_opy_:
      if kwargs.get(bstack1111ll1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭਎")):
        kwargs[bstack1111ll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧਏ")] = bstack111llll1_opy_(kwargs[bstack1111ll1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨਐ")], bstack1ll1l11ll_opy_)
      elif kwargs.get(bstack1111ll1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ਑")):
        kwargs[bstack1111ll1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ਒")] = bstack111llll1_opy_(kwargs[bstack1111ll1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪਓ")], bstack1ll1l11ll_opy_)
  except Exception as e:
    logger.error(bstack1111ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦਔ").format(str(e)))
  return bstack1lll11l1l1_opy_(self, *args, **kwargs)
def bstack1ll111l111_opy_(self, command_executor=bstack1111ll1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴࠷࠲࠸࠰࠳࠲࠵࠴࠱࠻࠶࠷࠸࠹ࠨਕ"), *args, **kwargs):
  bstack111ll1l1_opy_ = bstack1lll11l1l_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11lll1lll_opy_.on():
    return bstack111ll1l1_opy_
  try:
    logger.debug(bstack1111ll1_opy_ (u"࠭ࡃࡰ࡯ࡰࡥࡳࡪࠠࡆࡺࡨࡧࡺࡺ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡦࡢ࡮ࡶࡩࠥ࠳ࠠࡼࡿࠪਖ").format(str(command_executor)))
    logger.debug(bstack1111ll1_opy_ (u"ࠧࡉࡷࡥࠤ࡚ࡘࡌࠡ࡫ࡶࠤ࠲ࠦࡻࡾࠩਗ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫਘ") in command_executor._url:
      bstack11l11l1ll_opy_.bstack11llllll1_opy_(bstack1111ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪਙ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ਚ") in command_executor):
    bstack11l11l1ll_opy_.bstack11llllll1_opy_(bstack1111ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬਛ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1111l11_opy_.bstack1ll111l11_opy_(self)
  return bstack111ll1l1_opy_
def bstack1l1l11l11l_opy_(args):
  return bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷ࠭ਜ") in str(args)
def bstack1l1ll1ll_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll1ll1l11_opy_
  global bstack11lll111_opy_
  bstack1l1l1l111l_opy_ = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪਝ"), None) and bstack1llll1l11_opy_(
          threading.current_thread(), bstack1111ll1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ਞ"), None)
  bstack11l111l1_opy_ = getattr(self, bstack1111ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨਟ"), None) != None and getattr(self, bstack1111ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩਠ"), None) == True
  if not bstack11lll111_opy_ and bstack1ll111ll_opy_ and bstack1111ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪਡ") in CONFIG and CONFIG[bstack1111ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫਢ")] == True and bstack1l1lll1l_opy_.bstack11llllll_opy_(driver_command) and (bstack11l111l1_opy_ or bstack1l1l1l111l_opy_) and not bstack1l1l11l11l_opy_(args):
    try:
      bstack11lll111_opy_ = True
      logger.debug(bstack1111ll1_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧਣ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1111ll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫਤ").format(str(err)))
    bstack11lll111_opy_ = False
  response = bstack1ll1ll1l11_opy_(self, driver_command, *args, **kwargs)
  if (bstack1111ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਥ") in str(bstack1ll1l11ll_opy_).lower() or bstack1111ll1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨਦ") in str(bstack1ll1l11ll_opy_).lower()) and bstack11lll1lll_opy_.on():
    try:
      if driver_command == bstack1111ll1_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ਧ"):
        bstack1l1111l11_opy_.bstack1ll111lll1_opy_({
            bstack1111ll1_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩਨ"): response[bstack1111ll1_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ਩")],
            bstack1111ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬਪ"): bstack1l1111l11_opy_.current_test_uuid() if bstack1l1111l11_opy_.current_test_uuid() else bstack11lll1lll_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1ll11111ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack11l111ll1_opy_
  global bstack1l1ll1l111_opy_
  global bstack111111ll_opy_
  global bstack111l1l11l_opy_
  global bstack1l11l1llll_opy_
  global bstack1ll1l11ll_opy_
  global bstack1lll11l1l1_opy_
  global bstack111lll1ll_opy_
  global bstack1lllll1ll1_opy_
  global bstack1l1111l111_opy_
  CONFIG[bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਫ")] = str(bstack1ll1l11ll_opy_) + str(__version__)
  command_executor = bstack1l11lllll1_opy_()
  logger.debug(bstack11l11l1l_opy_.format(command_executor))
  proxy = bstack11111ll11_opy_(CONFIG, proxy)
  bstack1l1l11l111_opy_ = 0 if bstack1l1ll1l111_opy_ < 0 else bstack1l1ll1l111_opy_
  try:
    if bstack111l1l11l_opy_ is True:
      bstack1l1l11l111_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l11l1llll_opy_ is True:
      bstack1l1l11l111_opy_ = int(threading.current_thread().name)
  except:
    bstack1l1l11l111_opy_ = 0
  bstack11l1llll_opy_ = bstack1l1lll11_opy_(CONFIG, bstack1l1l11l111_opy_)
  logger.debug(bstack11l1111l_opy_.format(str(bstack11l1llll_opy_)))
  if bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫਬ") in CONFIG and bstack1l11l1ll11_opy_(CONFIG[bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਭ")]):
    bstack1ll11lll_opy_(bstack11l1llll_opy_)
  if bstack11l11l111_opy_.bstack1l1l1111_opy_(CONFIG, bstack1l1l11l111_opy_) and bstack11l11l111_opy_.bstack1l1111lll1_opy_(bstack11l1llll_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    bstack11l11l111_opy_.set_capabilities(bstack11l1llll_opy_, CONFIG)
  if desired_capabilities:
    bstack111l1l111_opy_ = bstack1l11ll11l_opy_(desired_capabilities)
    bstack111l1l111_opy_[bstack1111ll1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩਮ")] = bstack1lll1111l_opy_(CONFIG)
    bstack1lll1111_opy_ = bstack1l1lll11_opy_(bstack111l1l111_opy_)
    if bstack1lll1111_opy_:
      bstack11l1llll_opy_ = update(bstack1lll1111_opy_, bstack11l1llll_opy_)
    desired_capabilities = None
  if options:
    bstack11l1l1ll1_opy_(options, bstack11l1llll_opy_)
  if not options:
    options = bstack1ll1l111ll_opy_(bstack11l1llll_opy_)
  bstack1l1111l111_opy_ = CONFIG.get(bstack1111ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ"))[bstack1l1l11l111_opy_]
  if proxy and bstack111l11ll1_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫਰ")):
    options.proxy(proxy)
  if options and bstack111l11ll1_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ਱")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack111l11ll1_opy_() < version.parse(bstack1111ll1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਲ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11l1llll_opy_)
  logger.info(bstack1l11111l_opy_)
  if bstack111l11ll1_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧਲ਼")):
    bstack1lll11l1l1_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack111l11ll1_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ਴")):
    bstack1lll11l1l1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack111l11ll1_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩਵ")):
    bstack1lll11l1l1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1lll11l1l1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1lllllllll_opy_ = bstack1111ll1_opy_ (u"ࠪࠫਸ਼")
    if bstack111l11ll1_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ਷")):
      bstack1lllllllll_opy_ = self.caps.get(bstack1111ll1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧਸ"))
    else:
      bstack1lllllllll_opy_ = self.capabilities.get(bstack1111ll1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨਹ"))
    if bstack1lllllllll_opy_:
      bstack1l11llll_opy_(bstack1lllllllll_opy_)
      if bstack111l11ll1_opy_() <= version.parse(bstack1111ll1_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ਺")):
        self.command_executor._url = bstack1111ll1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ਻") + bstack1l1lll1lll_opy_ + bstack1111ll1_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ਼")
      else:
        self.command_executor._url = bstack1111ll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ਽") + bstack1lllllllll_opy_ + bstack1111ll1_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧਾ")
      logger.debug(bstack1lllll111_opy_.format(bstack1lllllllll_opy_))
    else:
      logger.debug(bstack1llllll1ll_opy_.format(bstack1111ll1_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨਿ")))
  except Exception as e:
    logger.debug(bstack1llllll1ll_opy_.format(e))
  if bstack1111ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬੀ") in bstack1ll1l11ll_opy_:
    bstack1llll11lll_opy_(bstack1l1ll1l111_opy_, bstack1lllll1ll1_opy_)
  bstack11l111ll1_opy_ = self.session_id
  if bstack1111ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧੁ") in bstack1ll1l11ll_opy_ or bstack1111ll1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨੂ") in bstack1ll1l11ll_opy_ or bstack1111ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ੃") in bstack1ll1l11ll_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1l1111l11_opy_.bstack1ll111l11_opy_(self)
  bstack111lll1ll_opy_.append(self)
  if bstack1111ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੄") in CONFIG and bstack1111ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੅") in CONFIG[bstack1111ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੆")][bstack1l1l11l111_opy_]:
    bstack111111ll_opy_ = CONFIG[bstack1111ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩੇ")][bstack1l1l11l111_opy_][bstack1111ll1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬੈ")]
  logger.debug(bstack11l111l11_opy_.format(bstack11l111ll1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1llll1l1l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l1l11l1ll_opy_
      if(bstack1111ll1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥ੉") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠩࢁࠫ੊")), bstack1111ll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪੋ"), bstack1111ll1_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ੌ")), bstack1111ll1_opy_ (u"ࠬࡽ੍ࠧ")) as fp:
          fp.write(bstack1111ll1_opy_ (u"ࠨࠢ੎"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1111ll1_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ੏")))):
          with open(args[1], bstack1111ll1_opy_ (u"ࠨࡴࠪ੐")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1111ll1_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨੑ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1lll11ll1_opy_)
            lines.insert(1, bstack11ll111l1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1111ll1_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ੒")), bstack1111ll1_opy_ (u"ࠫࡼ࠭੓")) as bstack1llllll1l_opy_:
              bstack1llllll1l_opy_.writelines(lines)
        CONFIG[bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ੔")] = str(bstack1ll1l11ll_opy_) + str(__version__)
        bstack1l1l11l111_opy_ = 0 if bstack1l1ll1l111_opy_ < 0 else bstack1l1ll1l111_opy_
        try:
          if bstack111l1l11l_opy_ is True:
            bstack1l1l11l111_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l11l1llll_opy_ is True:
            bstack1l1l11l111_opy_ = int(threading.current_thread().name)
        except:
          bstack1l1l11l111_opy_ = 0
        CONFIG[bstack1111ll1_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨ੕")] = False
        CONFIG[bstack1111ll1_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ੖")] = True
        bstack11l1llll_opy_ = bstack1l1lll11_opy_(CONFIG, bstack1l1l11l111_opy_)
        logger.debug(bstack11l1111l_opy_.format(str(bstack11l1llll_opy_)))
        if CONFIG.get(bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ੗")):
          bstack1ll11lll_opy_(bstack11l1llll_opy_)
        if bstack1111ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੘") in CONFIG and bstack1111ll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਖ਼") in CONFIG[bstack1111ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਗ਼")][bstack1l1l11l111_opy_]:
          bstack111111ll_opy_ = CONFIG[bstack1111ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਜ਼")][bstack1l1l11l111_opy_][bstack1111ll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫੜ")]
        args.append(os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠧࡿࠩ੝")), bstack1111ll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਫ਼"), bstack1111ll1_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ੟")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11l1llll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1111ll1_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ੠"))
      bstack1l1l11l1ll_opy_ = True
      return bstack1l1ll1111_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11l1ll11_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1l1ll1l111_opy_
    global bstack111111ll_opy_
    global bstack111l1l11l_opy_
    global bstack1l11l1llll_opy_
    global bstack1ll1l11ll_opy_
    CONFIG[bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭੡")] = str(bstack1ll1l11ll_opy_) + str(__version__)
    bstack1l1l11l111_opy_ = 0 if bstack1l1ll1l111_opy_ < 0 else bstack1l1ll1l111_opy_
    try:
      if bstack111l1l11l_opy_ is True:
        bstack1l1l11l111_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l11l1llll_opy_ is True:
        bstack1l1l11l111_opy_ = int(threading.current_thread().name)
    except:
      bstack1l1l11l111_opy_ = 0
    CONFIG[bstack1111ll1_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ੢")] = True
    bstack11l1llll_opy_ = bstack1l1lll11_opy_(CONFIG, bstack1l1l11l111_opy_)
    logger.debug(bstack11l1111l_opy_.format(str(bstack11l1llll_opy_)))
    if CONFIG.get(bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ੣")):
      bstack1ll11lll_opy_(bstack11l1llll_opy_)
    if bstack1111ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤") in CONFIG and bstack1111ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭੥") in CONFIG[bstack1111ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੦")][bstack1l1l11l111_opy_]:
      bstack111111ll_opy_ = CONFIG[bstack1111ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੧")][bstack1l1l11l111_opy_][bstack1111ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੨")]
    import urllib
    import json
    bstack111l1l1l1_opy_ = bstack1111ll1_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ੩") + urllib.parse.quote(json.dumps(bstack11l1llll_opy_))
    browser = self.connect(bstack111l1l1l1_opy_)
    return browser
except Exception as e:
    pass
def bstack1lll11l11_opy_():
    global bstack1l1l11l1ll_opy_
    global bstack1ll1l11ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11l1l1l1l_opy_
        if not bstack1ll111ll_opy_:
          global bstack1ll111l1l1_opy_
          if not bstack1ll111l1l1_opy_:
            from bstack_utils.helper import bstack11l11ll11_opy_, bstack11lll1ll_opy_
            bstack1ll111l1l1_opy_ = bstack11l11ll11_opy_()
            bstack11lll1ll_opy_(bstack1ll1l11ll_opy_)
          BrowserType.connect = bstack11l1l1l1l_opy_
          return
        BrowserType.launch = bstack11l1ll11_opy_
        bstack1l1l11l1ll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1llll1l1l_opy_
      bstack1l1l11l1ll_opy_ = True
    except Exception as e:
      pass
def bstack11lllll1l_opy_(context, bstack11l111ll_opy_):
  try:
    context.page.evaluate(bstack1111ll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ੪"), bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫ੫")+ json.dumps(bstack11l111ll_opy_) + bstack1111ll1_opy_ (u"ࠣࡿࢀࠦ੬"))
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢ੭"), e)
def bstack1l1l111ll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1111ll1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ੮"), bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ੯") + json.dumps(message) + bstack1111ll1_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨੰ") + json.dumps(level) + bstack1111ll1_opy_ (u"࠭ࡽࡾࠩੱ"))
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥੲ"), e)
def bstack11l1ll11l_opy_(self, url):
  global bstack1l1llll11_opy_
  try:
    bstack1111l1l11_opy_(url)
  except Exception as err:
    logger.debug(bstack1l11lll1l1_opy_.format(str(err)))
  try:
    bstack1l1llll11_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1111111_opy_ = str(e)
      if any(err_msg in bstack1l1111111_opy_ for err_msg in bstack1111ll1l1_opy_):
        bstack1111l1l11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l11lll1l1_opy_.format(str(err)))
    raise e
def bstack1l111llll1_opy_(self):
  global bstack111l1llll_opy_
  bstack111l1llll_opy_ = self
  return
def bstack11ll1l1l1_opy_(self):
  global bstack11111l1ll_opy_
  bstack11111l1ll_opy_ = self
  return
def bstack1lllll11_opy_(test_name, bstack1ll1l1l1_opy_):
  global CONFIG
  if percy.bstack111111ll1_opy_() == bstack1111ll1_opy_ (u"ࠣࡶࡵࡹࡪࠨੳ"):
    bstack1lll1l111l_opy_ = os.path.relpath(bstack1ll1l1l1_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1lll1l111l_opy_)
    bstack1lll11ll11_opy_ = suite_name + bstack1111ll1_opy_ (u"ࠤ࠰ࠦੴ") + test_name
    threading.current_thread().percySessionName = bstack1lll11ll11_opy_
def bstack1lllll1111_opy_(self, test, *args, **kwargs):
  global bstack1111ll1l_opy_
  test_name = None
  bstack1ll1l1l1_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1ll1l1l1_opy_ = str(test.source)
  bstack1lllll11_opy_(test_name, bstack1ll1l1l1_opy_)
  bstack1111ll1l_opy_(self, test, *args, **kwargs)
def bstack111lll111_opy_(driver, bstack1lll11ll11_opy_):
  if not bstack1l1lll1l1l_opy_ and bstack1lll11ll11_opy_:
      bstack11ll1ll11_opy_ = {
          bstack1111ll1_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪੵ"): bstack1111ll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ੶"),
          bstack1111ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ੷"): {
              bstack1111ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ੸"): bstack1lll11ll11_opy_
          }
      }
      bstack1llll1lll1_opy_ = bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ੹").format(json.dumps(bstack11ll1ll11_opy_))
      driver.execute_script(bstack1llll1lll1_opy_)
  if bstack11lll1ll1_opy_:
      bstack1llll1ll1_opy_ = {
          bstack1111ll1_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ੺"): bstack1111ll1_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ੻"),
          bstack1111ll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭੼"): {
              bstack1111ll1_opy_ (u"ࠫࡩࡧࡴࡢࠩ੽"): bstack1lll11ll11_opy_ + bstack1111ll1_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ੾"),
              bstack1111ll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ੿"): bstack1111ll1_opy_ (u"ࠧࡪࡰࡩࡳࠬ઀")
          }
      }
      if bstack11lll1ll1_opy_.status == bstack1111ll1_opy_ (u"ࠨࡒࡄࡗࡘ࠭ઁ"):
          bstack1ll111ll1_opy_ = bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧં").format(json.dumps(bstack1llll1ll1_opy_))
          driver.execute_script(bstack1ll111ll1_opy_)
          bstack1ll1l1ll1_opy_(driver, bstack1111ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪઃ"))
      elif bstack11lll1ll1_opy_.status == bstack1111ll1_opy_ (u"ࠫࡋࡇࡉࡍࠩ઄"):
          reason = bstack1111ll1_opy_ (u"ࠧࠨઅ")
          bstack1llll1l1_opy_ = bstack1lll11ll11_opy_ + bstack1111ll1_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠧઆ")
          if bstack11lll1ll1_opy_.message:
              reason = str(bstack11lll1ll1_opy_.message)
              bstack1llll1l1_opy_ = bstack1llll1l1_opy_ + bstack1111ll1_opy_ (u"ࠧࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࠧઇ") + reason
          bstack1llll1ll1_opy_[bstack1111ll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫઈ")] = {
              bstack1111ll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨઉ"): bstack1111ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩઊ"),
              bstack1111ll1_opy_ (u"ࠫࡩࡧࡴࡢࠩઋ"): bstack1llll1l1_opy_
          }
          bstack1ll111ll1_opy_ = bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪઌ").format(json.dumps(bstack1llll1ll1_opy_))
          driver.execute_script(bstack1ll111ll1_opy_)
          bstack1ll1l1ll1_opy_(driver, bstack1111ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ઍ"), reason)
          bstack1llll11l1_opy_(reason, str(bstack11lll1ll1_opy_), str(bstack1l1ll1l111_opy_), logger)
def bstack1llllllll_opy_(driver, test):
  if percy.bstack111111ll1_opy_() == bstack1111ll1_opy_ (u"ࠢࡵࡴࡸࡩࠧ઎") and percy.bstack1l11ll11_opy_() == bstack1111ll1_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥએ"):
      bstack1ll11ll111_opy_ = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬઐ"), None)
      bstack1l111l1ll1_opy_(driver, bstack1ll11ll111_opy_, test)
  if bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧઑ"), None) and bstack1llll1l11_opy_(
          threading.current_thread(), bstack1111ll1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ઒"), None):
      logger.info(bstack1111ll1_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧઓ"))
      bstack11l11l111_opy_.bstack11l1l111_opy_(driver, name=test.name, path=test.source)
def bstack1l1lll1ll1_opy_(test, bstack1lll11ll11_opy_):
    try:
      data = {}
      if test:
        data[bstack1111ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫઔ")] = bstack1lll11ll11_opy_
      if bstack11lll1ll1_opy_:
        if bstack11lll1ll1_opy_.status == bstack1111ll1_opy_ (u"ࠧࡑࡃࡖࡗࠬક"):
          data[bstack1111ll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨખ")] = bstack1111ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩગ")
        elif bstack11lll1ll1_opy_.status == bstack1111ll1_opy_ (u"ࠪࡊࡆࡏࡌࠨઘ"):
          data[bstack1111ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫઙ")] = bstack1111ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬચ")
          if bstack11lll1ll1_opy_.message:
            data[bstack1111ll1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭છ")] = str(bstack11lll1ll1_opy_.message)
      user = CONFIG[bstack1111ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩજ")]
      key = CONFIG[bstack1111ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫઝ")]
      url = bstack1111ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧઞ").format(user, key, bstack11l111ll1_opy_)
      headers = {
        bstack1111ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩટ"): bstack1111ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧઠ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l11l1l111_opy_.format(str(e)))
def bstack1l11l1lll1_opy_(test, bstack1lll11ll11_opy_):
  global CONFIG
  global bstack11111l1ll_opy_
  global bstack111l1llll_opy_
  global bstack11l111ll1_opy_
  global bstack11lll1ll1_opy_
  global bstack111111ll_opy_
  global bstack11111lll_opy_
  global bstack1lll11l11l_opy_
  global bstack1l11ll1ll_opy_
  global bstack11lllll1_opy_
  global bstack111lll1ll_opy_
  global bstack1l1111l111_opy_
  try:
    if not bstack11l111ll1_opy_:
      with open(os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠬࢄࠧડ")), bstack1111ll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઢ"), bstack1111ll1_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩણ"))) as f:
        bstack1ll1lll11l_opy_ = json.loads(bstack1111ll1_opy_ (u"ࠣࡽࠥત") + f.read().strip() + bstack1111ll1_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫથ") + bstack1111ll1_opy_ (u"ࠥࢁࠧદ"))
        bstack11l111ll1_opy_ = bstack1ll1lll11l_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack111lll1ll_opy_:
    for driver in bstack111lll1ll_opy_:
      if bstack11l111ll1_opy_ == driver.session_id:
        if test:
          bstack1llllllll_opy_(driver, test)
        bstack111lll111_opy_(driver, bstack1lll11ll11_opy_)
  elif bstack11l111ll1_opy_:
    bstack1l1lll1ll1_opy_(test, bstack1lll11ll11_opy_)
  if bstack11111l1ll_opy_:
    bstack1lll11l11l_opy_(bstack11111l1ll_opy_)
  if bstack111l1llll_opy_:
    bstack1l11ll1ll_opy_(bstack111l1llll_opy_)
  if bstack11ll1llll_opy_:
    bstack11lllll1_opy_()
def bstack1ll1l11111_opy_(self, test, *args, **kwargs):
  bstack1lll11ll11_opy_ = None
  if test:
    bstack1lll11ll11_opy_ = str(test.name)
  bstack1l11l1lll1_opy_(test, bstack1lll11ll11_opy_)
  bstack11111lll_opy_(self, test, *args, **kwargs)
def bstack1111ll11l_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack111111111_opy_
  global CONFIG
  global bstack111lll1ll_opy_
  global bstack11l111ll1_opy_
  bstack1ll11ll1_opy_ = None
  try:
    if bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪધ"), None):
      try:
        if not bstack11l111ll1_opy_:
          with open(os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠬࢄࠧન")), bstack1111ll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭઩"), bstack1111ll1_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩપ"))) as f:
            bstack1ll1lll11l_opy_ = json.loads(bstack1111ll1_opy_ (u"ࠣࡽࠥફ") + f.read().strip() + bstack1111ll1_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫબ") + bstack1111ll1_opy_ (u"ࠥࢁࠧભ"))
            bstack11l111ll1_opy_ = bstack1ll1lll11l_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack111lll1ll_opy_:
        for driver in bstack111lll1ll_opy_:
          if bstack11l111ll1_opy_ == driver.session_id:
            bstack1ll11ll1_opy_ = driver
    bstack1ll1ll1l1l_opy_ = bstack11l11l111_opy_.bstack1l111l11_opy_(test.tags)
    if bstack1ll11ll1_opy_:
      threading.current_thread().isA11yTest = bstack11l11l111_opy_.bstack1lll1lllll_opy_(bstack1ll11ll1_opy_, bstack1ll1ll1l1l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1ll1ll1l1l_opy_
  except:
    pass
  bstack111111111_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11lll1ll1_opy_
  bstack11lll1ll1_opy_ = self._test
def bstack1l1ll1ll1l_opy_():
  global bstack1l1ll11lll_opy_
  try:
    if os.path.exists(bstack1l1ll11lll_opy_):
      os.remove(bstack1l1ll11lll_opy_)
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧમ") + str(e))
def bstack1ll1l1l1ll_opy_():
  global bstack1l1ll11lll_opy_
  bstack11ll1111l_opy_ = {}
  try:
    if not os.path.isfile(bstack1l1ll11lll_opy_):
      with open(bstack1l1ll11lll_opy_, bstack1111ll1_opy_ (u"ࠬࡽࠧય")):
        pass
      with open(bstack1l1ll11lll_opy_, bstack1111ll1_opy_ (u"ࠨࡷࠬࠤર")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l1ll11lll_opy_):
      bstack11ll1111l_opy_ = json.load(open(bstack1l1ll11lll_opy_, bstack1111ll1_opy_ (u"ࠧࡳࡤࠪ઱")))
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪલ") + str(e))
  finally:
    return bstack11ll1111l_opy_
def bstack1llll11lll_opy_(platform_index, item_index):
  global bstack1l1ll11lll_opy_
  try:
    bstack11ll1111l_opy_ = bstack1ll1l1l1ll_opy_()
    bstack11ll1111l_opy_[item_index] = platform_index
    with open(bstack1l1ll11lll_opy_, bstack1111ll1_opy_ (u"ࠤࡺ࠯ࠧળ")) as outfile:
      json.dump(bstack11ll1111l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ઴") + str(e))
def bstack1l1ll1l1ll_opy_(bstack1ll1111ll1_opy_):
  global CONFIG
  bstack1l1l1l11ll_opy_ = bstack1111ll1_opy_ (u"ࠫࠬવ")
  if not bstack1111ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨશ") in CONFIG:
    logger.info(bstack1111ll1_opy_ (u"࠭ࡎࡰࠢࡳࡰࡦࡺࡦࡰࡴࡰࡷࠥࡶࡡࡴࡵࡨࡨࠥࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡶࡪࡶ࡯ࡳࡶࠣࡪࡴࡸࠠࡓࡱࡥࡳࡹࠦࡲࡶࡰࠪષ"))
  try:
    platform = CONFIG[bstack1111ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪસ")][bstack1ll1111ll1_opy_]
    if bstack1111ll1_opy_ (u"ࠨࡱࡶࠫહ") in platform:
      bstack1l1l1l11ll_opy_ += str(platform[bstack1111ll1_opy_ (u"ࠩࡲࡷࠬ઺")]) + bstack1111ll1_opy_ (u"ࠪ࠰ࠥ࠭઻")
    if bstack1111ll1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴ઼ࠧ") in platform:
      bstack1l1l1l11ll_opy_ += str(platform[bstack1111ll1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨઽ")]) + bstack1111ll1_opy_ (u"࠭ࠬࠡࠩા")
    if bstack1111ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫિ") in platform:
      bstack1l1l1l11ll_opy_ += str(platform[bstack1111ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬી")]) + bstack1111ll1_opy_ (u"ࠩ࠯ࠤࠬુ")
    if bstack1111ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬૂ") in platform:
      bstack1l1l1l11ll_opy_ += str(platform[bstack1111ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ૃ")]) + bstack1111ll1_opy_ (u"ࠬ࠲ࠠࠨૄ")
    if bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫૅ") in platform:
      bstack1l1l1l11ll_opy_ += str(platform[bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ૆")]) + bstack1111ll1_opy_ (u"ࠨ࠮ࠣࠫે")
    if bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪૈ") in platform:
      bstack1l1l1l11ll_opy_ += str(platform[bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫૉ")]) + bstack1111ll1_opy_ (u"ࠫ࠱ࠦࠧ૊")
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"࡙ࠬ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡺࡲࡪࡰࡪࠤ࡫ࡵࡲࠡࡴࡨࡴࡴࡸࡴࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡲࡲࠬો") + str(e))
  finally:
    if bstack1l1l1l11ll_opy_[len(bstack1l1l1l11ll_opy_) - 2:] == bstack1111ll1_opy_ (u"࠭ࠬࠡࠩૌ"):
      bstack1l1l1l11ll_opy_ = bstack1l1l1l11ll_opy_[:-2]
    return bstack1l1l1l11ll_opy_
def bstack1l11111ll1_opy_(path, bstack1l1l1l11ll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l11lll1_opy_ = ET.parse(path)
    bstack1l1l1ll1_opy_ = bstack1l11lll1_opy_.getroot()
    bstack11l1l1l11_opy_ = None
    for suite in bstack1l1l1ll1_opy_.iter(bstack1111ll1_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ્࠭")):
      if bstack1111ll1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ૎") in suite.attrib:
        suite.attrib[bstack1111ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ૏")] += bstack1111ll1_opy_ (u"ࠪࠤࠬૐ") + bstack1l1l1l11ll_opy_
        bstack11l1l1l11_opy_ = suite
    bstack11111l11l_opy_ = None
    for robot in bstack1l1l1ll1_opy_.iter(bstack1111ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૑")):
      bstack11111l11l_opy_ = robot
    bstack1l11ll111_opy_ = len(bstack11111l11l_opy_.findall(bstack1111ll1_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ૒")))
    if bstack1l11ll111_opy_ == 1:
      bstack11111l11l_opy_.remove(bstack11111l11l_opy_.findall(bstack1111ll1_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬ૓"))[0])
      bstack111llll1l_opy_ = ET.Element(bstack1111ll1_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭૔"), attrib={bstack1111ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭૕"): bstack1111ll1_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࡴࠩ૖"), bstack1111ll1_opy_ (u"ࠪ࡭ࡩ࠭૗"): bstack1111ll1_opy_ (u"ࠫࡸ࠶ࠧ૘")})
      bstack11111l11l_opy_.insert(1, bstack111llll1l_opy_)
      bstack1ll11lll1_opy_ = None
      for suite in bstack11111l11l_opy_.iter(bstack1111ll1_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ૙")):
        bstack1ll11lll1_opy_ = suite
      bstack1ll11lll1_opy_.append(bstack11l1l1l11_opy_)
      bstack1l11ll1lll_opy_ = None
      for status in bstack11l1l1l11_opy_.iter(bstack1111ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭૚")):
        bstack1l11ll1lll_opy_ = status
      bstack1ll11lll1_opy_.append(bstack1l11ll1lll_opy_)
    bstack1l11lll1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠬ૛") + str(e))
def bstack11l11ll1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1lllll1_opy_
  global CONFIG
  if bstack1111ll1_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧ૜") in options:
    del options[bstack1111ll1_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨ૝")]
  bstack1l1ll111l_opy_ = bstack1ll1l1l1ll_opy_()
  for bstack1l111l1111_opy_ in bstack1l1ll111l_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1111ll1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࡡࡵࡩࡸࡻ࡬ࡵࡵࠪ૞"), str(bstack1l111l1111_opy_), bstack1111ll1_opy_ (u"ࠫࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠨ૟"))
    bstack1l11111ll1_opy_(path, bstack1l1ll1l1ll_opy_(bstack1l1ll111l_opy_[bstack1l111l1111_opy_]))
  bstack1l1ll1ll1l_opy_()
  return bstack1l1lllll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l111ll1l_opy_(self, ff_profile_dir):
  global bstack1ll1l1l1l1_opy_
  if not ff_profile_dir:
    return None
  return bstack1ll1l1l1l1_opy_(self, ff_profile_dir)
def bstack111ll111_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l11l11lll_opy_
  bstack1l11ll11ll_opy_ = []
  if bstack1111ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૠ") in CONFIG:
    bstack1l11ll11ll_opy_ = CONFIG[bstack1111ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૡ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1111ll1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣૢ")],
      pabot_args[bstack1111ll1_opy_ (u"ࠣࡸࡨࡶࡧࡵࡳࡦࠤૣ")],
      argfile,
      pabot_args.get(bstack1111ll1_opy_ (u"ࠤ࡫࡭ࡻ࡫ࠢ૤")),
      pabot_args[bstack1111ll1_opy_ (u"ࠥࡴࡷࡵࡣࡦࡵࡶࡩࡸࠨ૥")],
      platform[0],
      bstack1l11l11lll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1111ll1_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦ૦")] or [(bstack1111ll1_opy_ (u"ࠧࠨ૧"), None)]
    for platform in enumerate(bstack1l11ll11ll_opy_)
  ]
def bstack1ll11l1ll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1llll1lll_opy_=bstack1111ll1_opy_ (u"࠭ࠧ૨")):
  global bstack1l111l1l1_opy_
  self.platform_index = platform_index
  self.bstack1l1llll1l_opy_ = bstack1llll1lll_opy_
  bstack1l111l1l1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1l11l1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1l1lll_opy_
  global bstack1l1llllll1_opy_
  bstack1llll11ll1_opy_ = copy.deepcopy(item)
  if not bstack1111ll1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૩") in item.options:
    bstack1llll11ll1_opy_.options[bstack1111ll1_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૪")] = []
  bstack11llll1l1_opy_ = bstack1llll11ll1_opy_.options[bstack1111ll1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૫")].copy()
  for v in bstack1llll11ll1_opy_.options[bstack1111ll1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૬")]:
    if bstack1111ll1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪ૭") in v:
      bstack11llll1l1_opy_.remove(v)
    if bstack1111ll1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬ૮") in v:
      bstack11llll1l1_opy_.remove(v)
    if bstack1111ll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ૯") in v:
      bstack11llll1l1_opy_.remove(v)
  bstack11llll1l1_opy_.insert(0, bstack1111ll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝ࡀࡻࡾࠩ૰").format(bstack1llll11ll1_opy_.platform_index))
  bstack11llll1l1_opy_.insert(0, bstack1111ll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࠿ࢁࡽࠨ૱").format(bstack1llll11ll1_opy_.bstack1l1llll1l_opy_))
  bstack1llll11ll1_opy_.options[bstack1111ll1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૲")] = bstack11llll1l1_opy_
  if bstack1l1llllll1_opy_:
    bstack1llll11ll1_opy_.options[bstack1111ll1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૳")].insert(0, bstack1111ll1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖ࠾ࢀࢃࠧ૴").format(bstack1l1llllll1_opy_))
  return bstack1ll1l1lll_opy_(caller_id, datasources, is_last, bstack1llll11ll1_opy_, outs_dir)
def bstack1ll11l111l_opy_(command, item_index):
  if bstack11l11l1ll_opy_.get_property(bstack1111ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭૵")):
    os.environ[bstack1111ll1_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ૶")] = json.dumps(CONFIG[bstack1111ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૷")][item_index % bstack1111ll1ll_opy_])
  global bstack1l1llllll1_opy_
  if bstack1l1llllll1_opy_:
    command[0] = command[0].replace(bstack1111ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૸"), bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭ૹ") + str(
      item_index) + bstack1111ll1_opy_ (u"ࠪࠤࠬૺ") + bstack1l1llllll1_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1111ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪૻ"),
                                    bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩૼ") + str(item_index), 1)
def bstack11ll1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack111l11ll_opy_
  bstack1ll11l111l_opy_(command, item_index)
  return bstack111l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l111l111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack111l11ll_opy_
  bstack1ll11l111l_opy_(command, item_index)
  return bstack111l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1ll11lllll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack111l11ll_opy_
  bstack1ll11l111l_opy_(command, item_index)
  return bstack111l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack11l111lll_opy_(self, runner, quiet=False, capture=True):
  global bstack1l11l1ll1l_opy_
  bstack1ll1l11l_opy_ = bstack1l11l1ll1l_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1111ll1_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭૽")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1111ll1_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫ૾")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1ll1l11l_opy_
def bstack111l1111_opy_(runner, hook_name, context, element, bstack1ll1ll11ll_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1ll1l11ll1_opy_.bstack11l1lllll_opy_(hook_name, element)
    bstack1ll1ll11ll_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1ll1l11ll1_opy_.bstack1l1l1ll1l_opy_(element)
      if hook_name not in [bstack1111ll1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬ૿"), bstack1111ll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬ଀")] and args and hasattr(args[0], bstack1111ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪଁ")):
        args[0].error_message = bstack1111ll1_opy_ (u"ࠫࠬଂ")
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡪࡤࡲࡩࡲࡥࠡࡪࡲࡳࡰࡹࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃࠧଃ").format(str(e)))
def bstack1llll111_opy_(runner, name, context, bstack1ll1ll11ll_opy_, *args):
    if runner.hooks.get(bstack1111ll1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ଄")).__name__ != bstack1111ll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣࡩ࡫ࡦࡢࡷ࡯ࡸࡤ࡮࡯ࡰ࡭ࠥଅ"):
      bstack111l1111_opy_(runner, name, context, runner, bstack1ll1ll11ll_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1111lll1_opy_(bstack1111ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧଆ")) else context.browser
      runner.driver_initialised = bstack1111ll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨଇ")
    except Exception as e:
      logger.debug(bstack1111ll1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡸ࡫ࠠࡢࡶࡷࡶ࡮ࡨࡵࡵࡧ࠽ࠤࢀࢃࠧଈ").format(str(e)))
def bstack1l111l1lll_opy_(runner, name, context, bstack1ll1ll11ll_opy_, *args):
    bstack111l1111_opy_(runner, name, context, context.feature, bstack1ll1ll11ll_opy_, *args)
    try:
      if not bstack1l1lll1l1l_opy_:
        bstack1ll11ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1111lll1_opy_(bstack1111ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪଉ")) else context.browser
        if is_driver_active(bstack1ll11ll1_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1111ll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨଊ")
          bstack11l111ll_opy_ = str(runner.feature.name)
          bstack11lllll1l_opy_(context, bstack11l111ll_opy_)
          bstack1ll11ll1_opy_.execute_script(bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫଋ") + json.dumps(bstack11l111ll_opy_) + bstack1111ll1_opy_ (u"ࠧࡾࡿࠪଌ"))
    except Exception as e:
      logger.debug(bstack1111ll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ଍").format(str(e)))
def bstack11ll111ll_opy_(runner, name, context, bstack1ll1ll11ll_opy_, *args):
    if hasattr(context, bstack1111ll1_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ଎")):
        bstack1ll1l11ll1_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack1111ll1_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬଏ")) else context.feature
    bstack111l1111_opy_(runner, name, context, target, bstack1ll1ll11ll_opy_, *args)
def bstack1lll1ll11_opy_(runner, name, context, bstack1ll1ll11ll_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1ll1l11ll1_opy_.start_test(context)
    bstack111l1111_opy_(runner, name, context, context.scenario, bstack1ll1ll11ll_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1ll1111l11_opy_.bstack1l1l1l1ll_opy_(context, *args)
    try:
      bstack1ll11ll1_opy_ = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪଐ"), context.browser)
      if is_driver_active(bstack1ll11ll1_opy_):
        bstack1l1111l11_opy_.bstack1ll111l11_opy_(bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ଑"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1111ll1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ଒")
        if (not bstack1l1lll1l1l_opy_):
          scenario_name = args[0].name
          feature_name = bstack11l111ll_opy_ = str(runner.feature.name)
          bstack11l111ll_opy_ = feature_name + bstack1111ll1_opy_ (u"ࠧࠡ࠯ࠣࠫଓ") + scenario_name
          if runner.driver_initialised == bstack1111ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥଔ"):
            bstack11lllll1l_opy_(context, bstack11l111ll_opy_)
            bstack1ll11ll1_opy_.execute_script(bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧକ") + json.dumps(bstack11l111ll_opy_) + bstack1111ll1_opy_ (u"ࠪࢁࢂ࠭ଖ"))
    except Exception as e:
      logger.debug(bstack1111ll1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬଗ").format(str(e)))
def bstack1l1ll1111l_opy_(runner, name, context, bstack1ll1ll11ll_opy_, *args):
    bstack111l1111_opy_(runner, name, context, args[0], bstack1ll1ll11ll_opy_, *args)
    try:
      bstack1ll11ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1111lll1_opy_(bstack1111ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫଘ")) else context.browser
      if is_driver_active(bstack1ll11ll1_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1111ll1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦଙ")
        bstack1ll1l11ll1_opy_.bstack111l1lll_opy_(args[0])
        if runner.driver_initialised == bstack1111ll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧଚ"):
          feature_name = bstack11l111ll_opy_ = str(runner.feature.name)
          bstack11l111ll_opy_ = feature_name + bstack1111ll1_opy_ (u"ࠨࠢ࠰ࠤࠬଛ") + context.scenario.name
          bstack1ll11ll1_opy_.execute_script(bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧଜ") + json.dumps(bstack11l111ll_opy_) + bstack1111ll1_opy_ (u"ࠪࢁࢂ࠭ଝ"))
    except Exception as e:
      logger.debug(bstack1111ll1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨଞ").format(str(e)))
def bstack1ll11llll1_opy_(runner, name, context, bstack1ll1ll11ll_opy_, *args):
  bstack1ll1l11ll1_opy_.bstack1lll111ll_opy_(args[0])
  try:
    bstack11ll11l11_opy_ = args[0].status.name
    bstack1ll11ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1111ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫଟ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1ll11ll1_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1111ll1_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭ଠ")
        feature_name = bstack11l111ll_opy_ = str(runner.feature.name)
        bstack11l111ll_opy_ = feature_name + bstack1111ll1_opy_ (u"ࠧࠡ࠯ࠣࠫଡ") + context.scenario.name
        bstack1ll11ll1_opy_.execute_script(bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ଢ") + json.dumps(bstack11l111ll_opy_) + bstack1111ll1_opy_ (u"ࠩࢀࢁࠬଣ"))
    if str(bstack11ll11l11_opy_).lower() == bstack1111ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪତ"):
      bstack1ll111l11l_opy_ = bstack1111ll1_opy_ (u"ࠫࠬଥ")
      bstack1l11111111_opy_ = bstack1111ll1_opy_ (u"ࠬ࠭ଦ")
      bstack1ll11ll11_opy_ = bstack1111ll1_opy_ (u"࠭ࠧଧ")
      try:
        import traceback
        bstack1ll111l11l_opy_ = runner.exception.__class__.__name__
        bstack1ll111l1l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l11111111_opy_ = bstack1111ll1_opy_ (u"ࠧࠡࠩନ").join(bstack1ll111l1l_opy_)
        bstack1ll11ll11_opy_ = bstack1ll111l1l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l11111l11_opy_.format(str(e)))
      bstack1ll111l11l_opy_ += bstack1ll11ll11_opy_
      bstack1l1l111ll_opy_(context, json.dumps(str(args[0].name) + bstack1111ll1_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ଩") + str(bstack1l11111111_opy_)),
                          bstack1111ll1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣପ"))
      if runner.driver_initialised == bstack1111ll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣଫ"):
        bstack11l1ll1ll_opy_(getattr(context, bstack1111ll1_opy_ (u"ࠫࡵࡧࡧࡦࠩବ"), None), bstack1111ll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧଭ"), bstack1ll111l11l_opy_)
        bstack1ll11ll1_opy_.execute_script(bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫମ") + json.dumps(str(args[0].name) + bstack1111ll1_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨଯ") + str(bstack1l11111111_opy_)) + bstack1111ll1_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨର"))
      if runner.driver_initialised == bstack1111ll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ଱"):
        bstack1ll1l1ll1_opy_(bstack1ll11ll1_opy_, bstack1111ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪଲ"), bstack1111ll1_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣଳ") + str(bstack1ll111l11l_opy_))
    else:
      bstack1l1l111ll_opy_(context, bstack1111ll1_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ଴"), bstack1111ll1_opy_ (u"ࠨࡩ࡯ࡨࡲࠦଵ"))
      if runner.driver_initialised == bstack1111ll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧଶ"):
        bstack11l1ll1ll_opy_(getattr(context, bstack1111ll1_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ଷ"), None), bstack1111ll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤସ"))
      bstack1ll11ll1_opy_.execute_script(bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨହ") + json.dumps(str(args[0].name) + bstack1111ll1_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣ଺")) + bstack1111ll1_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ଻"))
      if runner.driver_initialised == bstack1111ll1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳ଼ࠦ"):
        bstack1ll1l1ll1_opy_(bstack1ll11ll1_opy_, bstack1111ll1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢଽ"))
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧା").format(str(e)))
  bstack111l1111_opy_(runner, name, context, args[0], bstack1ll1ll11ll_opy_, *args)
def bstack1l11lll11_opy_(runner, name, context, bstack1ll1ll11ll_opy_, *args):
  bstack1ll1l11ll1_opy_.end_test(args[0])
  try:
    bstack1l1lll1ll_opy_ = args[0].status.name
    bstack1ll11ll1_opy_ = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨି"), context.browser)
    bstack1ll1111l11_opy_.bstack111l11l11_opy_(bstack1ll11ll1_opy_)
    if str(bstack1l1lll1ll_opy_).lower() == bstack1111ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪୀ"):
      bstack1ll111l11l_opy_ = bstack1111ll1_opy_ (u"ࠫࠬୁ")
      bstack1l11111111_opy_ = bstack1111ll1_opy_ (u"ࠬ࠭ୂ")
      bstack1ll11ll11_opy_ = bstack1111ll1_opy_ (u"࠭ࠧୃ")
      try:
        import traceback
        bstack1ll111l11l_opy_ = runner.exception.__class__.__name__
        bstack1ll111l1l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l11111111_opy_ = bstack1111ll1_opy_ (u"ࠧࠡࠩୄ").join(bstack1ll111l1l_opy_)
        bstack1ll11ll11_opy_ = bstack1ll111l1l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l11111l11_opy_.format(str(e)))
      bstack1ll111l11l_opy_ += bstack1ll11ll11_opy_
      bstack1l1l111ll_opy_(context, json.dumps(str(args[0].name) + bstack1111ll1_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ୅") + str(bstack1l11111111_opy_)),
                          bstack1111ll1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ୆"))
      if runner.driver_initialised == bstack1111ll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧେ") or runner.driver_initialised == bstack1111ll1_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫୈ"):
        bstack11l1ll1ll_opy_(getattr(context, bstack1111ll1_opy_ (u"ࠬࡶࡡࡨࡧࠪ୉"), None), bstack1111ll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ୊"), bstack1ll111l11l_opy_)
        bstack1ll11ll1_opy_.execute_script(bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬୋ") + json.dumps(str(args[0].name) + bstack1111ll1_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢୌ") + str(bstack1l11111111_opy_)) + bstack1111ll1_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾ୍ࠩ"))
      if runner.driver_initialised == bstack1111ll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ୎") or runner.driver_initialised == bstack1111ll1_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫ୏"):
        bstack1ll1l1ll1_opy_(bstack1ll11ll1_opy_, bstack1111ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ୐"), bstack1111ll1_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ୑") + str(bstack1ll111l11l_opy_))
    else:
      bstack1l1l111ll_opy_(context, bstack1111ll1_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣ୒"), bstack1111ll1_opy_ (u"ࠣ࡫ࡱࡪࡴࠨ୓"))
      if runner.driver_initialised == bstack1111ll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ୔") or runner.driver_initialised == bstack1111ll1_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ୕"):
        bstack11l1ll1ll_opy_(getattr(context, bstack1111ll1_opy_ (u"ࠫࡵࡧࡧࡦࠩୖ"), None), bstack1111ll1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧୗ"))
      bstack1ll11ll1_opy_.execute_script(bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ୘") + json.dumps(str(args[0].name) + bstack1111ll1_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦ୙")) + bstack1111ll1_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧ୚"))
      if runner.driver_initialised == bstack1111ll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ୛") or runner.driver_initialised == bstack1111ll1_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪଡ଼"):
        bstack1ll1l1ll1_opy_(bstack1ll11ll1_opy_, bstack1111ll1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦଢ଼"))
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ୞").format(str(e)))
  bstack111l1111_opy_(runner, name, context, context.scenario, bstack1ll1ll11ll_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack111ll1111_opy_(runner, name, context, bstack1ll1ll11ll_opy_, *args):
    target = context.scenario if hasattr(context, bstack1111ll1_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨୟ")) else context.feature
    bstack111l1111_opy_(runner, name, context, target, bstack1ll1ll11ll_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack11llll1ll_opy_(runner, name, context, bstack1ll1ll11ll_opy_, *args):
    try:
      bstack1ll11ll1_opy_ = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ୠ"), context.browser)
      if context.failed is True:
        bstack11ll11ll_opy_ = []
        bstack1l11lll11l_opy_ = []
        bstack11111111l_opy_ = []
        bstack1ll1l11l11_opy_ = bstack1111ll1_opy_ (u"ࠨࠩୡ")
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11ll11ll_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1ll111l1l_opy_ = traceback.format_tb(exc_tb)
            bstack11l1ll1l1_opy_ = bstack1111ll1_opy_ (u"ࠩࠣࠫୢ").join(bstack1ll111l1l_opy_)
            bstack1l11lll11l_opy_.append(bstack11l1ll1l1_opy_)
            bstack11111111l_opy_.append(bstack1ll111l1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l11111l11_opy_.format(str(e)))
        bstack1ll111l11l_opy_ = bstack1111ll1_opy_ (u"ࠪࠫୣ")
        for i in range(len(bstack11ll11ll_opy_)):
          bstack1ll111l11l_opy_ += bstack11ll11ll_opy_[i] + bstack11111111l_opy_[i] + bstack1111ll1_opy_ (u"ࠫࡡࡴࠧ୤")
        bstack1ll1l11l11_opy_ = bstack1111ll1_opy_ (u"ࠬࠦࠧ୥").join(bstack1l11lll11l_opy_)
        if runner.driver_initialised in [bstack1111ll1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ୦"), bstack1111ll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ୧")]:
          bstack1l1l111ll_opy_(context, bstack1ll1l11l11_opy_, bstack1111ll1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ୨"))
          bstack11l1ll1ll_opy_(getattr(context, bstack1111ll1_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ୩"), None), bstack1111ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ୪"), bstack1ll111l11l_opy_)
          bstack1ll11ll1_opy_.execute_script(bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ୫") + json.dumps(bstack1ll1l11l11_opy_) + bstack1111ll1_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬ୬"))
          bstack1ll1l1ll1_opy_(bstack1ll11ll1_opy_, bstack1111ll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ୭"), bstack1111ll1_opy_ (u"ࠢࡔࡱࡰࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢ࡟ࡲࠧ୮") + str(bstack1ll111l11l_opy_))
          bstack1lll1llll1_opy_ = bstack1l11111lll_opy_(bstack1ll1l11l11_opy_, runner.feature.name, logger)
          if (bstack1lll1llll1_opy_ != None):
            bstack1lll1l11ll_opy_.append(bstack1lll1llll1_opy_)
      else:
        if runner.driver_initialised in [bstack1111ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ୯"), bstack1111ll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ୰")]:
          bstack1l1l111ll_opy_(context, bstack1111ll1_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨୱ") + str(runner.feature.name) + bstack1111ll1_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨ୲"), bstack1111ll1_opy_ (u"ࠧ࡯࡮ࡧࡱࠥ୳"))
          bstack11l1ll1ll_opy_(getattr(context, bstack1111ll1_opy_ (u"࠭ࡰࡢࡩࡨࠫ୴"), None), bstack1111ll1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ୵"))
          bstack1ll11ll1_opy_.execute_script(bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭୶") + json.dumps(bstack1111ll1_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧ୷") + str(runner.feature.name) + bstack1111ll1_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧ୸")) + bstack1111ll1_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪ୹"))
          bstack1ll1l1ll1_opy_(bstack1ll11ll1_opy_, bstack1111ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ୺"))
          bstack1lll1llll1_opy_ = bstack1l11111lll_opy_(bstack1ll1l11l11_opy_, runner.feature.name, logger)
          if (bstack1lll1llll1_opy_ != None):
            bstack1lll1l11ll_opy_.append(bstack1lll1llll1_opy_)
    except Exception as e:
      logger.debug(bstack1111ll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ୻").format(str(e)))
    bstack111l1111_opy_(runner, name, context, context.feature, bstack1ll1ll11ll_opy_, *args)
def bstack1l11ll1111_opy_(runner, name, context, bstack1ll1ll11ll_opy_, *args):
    bstack111l1111_opy_(runner, name, context, runner, bstack1ll1ll11ll_opy_, *args)
def bstack1l111ll11_opy_(self, name, context, *args):
  if bstack1ll111ll_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1111ll1ll_opy_
    bstack1ll11l11_opy_ = CONFIG[bstack1111ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ୼")][platform_index]
    os.environ[bstack1111ll1_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ୽")] = json.dumps(bstack1ll11l11_opy_)
  global bstack1ll1ll11ll_opy_
  if not hasattr(self, bstack1111ll1_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࡪࠧ୾")):
    self.driver_initialised = None
  bstack1ll11lll1l_opy_ = {
      bstack1111ll1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧ୿"): bstack1llll111_opy_,
      bstack1111ll1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ஀"): bstack1l111l1lll_opy_,
      bstack1111ll1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡺࡡࡨࠩ஁"): bstack11ll111ll_opy_,
      bstack1111ll1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨஂ"): bstack1lll1ll11_opy_,
      bstack1111ll1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠬஃ"): bstack1l1ll1111l_opy_,
      bstack1111ll1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡶࡨࡴࠬ஄"): bstack1ll11llll1_opy_,
      bstack1111ll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪஅ"): bstack1l11lll11_opy_,
      bstack1111ll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡷࡥ࡬࠭ஆ"): bstack111ll1111_opy_,
      bstack1111ll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫஇ"): bstack11llll1ll_opy_,
      bstack1111ll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨஈ"): bstack1l11ll1111_opy_
  }
  handler = bstack1ll11lll1l_opy_.get(name, bstack1ll1ll11ll_opy_)
  handler(self, name, context, bstack1ll1ll11ll_opy_, *args)
  if name in [bstack1111ll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭உ"), bstack1111ll1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨஊ"), bstack1111ll1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫ஋")]:
    try:
      bstack1ll11ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1111lll1_opy_(bstack1111ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ஌")) else context.browser
      bstack11l1ll1l_opy_ = (
        (name == bstack1111ll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭஍") and self.driver_initialised == bstack1111ll1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣஎ")) or
        (name == bstack1111ll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬஏ") and self.driver_initialised == bstack1111ll1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢஐ")) or
        (name == bstack1111ll1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ஑") and self.driver_initialised in [bstack1111ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥஒ"), bstack1111ll1_opy_ (u"ࠤ࡬ࡲࡸࡺࡥࡱࠤஓ")]) or
        (name == bstack1111ll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧஔ") and self.driver_initialised == bstack1111ll1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤக"))
      )
      if bstack11l1ll1l_opy_:
        self.driver_initialised = None
        bstack1ll11ll1_opy_.quit()
    except Exception:
      pass
def bstack1ll111llll_opy_(config, startdir):
  return bstack1111ll1_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥ஖").format(bstack1111ll1_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧ஗"))
notset = Notset()
def bstack1l1l1lll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll1ll1l_opy_
  if str(name).lower() == bstack1111ll1_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧ஘"):
    return bstack1111ll1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢங")
  else:
    return bstack1ll1ll1l_opy_(self, name, default, skip)
def bstack1l1ll11l_opy_(item, when):
  global bstack1llll11111_opy_
  try:
    bstack1llll11111_opy_(item, when)
  except Exception as e:
    pass
def bstack11l111l1l_opy_():
  return
def bstack1ll1ll111_opy_(type, name, status, reason, bstack1ll1l1ll11_opy_, bstack1lll1l1l1l_opy_):
  bstack11ll1ll11_opy_ = {
    bstack1111ll1_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩச"): type,
    bstack1111ll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭஛"): {}
  }
  if type == bstack1111ll1_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ஜ"):
    bstack11ll1ll11_opy_[bstack1111ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ஝")][bstack1111ll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬஞ")] = bstack1ll1l1ll11_opy_
    bstack11ll1ll11_opy_[bstack1111ll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪட")][bstack1111ll1_opy_ (u"ࠨࡦࡤࡸࡦ࠭஠")] = json.dumps(str(bstack1lll1l1l1l_opy_))
  if type == bstack1111ll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ஡"):
    bstack11ll1ll11_opy_[bstack1111ll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭஢")][bstack1111ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩண")] = name
  if type == bstack1111ll1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨத"):
    bstack11ll1ll11_opy_[bstack1111ll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ஥")][bstack1111ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ஦")] = status
    if status == bstack1111ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ஧"):
      bstack11ll1ll11_opy_[bstack1111ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬந")][bstack1111ll1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪன")] = json.dumps(str(reason))
  bstack1llll1lll1_opy_ = bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩப").format(json.dumps(bstack11ll1ll11_opy_))
  return bstack1llll1lll1_opy_
def bstack1l11l1lll_opy_(driver_command, response):
    if driver_command == bstack1111ll1_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ஫"):
        bstack1l1111l11_opy_.bstack1ll111lll1_opy_({
            bstack1111ll1_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ஬"): response[bstack1111ll1_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭஭")],
            bstack1111ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨம"): bstack1l1111l11_opy_.current_test_uuid()
        })
def bstack1llll1ll_opy_(item, call, rep):
  global bstack1lll1lll1_opy_
  global bstack111lll1ll_opy_
  global bstack1l1lll1l1l_opy_
  name = bstack1111ll1_opy_ (u"ࠩࠪய")
  try:
    if rep.when == bstack1111ll1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨர"):
      bstack11l111ll1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l1lll1l1l_opy_:
          name = str(rep.nodeid)
          bstack1l11ll1ll1_opy_ = bstack1ll1ll111_opy_(bstack1111ll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬற"), name, bstack1111ll1_opy_ (u"ࠬ࠭ல"), bstack1111ll1_opy_ (u"࠭ࠧள"), bstack1111ll1_opy_ (u"ࠧࠨழ"), bstack1111ll1_opy_ (u"ࠨࠩவ"))
          threading.current_thread().bstack1ll11llll_opy_ = name
          for driver in bstack111lll1ll_opy_:
            if bstack11l111ll1_opy_ == driver.session_id:
              driver.execute_script(bstack1l11ll1ll1_opy_)
      except Exception as e:
        logger.debug(bstack1111ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩஶ").format(str(e)))
      try:
        bstack1lllll1ll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1111ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫஷ"):
          status = bstack1111ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫஸ") if rep.outcome.lower() == bstack1111ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬஹ") else bstack1111ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭஺")
          reason = bstack1111ll1_opy_ (u"ࠧࠨ஻")
          if status == bstack1111ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ஼"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1111ll1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ஽") if status == bstack1111ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪா") else bstack1111ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪி")
          data = name + bstack1111ll1_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧீ") if status == bstack1111ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ு") else name + bstack1111ll1_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪூ") + reason
          bstack11lllllll1_opy_ = bstack1ll1ll111_opy_(bstack1111ll1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ௃"), bstack1111ll1_opy_ (u"ࠩࠪ௄"), bstack1111ll1_opy_ (u"ࠪࠫ௅"), bstack1111ll1_opy_ (u"ࠫࠬெ"), level, data)
          for driver in bstack111lll1ll_opy_:
            if bstack11l111ll1_opy_ == driver.session_id:
              driver.execute_script(bstack11lllllll1_opy_)
      except Exception as e:
        logger.debug(bstack1111ll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩே").format(str(e)))
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪை").format(str(e)))
  bstack1lll1lll1_opy_(item, call, rep)
def bstack1l111l1ll1_opy_(driver, bstack1ll11l1111_opy_, test=None):
  global bstack1l1ll1l111_opy_
  if test != None:
    bstack1ll11l11ll_opy_ = getattr(test, bstack1111ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ௉"), None)
    bstack111lllll1_opy_ = getattr(test, bstack1111ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ொ"), None)
    PercySDK.screenshot(driver, bstack1ll11l1111_opy_, bstack1ll11l11ll_opy_=bstack1ll11l11ll_opy_, bstack111lllll1_opy_=bstack111lllll1_opy_, bstack1111l1111_opy_=bstack1l1ll1l111_opy_)
  else:
    PercySDK.screenshot(driver, bstack1ll11l1111_opy_)
def bstack1lllll1l1l_opy_(driver):
  if bstack111l1l11_opy_.bstack1lll1l1111_opy_() is True or bstack111l1l11_opy_.capturing() is True:
    return
  bstack111l1l11_opy_.bstack11ll11ll1_opy_()
  while not bstack111l1l11_opy_.bstack1lll1l1111_opy_():
    bstack1lll1l11l_opy_ = bstack111l1l11_opy_.bstack1lll111l_opy_()
    bstack1l111l1ll1_opy_(driver, bstack1lll1l11l_opy_)
  bstack111l1l11_opy_.bstack1l11ll1l11_opy_()
def bstack1lllllll1_opy_(sequence, driver_command, response = None, bstack1llll1l111_opy_ = None, args = None):
    try:
      if sequence != bstack1111ll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩோ"):
        return
      if percy.bstack111111ll1_opy_() == bstack1111ll1_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤௌ"):
        return
      bstack1lll1l11l_opy_ = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫்ࠧ"), None)
      for command in bstack1l1l11ll1l_opy_:
        if command == driver_command:
          for driver in bstack111lll1ll_opy_:
            bstack1lllll1l1l_opy_(driver)
      bstack1ll1l11l1_opy_ = percy.bstack1l11ll11_opy_()
      if driver_command in bstack1lll1l111_opy_[bstack1ll1l11l1_opy_]:
        bstack111l1l11_opy_.bstack11l11111_opy_(bstack1lll1l11l_opy_, driver_command)
    except Exception as e:
      pass
def bstack1lll1l1ll_opy_(framework_name):
  if bstack11l11l1ll_opy_.get_property(bstack1111ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ௎")):
      return
  bstack11l11l1ll_opy_.bstack11llllll1_opy_(bstack1111ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ௏"), True)
  global bstack1ll1l11ll_opy_
  global bstack1l1l11l1ll_opy_
  global bstack111lllll_opy_
  bstack1ll1l11ll_opy_ = framework_name
  logger.info(bstack1111l11l_opy_.format(bstack1ll1l11ll_opy_.split(bstack1111ll1_opy_ (u"ࠧ࠮ࠩௐ"))[0]))
  bstack1l1l1l11_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1ll111ll_opy_:
      Service.start = bstack1l1lll11ll_opy_
      Service.stop = bstack1lll1l11_opy_
      webdriver.Remote.get = bstack11l1ll11l_opy_
      WebDriver.close = bstack1l1ll1l1l_opy_
      WebDriver.quit = bstack11l1ll111_opy_
      webdriver.Remote.__init__ = bstack1ll11111ll_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1ll111ll_opy_:
        webdriver.Remote.__init__ = bstack1ll111l111_opy_
    WebDriver.execute = bstack1l1ll1ll_opy_
    bstack1l1l11l1ll_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1ll111ll_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack11111l1l_opy_
  except Exception as e:
    pass
  bstack1lll11l11_opy_()
  if not bstack1l1l11l1ll_opy_:
    bstack111l11lll_opy_(bstack1111ll1_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥ௑"), bstack1l1lllll11_opy_)
  if bstack1ll111111l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack111l1l1ll_opy_
    except Exception as e:
      logger.error(bstack1ll1l1l11l_opy_.format(str(e)))
  if bstack1l1l1ll111_opy_():
    bstack1lll11111l_opy_(CONFIG, logger)
  if (bstack1111ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௒") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack111111ll1_opy_() == bstack1111ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣ௓"):
          bstack1l1l1l1lll_opy_(bstack1lllllll1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l111ll1l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11ll1l1l1_opy_
      except Exception as e:
        logger.warn(bstack1l11l1111_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l111llll1_opy_
      except Exception as e:
        logger.debug(bstack1l11l11l1_opy_ + str(e))
    except Exception as e:
      bstack111l11lll_opy_(e, bstack1l11l1111_opy_)
    Output.start_test = bstack1lllll1111_opy_
    Output.end_test = bstack1ll1l11111_opy_
    TestStatus.__init__ = bstack1111ll11l_opy_
    QueueItem.__init__ = bstack1ll11l1ll_opy_
    pabot._create_items = bstack111ll111_opy_
    try:
      from pabot import __version__ as bstack111ll1l11_opy_
      if version.parse(bstack111ll1l11_opy_) >= version.parse(bstack1111ll1_opy_ (u"ࠫ࠷࠴࠱࠶࠰࠳ࠫ௔")):
        pabot._run = bstack1ll11lllll_opy_
      elif version.parse(bstack111ll1l11_opy_) >= version.parse(bstack1111ll1_opy_ (u"ࠬ࠸࠮࠲࠵࠱࠴ࠬ௕")):
        pabot._run = bstack1l111l111l_opy_
      else:
        pabot._run = bstack11ll1lll_opy_
    except Exception as e:
      pabot._run = bstack11ll1lll_opy_
    pabot._create_command_for_execution = bstack1l1l11l1_opy_
    pabot._report_results = bstack11l11ll1l_opy_
  if bstack1111ll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭௖") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack111l11lll_opy_(e, bstack1lll111l11_opy_)
    Runner.run_hook = bstack1l111ll11_opy_
    Step.run = bstack11l111lll_opy_
  if bstack1111ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧௗ") in str(framework_name).lower():
    if not bstack1ll111ll_opy_:
      return
    try:
      if percy.bstack111111ll1_opy_() == bstack1111ll1_opy_ (u"ࠣࡶࡵࡹࡪࠨ௘"):
          bstack1l1l1l1lll_opy_(bstack1lllllll1_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1ll111llll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11l111l1l_opy_
      Config.getoption = bstack1l1l1lll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1llll1ll_opy_
    except Exception as e:
      pass
def bstack1lllll111l_opy_():
  global CONFIG
  if bstack1111ll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ௙") in CONFIG and int(CONFIG[bstack1111ll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ௚")]) > 1:
    logger.warn(bstack11lllllll_opy_)
def bstack11111lll1_opy_(arg, bstack1llll11l_opy_, bstack1ll1l11l1l_opy_=None):
  global CONFIG
  global bstack1l1lll1lll_opy_
  global bstack1l1lll1111_opy_
  global bstack1ll111ll_opy_
  global bstack11l11l1ll_opy_
  bstack11llllllll_opy_ = bstack1111ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௛")
  if bstack1llll11l_opy_ and isinstance(bstack1llll11l_opy_, str):
    bstack1llll11l_opy_ = eval(bstack1llll11l_opy_)
  CONFIG = bstack1llll11l_opy_[bstack1111ll1_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ௜")]
  bstack1l1lll1lll_opy_ = bstack1llll11l_opy_[bstack1111ll1_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ௝")]
  bstack1l1lll1111_opy_ = bstack1llll11l_opy_[bstack1111ll1_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ௞")]
  bstack1ll111ll_opy_ = bstack1llll11l_opy_[bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ௟")]
  bstack11l11l1ll_opy_.bstack11llllll1_opy_(bstack1111ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ௠"), bstack1ll111ll_opy_)
  os.environ[bstack1111ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ௡")] = bstack11llllllll_opy_
  os.environ[bstack1111ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪ௢")] = json.dumps(CONFIG)
  os.environ[bstack1111ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ௣")] = bstack1l1lll1lll_opy_
  os.environ[bstack1111ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ௤")] = str(bstack1l1lll1111_opy_)
  os.environ[bstack1111ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭௥")] = str(True)
  if bstack1l1l1l1l_opy_(arg, [bstack1111ll1_opy_ (u"ࠨ࠯ࡱࠫ௦"), bstack1111ll1_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ௧")]) != -1:
    os.environ[bstack1111ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫ௨")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1l1l111ll1_opy_)
    return
  bstack1l11l1l11l_opy_()
  global bstack1llll1ll1l_opy_
  global bstack1l1ll1l111_opy_
  global bstack1l11l11lll_opy_
  global bstack1l1llllll1_opy_
  global bstack1ll1111l_opy_
  global bstack111lllll_opy_
  global bstack111l1l11l_opy_
  arg.append(bstack1111ll1_opy_ (u"ࠦ࠲࡝ࠢ௩"))
  arg.append(bstack1111ll1_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿ࡓ࡯ࡥࡷ࡯ࡩࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡮ࡲࡲࡶࡹ࡫ࡤ࠻ࡲࡼࡸࡪࡹࡴ࠯ࡒࡼࡸࡪࡹࡴࡘࡣࡵࡲ࡮ࡴࡧࠣ௪"))
  arg.append(bstack1111ll1_opy_ (u"ࠨ࠭ࡘࠤ௫"))
  arg.append(bstack1111ll1_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡕࡪࡨࠤ࡭ࡵ࡯࡬࡫ࡰࡴࡱࠨ௬"))
  global bstack1lll11l1l1_opy_
  global bstack1l111ll11l_opy_
  global bstack1ll1ll1l11_opy_
  global bstack111111111_opy_
  global bstack1ll1l1l1l1_opy_
  global bstack1l111l1l1_opy_
  global bstack1ll1l1lll_opy_
  global bstack1l11l1l11_opy_
  global bstack1l1llll11_opy_
  global bstack1lll1l1l1_opy_
  global bstack1ll1ll1l_opy_
  global bstack1llll11111_opy_
  global bstack1lll1lll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll11l1l1_opy_ = webdriver.Remote.__init__
    bstack1l111ll11l_opy_ = WebDriver.quit
    bstack1l11l1l11_opy_ = WebDriver.close
    bstack1l1llll11_opy_ = WebDriver.get
    bstack1ll1ll1l11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1ll11111l_opy_(CONFIG) and bstack1l1l11ll_opy_():
    if bstack111l11ll1_opy_() < version.parse(bstack1lll11l111_opy_):
      logger.error(bstack1l1ll1l11_opy_.format(bstack111l11ll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1lll1l1l1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll1l1l11l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll1ll1l_opy_ = Config.getoption
    from _pytest import runner
    bstack1llll11111_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l11l111ll_opy_)
  try:
    from pytest_bdd import reporting
    bstack1lll1lll1_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1111ll1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ௭"))
  bstack1l11l11lll_opy_ = CONFIG.get(bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭௮"), {}).get(bstack1111ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ௯"))
  bstack111l1l11l_opy_ = True
  bstack1lll1l1ll_opy_(bstack1l1ll111l1_opy_)
  os.environ[bstack1111ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ௰")] = CONFIG[bstack1111ll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ௱")]
  os.environ[bstack1111ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ௲")] = CONFIG[bstack1111ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ௳")]
  os.environ[bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ௴")] = bstack1ll111ll_opy_.__str__()
  from _pytest.config import main as bstack1l1l11111l_opy_
  bstack1ll1ll1ll1_opy_ = []
  try:
    bstack1111l11ll_opy_ = bstack1l1l11111l_opy_(arg)
    if bstack1111ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭௵") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1l1l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll1ll1ll1_opy_.append(bstack11l1l1l1_opy_)
    try:
      bstack1111l1l1_opy_ = (bstack1ll1ll1ll1_opy_, int(bstack1111l11ll_opy_))
      bstack1ll1l11l1l_opy_.append(bstack1111l1l1_opy_)
    except:
      bstack1ll1l11l1l_opy_.append((bstack1ll1ll1ll1_opy_, bstack1111l11ll_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1ll1ll1ll1_opy_.append({bstack1111ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ௶"): bstack1111ll1_opy_ (u"ࠫࡕࡸ࡯ࡤࡧࡶࡷࠥ࠭௷") + os.environ.get(bstack1111ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ௸")), bstack1111ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ௹"): traceback.format_exc(), bstack1111ll1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭௺"): int(os.environ.get(bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ௻")))})
    bstack1ll1l11l1l_opy_.append((bstack1ll1ll1ll1_opy_, 1))
def bstack1l111lll1l_opy_(arg):
  global bstack11l1lll11_opy_
  bstack1lll1l1ll_opy_(bstack1l11l111l1_opy_)
  os.environ[bstack1111ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ௼")] = str(bstack1l1lll1111_opy_)
  from behave.__main__ import main as bstack11l11l11l_opy_
  status_code = bstack11l11l11l_opy_(arg)
  if status_code != 0:
    bstack11l1lll11_opy_ = status_code
def bstack1l11l11l1l_opy_():
  logger.info(bstack11l1lll1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1111ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ௽"), help=bstack1111ll1_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࠬ௾"))
  parser.add_argument(bstack1111ll1_opy_ (u"ࠬ࠳ࡵࠨ௿"), bstack1111ll1_opy_ (u"࠭࠭࠮ࡷࡶࡩࡷࡴࡡ࡮ࡧࠪఀ"), help=bstack1111ll1_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡺࡹࡥࡳࡰࡤࡱࡪ࠭ఁ"))
  parser.add_argument(bstack1111ll1_opy_ (u"ࠨ࠯࡮ࠫం"), bstack1111ll1_opy_ (u"ࠩ࠰࠱ࡰ࡫ࡹࠨః"), help=bstack1111ll1_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠫఄ"))
  parser.add_argument(bstack1111ll1_opy_ (u"ࠫ࠲࡬ࠧఅ"), bstack1111ll1_opy_ (u"ࠬ࠳࠭ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪఆ"), help=bstack1111ll1_opy_ (u"࡙࠭ࡰࡷࡵࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬఇ"))
  bstack11111llll_opy_ = parser.parse_args()
  try:
    bstack11l111111_opy_ = bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡧࡦࡰࡨࡶ࡮ࡩ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫఈ")
    if bstack11111llll_opy_.framework and bstack11111llll_opy_.framework not in (bstack1111ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨఉ"), bstack1111ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪఊ")):
      bstack11l111111_opy_ = bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩఋ")
    bstack11lll11l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l111111_opy_)
    bstack1l1ll1lll_opy_ = open(bstack11lll11l_opy_, bstack1111ll1_opy_ (u"ࠫࡷ࠭ఌ"))
    bstack1l11l1l1_opy_ = bstack1l1ll1lll_opy_.read()
    bstack1l1ll1lll_opy_.close()
    if bstack11111llll_opy_.username:
      bstack1l11l1l1_opy_ = bstack1l11l1l1_opy_.replace(bstack1111ll1_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ఍"), bstack11111llll_opy_.username)
    if bstack11111llll_opy_.key:
      bstack1l11l1l1_opy_ = bstack1l11l1l1_opy_.replace(bstack1111ll1_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨఎ"), bstack11111llll_opy_.key)
    if bstack11111llll_opy_.framework:
      bstack1l11l1l1_opy_ = bstack1l11l1l1_opy_.replace(bstack1111ll1_opy_ (u"࡚ࠧࡑࡘࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨఏ"), bstack11111llll_opy_.framework)
    file_name = bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫఐ")
    file_path = os.path.abspath(file_name)
    bstack1l1111111l_opy_ = open(file_path, bstack1111ll1_opy_ (u"ࠩࡺࠫ఑"))
    bstack1l1111111l_opy_.write(bstack1l11l1l1_opy_)
    bstack1l1111111l_opy_.close()
    logger.info(bstack11ll11l1l_opy_)
    try:
      os.environ[bstack1111ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬఒ")] = bstack11111llll_opy_.framework if bstack11111llll_opy_.framework != None else bstack1111ll1_opy_ (u"ࠦࠧఓ")
      config = yaml.safe_load(bstack1l11l1l1_opy_)
      config[bstack1111ll1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬఔ")] = bstack1111ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡳࡦࡶࡸࡴࠬక")
      bstack1l11lll111_opy_(bstack1l1l111111_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1llll11l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll1ll11l1_opy_.format(str(e)))
def bstack1l11lll111_opy_(bstack1l111111ll_opy_, config, bstack1l1l1ll11_opy_={}):
  global bstack1ll111ll_opy_
  global bstack1llll11l11_opy_
  global bstack11l11l1ll_opy_
  if not config:
    return
  bstack1lll1l1l_opy_ = bstack1llllllll1_opy_ if not bstack1ll111ll_opy_ else (
    bstack1ll1111111_opy_ if bstack1111ll1_opy_ (u"ࠧࡢࡲࡳࠫఖ") in config else bstack1ll1l1l111_opy_)
  bstack1ll1lll11_opy_ = False
  bstack1l11lll1l_opy_ = False
  if bstack1ll111ll_opy_ is True:
      if bstack1111ll1_opy_ (u"ࠨࡣࡳࡴࠬగ") in config:
          bstack1ll1lll11_opy_ = True
      else:
          bstack1l11lll1l_opy_ = True
  bstack1ll1llll1l_opy_ = bstack1ll11l1l1_opy_.bstack11l1llll1_opy_(config, bstack1llll11l11_opy_)
  data = {
    bstack1111ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫఘ"): config[bstack1111ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬఙ")],
    bstack1111ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧచ"): config[bstack1111ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨఛ")],
    bstack1111ll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪజ"): bstack1l111111ll_opy_,
    bstack1111ll1_opy_ (u"ࠧࡥࡧࡷࡩࡨࡺࡥࡥࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫఝ"): os.environ.get(bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪఞ"), bstack1llll11l11_opy_),
    bstack1111ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫట"): bstack11ll1111_opy_,
    bstack1111ll1_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰࠬఠ"): bstack1ll1l1llll_opy_(),
    bstack1111ll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧడ"): {
      bstack1111ll1_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪఢ"): str(config[bstack1111ll1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ణ")]) if bstack1111ll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧత") in config else bstack1111ll1_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤథ"),
      bstack1111ll1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨ࡚ࡪࡸࡳࡪࡱࡱࠫద"): sys.version,
      bstack1111ll1_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬధ"): bstack111ll11l1_opy_(os.getenv(bstack1111ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨన"), bstack1111ll1_opy_ (u"ࠧࠨ఩"))),
      bstack1111ll1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨప"): bstack1111ll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧఫ"),
      bstack1111ll1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩబ"): bstack1lll1l1l_opy_,
      bstack1111ll1_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧభ"): bstack1ll1llll1l_opy_,
      bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡣࡺࡻࡩࡥࠩమ"): os.environ[bstack1111ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩయ")],
      bstack1111ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨర"): bstack11llll111_opy_(os.environ.get(bstack1111ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨఱ"), bstack1llll11l11_opy_)),
      bstack1111ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪల"): config[bstack1111ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫళ")] if config[bstack1111ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬఴ")] else bstack1111ll1_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦవ"),
      bstack1111ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭శ"): str(config[bstack1111ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧష")]) if bstack1111ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨస") in config else bstack1111ll1_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣహ"),
      bstack1111ll1_opy_ (u"ࠨࡱࡶࠫ఺"): sys.platform,
      bstack1111ll1_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ఻"): socket.gethostname(),
      bstack1111ll1_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨ఼ࠬ"): bstack11l11l1ll_opy_.get_property(bstack1111ll1_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ఽ"))
    }
  }
  if not bstack11l11l1ll_opy_.get_property(bstack1111ll1_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬా")) is None:
    data[bstack1111ll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩి")][bstack1111ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡏࡨࡸࡦࡪࡡࡵࡣࠪీ")] = {
      bstack1111ll1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨు"): bstack1111ll1_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧూ"),
      bstack1111ll1_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪృ"): bstack11l11l1ll_opy_.get_property(bstack1111ll1_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫౄ")),
      bstack1111ll1_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࡓࡻ࡭ࡣࡧࡵࠫ౅"): bstack11l11l1ll_opy_.get_property(bstack1111ll1_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡎࡰࠩె"))
    }
  if bstack1l111111ll_opy_ == bstack111ll1l1l_opy_:
    data[bstack1111ll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪే")][bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡃࡰࡰࡩ࡭࡬࠭ై")] = bstack1lll11ll1l_opy_(config)
    data[bstack1111ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ౉")][bstack1111ll1_opy_ (u"ࠪ࡭ࡸࡖࡥࡳࡥࡼࡅࡺࡺ࡯ࡆࡰࡤࡦࡱ࡫ࡤࠨొ")] = percy.bstack1ll1111l1l_opy_
    data[bstack1111ll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧో")][bstack1111ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡆࡺ࡯࡬ࡥࡋࡧࠫౌ")] = percy.bstack1l1l1111l_opy_
  update(data[bstack1111ll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴ్ࠩ")], bstack1l1l1ll11_opy_)
  try:
    response = bstack1ll1llllll_opy_(bstack1111ll1_opy_ (u"ࠧࡑࡑࡖࡘࠬ౎"), bstack1ll1lll1l1_opy_(bstack11l1lll1l_opy_), data, {
      bstack1111ll1_opy_ (u"ࠨࡣࡸࡸ࡭࠭౏"): (config[bstack1111ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ౐")], config[bstack1111ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭౑")])
    })
    if response:
      logger.debug(bstack1lll1ll1l_opy_.format(bstack1l111111ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11ll1ll1l_opy_.format(str(e)))
def bstack111ll11l1_opy_(framework):
  return bstack1111ll1_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣ౒").format(str(framework), __version__) if framework else bstack1111ll1_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨ౓").format(
    __version__)
def bstack1l11l1l11l_opy_():
  global CONFIG
  global bstack1l1111l1l1_opy_
  if bool(CONFIG):
    return
  try:
    bstack1111l1l1l_opy_()
    logger.debug(bstack1l1ll11ll_opy_.format(str(CONFIG)))
    bstack1l1111l1l1_opy_ = bstack1111111ll_opy_.bstack11ll11l1_opy_(CONFIG, bstack1l1111l1l1_opy_)
    bstack1l1l1l11_opy_()
  except Exception as e:
    logger.error(bstack1111ll1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥ౔") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll111l1_opy_
  atexit.register(bstack11lll1111_opy_)
  signal.signal(signal.SIGINT, bstack1111l111_opy_)
  signal.signal(signal.SIGTERM, bstack1111l111_opy_)
def bstack1ll111l1_opy_(exctype, value, traceback):
  global bstack111lll1ll_opy_
  try:
    for driver in bstack111lll1ll_opy_:
      bstack1ll1l1ll1_opy_(driver, bstack1111ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪౕࠧ"), bstack1111ll1_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱౖࠦ") + str(value))
  except Exception:
    pass
  bstack1lll1ll111_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1lll1ll111_opy_(message=bstack1111ll1_opy_ (u"ࠩࠪ౗"), bstack1111llll1_opy_ = False):
  global CONFIG
  bstack11l1l1ll_opy_ = bstack1111ll1_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠬౘ") if bstack1111llll1_opy_ else bstack1111ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪౙ")
  try:
    if message:
      bstack1l1l1ll11_opy_ = {
        bstack11l1l1ll_opy_ : str(message)
      }
      bstack1l11lll111_opy_(bstack111ll1l1l_opy_, CONFIG, bstack1l1l1ll11_opy_)
    else:
      bstack1l11lll111_opy_(bstack111ll1l1l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11ll1l111_opy_.format(str(e)))
def bstack1lll11ll_opy_(bstack1ll11l1l11_opy_, size):
  bstack1lll1l1l11_opy_ = []
  while len(bstack1ll11l1l11_opy_) > size:
    bstack111lll11l_opy_ = bstack1ll11l1l11_opy_[:size]
    bstack1lll1l1l11_opy_.append(bstack111lll11l_opy_)
    bstack1ll11l1l11_opy_ = bstack1ll11l1l11_opy_[size:]
  bstack1lll1l1l11_opy_.append(bstack1ll11l1l11_opy_)
  return bstack1lll1l1l11_opy_
def bstack1lll111l1_opy_(args):
  if bstack1111ll1_opy_ (u"ࠬ࠳࡭ࠨౚ") in args and bstack1111ll1_opy_ (u"࠭ࡰࡥࡤࠪ౛") in args:
    return True
  return False
def run_on_browserstack(bstack1l1lll1l1_opy_=None, bstack1ll1l11l1l_opy_=None, bstack1l1ll1l11l_opy_=False):
  global CONFIG
  global bstack1l1lll1lll_opy_
  global bstack1l1lll1111_opy_
  global bstack1llll11l11_opy_
  global bstack11l11l1ll_opy_
  bstack11llllllll_opy_ = bstack1111ll1_opy_ (u"ࠧࠨ౜")
  bstack11l1l11ll_opy_(bstack111111lll_opy_, logger)
  if bstack1l1lll1l1_opy_ and isinstance(bstack1l1lll1l1_opy_, str):
    bstack1l1lll1l1_opy_ = eval(bstack1l1lll1l1_opy_)
  if bstack1l1lll1l1_opy_:
    CONFIG = bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨౝ")]
    bstack1l1lll1lll_opy_ = bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ౞")]
    bstack1l1lll1111_opy_ = bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ౟")]
    bstack11l11l1ll_opy_.bstack11llllll1_opy_(bstack1111ll1_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ౠ"), bstack1l1lll1111_opy_)
    bstack11llllllll_opy_ = bstack1111ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬౡ")
  bstack11l11l1ll_opy_.bstack11llllll1_opy_(bstack1111ll1_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨౢ"), uuid4().__str__())
  logger.debug(bstack1111ll1_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥ࠿ࠪౣ") + bstack11l11l1ll_opy_.get_property(bstack1111ll1_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ౤")))
  if not bstack1l1ll1l11l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1l1l111ll1_opy_)
      return
    if sys.argv[1] == bstack1111ll1_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬ౥") or sys.argv[1] == bstack1111ll1_opy_ (u"ࠪ࠱ࡻ࠭౦"):
      logger.info(bstack1111ll1_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀࠫ౧").format(__version__))
      return
    if sys.argv[1] == bstack1111ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ౨"):
      bstack1l11l11l1l_opy_()
      return
  args = sys.argv
  bstack1l11l1l11l_opy_()
  global bstack1llll1ll1l_opy_
  global bstack1111ll1ll_opy_
  global bstack111l1l11l_opy_
  global bstack1l11l1llll_opy_
  global bstack1l1ll1l111_opy_
  global bstack1l11l11lll_opy_
  global bstack1l1llllll1_opy_
  global bstack1l1l111l1l_opy_
  global bstack1ll1111l_opy_
  global bstack111lllll_opy_
  global bstack1lll111l1l_opy_
  bstack1111ll1ll_opy_ = len(CONFIG.get(bstack1111ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౩"), []))
  if not bstack11llllllll_opy_:
    if args[1] == bstack1111ll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ౪") or args[1] == bstack1111ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ౫"):
      bstack11llllllll_opy_ = bstack1111ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ౬")
      args = args[2:]
    elif args[1] == bstack1111ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ౭"):
      bstack11llllllll_opy_ = bstack1111ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ౮")
      args = args[2:]
    elif args[1] == bstack1111ll1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ౯"):
      bstack11llllllll_opy_ = bstack1111ll1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ౰")
      args = args[2:]
    elif args[1] == bstack1111ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ౱"):
      bstack11llllllll_opy_ = bstack1111ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ౲")
      args = args[2:]
    elif args[1] == bstack1111ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ౳"):
      bstack11llllllll_opy_ = bstack1111ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ౴")
      args = args[2:]
    elif args[1] == bstack1111ll1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ౵"):
      bstack11llllllll_opy_ = bstack1111ll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ౶")
      args = args[2:]
    else:
      if not bstack1111ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ౷") in CONFIG or str(CONFIG[bstack1111ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ౸")]).lower() in [bstack1111ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ౹"), bstack1111ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪ౺")]:
        bstack11llllllll_opy_ = bstack1111ll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ౻")
        args = args[1:]
      elif str(CONFIG[bstack1111ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ౼")]).lower() == bstack1111ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ౽"):
        bstack11llllllll_opy_ = bstack1111ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ౾")
        args = args[1:]
      elif str(CONFIG[bstack1111ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ౿")]).lower() == bstack1111ll1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧಀ"):
        bstack11llllllll_opy_ = bstack1111ll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨಁ")
        args = args[1:]
      elif str(CONFIG[bstack1111ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ಂ")]).lower() == bstack1111ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫಃ"):
        bstack11llllllll_opy_ = bstack1111ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ಄")
        args = args[1:]
      elif str(CONFIG[bstack1111ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩಅ")]).lower() == bstack1111ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧಆ"):
        bstack11llllllll_opy_ = bstack1111ll1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨಇ")
        args = args[1:]
      else:
        os.environ[bstack1111ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫಈ")] = bstack11llllllll_opy_
        bstack1l11l1l1l1_opy_(bstack1ll111ll1l_opy_)
  os.environ[bstack1111ll1_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫಉ")] = bstack11llllllll_opy_
  bstack1llll11l11_opy_ = bstack11llllllll_opy_
  global bstack1l1ll1111_opy_
  global bstack1ll111l1l1_opy_
  if bstack1l1lll1l1_opy_:
    try:
      os.environ[bstack1111ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ಊ")] = bstack11llllllll_opy_
      bstack1l11lll111_opy_(bstack1l1l1l1l1_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack111l1lll1_opy_.format(str(e)))
  global bstack1lll11l1l1_opy_
  global bstack1l111ll11l_opy_
  global bstack1111ll1l_opy_
  global bstack11111lll_opy_
  global bstack1l11ll1ll_opy_
  global bstack1lll11l11l_opy_
  global bstack111111111_opy_
  global bstack1ll1l1l1l1_opy_
  global bstack111l11ll_opy_
  global bstack1l111l1l1_opy_
  global bstack1ll1l1lll_opy_
  global bstack1l11l1l11_opy_
  global bstack1ll1ll11ll_opy_
  global bstack1l11l1ll1l_opy_
  global bstack1l1llll11_opy_
  global bstack1lll1l1l1_opy_
  global bstack1ll1ll1l_opy_
  global bstack1llll11111_opy_
  global bstack1l1lllll1_opy_
  global bstack1lll1lll1_opy_
  global bstack1ll1ll1l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll11l1l1_opy_ = webdriver.Remote.__init__
    bstack1l111ll11l_opy_ = WebDriver.quit
    bstack1l11l1l11_opy_ = WebDriver.close
    bstack1l1llll11_opy_ = WebDriver.get
    bstack1ll1ll1l11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1ll1111_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack11l11ll11_opy_
    bstack1ll111l1l1_opy_ = bstack11l11ll11_opy_()
  except Exception as e:
    pass
  try:
    global bstack11lllll1_opy_
    from QWeb.keywords import browser
    bstack11lllll1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1ll11111l_opy_(CONFIG) and bstack1l1l11ll_opy_():
    if bstack111l11ll1_opy_() < version.parse(bstack1lll11l111_opy_):
      logger.error(bstack1l1ll1l11_opy_.format(bstack111l11ll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1lll1l1l1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll1l1l11l_opy_.format(str(e)))
  if not CONFIG.get(bstack1111ll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧಋ"), False) and not bstack1l1lll1l1_opy_:
    logger.info(bstack1ll11l11l_opy_)
  if bstack11llllllll_opy_ != bstack1111ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ಌ") or (bstack11llllllll_opy_ == bstack1111ll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ಍") and not bstack1l1lll1l1_opy_):
    bstack1lllll1l1_opy_()
  if (bstack11llllllll_opy_ in [bstack1111ll1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧಎ"), bstack1111ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨಏ"), bstack1111ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫಐ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l111ll1l_opy_
        bstack1lll11l11l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l11l1111_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l11ll1ll_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l11l11l1_opy_ + str(e))
    except Exception as e:
      bstack111l11lll_opy_(e, bstack1l11l1111_opy_)
    if bstack11llllllll_opy_ != bstack1111ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ಑"):
      bstack1l1ll1ll1l_opy_()
    bstack1111ll1l_opy_ = Output.start_test
    bstack11111lll_opy_ = Output.end_test
    bstack111111111_opy_ = TestStatus.__init__
    bstack111l11ll_opy_ = pabot._run
    bstack1l111l1l1_opy_ = QueueItem.__init__
    bstack1ll1l1lll_opy_ = pabot._create_command_for_execution
    bstack1l1lllll1_opy_ = pabot._report_results
  if bstack11llllllll_opy_ == bstack1111ll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬಒ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack111l11lll_opy_(e, bstack1lll111l11_opy_)
    bstack1ll1ll11ll_opy_ = Runner.run_hook
    bstack1l11l1ll1l_opy_ = Step.run
  if bstack11llllllll_opy_ == bstack1111ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ಓ"):
    try:
      from _pytest.config import Config
      bstack1ll1ll1l_opy_ = Config.getoption
      from _pytest import runner
      bstack1llll11111_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l11l111ll_opy_)
    try:
      from pytest_bdd import reporting
      bstack1lll1lll1_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1111ll1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨಔ"))
  try:
    framework_name = bstack1111ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧಕ") if bstack11llllllll_opy_ in [bstack1111ll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨಖ"), bstack1111ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩಗ"), bstack1111ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬಘ")] else bstack1lllll1l11_opy_(bstack11llllllll_opy_)
    bstack111l11l1l_opy_ = {
      bstack1111ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ಙ"): bstack1111ll1_opy_ (u"࠭ࡻ࠱ࡿ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬಚ").format(framework_name) if bstack11llllllll_opy_ == bstack1111ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧಛ") and bstack1ll11l1lll_opy_() else framework_name,
      bstack1111ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬಜ"): bstack11llll111_opy_(framework_name),
      bstack1111ll1_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧಝ"): __version__,
      bstack1111ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫಞ"): bstack11llllllll_opy_
    }
    if bstack11llllllll_opy_ in bstack1l1lllll_opy_:
      if bstack1ll111ll_opy_ and bstack1111ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫಟ") in CONFIG and CONFIG[bstack1111ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬಠ")] == True:
        if bstack1111ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ಡ") in CONFIG:
          os.environ[bstack1111ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨಢ")] = os.getenv(bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩಣ"), json.dumps(CONFIG[bstack1111ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩತ")]))
          CONFIG[bstack1111ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪಥ")].pop(bstack1111ll1_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩದ"), None)
          CONFIG[bstack1111ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬಧ")].pop(bstack1111ll1_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫನ"), None)
        bstack111l11l1l_opy_[bstack1111ll1_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ಩")] = {
          bstack1111ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಪ"): bstack1111ll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫಫ"),
          bstack1111ll1_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫಬ"): str(bstack111l11ll1_opy_())
        }
    if bstack11llllllll_opy_ not in [bstack1111ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬಭ")]:
      bstack1l1l11ll11_opy_ = bstack1l1111l11_opy_.launch(CONFIG, bstack111l11l1l_opy_)
  except Exception as e:
    logger.debug(bstack1l1111l11l_opy_.format(bstack1111ll1_opy_ (u"࡚ࠬࡥࡴࡶࡋࡹࡧ࠭ಮ"), str(e)))
  if bstack11llllllll_opy_ == bstack1111ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ಯ"):
    bstack111l1l11l_opy_ = True
    if bstack1l1lll1l1_opy_ and bstack1l1ll1l11l_opy_:
      bstack1l11l11lll_opy_ = CONFIG.get(bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫರ"), {}).get(bstack1111ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪಱ"))
      bstack1lll1l1ll_opy_(bstack11l11lll_opy_)
    elif bstack1l1lll1l1_opy_:
      bstack1l11l11lll_opy_ = CONFIG.get(bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ಲ"), {}).get(bstack1111ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬಳ"))
      global bstack111lll1ll_opy_
      try:
        if bstack1lll111l1_opy_(bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ಴")]) and multiprocessing.current_process().name == bstack1111ll1_opy_ (u"ࠬ࠶ࠧವ"):
          bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩಶ")].remove(bstack1111ll1_opy_ (u"ࠧ࠮࡯ࠪಷ"))
          bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫಸ")].remove(bstack1111ll1_opy_ (u"ࠩࡳࡨࡧ࠭ಹ"))
          bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭಺")] = bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ಻")][0]
          with open(bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ಼")], bstack1111ll1_opy_ (u"࠭ࡲࠨಽ")) as f:
            bstack1l111lll11_opy_ = f.read()
          bstack11l1l11l_opy_ = bstack1111ll1_opy_ (u"ࠢࠣࠤࡩࡶࡴࡳࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡥ࡭ࠣ࡭ࡲࡶ࡯ࡳࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡁࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࠫࡿࢂ࠯࠻ࠡࡨࡵࡳࡲࠦࡰࡥࡤࠣ࡭ࡲࡶ࡯ࡳࡶࠣࡔࡩࡨ࠻ࠡࡱࡪࡣࡩࡨࠠ࠾ࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࡶࡪࡧ࡫࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡥࡧࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯࠭ࡹࡥ࡭ࡨ࠯ࠤࡦࡸࡧ࠭ࠢࡷࡩࡲࡶ࡯ࡳࡣࡵࡽࠥࡃࠠ࠱ࠫ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡶࡾࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡢࡴࡪࠤࡂࠦࡳࡵࡴࠫ࡭ࡳࡺࠨࡢࡴࡪ࠭࠰࠷࠰ࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡦࡺࡦࡩࡵࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡥࡸࠦࡥ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡳࡥࡸࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡵࡧࡠࡦࡥࠬࡸ࡫࡬ࡧ࠮ࡤࡶ࡬࠲ࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࠡ࠿ࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࡶࡪࡧ࡫ࠡ࠿ࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠮ࠩ࠯ࡵࡨࡸࡤࡺࡲࡢࡥࡨࠬ࠮ࡢ࡮ࠣࠤࠥಾ").format(str(bstack1l1lll1l1_opy_))
          bstack1llll111l1_opy_ = bstack11l1l11l_opy_ + bstack1l111lll11_opy_
          bstack111111l1_opy_ = bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫಿ")] + bstack1111ll1_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡸࡪࡳࡰ࠯ࡲࡼࠫೀ")
          with open(bstack111111l1_opy_, bstack1111ll1_opy_ (u"ࠪࡻࠬು")):
            pass
          with open(bstack111111l1_opy_, bstack1111ll1_opy_ (u"ࠦࡼ࠱ࠢೂ")) as f:
            f.write(bstack1llll111l1_opy_)
          import subprocess
          bstack1llll1llll_opy_ = subprocess.run([bstack1111ll1_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧೃ"), bstack111111l1_opy_])
          if os.path.exists(bstack111111l1_opy_):
            os.unlink(bstack111111l1_opy_)
          os._exit(bstack1llll1llll_opy_.returncode)
        else:
          if bstack1lll111l1_opy_(bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩೄ")]):
            bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ೅")].remove(bstack1111ll1_opy_ (u"ࠨ࠯ࡰࠫೆ"))
            bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬೇ")].remove(bstack1111ll1_opy_ (u"ࠪࡴࡩࡨࠧೈ"))
            bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ೉")] = bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨೊ")][0]
          bstack1lll1l1ll_opy_(bstack11l11lll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩೋ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1111ll1_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩೌ")] = bstack1111ll1_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡ್ࠪ")
          mod_globals[bstack1111ll1_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫ೎")] = os.path.abspath(bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭೏")])
          exec(open(bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ೐")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1111ll1_opy_ (u"ࠬࡉࡡࡶࡩ࡫ࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠬ೑").format(str(e)))
          for driver in bstack111lll1ll_opy_:
            bstack1ll1l11l1l_opy_.append({
              bstack1111ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ೒"): bstack1l1lll1l1_opy_[bstack1111ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ೓")],
              bstack1111ll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ೔"): str(e),
              bstack1111ll1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨೕ"): multiprocessing.current_process().name
            })
            bstack1ll1l1ll1_opy_(driver, bstack1111ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪೖ"), bstack1111ll1_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢ೗") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack111lll1ll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l1lll1111_opy_, CONFIG, logger)
      bstack1l1ll11ll1_opy_()
      bstack1lllll111l_opy_()
      bstack1llll11l_opy_ = {
        bstack1111ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ೘"): args[0],
        bstack1111ll1_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭೙"): CONFIG,
        bstack1111ll1_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ೚"): bstack1l1lll1lll_opy_,
        bstack1111ll1_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ೛"): bstack1l1lll1111_opy_
      }
      percy.bstack1ll1l1111_opy_()
      if bstack1111ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ೜") in CONFIG:
        bstack11ll111l_opy_ = []
        manager = multiprocessing.Manager()
        bstack111l1ll1_opy_ = manager.list()
        if bstack1lll111l1_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1111ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ೝ")]):
            if index == 0:
              bstack1llll11l_opy_[bstack1111ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧೞ")] = args
            bstack11ll111l_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1llll11l_opy_, bstack111l1ll1_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1111ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ೟")]):
            bstack11ll111l_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1llll11l_opy_, bstack111l1ll1_opy_)))
        for t in bstack11ll111l_opy_:
          t.start()
        for t in bstack11ll111l_opy_:
          t.join()
        bstack1l1l111l1l_opy_ = list(bstack111l1ll1_opy_)
      else:
        if bstack1lll111l1_opy_(args):
          bstack1llll11l_opy_[bstack1111ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩೠ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1llll11l_opy_,))
          test.start()
          test.join()
        else:
          bstack1lll1l1ll_opy_(bstack11l11lll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1111ll1_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩೡ")] = bstack1111ll1_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪೢ")
          mod_globals[bstack1111ll1_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫೣ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11llllllll_opy_ == bstack1111ll1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ೤") or bstack11llllllll_opy_ == bstack1111ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ೥"):
    percy.init(bstack1l1lll1111_opy_, CONFIG, logger)
    percy.bstack1ll1l1111_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack111l11lll_opy_(e, bstack1l11l1111_opy_)
    bstack1l1ll11ll1_opy_()
    bstack1lll1l1ll_opy_(bstack1l1l1l11l1_opy_)
    if bstack1ll111ll_opy_:
      bstack1llllll111_opy_(bstack1l1l1l11l1_opy_, args)
      if bstack1111ll1_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ೦") in args:
        i = args.index(bstack1111ll1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ೧"))
        args.pop(i)
        args.pop(i)
      if bstack1111ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ೨") not in CONFIG:
        CONFIG[bstack1111ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ೩")] = [{}]
        bstack1111ll1ll_opy_ = 1
      if bstack1llll1ll1l_opy_ == 0:
        bstack1llll1ll1l_opy_ = 1
      args.insert(0, str(bstack1llll1ll1l_opy_))
      args.insert(0, str(bstack1111ll1_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ೪")))
    if bstack1l1111l11_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l11ll111l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11l11l11_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1111ll1_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥ೫"),
        ).parse_args(bstack1l11ll111l_opy_)
        bstack11l11llll_opy_ = args.index(bstack1l11ll111l_opy_[0]) if len(bstack1l11ll111l_opy_) > 0 else len(args)
        args.insert(bstack11l11llll_opy_, str(bstack1111ll1_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨ೬")))
        args.insert(bstack11l11llll_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1111ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩ೭"))))
        if bstack1l11l1ll11_opy_(os.environ.get(bstack1111ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ೮"))) and str(os.environ.get(bstack1111ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫ೯"), bstack1111ll1_opy_ (u"ࠨࡰࡸࡰࡱ࠭೰"))) != bstack1111ll1_opy_ (u"ࠩࡱࡹࡱࡲࠧೱ"):
          for bstack1l1ll1llll_opy_ in bstack11l11l11_opy_:
            args.remove(bstack1l1ll1llll_opy_)
          bstack111l1l1l_opy_ = os.environ.get(bstack1111ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧೲ")).split(bstack1111ll1_opy_ (u"ࠫ࠱࠭ೳ"))
          for bstack111ll1ll_opy_ in bstack111l1l1l_opy_:
            args.append(bstack111ll1ll_opy_)
      except Exception as e:
        logger.error(bstack1111ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡹࡺࡡࡤࡪ࡬ࡲ࡬ࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࠣ೴").format(e))
    pabot.main(args)
  elif bstack11llllllll_opy_ == bstack1111ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ೵"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack111l11lll_opy_(e, bstack1l11l1111_opy_)
    for a in args:
      if bstack1111ll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭೶") in a:
        bstack1l1ll1l111_opy_ = int(a.split(bstack1111ll1_opy_ (u"ࠨ࠼ࠪ೷"))[1])
      if bstack1111ll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭೸") in a:
        bstack1l11l11lll_opy_ = str(a.split(bstack1111ll1_opy_ (u"ࠪ࠾ࠬ೹"))[1])
      if bstack1111ll1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫ೺") in a:
        bstack1l1llllll1_opy_ = str(a.split(bstack1111ll1_opy_ (u"ࠬࡀࠧ೻"))[1])
    bstack1l111lllll_opy_ = None
    if bstack1111ll1_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬ೼") in args:
      i = args.index(bstack1111ll1_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭೽"))
      args.pop(i)
      bstack1l111lllll_opy_ = args.pop(i)
    if bstack1l111lllll_opy_ is not None:
      global bstack1lllll1ll1_opy_
      bstack1lllll1ll1_opy_ = bstack1l111lllll_opy_
    bstack1lll1l1ll_opy_(bstack1l1l1l11l1_opy_)
    run_cli(args)
    if bstack1111ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬ೾") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1l1l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll1l11l1l_opy_.append(bstack11l1l1l1_opy_)
  elif bstack11llllllll_opy_ == bstack1111ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ೿"):
    percy.init(bstack1l1lll1111_opy_, CONFIG, logger)
    percy.bstack1ll1l1111_opy_()
    bstack11l1111l1_opy_ = bstack11llll1l_opy_(args, logger, CONFIG, bstack1ll111ll_opy_)
    bstack11l1111l1_opy_.bstack11lll1l1_opy_()
    bstack1l1ll11ll1_opy_()
    bstack1l11l1llll_opy_ = True
    bstack111lllll_opy_ = bstack11l1111l1_opy_.bstack1l11l1l1l_opy_()
    bstack11l1111l1_opy_.bstack1llll11l_opy_(bstack1l1lll1l1l_opy_)
    bstack1lll1l1ll1_opy_ = bstack11l1111l1_opy_.bstack11lllll1ll_opy_(bstack11111lll1_opy_, {
      bstack1111ll1_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫഀ"): bstack1l1lll1lll_opy_,
      bstack1111ll1_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ഁ"): bstack1l1lll1111_opy_,
      bstack1111ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨം"): bstack1ll111ll_opy_
    })
    try:
      bstack1ll1ll1ll1_opy_, bstack1l11111l1l_opy_ = map(list, zip(*bstack1lll1l1ll1_opy_))
      bstack1ll1111l_opy_ = bstack1ll1ll1ll1_opy_[0]
      for status_code in bstack1l11111l1l_opy_:
        if status_code != 0:
          bstack1lll111l1l_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1111ll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡦࡴࡵࡳࡷࡹࠠࡢࡰࡧࠤࡸࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠰ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠺ࠡࡽࢀࠦഃ").format(str(e)))
  elif bstack11llllllll_opy_ == bstack1111ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧഄ"):
    try:
      from behave.__main__ import main as bstack11l11l11l_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack111l11lll_opy_(e, bstack1lll111l11_opy_)
    bstack1l1ll11ll1_opy_()
    bstack1l11l1llll_opy_ = True
    bstack1l111ll1_opy_ = 1
    if bstack1111ll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨഅ") in CONFIG:
      bstack1l111ll1_opy_ = CONFIG[bstack1111ll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩആ")]
    if bstack1111ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ഇ") in CONFIG:
      bstack11ll1l1l_opy_ = int(bstack1l111ll1_opy_) * int(len(CONFIG[bstack1111ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧഈ")]))
    else:
      bstack11ll1l1l_opy_ = int(bstack1l111ll1_opy_)
    config = Configuration(args)
    bstack1lll1ll1l1_opy_ = config.paths
    if len(bstack1lll1ll1l1_opy_) == 0:
      import glob
      pattern = bstack1111ll1_opy_ (u"ࠬ࠰ࠪ࠰ࠬ࠱ࡪࡪࡧࡴࡶࡴࡨࠫഉ")
      bstack1ll1l1l1l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1ll1l1l1l_opy_)
      config = Configuration(args)
      bstack1lll1ll1l1_opy_ = config.paths
    bstack1lllllll11_opy_ = [os.path.normpath(item) for item in bstack1lll1ll1l1_opy_]
    bstack111lll1l1_opy_ = [os.path.normpath(item) for item in args]
    bstack1lll11lll1_opy_ = [item for item in bstack111lll1l1_opy_ if item not in bstack1lllllll11_opy_]
    import platform as pf
    if pf.system().lower() == bstack1111ll1_opy_ (u"࠭ࡷࡪࡰࡧࡳࡼࡹࠧഊ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1lllllll11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1lllll11ll_opy_)))
                    for bstack1lllll11ll_opy_ in bstack1lllllll11_opy_]
    bstack111111l1l_opy_ = []
    for spec in bstack1lllllll11_opy_:
      bstack11l11111l_opy_ = []
      bstack11l11111l_opy_ += bstack1lll11lll1_opy_
      bstack11l11111l_opy_.append(spec)
      bstack111111l1l_opy_.append(bstack11l11111l_opy_)
    execution_items = []
    for bstack11l11111l_opy_ in bstack111111l1l_opy_:
      if bstack1111ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪഋ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1111ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫഌ")]):
          item = {}
          item[bstack1111ll1_opy_ (u"ࠩࡤࡶ࡬࠭഍")] = bstack1111ll1_opy_ (u"ࠪࠤࠬഎ").join(bstack11l11111l_opy_)
          item[bstack1111ll1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪഏ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1111ll1_opy_ (u"ࠬࡧࡲࡨࠩഐ")] = bstack1111ll1_opy_ (u"࠭ࠠࠨ഑").join(bstack11l11111l_opy_)
        item[bstack1111ll1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ഒ")] = 0
        execution_items.append(item)
    bstack1l1llll111_opy_ = bstack1lll11ll_opy_(execution_items, bstack11ll1l1l_opy_)
    for execution_item in bstack1l1llll111_opy_:
      bstack11ll111l_opy_ = []
      for item in execution_item:
        bstack11ll111l_opy_.append(bstack1lllll11l1_opy_(name=str(item[bstack1111ll1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧഓ")]),
                                             target=bstack1l111lll1l_opy_,
                                             args=(item[bstack1111ll1_opy_ (u"ࠩࡤࡶ࡬࠭ഔ")],)))
      for t in bstack11ll111l_opy_:
        t.start()
      for t in bstack11ll111l_opy_:
        t.join()
  else:
    bstack1l11l1l1l1_opy_(bstack1ll111ll1l_opy_)
  if not bstack1l1lll1l1_opy_:
    bstack1ll11ll1l_opy_()
  bstack1111111ll_opy_.bstack1111l111l_opy_()
def browserstack_initialize(bstack1lll1ll1_opy_=None):
  run_on_browserstack(bstack1lll1ll1_opy_, None, True)
def bstack1ll11ll1l_opy_():
  global CONFIG
  global bstack1llll11l11_opy_
  global bstack1lll111l1l_opy_
  global bstack11l1lll11_opy_
  global bstack11l11l1ll_opy_
  bstack1l1111l11_opy_.stop()
  bstack11lll1lll_opy_.bstack1l1lllllll_opy_()
  [bstack1l1ll111_opy_, bstack1l1l1l1l11_opy_] = get_build_link()
  if bstack1l1ll111_opy_ is not None and bstack1l11l1111l_opy_() != -1:
    sessions = bstack1llllll11l_opy_(bstack1l1ll111_opy_)
    bstack1ll1ll1lll_opy_(sessions, bstack1l1l1l1l11_opy_)
  if bstack1llll11l11_opy_ == bstack1111ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪക") and bstack1lll111l1l_opy_ != 0:
    sys.exit(bstack1lll111l1l_opy_)
  if bstack1llll11l11_opy_ == bstack1111ll1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫഖ") and bstack11l1lll11_opy_ != 0:
    sys.exit(bstack11l1lll11_opy_)
def bstack1lllll1l11_opy_(bstack1l1ll111ll_opy_):
  if bstack1l1ll111ll_opy_:
    return bstack1l1ll111ll_opy_.capitalize()
  else:
    return bstack1111ll1_opy_ (u"ࠬ࠭ഗ")
def bstack1ll1l111_opy_(bstack1l1l111l_opy_):
  if bstack1111ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫഘ") in bstack1l1l111l_opy_ and bstack1l1l111l_opy_[bstack1111ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬങ")] != bstack1111ll1_opy_ (u"ࠨࠩച"):
    return bstack1l1l111l_opy_[bstack1111ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧഛ")]
  else:
    bstack1lll11ll11_opy_ = bstack1111ll1_opy_ (u"ࠥࠦജ")
    if bstack1111ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫഝ") in bstack1l1l111l_opy_ and bstack1l1l111l_opy_[bstack1111ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬഞ")] != None:
      bstack1lll11ll11_opy_ += bstack1l1l111l_opy_[bstack1111ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ട")] + bstack1111ll1_opy_ (u"ࠢ࠭ࠢࠥഠ")
      if bstack1l1l111l_opy_[bstack1111ll1_opy_ (u"ࠨࡱࡶࠫഡ")] == bstack1111ll1_opy_ (u"ࠤ࡬ࡳࡸࠨഢ"):
        bstack1lll11ll11_opy_ += bstack1111ll1_opy_ (u"ࠥ࡭ࡔ࡙ࠠࠣണ")
      bstack1lll11ll11_opy_ += (bstack1l1l111l_opy_[bstack1111ll1_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨത")] or bstack1111ll1_opy_ (u"ࠬ࠭ഥ"))
      return bstack1lll11ll11_opy_
    else:
      bstack1lll11ll11_opy_ += bstack1lllll1l11_opy_(bstack1l1l111l_opy_[bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧദ")]) + bstack1111ll1_opy_ (u"ࠢࠡࠤധ") + (
              bstack1l1l111l_opy_[bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪന")] or bstack1111ll1_opy_ (u"ࠩࠪഩ")) + bstack1111ll1_opy_ (u"ࠥ࠰ࠥࠨപ")
      if bstack1l1l111l_opy_[bstack1111ll1_opy_ (u"ࠫࡴࡹࠧഫ")] == bstack1111ll1_opy_ (u"ࠧ࡝ࡩ࡯ࡦࡲࡻࡸࠨബ"):
        bstack1lll11ll11_opy_ += bstack1111ll1_opy_ (u"ࠨࡗࡪࡰࠣࠦഭ")
      bstack1lll11ll11_opy_ += bstack1l1l111l_opy_[bstack1111ll1_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫമ")] or bstack1111ll1_opy_ (u"ࠨࠩയ")
      return bstack1lll11ll11_opy_
def bstack1l11ll1l1_opy_(bstack1l11llllll_opy_):
  if bstack1l11llllll_opy_ == bstack1111ll1_opy_ (u"ࠤࡧࡳࡳ࡫ࠢര"):
    return bstack1111ll1_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭റ")
  elif bstack1l11llllll_opy_ == bstack1111ll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦല"):
    return bstack1111ll1_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡊࡦ࡯࡬ࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨള")
  elif bstack1l11llllll_opy_ == bstack1111ll1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨഴ"):
    return bstack1111ll1_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡓࡥࡸࡹࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧവ")
  elif bstack1l11llllll_opy_ == bstack1111ll1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢശ"):
    return bstack1111ll1_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡆࡴࡵࡳࡷࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫഷ")
  elif bstack1l11llllll_opy_ == bstack1111ll1_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦസ"):
    return bstack1111ll1_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࠣࡦࡧࡤ࠷࠷࠼࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࠥࡨࡩࡦ࠹࠲࠷ࠤࡁࡘ࡮ࡳࡥࡰࡷࡷࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩഹ")
  elif bstack1l11llllll_opy_ == bstack1111ll1_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠨഺ"):
    return bstack1111ll1_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࡔࡸࡲࡳ࡯࡮ࡨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄ഻ࠧ")
  else:
    return bstack1111ll1_opy_ (u"ࠧ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁ഼ࠫ") + bstack1lllll1l11_opy_(
      bstack1l11llllll_opy_) + bstack1111ll1_opy_ (u"ࠨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧഽ")
def bstack1l1ll11l1l_opy_(session):
  return bstack1111ll1_opy_ (u"ࠩ࠿ࡸࡷࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡲࡰࡹࠥࡂࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠦࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠧࡄ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࡽࢀࠦࠥࡺࡡࡳࡩࡨࡸࡂࠨ࡟ࡣ࡮ࡤࡲࡰࠨ࠾ࡼࡿ࠿࠳ࡦࡄ࠼࠰ࡶࡧࡂࢀࢃࡻࡾ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀ࠴ࡺࡲ࠿ࠩാ").format(
    session[bstack1111ll1_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧി")], bstack1ll1l111_opy_(session), bstack1l11ll1l1_opy_(session[bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠪീ")]),
    bstack1l11ll1l1_opy_(session[bstack1111ll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬു")]),
    bstack1lllll1l11_opy_(session[bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧൂ")] or session[bstack1111ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧൃ")] or bstack1111ll1_opy_ (u"ࠨࠩൄ")) + bstack1111ll1_opy_ (u"ࠤࠣࠦ൅") + (session[bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬെ")] or bstack1111ll1_opy_ (u"ࠫࠬേ")),
    session[bstack1111ll1_opy_ (u"ࠬࡵࡳࠨൈ")] + bstack1111ll1_opy_ (u"ࠨࠠࠣ൉") + session[bstack1111ll1_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫൊ")], session[bstack1111ll1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪോ")] or bstack1111ll1_opy_ (u"ࠩࠪൌ"),
    session[bstack1111ll1_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺ്ࠧ")] if session[bstack1111ll1_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨൎ")] else bstack1111ll1_opy_ (u"ࠬ࠭൏"))
def bstack1ll1ll1lll_opy_(sessions, bstack1l1l1l1l11_opy_):
  try:
    bstack1l1l1lllll_opy_ = bstack1111ll1_opy_ (u"ࠨࠢ൐")
    if not os.path.exists(bstack1lll1l1lll_opy_):
      os.mkdir(bstack1lll1l1lll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1111ll1_opy_ (u"ࠧࡢࡵࡶࡩࡹࡹ࠯ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬ൑")), bstack1111ll1_opy_ (u"ࠨࡴࠪ൒")) as f:
      bstack1l1l1lllll_opy_ = f.read()
    bstack1l1l1lllll_opy_ = bstack1l1l1lllll_opy_.replace(bstack1111ll1_opy_ (u"ࠩࡾࠩࡗࡋࡓࡖࡎࡗࡗࡤࡉࡏࡖࡐࡗࠩࢂ࠭൓"), str(len(sessions)))
    bstack1l1l1lllll_opy_ = bstack1l1l1lllll_opy_.replace(bstack1111ll1_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠦࡿࠪൔ"), bstack1l1l1l1l11_opy_)
    bstack1l1l1lllll_opy_ = bstack1l1l1lllll_opy_.replace(bstack1111ll1_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇࠨࢁࠬൕ"),
                                              sessions[0].get(bstack1111ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡧ࡭ࡦࠩൖ")) if sessions[0] else bstack1111ll1_opy_ (u"࠭ࠧൗ"))
    with open(os.path.join(bstack1lll1l1lll_opy_, bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫ൘")), bstack1111ll1_opy_ (u"ࠨࡹࠪ൙")) as stream:
      stream.write(bstack1l1l1lllll_opy_.split(bstack1111ll1_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭൚"))[0])
      for session in sessions:
        stream.write(bstack1l1ll11l1l_opy_(session))
      stream.write(bstack1l1l1lllll_opy_.split(bstack1111ll1_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧ൛"))[1])
    logger.info(bstack1111ll1_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡢࡶ࡫࡯ࡨࠥࡧࡲࡵ࡫ࡩࡥࡨࡺࡳࠡࡣࡷࠤࢀࢃࠧ൜").format(bstack1lll1l1lll_opy_));
  except Exception as e:
    logger.debug(bstack111l11l1_opy_.format(str(e)))
def bstack1llllll11l_opy_(bstack1l1ll111_opy_):
  global CONFIG
  try:
    host = bstack1111ll1_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨ൝") if bstack1111ll1_opy_ (u"࠭ࡡࡱࡲࠪ൞") in CONFIG else bstack1111ll1_opy_ (u"ࠧࡢࡲ࡬ࠫൟ")
    user = CONFIG[bstack1111ll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪൠ")]
    key = CONFIG[bstack1111ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬൡ")]
    bstack11l1l11l1_opy_ = bstack1111ll1_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩൢ") if bstack1111ll1_opy_ (u"ࠫࡦࡶࡰࠨൣ") in CONFIG else bstack1111ll1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ൤")
    url = bstack1111ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠴ࡪࡴࡱࡱࠫ൥").format(user, key, host, bstack11l1l11l1_opy_,
                                                                                bstack1l1ll111_opy_)
    headers = {
      bstack1111ll1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭൦"): bstack1111ll1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ൧"),
    }
    proxies = bstack1lll1lll_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1111ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ൨")], response.json()))
  except Exception as e:
    logger.debug(bstack1l11llll1_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack11ll1111_opy_
  try:
    if bstack1111ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭൩") in CONFIG:
      host = bstack1111ll1_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧ൪") if bstack1111ll1_opy_ (u"ࠬࡧࡰࡱࠩ൫") in CONFIG else bstack1111ll1_opy_ (u"࠭ࡡࡱ࡫ࠪ൬")
      user = CONFIG[bstack1111ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ൭")]
      key = CONFIG[bstack1111ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ൮")]
      bstack11l1l11l1_opy_ = bstack1111ll1_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ൯") if bstack1111ll1_opy_ (u"ࠪࡥࡵࡶࠧ൰") in CONFIG else bstack1111ll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭൱")
      url = bstack1111ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠬ൲").format(user, key, host, bstack11l1l11l1_opy_)
      headers = {
        bstack1111ll1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬ൳"): bstack1111ll1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ൴"),
      }
      if bstack1111ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ൵") in CONFIG:
        params = {bstack1111ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ൶"): CONFIG[bstack1111ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭൷")], bstack1111ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ൸"): CONFIG[bstack1111ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ൹")]}
      else:
        params = {bstack1111ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫൺ"): CONFIG[bstack1111ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪൻ")]}
      proxies = bstack1lll1lll_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1ll1l1111l_opy_ = response.json()[0][bstack1111ll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡨࡵࡪ࡮ࡧࠫർ")]
        if bstack1ll1l1111l_opy_:
          bstack1l1l1l1l11_opy_ = bstack1ll1l1111l_opy_[bstack1111ll1_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ൽ")].split(bstack1111ll1_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥ࠰ࡦࡺ࡯࡬ࡥࠩൾ"))[0] + bstack1111ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡶ࠳ࠬൿ") + bstack1ll1l1111l_opy_[
            bstack1111ll1_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ඀")]
          logger.info(bstack1llll111l_opy_.format(bstack1l1l1l1l11_opy_))
          bstack11ll1111_opy_ = bstack1ll1l1111l_opy_[bstack1111ll1_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩඁ")]
          bstack1lll111lll_opy_ = CONFIG[bstack1111ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪං")]
          if bstack1111ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪඃ") in CONFIG:
            bstack1lll111lll_opy_ += bstack1111ll1_opy_ (u"ࠩࠣࠫ඄") + CONFIG[bstack1111ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬඅ")]
          if bstack1lll111lll_opy_ != bstack1ll1l1111l_opy_[bstack1111ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩආ")]:
            logger.debug(bstack1lll1llll_opy_.format(bstack1ll1l1111l_opy_[bstack1111ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪඇ")], bstack1lll111lll_opy_))
          return [bstack1ll1l1111l_opy_[bstack1111ll1_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩඈ")], bstack1l1l1l1l11_opy_]
    else:
      logger.warn(bstack1111111l_opy_)
  except Exception as e:
    logger.debug(bstack111l1ll1l_opy_.format(str(e)))
  return [None, None]
def bstack1111l1l11_opy_(url, bstack1l1111l1l_opy_=False):
  global CONFIG
  global bstack1l111lll1_opy_
  if not bstack1l111lll1_opy_:
    hostname = bstack1l111llll_opy_(url)
    is_private = bstack11llllll1l_opy_(hostname)
    if (bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫඉ") in CONFIG and not bstack1l11l1ll11_opy_(CONFIG[bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬඊ")])) and (is_private or bstack1l1111l1l_opy_):
      bstack1l111lll1_opy_ = hostname
def bstack1l111llll_opy_(url):
  return urlparse(url).hostname
def bstack11llllll1l_opy_(hostname):
  for bstack1l11l11l11_opy_ in bstack1lll111111_opy_:
    regex = re.compile(bstack1l11l11l11_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1111lll1_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1l1ll1l111_opy_
  bstack1l11lll1ll_opy_ = not (bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭උ"), None) and bstack1llll1l11_opy_(
          threading.current_thread(), bstack1111ll1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩඌ"), None))
  bstack1l1ll1lll1_opy_ = getattr(driver, bstack1111ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫඍ"), None) != True
  if not bstack11l11l111_opy_.bstack1l1l1111_opy_(CONFIG, bstack1l1ll1l111_opy_) or (bstack1l1ll1lll1_opy_ and bstack1l11lll1ll_opy_):
    logger.warning(bstack1111ll1_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣඎ"))
    return {}
  try:
    logger.debug(bstack1111ll1_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪඏ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l1lll1l_opy_.bstack1l11l111_opy_)
    return results
  except Exception:
    logger.error(bstack1111ll1_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡼ࡫ࡲࡦࠢࡩࡳࡺࡴࡤ࠯ࠤඐ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1l1ll1l111_opy_
  bstack1l11lll1ll_opy_ = not (bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬඑ"), None) and bstack1llll1l11_opy_(
          threading.current_thread(), bstack1111ll1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨඒ"), None))
  bstack1l1ll1lll1_opy_ = getattr(driver, bstack1111ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪඓ"), None) != True
  if not bstack11l11l111_opy_.bstack1l1l1111_opy_(CONFIG, bstack1l1ll1l111_opy_) or (bstack1l1ll1lll1_opy_ and bstack1l11lll1ll_opy_):
    logger.warning(bstack1111ll1_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿ࠮ࠣඔ"))
    return {}
  try:
    logger.debug(bstack1111ll1_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻࠪඕ"))
    logger.debug(perform_scan(driver))
    bstack1lll1ll11l_opy_ = driver.execute_async_script(bstack1l1lll1l_opy_.bstack1ll11ll1l1_opy_)
    return bstack1lll1ll11l_opy_
  except Exception:
    logger.error(bstack1111ll1_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢඖ"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1l1ll1l111_opy_
  bstack1l11lll1ll_opy_ = not (bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ඗"), None) and bstack1llll1l11_opy_(
          threading.current_thread(), bstack1111ll1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ඘"), None))
  bstack1l1ll1lll1_opy_ = getattr(driver, bstack1111ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ඙"), None) != True
  if not bstack11l11l111_opy_.bstack1l1l1111_opy_(CONFIG, bstack1l1ll1l111_opy_) or (bstack1l1ll1lll1_opy_ and bstack1l11lll1ll_opy_):
    logger.warning(bstack1111ll1_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡹࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱ࠲ࠧක"))
    return {}
  try:
    bstack11ll1l11_opy_ = driver.execute_async_script(bstack1l1lll1l_opy_.perform_scan, {bstack1111ll1_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫඛ"): kwargs.get(bstack1111ll1_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤࡩ࡯࡮࡯ࡤࡲࡩ࠭ග"), None) or bstack1111ll1_opy_ (u"࠭ࠧඝ")})
    return bstack11ll1l11_opy_
  except Exception:
    logger.error(bstack1111ll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠨඞ"))
    return {}