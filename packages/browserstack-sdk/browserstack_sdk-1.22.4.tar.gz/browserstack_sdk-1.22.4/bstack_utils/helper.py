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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack111ll1l111_opy_, bstack1lll111111_opy_, bstack1lll11l1_opy_, bstack1l1l1l111_opy_,
                                    bstack111ll11lll_opy_, bstack111l1lll11_opy_, bstack111ll111l1_opy_, bstack111ll11ll1_opy_)
from bstack_utils.messages import bstack1llll1l1l1_opy_, bstack1ll1l1l11l_opy_
from bstack_utils.proxy import bstack1lll1lll_opy_, bstack1lll11llll_opy_
bstack11l11l1ll_opy_ = Config.bstack1111l1lll_opy_()
logger = logging.getLogger(__name__)
def bstack11l1111l11_opy_(config):
    return config[bstack1111ll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧኲ")]
def bstack11l11l1ll1_opy_(config):
    return config[bstack1111ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩኳ")]
def bstack111llllll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111l11l1l1_opy_(obj):
    values = []
    bstack11111l111l_opy_ = re.compile(bstack1111ll1_opy_ (u"ࡲࠣࡠࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࡜ࡥ࠭ࠧࠦኴ"), re.I)
    for key in obj.keys():
        if bstack11111l111l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l111l11_opy_(config):
    tags = []
    tags.extend(bstack111l11l1l1_opy_(os.environ))
    tags.extend(bstack111l11l1l1_opy_(config))
    return tags
def bstack11111l1l1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111111l11l_opy_(bstack1111l11l11_opy_):
    if not bstack1111l11l11_opy_:
        return bstack1111ll1_opy_ (u"ࠨࠩኵ")
    return bstack1111ll1_opy_ (u"ࠤࡾࢁࠥ࠮ࡻࡾࠫࠥ኶").format(bstack1111l11l11_opy_.name, bstack1111l11l11_opy_.email)
def bstack11l11l11l1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11111l1l11_opy_ = repo.common_dir
        info = {
            bstack1111ll1_opy_ (u"ࠥࡷ࡭ࡧࠢ኷"): repo.head.commit.hexsha,
            bstack1111ll1_opy_ (u"ࠦࡸ࡮࡯ࡳࡶࡢࡷ࡭ࡧࠢኸ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1111ll1_opy_ (u"ࠧࡨࡲࡢࡰࡦ࡬ࠧኹ"): repo.active_branch.name,
            bstack1111ll1_opy_ (u"ࠨࡴࡢࡩࠥኺ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1111ll1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࠥኻ"): bstack111111l11l_opy_(repo.head.commit.committer),
            bstack1111ll1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࡣࡩࡧࡴࡦࠤኼ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1111ll1_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࠤኽ"): bstack111111l11l_opy_(repo.head.commit.author),
            bstack1111ll1_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡢࡨࡦࡺࡥࠣኾ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1111ll1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧ኿"): repo.head.commit.message,
            bstack1111ll1_opy_ (u"ࠧࡸ࡯ࡰࡶࠥዀ"): repo.git.rev_parse(bstack1111ll1_opy_ (u"ࠨ࠭࠮ࡵ࡫ࡳࡼ࠳ࡴࡰࡲ࡯ࡩࡻ࡫࡬ࠣ዁")),
            bstack1111ll1_opy_ (u"ࠢࡤࡱࡰࡱࡴࡴ࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣዂ"): bstack11111l1l11_opy_,
            bstack1111ll1_opy_ (u"ࠣࡹࡲࡶࡰࡺࡲࡦࡧࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦዃ"): subprocess.check_output([bstack1111ll1_opy_ (u"ࠤࡪ࡭ࡹࠨዄ"), bstack1111ll1_opy_ (u"ࠥࡶࡪࡼ࠭ࡱࡣࡵࡷࡪࠨዅ"), bstack1111ll1_opy_ (u"ࠦ࠲࠳ࡧࡪࡶ࠰ࡧࡴࡳ࡭ࡰࡰ࠰ࡨ࡮ࡸࠢ዆")]).strip().decode(
                bstack1111ll1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ዇")),
            bstack1111ll1_opy_ (u"ࠨ࡬ࡢࡵࡷࡣࡹࡧࡧࠣወ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1111ll1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡳࡠࡵ࡬ࡲࡨ࡫࡟࡭ࡣࡶࡸࡤࡺࡡࡨࠤዉ"): repo.git.rev_list(
                bstack1111ll1_opy_ (u"ࠣࡽࢀ࠲࠳ࢁࡽࠣዊ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1111llll1l_opy_ = []
        for remote in remotes:
            bstack1111ll1l11_opy_ = {
                bstack1111ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢዋ"): remote.name,
                bstack1111ll1_opy_ (u"ࠥࡹࡷࡲࠢዌ"): remote.url,
            }
            bstack1111llll1l_opy_.append(bstack1111ll1l11_opy_)
        bstack111l11lll1_opy_ = {
            bstack1111ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤው"): bstack1111ll1_opy_ (u"ࠧ࡭ࡩࡵࠤዎ"),
            **info,
            bstack1111ll1_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡹࠢዏ"): bstack1111llll1l_opy_
        }
        bstack111l11lll1_opy_ = bstack1111l1l1ll_opy_(bstack111l11lll1_opy_)
        return bstack111l11lll1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1111ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥዐ").format(err))
        return {}
def bstack1111l1l1ll_opy_(bstack111l11lll1_opy_):
    bstack11111l11l1_opy_ = bstack1111l11111_opy_(bstack111l11lll1_opy_)
    if bstack11111l11l1_opy_ and bstack11111l11l1_opy_ > bstack111ll11lll_opy_:
        bstack1111111ll1_opy_ = bstack11111l11l1_opy_ - bstack111ll11lll_opy_
        bstack1111l1111l_opy_ = bstack111l1ll111_opy_(bstack111l11lll1_opy_[bstack1111ll1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤዑ")], bstack1111111ll1_opy_)
        bstack111l11lll1_opy_[bstack1111ll1_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥዒ")] = bstack1111l1111l_opy_
        logger.info(bstack1111ll1_opy_ (u"ࠥࡘ࡭࡫ࠠࡤࡱࡰࡱ࡮ࡺࠠࡩࡣࡶࠤࡧ࡫ࡥ࡯ࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨ࠳ࠦࡓࡪࡼࡨࠤࡴ࡬ࠠࡤࡱࡰࡱ࡮ࡺࠠࡢࡨࡷࡩࡷࠦࡴࡳࡷࡱࡧࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡻࡾࠢࡎࡆࠧዓ")
                    .format(bstack1111l11111_opy_(bstack111l11lll1_opy_) / 1024))
    return bstack111l11lll1_opy_
def bstack1111l11111_opy_(bstack1l1ll111l_opy_):
    try:
        if bstack1l1ll111l_opy_:
            bstack111l11111l_opy_ = json.dumps(bstack1l1ll111l_opy_)
            bstack1111l11l1l_opy_ = sys.getsizeof(bstack111l11111l_opy_)
            return bstack1111l11l1l_opy_
    except Exception as e:
        logger.debug(bstack1111ll1_opy_ (u"ࠦࡘࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡦࡲࡣࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡵ࡬ࡾࡪࠦ࡯ࡧࠢࡍࡗࡔࡔࠠࡰࡤ࡭ࡩࡨࡺ࠺ࠡࡽࢀࠦዔ").format(e))
    return -1
def bstack111l1ll111_opy_(field, bstack11111l1lll_opy_):
    try:
        bstack111l1111ll_opy_ = len(bytes(bstack111l1lll11_opy_, bstack1111ll1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫዕ")))
        bstack111111l1ll_opy_ = bytes(field, bstack1111ll1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬዖ"))
        bstack11111llll1_opy_ = len(bstack111111l1ll_opy_)
        bstack1111ll1l1l_opy_ = ceil(bstack11111llll1_opy_ - bstack11111l1lll_opy_ - bstack111l1111ll_opy_)
        if bstack1111ll1l1l_opy_ > 0:
            bstack1111lll111_opy_ = bstack111111l1ll_opy_[:bstack1111ll1l1l_opy_].decode(bstack1111ll1_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭዗"), errors=bstack1111ll1_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࠨዘ")) + bstack111l1lll11_opy_
            return bstack1111lll111_opy_
    except Exception as e:
        logger.debug(bstack1111ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡵࡴࡸࡲࡨࡧࡴࡪࡰࡪࠤ࡫࡯ࡥ࡭ࡦ࠯ࠤࡳࡵࡴࡩ࡫ࡱ࡫ࠥࡽࡡࡴࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨࠥ࡮ࡥࡳࡧ࠽ࠤࢀࢃࠢዙ").format(e))
    return field
def bstack1l111111l_opy_():
    env = os.environ
    if (bstack1111ll1_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣዚ") in env and len(env[bstack1111ll1_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤዛ")]) > 0) or (
            bstack1111ll1_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦዜ") in env and len(env[bstack1111ll1_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧዝ")]) > 0):
        return {
            bstack1111ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧዞ"): bstack1111ll1_opy_ (u"ࠣࡌࡨࡲࡰ࡯࡮ࡴࠤዟ"),
            bstack1111ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧዠ"): env.get(bstack1111ll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨዡ")),
            bstack1111ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨዢ"): env.get(bstack1111ll1_opy_ (u"ࠧࡐࡏࡃࡡࡑࡅࡒࡋࠢዣ")),
            bstack1111ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧዤ"): env.get(bstack1111ll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨዥ"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠣࡅࡌࠦዦ")) == bstack1111ll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢዧ") and bstack1l11l1ll11_opy_(env.get(bstack1111ll1_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡆࡍࠧየ"))):
        return {
            bstack1111ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤዩ"): bstack1111ll1_opy_ (u"ࠧࡉࡩࡳࡥ࡯ࡩࡈࡏࠢዪ"),
            bstack1111ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤያ"): env.get(bstack1111ll1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥዬ")),
            bstack1111ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥይ"): env.get(bstack1111ll1_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡍࡓࡇࠨዮ")),
            bstack1111ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤዯ"): env.get(bstack1111ll1_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࠢደ"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠧࡉࡉࠣዱ")) == bstack1111ll1_opy_ (u"ࠨࡴࡳࡷࡨࠦዲ") and bstack1l11l1ll11_opy_(env.get(bstack1111ll1_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙ࠢዳ"))):
        return {
            bstack1111ll1_opy_ (u"ࠣࡰࡤࡱࡪࠨዴ"): bstack1111ll1_opy_ (u"ࠤࡗࡶࡦࡼࡩࡴࠢࡆࡍࠧድ"),
            bstack1111ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨዶ"): env.get(bstack1111ll1_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢ࡛ࡊࡈ࡟ࡖࡔࡏࠦዷ")),
            bstack1111ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢዸ"): env.get(bstack1111ll1_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣዹ")),
            bstack1111ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨዺ"): env.get(bstack1111ll1_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢዻ"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠤࡆࡍࠧዼ")) == bstack1111ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣዽ") and env.get(bstack1111ll1_opy_ (u"ࠦࡈࡏ࡟ࡏࡃࡐࡉࠧዾ")) == bstack1111ll1_opy_ (u"ࠧࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠢዿ"):
        return {
            bstack1111ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦጀ"): bstack1111ll1_opy_ (u"ࠢࡄࡱࡧࡩࡸ࡮ࡩࡱࠤጁ"),
            bstack1111ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦጂ"): None,
            bstack1111ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦጃ"): None,
            bstack1111ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤጄ"): None
        }
    if env.get(bstack1111ll1_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠢጅ")) and env.get(bstack1111ll1_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠣጆ")):
        return {
            bstack1111ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦጇ"): bstack1111ll1_opy_ (u"ࠢࡃ࡫ࡷࡦࡺࡩ࡫ࡦࡶࠥገ"),
            bstack1111ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦጉ"): env.get(bstack1111ll1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡍࡉࡕࡡࡋࡘ࡙ࡖ࡟ࡐࡔࡌࡋࡎࡔࠢጊ")),
            bstack1111ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧጋ"): None,
            bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥጌ"): env.get(bstack1111ll1_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢግ"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠨࡃࡊࠤጎ")) == bstack1111ll1_opy_ (u"ࠢࡵࡴࡸࡩࠧጏ") and bstack1l11l1ll11_opy_(env.get(bstack1111ll1_opy_ (u"ࠣࡆࡕࡓࡓࡋࠢጐ"))):
        return {
            bstack1111ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ጑"): bstack1111ll1_opy_ (u"ࠥࡈࡷࡵ࡮ࡦࠤጒ"),
            bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢጓ"): env.get(bstack1111ll1_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡐࡎࡔࡋࠣጔ")),
            bstack1111ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣጕ"): None,
            bstack1111ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ጖"): env.get(bstack1111ll1_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ጗"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠤࡆࡍࠧጘ")) == bstack1111ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣጙ") and bstack1l11l1ll11_opy_(env.get(bstack1111ll1_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋࠢጚ"))):
        return {
            bstack1111ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥጛ"): bstack1111ll1_opy_ (u"ࠨࡓࡦ࡯ࡤࡴ࡭ࡵࡲࡦࠤጜ"),
            bstack1111ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥጝ"): env.get(bstack1111ll1_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡔࡘࡇࡂࡐࡌ࡞ࡆ࡚ࡉࡐࡐࡢ࡙ࡗࡒࠢጞ")),
            bstack1111ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦጟ"): env.get(bstack1111ll1_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣጠ")),
            bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥጡ"): env.get(bstack1111ll1_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠣጢ"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠨࡃࡊࠤጣ")) == bstack1111ll1_opy_ (u"ࠢࡵࡴࡸࡩࠧጤ") and bstack1l11l1ll11_opy_(env.get(bstack1111ll1_opy_ (u"ࠣࡉࡌࡘࡑࡇࡂࡠࡅࡌࠦጥ"))):
        return {
            bstack1111ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢጦ"): bstack1111ll1_opy_ (u"ࠥࡋ࡮ࡺࡌࡢࡤࠥጧ"),
            bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢጨ"): env.get(bstack1111ll1_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤ࡛ࡒࡍࠤጩ")),
            bstack1111ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣጪ"): env.get(bstack1111ll1_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧጫ")),
            bstack1111ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢጬ"): env.get(bstack1111ll1_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡌࡈࠧጭ"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠥࡇࡎࠨጮ")) == bstack1111ll1_opy_ (u"ࠦࡹࡸࡵࡦࠤጯ") and bstack1l11l1ll11_opy_(env.get(bstack1111ll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠣጰ"))):
        return {
            bstack1111ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦጱ"): bstack1111ll1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡱࡩࡵࡧࠥጲ"),
            bstack1111ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦጳ"): env.get(bstack1111ll1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣጴ")),
            bstack1111ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧጵ"): env.get(bstack1111ll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡍࡃࡅࡉࡑࠨጶ")) or env.get(bstack1111ll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣጷ")),
            bstack1111ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧጸ"): env.get(bstack1111ll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤጹ"))
        }
    if bstack1l11l1ll11_opy_(env.get(bstack1111ll1_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥጺ"))):
        return {
            bstack1111ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢጻ"): bstack1111ll1_opy_ (u"࡚ࠥ࡮ࡹࡵࡢ࡮ࠣࡗࡹࡻࡤࡪࡱࠣࡘࡪࡧ࡭ࠡࡕࡨࡶࡻ࡯ࡣࡦࡵࠥጼ"),
            bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢጽ"): bstack1111ll1_opy_ (u"ࠧࢁࡽࡼࡿࠥጾ").format(env.get(bstack1111ll1_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩጿ")), env.get(bstack1111ll1_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࡎࡊࠧፀ"))),
            bstack1111ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥፁ"): env.get(bstack1111ll1_opy_ (u"ࠤࡖ࡝ࡘ࡚ࡅࡎࡡࡇࡉࡋࡏࡎࡊࡖࡌࡓࡓࡏࡄࠣፂ")),
            bstack1111ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤፃ"): env.get(bstack1111ll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦፄ"))
        }
    if bstack1l11l1ll11_opy_(env.get(bstack1111ll1_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘࠢፅ"))):
        return {
            bstack1111ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦፆ"): bstack1111ll1_opy_ (u"ࠢࡂࡲࡳࡺࡪࡿ࡯ࡳࠤፇ"),
            bstack1111ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦፈ"): bstack1111ll1_opy_ (u"ࠤࡾࢁ࠴ࡶࡲࡰ࡬ࡨࡧࡹ࠵ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠣፉ").format(env.get(bstack1111ll1_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤ࡛ࡒࡍࠩፊ")), env.get(bstack1111ll1_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡁࡄࡅࡒ࡙ࡓ࡚࡟ࡏࡃࡐࡉࠬፋ")), env.get(bstack1111ll1_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡕࡏ࡙ࡌ࠭ፌ")), env.get(bstack1111ll1_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪፍ"))),
            bstack1111ll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤፎ"): env.get(bstack1111ll1_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧፏ")),
            bstack1111ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣፐ"): env.get(bstack1111ll1_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦፑ"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠦࡆࡠࡕࡓࡇࡢࡌ࡙࡚ࡐࡠࡗࡖࡉࡗࡥࡁࡈࡇࡑࡘࠧፒ")) and env.get(bstack1111ll1_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢፓ")):
        return {
            bstack1111ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦፔ"): bstack1111ll1_opy_ (u"ࠢࡂࡼࡸࡶࡪࠦࡃࡊࠤፕ"),
            bstack1111ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦፖ"): bstack1111ll1_opy_ (u"ࠤࡾࢁࢀࢃ࠯ࡠࡤࡸ࡭ࡱࡪ࠯ࡳࡧࡶࡹࡱࡺࡳࡀࡤࡸ࡭ࡱࡪࡉࡥ࠿ࡾࢁࠧፗ").format(env.get(bstack1111ll1_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ፘ")), env.get(bstack1111ll1_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࠩፙ")), env.get(bstack1111ll1_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬፚ"))),
            bstack1111ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ፛"): env.get(bstack1111ll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢ፜")),
            bstack1111ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ፝"): env.get(bstack1111ll1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤ፞"))
        }
    if any([env.get(bstack1111ll1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ፟")), env.get(bstack1111ll1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥ፠")), env.get(bstack1111ll1_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤ፡"))]):
        return {
            bstack1111ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ።"): bstack1111ll1_opy_ (u"ࠢࡂ࡙ࡖࠤࡈࡵࡤࡦࡄࡸ࡭ࡱࡪࠢ፣"),
            bstack1111ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ፤"): env.get(bstack1111ll1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡖࡕࡃࡎࡌࡇࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ፥")),
            bstack1111ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ፦"): env.get(bstack1111ll1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ፧")),
            bstack1111ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ፨"): env.get(bstack1111ll1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ፩"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧ፪")):
        return {
            bstack1111ll1_opy_ (u"ࠣࡰࡤࡱࡪࠨ፫"): bstack1111ll1_opy_ (u"ࠤࡅࡥࡲࡨ࡯ࡰࠤ፬"),
            bstack1111ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ፭"): env.get(bstack1111ll1_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡕࡩࡸࡻ࡬ࡵࡵࡘࡶࡱࠨ፮")),
            bstack1111ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ፯"): env.get(bstack1111ll1_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡳࡩࡱࡵࡸࡏࡵࡢࡏࡣࡰࡩࠧ፰")),
            bstack1111ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ፱"): env.get(bstack1111ll1_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨ፲"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࠥ፳")) or env.get(bstack1111ll1_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧ፴")):
        return {
            bstack1111ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ፵"): bstack1111ll1_opy_ (u"ࠧ࡝ࡥࡳࡥ࡮ࡩࡷࠨ፶"),
            bstack1111ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ፷"): env.get(bstack1111ll1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ፸")),
            bstack1111ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ፹"): bstack1111ll1_opy_ (u"ࠤࡐࡥ࡮ࡴࠠࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠤ፺") if env.get(bstack1111ll1_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧ፻")) else None,
            bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ፼"): env.get(bstack1111ll1_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡇࡊࡖࡢࡇࡔࡓࡍࡊࡖࠥ፽"))
        }
    if any([env.get(bstack1111ll1_opy_ (u"ࠨࡇࡄࡒࡢࡔࡗࡕࡊࡆࡅࡗࠦ፾")), env.get(bstack1111ll1_opy_ (u"ࠢࡈࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣ፿")), env.get(bstack1111ll1_opy_ (u"ࠣࡉࡒࡓࡌࡒࡅࡠࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᎀ"))]):
        return {
            bstack1111ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᎁ"): bstack1111ll1_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡇࡱࡵࡵࡥࠤᎂ"),
            bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᎃ"): None,
            bstack1111ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᎄ"): env.get(bstack1111ll1_opy_ (u"ࠨࡐࡓࡑࡍࡉࡈ࡚࡟ࡊࡆࠥᎅ")),
            bstack1111ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᎆ"): env.get(bstack1111ll1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᎇ"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࠧᎈ")):
        return {
            bstack1111ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣᎉ"): bstack1111ll1_opy_ (u"ࠦࡘ࡮ࡩࡱࡲࡤࡦࡱ࡫ࠢᎊ"),
            bstack1111ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎋ"): env.get(bstack1111ll1_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᎌ")),
            bstack1111ll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᎍ"): bstack1111ll1_opy_ (u"ࠣࡌࡲࡦࠥࠩࡻࡾࠤᎎ").format(env.get(bstack1111ll1_opy_ (u"ࠩࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠬᎏ"))) if env.get(bstack1111ll1_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉࠨ᎐")) else None,
            bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᎑"): env.get(bstack1111ll1_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᎒"))
        }
    if bstack1l11l1ll11_opy_(env.get(bstack1111ll1_opy_ (u"ࠨࡎࡆࡖࡏࡍࡋ࡟ࠢ᎓"))):
        return {
            bstack1111ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᎔"): bstack1111ll1_opy_ (u"ࠣࡐࡨࡸࡱ࡯ࡦࡺࠤ᎕"),
            bstack1111ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᎖"): env.get(bstack1111ll1_opy_ (u"ࠥࡈࡊࡖࡌࡐ࡛ࡢ࡙ࡗࡒࠢ᎗")),
            bstack1111ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᎘"): env.get(bstack1111ll1_opy_ (u"࡙ࠧࡉࡕࡇࡢࡒࡆࡓࡅࠣ᎙")),
            bstack1111ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᎚"): env.get(bstack1111ll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤ᎛"))
        }
    if bstack1l11l1ll11_opy_(env.get(bstack1111ll1_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡃࡆࡘࡎࡕࡎࡔࠤ᎜"))):
        return {
            bstack1111ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᎝"): bstack1111ll1_opy_ (u"ࠥࡋ࡮ࡺࡈࡶࡤࠣࡅࡨࡺࡩࡰࡰࡶࠦ᎞"),
            bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᎟"): bstack1111ll1_opy_ (u"ࠧࢁࡽ࠰ࡽࢀ࠳ࡦࡩࡴࡪࡱࡱࡷ࠴ࡸࡵ࡯ࡵ࠲ࡿࢂࠨᎠ").format(env.get(bstack1111ll1_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡓࡆࡔ࡙ࡉࡗࡥࡕࡓࡎࠪᎡ")), env.get(bstack1111ll1_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡇࡓࡓࡘࡏࡔࡐࡔ࡜ࠫᎢ")), env.get(bstack1111ll1_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠨᎣ"))),
            bstack1111ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᎤ"): env.get(bstack1111ll1_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢ࡛ࡔࡘࡋࡇࡎࡒ࡛ࠧᎥ")),
            bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᎦ"): env.get(bstack1111ll1_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠧᎧ"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠨࡃࡊࠤᎨ")) == bstack1111ll1_opy_ (u"ࠢࡵࡴࡸࡩࠧᎩ") and env.get(bstack1111ll1_opy_ (u"ࠣࡘࡈࡖࡈࡋࡌࠣᎪ")) == bstack1111ll1_opy_ (u"ࠤ࠴ࠦᎫ"):
        return {
            bstack1111ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣᎬ"): bstack1111ll1_opy_ (u"࡛ࠦ࡫ࡲࡤࡧ࡯ࠦᎭ"),
            bstack1111ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎮ"): bstack1111ll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡻࡾࠤᎯ").format(env.get(bstack1111ll1_opy_ (u"ࠧࡗࡇࡕࡇࡊࡒ࡟ࡖࡔࡏࠫᎰ"))),
            bstack1111ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᎱ"): None,
            bstack1111ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᎲ"): None,
        }
    if env.get(bstack1111ll1_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᎳ")):
        return {
            bstack1111ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᎴ"): bstack1111ll1_opy_ (u"࡚ࠧࡥࡢ࡯ࡦ࡭ࡹࡿࠢᎵ"),
            bstack1111ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᎶ"): None,
            bstack1111ll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᎷ"): env.get(bstack1111ll1_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠤᎸ")),
            bstack1111ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᎹ"): env.get(bstack1111ll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᎺ"))
        }
    if any([env.get(bstack1111ll1_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋࠢᎻ")), env.get(bstack1111ll1_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡕࡐࠧᎼ")), env.get(bstack1111ll1_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦᎽ")), env.get(bstack1111ll1_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢࡘࡊࡇࡍࠣᎾ"))]):
        return {
            bstack1111ll1_opy_ (u"ࠣࡰࡤࡱࡪࠨᎿ"): bstack1111ll1_opy_ (u"ࠤࡆࡳࡳࡩ࡯ࡶࡴࡶࡩࠧᏀ"),
            bstack1111ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᏁ"): None,
            bstack1111ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᏂ"): env.get(bstack1111ll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᏃ")) or None,
            bstack1111ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᏄ"): env.get(bstack1111ll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤᏅ"), 0)
        }
    if env.get(bstack1111ll1_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᏆ")):
        return {
            bstack1111ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᏇ"): bstack1111ll1_opy_ (u"ࠥࡋࡴࡉࡄࠣᏈ"),
            bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᏉ"): None,
            bstack1111ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᏊ"): env.get(bstack1111ll1_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᏋ")),
            bstack1111ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᏌ"): env.get(bstack1111ll1_opy_ (u"ࠣࡉࡒࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡃࡐࡗࡑࡘࡊࡘࠢᏍ"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᏎ")):
        return {
            bstack1111ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣᏏ"): bstack1111ll1_opy_ (u"ࠦࡈࡵࡤࡦࡈࡵࡩࡸ࡮ࠢᏐ"),
            bstack1111ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᏑ"): env.get(bstack1111ll1_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᏒ")),
            bstack1111ll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᏓ"): env.get(bstack1111ll1_opy_ (u"ࠣࡅࡉࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᏔ")),
            bstack1111ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᏕ"): env.get(bstack1111ll1_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᏖ"))
        }
    return {bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏗ"): None}
def get_host_info():
    return {
        bstack1111ll1_opy_ (u"ࠧ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠢᏘ"): platform.node(),
        bstack1111ll1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣᏙ"): platform.system(),
        bstack1111ll1_opy_ (u"ࠢࡵࡻࡳࡩࠧᏚ"): platform.machine(),
        bstack1111ll1_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤᏛ"): platform.version(),
        bstack1111ll1_opy_ (u"ࠤࡤࡶࡨ࡮ࠢᏜ"): platform.architecture()[0]
    }
def bstack1l1l11ll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111111l111_opy_():
    if bstack11l11l1ll_opy_.get_property(bstack1111ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫᏝ")):
        return bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᏞ")
    return bstack1111ll1_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠫᏟ")
def bstack111l1111l1_opy_(driver):
    info = {
        bstack1111ll1_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᏠ"): driver.capabilities,
        bstack1111ll1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫᏡ"): driver.session_id,
        bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᏢ"): driver.capabilities.get(bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᏣ"), None),
        bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᏤ"): driver.capabilities.get(bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᏥ"), None),
        bstack1111ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧᏦ"): driver.capabilities.get(bstack1111ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᏧ"), None),
    }
    if bstack111111l111_opy_() == bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭Ꮸ"):
        info[bstack1111ll1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩᏩ")] = bstack1111ll1_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨᏪ") if bstack11l11l1l1_opy_() else bstack1111ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᏫ")
    return info
def bstack11l11l1l1_opy_():
    if bstack11l11l1ll_opy_.get_property(bstack1111ll1_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪᏬ")):
        return True
    if bstack1l11l1ll11_opy_(os.environ.get(bstack1111ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭Ꮽ"), None)):
        return True
    return False
def bstack1ll1llllll_opy_(bstack11111ll1l1_opy_, url, data, config):
    headers = config.get(bstack1111ll1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᏮ"), None)
    proxies = bstack1lll1lll_opy_(config, url)
    auth = config.get(bstack1111ll1_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᏯ"), None)
    response = requests.request(
            bstack11111ll1l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1lll11ll_opy_(bstack1ll11l1l11_opy_, size):
    bstack1lll1l1l11_opy_ = []
    while len(bstack1ll11l1l11_opy_) > size:
        bstack111lll11l_opy_ = bstack1ll11l1l11_opy_[:size]
        bstack1lll1l1l11_opy_.append(bstack111lll11l_opy_)
        bstack1ll11l1l11_opy_ = bstack1ll11l1l11_opy_[size:]
    bstack1lll1l1l11_opy_.append(bstack1ll11l1l11_opy_)
    return bstack1lll1l1l11_opy_
def bstack1111ll1111_opy_(message, bstack1111ll111l_opy_=False):
    os.write(1, bytes(message, bstack1111ll1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᏰ")))
    os.write(1, bytes(bstack1111ll1_opy_ (u"ࠩ࡟ࡲࠬᏱ"), bstack1111ll1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᏲ")))
    if bstack1111ll111l_opy_:
        with open(bstack1111ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡴ࠷࠱ࡺ࠯ࠪᏳ") + os.environ[bstack1111ll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᏴ")] + bstack1111ll1_opy_ (u"࠭࠮࡭ࡱࡪࠫᏵ"), bstack1111ll1_opy_ (u"ࠧࡢࠩ᏶")) as f:
            f.write(message + bstack1111ll1_opy_ (u"ࠨ࡞ࡱࠫ᏷"))
def bstack1111l1ll11_opy_():
    return os.environ[bstack1111ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬᏸ")].lower() == bstack1111ll1_opy_ (u"ࠪࡸࡷࡻࡥࠨᏹ")
def bstack1ll1lll1l1_opy_(bstack1111lll1l1_opy_):
    return bstack1111ll1_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪᏺ").format(bstack111ll1l111_opy_, bstack1111lll1l1_opy_)
def bstack111lll1l_opy_():
    return bstack11l1lll1ll_opy_().replace(tzinfo=None).isoformat() + bstack1111ll1_opy_ (u"ࠬࡠࠧᏻ")
def bstack1111l111ll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1111ll1_opy_ (u"࡚࠭ࠨᏼ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1111ll1_opy_ (u"࡛ࠧࠩᏽ")))).total_seconds() * 1000
def bstack111l11ll11_opy_(timestamp):
    return bstack1111ll11ll_opy_(timestamp).isoformat() + bstack1111ll1_opy_ (u"ࠨ࡜ࠪ᏾")
def bstack111111ll1l_opy_(bstack11111lllll_opy_):
    date_format = bstack1111ll1_opy_ (u"ࠩࠨ࡝ࠪࡳࠥࡥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠧ᏿")
    bstack11111lll1l_opy_ = datetime.datetime.strptime(bstack11111lllll_opy_, date_format)
    return bstack11111lll1l_opy_.isoformat() + bstack1111ll1_opy_ (u"ࠪ࡞ࠬ᐀")
def bstack111l11l11l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1111ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᐁ")
    else:
        return bstack1111ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᐂ")
def bstack1l11l1ll11_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1111ll1_opy_ (u"࠭ࡴࡳࡷࡨࠫᐃ")
def bstack11111l11ll_opy_(val):
    return val.__str__().lower() == bstack1111ll1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᐄ")
def bstack11l1lll111_opy_(bstack111l111111_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111l111111_opy_ as e:
                print(bstack1111ll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣᐅ").format(func.__name__, bstack111l111111_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1111lll11l_opy_(bstack1111l1lll1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1111l1lll1_opy_(cls, *args, **kwargs)
            except bstack111l111111_opy_ as e:
                print(bstack1111ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤᐆ").format(bstack1111l1lll1_opy_.__name__, bstack111l111111_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1111lll11l_opy_
    else:
        return decorator
def bstack1l111l1ll_opy_(bstack11l11lll11_opy_):
    if bstack1111ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᐇ") in bstack11l11lll11_opy_ and bstack11111l11ll_opy_(bstack11l11lll11_opy_[bstack1111ll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᐈ")]):
        return False
    if bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᐉ") in bstack11l11lll11_opy_ and bstack11111l11ll_opy_(bstack11l11lll11_opy_[bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᐊ")]):
        return False
    return True
def bstack1ll11l1lll_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1l11lllll1_opy_(hub_url):
    if bstack111l11ll1_opy_() <= version.parse(bstack1111ll1_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᐋ")):
        if hub_url != bstack1111ll1_opy_ (u"ࠨࠩᐌ"):
            return bstack1111ll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᐍ") + hub_url + bstack1111ll1_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢᐎ")
        return bstack1lll11l1_opy_
    if hub_url != bstack1111ll1_opy_ (u"ࠫࠬᐏ"):
        return bstack1111ll1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᐐ") + hub_url + bstack1111ll1_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢᐑ")
    return bstack1l1l1l111_opy_
def bstack1111111lll_opy_():
    return isinstance(os.getenv(bstack1111ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ᐒ")), str)
def bstack1l111llll_opy_(url):
    return urlparse(url).hostname
def bstack11llllll1l_opy_(hostname):
    for bstack1l11l11l11_opy_ in bstack1lll111111_opy_:
        regex = re.compile(bstack1l11l11l11_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111l1l1111_opy_(bstack1111111l1l_opy_, file_name, logger):
    bstack1l1l111l1_opy_ = os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠨࢀࠪᐓ")), bstack1111111l1l_opy_)
    try:
        if not os.path.exists(bstack1l1l111l1_opy_):
            os.makedirs(bstack1l1l111l1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠩࢁࠫᐔ")), bstack1111111l1l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1111ll1_opy_ (u"ࠪࡻࠬᐕ")):
                pass
            with open(file_path, bstack1111ll1_opy_ (u"ࠦࡼ࠱ࠢᐖ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1llll1l1l1_opy_.format(str(e)))
def bstack1111lll1ll_opy_(file_name, key, value, logger):
    file_path = bstack111l1l1111_opy_(bstack1111ll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᐗ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11ll1111l_opy_ = json.load(open(file_path, bstack1111ll1_opy_ (u"࠭ࡲࡣࠩᐘ")))
        else:
            bstack11ll1111l_opy_ = {}
        bstack11ll1111l_opy_[key] = value
        with open(file_path, bstack1111ll1_opy_ (u"ࠢࡸ࠭ࠥᐙ")) as outfile:
            json.dump(bstack11ll1111l_opy_, outfile)
def bstack111llll11_opy_(file_name, logger):
    file_path = bstack111l1l1111_opy_(bstack1111ll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᐚ"), file_name, logger)
    bstack11ll1111l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1111ll1_opy_ (u"ࠩࡵࠫᐛ")) as bstack1lll1lll11_opy_:
            bstack11ll1111l_opy_ = json.load(bstack1lll1lll11_opy_)
    return bstack11ll1111l_opy_
def bstack11l1l11ll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1111ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧᐜ") + file_path + bstack1111ll1_opy_ (u"ࠫࠥ࠭ᐝ") + str(e))
def bstack111l11ll1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1111ll1_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢᐞ")
def bstack1lll1111l_opy_(config):
    if bstack1111ll1_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᐟ") in config:
        del (config[bstack1111ll1_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᐠ")])
        return False
    if bstack111l11ll1_opy_() < version.parse(bstack1111ll1_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧᐡ")):
        return False
    if bstack111l11ll1_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨᐢ")):
        return True
    if bstack1111ll1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᐣ") in config and config[bstack1111ll1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᐤ")] is False:
        return False
    else:
        return True
def bstack1l1l1l1l_opy_(args_list, bstack11111ll111_opy_):
    index = -1
    for value in bstack11111ll111_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11lll111ll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11lll111ll_opy_ = bstack11lll111ll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1111ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᐥ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1111ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᐦ"), exception=exception)
    def bstack11l11ll1ll_opy_(self):
        if self.result != bstack1111ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᐧ"):
            return None
        if isinstance(self.exception_type, str) and bstack1111ll1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᐨ") in self.exception_type:
            return bstack1111ll1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᐩ")
        return bstack1111ll1_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᐪ")
    def bstack11111l1ll1_opy_(self):
        if self.result != bstack1111ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᐫ"):
            return None
        if self.bstack11lll111ll_opy_:
            return self.bstack11lll111ll_opy_
        return bstack1111llllll_opy_(self.exception)
def bstack1111llllll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1111l1l111_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1llll1l11_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1lll11111l_opy_(config, logger):
    try:
        import playwright
        bstack11111ll1ll_opy_ = playwright.__file__
        bstack1111llll11_opy_ = os.path.split(bstack11111ll1ll_opy_)
        bstack111l11ll1l_opy_ = bstack1111llll11_opy_[0] + bstack1111ll1_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨᐬ")
        os.environ[bstack1111ll1_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩᐭ")] = bstack1lll11llll_opy_(config)
        with open(bstack111l11ll1l_opy_, bstack1111ll1_opy_ (u"ࠧࡳࠩᐮ")) as f:
            bstack1l111lll11_opy_ = f.read()
            bstack111111lll1_opy_ = bstack1111ll1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧᐯ")
            bstack111l11l1ll_opy_ = bstack1l111lll11_opy_.find(bstack111111lll1_opy_)
            if bstack111l11l1ll_opy_ == -1:
              process = subprocess.Popen(bstack1111ll1_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨᐰ"), shell=True, cwd=bstack1111llll11_opy_[0])
              process.wait()
              bstack111l1l1ll1_opy_ = bstack1111ll1_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪᐱ")
              bstack111l111lll_opy_ = bstack1111ll1_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣᐲ")
              bstack111l1l1l1l_opy_ = bstack1l111lll11_opy_.replace(bstack111l1l1ll1_opy_, bstack111l111lll_opy_)
              with open(bstack111l11ll1l_opy_, bstack1111ll1_opy_ (u"ࠬࡽࠧᐳ")) as f:
                f.write(bstack111l1l1l1l_opy_)
    except Exception as e:
        logger.error(bstack1ll1l1l11l_opy_.format(str(e)))
def bstack1ll1l1llll_opy_():
  try:
    bstack1111lllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111ll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ᐴ"))
    bstack11111lll11_opy_ = []
    if os.path.exists(bstack1111lllll1_opy_):
      with open(bstack1111lllll1_opy_) as f:
        bstack11111lll11_opy_ = json.load(f)
      os.remove(bstack1111lllll1_opy_)
    return bstack11111lll11_opy_
  except:
    pass
  return []
def bstack1l11llll_opy_(bstack1lllllllll_opy_):
  try:
    bstack11111lll11_opy_ = []
    bstack1111lllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111ll1_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧᐵ"))
    if os.path.exists(bstack1111lllll1_opy_):
      with open(bstack1111lllll1_opy_) as f:
        bstack11111lll11_opy_ = json.load(f)
    bstack11111lll11_opy_.append(bstack1lllllllll_opy_)
    with open(bstack1111lllll1_opy_, bstack1111ll1_opy_ (u"ࠨࡹࠪᐶ")) as f:
        json.dump(bstack11111lll11_opy_, f)
  except:
    pass
def bstack1ll1l1l11_opy_(logger, bstack1111l11lll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1111ll1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᐷ"), bstack1111ll1_opy_ (u"ࠪࠫᐸ"))
    if test_name == bstack1111ll1_opy_ (u"ࠫࠬᐹ"):
        test_name = threading.current_thread().__dict__.get(bstack1111ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫᐺ"), bstack1111ll1_opy_ (u"࠭ࠧᐻ"))
    bstack111l11l111_opy_ = bstack1111ll1_opy_ (u"ࠧ࠭ࠢࠪᐼ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1111l11lll_opy_:
        bstack1l1l11l111_opy_ = os.environ.get(bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᐽ"), bstack1111ll1_opy_ (u"ࠩ࠳ࠫᐾ"))
        bstack1lll1llll1_opy_ = {bstack1111ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨᐿ"): test_name, bstack1111ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᑀ"): bstack111l11l111_opy_, bstack1111ll1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᑁ"): bstack1l1l11l111_opy_}
        bstack1111l111l1_opy_ = []
        bstack1111l1llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᑂ"))
        if os.path.exists(bstack1111l1llll_opy_):
            with open(bstack1111l1llll_opy_) as f:
                bstack1111l111l1_opy_ = json.load(f)
        bstack1111l111l1_opy_.append(bstack1lll1llll1_opy_)
        with open(bstack1111l1llll_opy_, bstack1111ll1_opy_ (u"ࠧࡸࠩᑃ")) as f:
            json.dump(bstack1111l111l1_opy_, f)
    else:
        bstack1lll1llll1_opy_ = {bstack1111ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᑄ"): test_name, bstack1111ll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᑅ"): bstack111l11l111_opy_, bstack1111ll1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᑆ"): str(multiprocessing.current_process().name)}
        if bstack1111ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨᑇ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1lll1llll1_opy_)
  except Exception as e:
      logger.warn(bstack1111ll1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᑈ").format(e))
def bstack1llll11l1_opy_(error_message, test_name, index, logger):
  try:
    bstack111111ll11_opy_ = []
    bstack1lll1llll1_opy_ = {bstack1111ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᑉ"): test_name, bstack1111ll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᑊ"): error_message, bstack1111ll1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᑋ"): index}
    bstack111l1l11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᑌ"))
    if os.path.exists(bstack111l1l11l1_opy_):
        with open(bstack111l1l11l1_opy_) as f:
            bstack111111ll11_opy_ = json.load(f)
    bstack111111ll11_opy_.append(bstack1lll1llll1_opy_)
    with open(bstack111l1l11l1_opy_, bstack1111ll1_opy_ (u"ࠪࡻࠬᑍ")) as f:
        json.dump(bstack111111ll11_opy_, f)
  except Exception as e:
    logger.warn(bstack1111ll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᑎ").format(e))
def bstack1l11111lll_opy_(bstack1ll1l11l11_opy_, name, logger):
  try:
    bstack1lll1llll1_opy_ = {bstack1111ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᑏ"): name, bstack1111ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᑐ"): bstack1ll1l11l11_opy_, bstack1111ll1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᑑ"): str(threading.current_thread()._name)}
    return bstack1lll1llll1_opy_
  except Exception as e:
    logger.warn(bstack1111ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᑒ").format(e))
  return
def bstack11111l1111_opy_():
    return platform.system() == bstack1111ll1_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪᑓ")
def bstack1ll1ll111l_opy_(bstack111l111ll1_opy_, config, logger):
    bstack1111l1l1l1_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111l111ll1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1111ll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤᑔ").format(e))
    return bstack1111l1l1l1_opy_
def bstack111l1l111l_opy_(bstack111l1l1lll_opy_, bstack111l11llll_opy_):
    bstack111111llll_opy_ = version.parse(bstack111l1l1lll_opy_)
    bstack111l111l1l_opy_ = version.parse(bstack111l11llll_opy_)
    if bstack111111llll_opy_ > bstack111l111l1l_opy_:
        return 1
    elif bstack111111llll_opy_ < bstack111l111l1l_opy_:
        return -1
    else:
        return 0
def bstack11l1lll1ll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1111ll11ll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111ll11l1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack111llll1_opy_(options, framework):
    if options is None:
        return
    if getattr(options, bstack1111ll1_opy_ (u"ࠫ࡬࡫ࡴࠨᑕ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1l1lll1l_opy_ = caps.get(bstack1111ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᑖ"))
    bstack11111ll11l_opy_ = True
    if bstack11111l11ll_opy_(caps.get(bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦ࡙࠶ࡇࠬᑗ"))) or bstack11111l11ll_opy_(caps.get(bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡢࡻ࠸ࡩࠧᑘ"))):
        bstack11111ll11l_opy_ = False
    if bstack1lll1111l_opy_({bstack1111ll1_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣᑙ"): bstack11111ll11l_opy_}):
        bstack1l1l1lll1l_opy_ = bstack1l1l1lll1l_opy_ or {}
        bstack1l1l1lll1l_opy_[bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᑚ")] = bstack1111ll11l1_opy_(framework)
        bstack1l1l1lll1l_opy_[bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᑛ")] = bstack1111l1ll11_opy_()
        if getattr(options, bstack1111ll1_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬᑜ"), None):
            options.set_capability(bstack1111ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᑝ"), bstack1l1l1lll1l_opy_)
        else:
            options[bstack1111ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᑞ")] = bstack1l1l1lll1l_opy_
    else:
        if getattr(options, bstack1111ll1_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨᑟ"), None):
            options.set_capability(bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᑠ"), bstack1111ll11l1_opy_(framework))
            options.set_capability(bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᑡ"), bstack1111l1ll11_opy_())
        else:
            options[bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᑢ")] = bstack1111ll11l1_opy_(framework)
            options[bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᑣ")] = bstack1111l1ll11_opy_()
    return options
def bstack1111l1ll1l_opy_(bstack1111ll1lll_opy_, framework):
    if bstack1111ll1lll_opy_ and len(bstack1111ll1lll_opy_.split(bstack1111ll1_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᑤ"))) > 1:
        ws_url = bstack1111ll1lll_opy_.split(bstack1111ll1_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᑥ"))[0]
        if bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᑦ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack111l1l11ll_opy_ = json.loads(urllib.parse.unquote(bstack1111ll1lll_opy_.split(bstack1111ll1_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᑧ"))[1]))
            bstack111l1l11ll_opy_ = bstack111l1l11ll_opy_ or {}
            bstack111l1l11ll_opy_[bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᑨ")] = str(framework) + str(__version__)
            bstack111l1l11ll_opy_[bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᑩ")] = bstack1111l1ll11_opy_()
            bstack1111ll1lll_opy_ = bstack1111ll1lll_opy_.split(bstack1111ll1_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᑪ"))[0] + bstack1111ll1_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᑫ") + urllib.parse.quote(json.dumps(bstack111l1l11ll_opy_))
    return bstack1111ll1lll_opy_
def bstack11l11ll11_opy_():
    global bstack1ll111l1l1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll111l1l1_opy_ = BrowserType.connect
    return bstack1ll111l1l1_opy_
def bstack11lll1ll_opy_(framework_name):
    global bstack1ll1l11ll_opy_
    bstack1ll1l11ll_opy_ = framework_name
    return framework_name
def bstack11l1l1l1l_opy_(self, *args, **kwargs):
    global bstack1ll111l1l1_opy_
    try:
        global bstack1ll1l11ll_opy_
        if bstack1111ll1_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᑬ") in kwargs:
            kwargs[bstack1111ll1_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᑭ")] = bstack1111l1ll1l_opy_(
                kwargs.get(bstack1111ll1_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᑮ"), None),
                bstack1ll1l11ll_opy_
            )
    except Exception as e:
        logger.error(bstack1111ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡗࡉࡑࠠࡤࡣࡳࡷ࠿ࠦࡻࡾࠤᑯ").format(str(e)))
    return bstack1ll111l1l1_opy_(self, *args, **kwargs)
def bstack1111l11ll1_opy_(bstack1111ll1ll1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1lll1lll_opy_(bstack1111ll1ll1_opy_, bstack1111ll1_opy_ (u"ࠥࠦᑰ"))
        if proxies and proxies.get(bstack1111ll1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᑱ")):
            parsed_url = urlparse(proxies.get(bstack1111ll1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᑲ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1111ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩᑳ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1111ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪᑴ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1111ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫᑵ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1111ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬᑶ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1lll11ll1l_opy_(bstack1111ll1ll1_opy_):
    bstack111l1l1l11_opy_ = {
        bstack111ll11ll1_opy_[bstack111111l1l1_opy_]: bstack1111ll1ll1_opy_[bstack111111l1l1_opy_]
        for bstack111111l1l1_opy_ in bstack1111ll1ll1_opy_
        if bstack111111l1l1_opy_ in bstack111ll11ll1_opy_
    }
    bstack111l1l1l11_opy_[bstack1111ll1_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥᑷ")] = bstack1111l11ll1_opy_(bstack1111ll1ll1_opy_, bstack11l11l1ll_opy_.get_property(bstack1111ll1_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᑸ")))
    bstack1111l1l11l_opy_ = [element.lower() for element in bstack111ll111l1_opy_]
    bstack111l1ll11l_opy_(bstack111l1l1l11_opy_, bstack1111l1l11l_opy_)
    return bstack111l1l1l11_opy_
def bstack111l1ll11l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1111ll1_opy_ (u"ࠧ࠰ࠪࠫࠬࠥᑹ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111l1ll11l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111l1ll11l_opy_(item, keys)