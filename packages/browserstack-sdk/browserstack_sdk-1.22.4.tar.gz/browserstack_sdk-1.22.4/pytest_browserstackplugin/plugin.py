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
import datetime
import inspect
import logging
import os
import signal
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l1lll11_opy_, bstack1l11ll11l_opy_, update, bstack1ll1l111ll_opy_,
                                       bstack1ll111llll_opy_, bstack11l111l1l_opy_, bstack1l1lll11ll_opy_, bstack1lll1l11_opy_,
                                       bstack1l1ll1l1l_opy_, bstack11l1l1ll1_opy_, bstack111l11lll_opy_, bstack111ll11l_opy_,
                                       bstack11111ll11_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l1l11l11l_opy_)
from browserstack_sdk.bstack1l111111_opy_ import bstack11llll1l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1111111ll_opy_
from bstack_utils.capture import bstack11lll11lll_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l1l1l1ll1_opy_, bstack1lll11l111_opy_, bstack1111ll1l1_opy_, \
    bstack1l1ll111l1_opy_
from bstack_utils.helper import bstack1llll1l11_opy_, bstack1111ll11ll_opy_, bstack11l1lll1ll_opy_, bstack1l1l11ll_opy_, bstack1111l1ll11_opy_, bstack111lll1l_opy_, \
    bstack111l11l11l_opy_, \
    bstack11111l1l1l_opy_, bstack111l11ll1_opy_, bstack1l11lllll1_opy_, bstack1111111lll_opy_, bstack1ll11l1lll_opy_, Notset, \
    bstack1lll1111l_opy_, bstack1111l111ll_opy_, bstack1111llllll_opy_, Result, bstack111l11ll11_opy_, bstack1111l1l111_opy_, bstack11l1lll111_opy_, \
    bstack1l11llll_opy_, bstack1ll1l1l11_opy_, bstack1l11l1ll11_opy_, bstack11111l1111_opy_
from bstack_utils.bstack11111111l1_opy_ import bstack1llllllllll_opy_
from bstack_utils.messages import bstack1llllll1ll_opy_, bstack1lllll111_opy_, bstack1l11111l_opy_, bstack11l11l1l_opy_, bstack1l11l111ll_opy_, \
    bstack1ll1l1l11l_opy_, bstack1l1ll1l11_opy_, bstack11l1111l_opy_, bstack1l11lll1l1_opy_, bstack11l111l11_opy_, \
    bstack1l1lllll11_opy_, bstack1111l11l_opy_
from bstack_utils.proxy import bstack1lll11llll_opy_, bstack11l1l1111_opy_
from bstack_utils.bstack11ll11111_opy_ import bstack1lll111ll1l_opy_, bstack1lll111llll_opy_, bstack1lll11l1lll_opy_, bstack1lll111l1ll_opy_, \
    bstack1lll11l11ll_opy_, bstack1lll11l1l11_opy_, bstack1lll11l11l1_opy_, bstack1lllll1ll_opy_, bstack1lll111ll11_opy_
from bstack_utils.bstack1ll11l1l1l_opy_ import bstack1l1l1l1lll_opy_
from bstack_utils.bstack1ll1lll1_opy_ import bstack1ll1ll111_opy_, bstack1111l1l11_opy_, bstack1ll11lll_opy_, \
    bstack1ll1l1ll1_opy_, bstack11l1ll1ll_opy_
from bstack_utils.bstack11lll1111l_opy_ import bstack11lll1ll1l_opy_
from bstack_utils.bstack1111lll11_opy_ import bstack11lll1lll_opy_
import bstack_utils.bstack1lllllll1l_opy_ as bstack11l11l111_opy_
from bstack_utils.bstack1ll1lllll_opy_ import bstack1l1111l11_opy_
from bstack_utils.bstack1l1lll1l_opy_ import bstack1l1lll1l_opy_
bstack1lll11l1l1_opy_ = None
bstack1l111ll11l_opy_ = None
bstack111111111_opy_ = None
bstack1ll1l1l1l1_opy_ = None
bstack1l111l1l1_opy_ = None
bstack1ll1l1lll_opy_ = None
bstack1lll1l1l1_opy_ = None
bstack1l11l1l11_opy_ = None
bstack1l1llll11_opy_ = None
bstack1l1ll1111_opy_ = None
bstack1ll1ll1l_opy_ = None
bstack1llll11111_opy_ = None
bstack1lll1lll1_opy_ = None
bstack1ll1l11ll_opy_ = bstack1111ll1_opy_ (u"ࠫࠬឝ")
CONFIG = {}
bstack1l1lll1111_opy_ = False
bstack1l1lll1lll_opy_ = bstack1111ll1_opy_ (u"ࠬ࠭ឞ")
bstack1l11l11lll_opy_ = bstack1111ll1_opy_ (u"࠭ࠧស")
bstack111l1l11l_opy_ = False
bstack111lll1ll_opy_ = []
bstack1l1111l1l1_opy_ = bstack1l1l1l1ll1_opy_
bstack1ll11l1llll_opy_ = bstack1111ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧហ")
bstack1ll111l11ll_opy_ = False
bstack1l1111l111_opy_ = {}
bstack11lll111_opy_ = False
logger = bstack1111111ll_opy_.get_logger(__name__, bstack1l1111l1l1_opy_)
store = {
    bstack1111ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬឡ"): []
}
bstack1ll11l111l1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11ll11l1l1_opy_ = {}
current_test_uuid = None
def bstack11lllll1l_opy_(page, bstack11l111ll_opy_):
    try:
        page.evaluate(bstack1111ll1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥអ"),
                      bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧឣ") + json.dumps(
                          bstack11l111ll_opy_) + bstack1111ll1_opy_ (u"ࠦࢂࢃࠢឤ"))
    except Exception as e:
        print(bstack1111ll1_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥឥ"), e)
def bstack1l1l111ll_opy_(page, message, level):
    try:
        page.evaluate(bstack1111ll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢឦ"), bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬឧ") + json.dumps(
            message) + bstack1111ll1_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫឨ") + json.dumps(level) + bstack1111ll1_opy_ (u"ࠩࢀࢁࠬឩ"))
    except Exception as e:
        print(bstack1111ll1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࠨឪ"), e)
def pytest_configure(config):
    bstack11l11l1ll_opy_ = Config.bstack1111l1lll_opy_()
    config.args = bstack11lll1lll_opy_.bstack1ll11ll1l1l_opy_(config.args)
    bstack11l11l1ll_opy_.bstack11l1l1lll_opy_(bstack1l11l1ll11_opy_(config.getoption(bstack1111ll1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨឫ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1ll11l11ll1_opy_ = item.config.getoption(bstack1111ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧឬ"))
    plugins = item.config.getoption(bstack1111ll1_opy_ (u"ࠨࡰ࡭ࡷࡪ࡭ࡳࡹࠢឭ"))
    report = outcome.get_result()
    bstack1ll111llll1_opy_(item, call, report)
    if bstack1111ll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧឮ") not in plugins or bstack1ll11l1lll_opy_():
        return
    summary = []
    driver = getattr(item, bstack1111ll1_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤឯ"), None)
    page = getattr(item, bstack1111ll1_opy_ (u"ࠤࡢࡴࡦ࡭ࡥࠣឰ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1ll11ll111l_opy_(item, report, summary, bstack1ll11l11ll1_opy_)
    if (page is not None):
        bstack1ll11l1111l_opy_(item, report, summary, bstack1ll11l11ll1_opy_)
def bstack1ll11ll111l_opy_(item, report, summary, bstack1ll11l11ll1_opy_):
    if report.when == bstack1111ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩឱ") and report.skipped:
        bstack1lll111ll11_opy_(report)
    if report.when in [bstack1111ll1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥឲ"), bstack1111ll1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢឳ")]:
        return
    if not bstack1111l1ll11_opy_():
        return
    try:
        if (str(bstack1ll11l11ll1_opy_).lower() != bstack1111ll1_opy_ (u"࠭ࡴࡳࡷࡨࠫ឴")):
            item._driver.execute_script(
                bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ឵") + json.dumps(
                    report.nodeid) + bstack1111ll1_opy_ (u"ࠨࡿࢀࠫា"))
        os.environ[bstack1111ll1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬិ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1111ll1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩ࠿ࠦࡻ࠱ࡿࠥី").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111ll1_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨឹ")))
    bstack1ll111l11l_opy_ = bstack1111ll1_opy_ (u"ࠧࠨឺ")
    bstack1lll111ll11_opy_(report)
    if not passed:
        try:
            bstack1ll111l11l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1111ll1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨុ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll111l11l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1111ll1_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤូ")))
        bstack1ll111l11l_opy_ = bstack1111ll1_opy_ (u"ࠣࠤួ")
        if not passed:
            try:
                bstack1ll111l11l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1111ll1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤើ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll111l11l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧឿ")
                    + json.dumps(bstack1111ll1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠥࠧៀ"))
                    + bstack1111ll1_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣេ")
                )
            else:
                item._driver.execute_script(
                    bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫែ")
                    + json.dumps(str(bstack1ll111l11l_opy_))
                    + bstack1111ll1_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥៃ")
                )
        except Exception as e:
            summary.append(bstack1111ll1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡ࡯ࡰࡲࡸࡦࡺࡥ࠻ࠢࡾ࠴ࢂࠨោ").format(e))
def bstack1ll111ll11l_opy_(test_name, error_message):
    try:
        bstack1ll111l1l11_opy_ = []
        bstack1l1l11l111_opy_ = os.environ.get(bstack1111ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩៅ"), bstack1111ll1_opy_ (u"ࠪ࠴ࠬំ"))
        bstack1lll1llll1_opy_ = {bstack1111ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩះ"): test_name, bstack1111ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫៈ"): error_message, bstack1111ll1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ៉"): bstack1l1l11l111_opy_}
        bstack1ll11l1l111_opy_ = os.path.join(tempfile.gettempdir(), bstack1111ll1_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ៊"))
        if os.path.exists(bstack1ll11l1l111_opy_):
            with open(bstack1ll11l1l111_opy_) as f:
                bstack1ll111l1l11_opy_ = json.load(f)
        bstack1ll111l1l11_opy_.append(bstack1lll1llll1_opy_)
        with open(bstack1ll11l1l111_opy_, bstack1111ll1_opy_ (u"ࠨࡹࠪ់")) as f:
            json.dump(bstack1ll111l1l11_opy_, f)
    except Exception as e:
        logger.debug(bstack1111ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵ࡫ࡲࡴ࡫ࡶࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡹࡵࡧࡶࡸࠥ࡫ࡲࡳࡱࡵࡷ࠿ࠦࠧ៌") + str(e))
def bstack1ll11l1111l_opy_(item, report, summary, bstack1ll11l11ll1_opy_):
    if report.when in [bstack1111ll1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ៍"), bstack1111ll1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ៎")]:
        return
    if (str(bstack1ll11l11ll1_opy_).lower() != bstack1111ll1_opy_ (u"ࠬࡺࡲࡶࡧࠪ៏")):
        bstack11lllll1l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111ll1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ័")))
    bstack1ll111l11l_opy_ = bstack1111ll1_opy_ (u"ࠢࠣ៑")
    bstack1lll111ll11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll111l11l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1111ll1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽ្ࠣ").format(e)
                )
        try:
            if passed:
                bstack11l1ll1ll_opy_(getattr(item, bstack1111ll1_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ៓"), None), bstack1111ll1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ។"))
            else:
                error_message = bstack1111ll1_opy_ (u"ࠫࠬ៕")
                if bstack1ll111l11l_opy_:
                    bstack1l1l111ll_opy_(item._page, str(bstack1ll111l11l_opy_), bstack1111ll1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ៖"))
                    bstack11l1ll1ll_opy_(getattr(item, bstack1111ll1_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬៗ"), None), bstack1111ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ៘"), str(bstack1ll111l11l_opy_))
                    error_message = str(bstack1ll111l11l_opy_)
                else:
                    bstack11l1ll1ll_opy_(getattr(item, bstack1111ll1_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ៙"), None), bstack1111ll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ៚"))
                bstack1ll111ll11l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1111ll1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢ៛").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1111ll1_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣៜ"), default=bstack1111ll1_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ៝"), help=bstack1111ll1_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ៞"))
    parser.addoption(bstack1111ll1_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ៟"), default=bstack1111ll1_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢ០"), help=bstack1111ll1_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣ១"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1111ll1_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧ២"), action=bstack1111ll1_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥ៣"), default=bstack1111ll1_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧ៤"),
                         help=bstack1111ll1_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧ៥"))
def bstack11lll11l1l_opy_(log):
    if not (log[bstack1111ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ៦")] and log[bstack1111ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ៧")].strip()):
        return
    active = bstack11llll1l1l_opy_()
    log = {
        bstack1111ll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ៨"): log[bstack1111ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ៩")],
        bstack1111ll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ៪"): bstack11l1lll1ll_opy_().isoformat() + bstack1111ll1_opy_ (u"ࠬࡠࠧ៫"),
        bstack1111ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ៬"): log[bstack1111ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ៭")],
    }
    if active:
        if active[bstack1111ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭៮")] == bstack1111ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ៯"):
            log[bstack1111ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ៰")] = active[bstack1111ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ៱")]
        elif active[bstack1111ll1_opy_ (u"ࠬࡺࡹࡱࡧࠪ៲")] == bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࠫ៳"):
            log[bstack1111ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ៴")] = active[bstack1111ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ៵")]
    bstack1l1111l11_opy_.bstack1l1111l1_opy_([log])
def bstack11llll1l1l_opy_():
    if len(store[bstack1111ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭៶")]) > 0 and store[bstack1111ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ៷")][-1]:
        return {
            bstack1111ll1_opy_ (u"ࠫࡹࡿࡰࡦࠩ៸"): bstack1111ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ៹"),
            bstack1111ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭៺"): store[bstack1111ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ៻")][-1]
        }
    if store.get(bstack1111ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ៼"), None):
        return {
            bstack1111ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ៽"): bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࠨ៾"),
            bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ៿"): store[bstack1111ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ᠀")]
        }
    return None
bstack11llll1lll_opy_ = bstack11lll11lll_opy_(bstack11lll11l1l_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1ll111l11ll_opy_
        item._1ll11l1ll11_opy_ = True
        bstack1ll1ll1l1l_opy_ = bstack11l11l111_opy_.bstack1l111l11_opy_(bstack11111l1l1l_opy_(item.own_markers))
        item._a11y_test_case = bstack1ll1ll1l1l_opy_
        if bstack1ll111l11ll_opy_:
            driver = getattr(item, bstack1111ll1_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ᠁"), None)
            item._a11y_started = bstack11l11l111_opy_.bstack1lll1lllll_opy_(driver, bstack1ll1ll1l1l_opy_)
        if not bstack1l1111l11_opy_.on() or bstack1ll11l1llll_opy_ != bstack1111ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ᠂"):
            return
        global current_test_uuid, bstack11llll1lll_opy_
        bstack11llll1lll_opy_.start()
        bstack11ll11ll1l_opy_ = {
            bstack1111ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᠃"): uuid4().__str__(),
            bstack1111ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭᠄"): bstack11l1lll1ll_opy_().isoformat() + bstack1111ll1_opy_ (u"ࠪ࡞ࠬ᠅")
        }
        current_test_uuid = bstack11ll11ll1l_opy_[bstack1111ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩ᠆")]
        store[bstack1111ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ᠇")] = bstack11ll11ll1l_opy_[bstack1111ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᠈")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11ll11l1l1_opy_[item.nodeid] = {**_11ll11l1l1_opy_[item.nodeid], **bstack11ll11ll1l_opy_}
        bstack1ll11l111ll_opy_(item, _11ll11l1l1_opy_[item.nodeid], bstack1111ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ᠉"))
    except Exception as err:
        print(bstack1111ll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡥࡤࡰࡱࡀࠠࡼࡿࠪ᠊"), str(err))
def pytest_runtest_setup(item):
    global bstack1ll11l111l1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1111111lll_opy_():
        atexit.register(bstack11lll1111_opy_)
        if not bstack1ll11l111l1_opy_:
            try:
                bstack1ll11ll1111_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11111l1111_opy_():
                    bstack1ll11ll1111_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll11ll1111_opy_:
                    signal.signal(s, bstack1ll111lllll_opy_)
                bstack1ll11l111l1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1111ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡧࡪࡵࡷࡩࡷࠦࡳࡪࡩࡱࡥࡱࠦࡨࡢࡰࡧࡰࡪࡸࡳ࠻ࠢࠥ᠋") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll111ll1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1111ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᠌")
    try:
        if not bstack1l1111l11_opy_.on():
            return
        bstack11llll1lll_opy_.start()
        uuid = uuid4().__str__()
        bstack11ll11ll1l_opy_ = {
            bstack1111ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩ᠍"): uuid,
            bstack1111ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ᠎"): bstack11l1lll1ll_opy_().isoformat() + bstack1111ll1_opy_ (u"࡚࠭ࠨ᠏"),
            bstack1111ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬ᠐"): bstack1111ll1_opy_ (u"ࠨࡪࡲࡳࡰ࠭᠑"),
            bstack1111ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ᠒"): bstack1111ll1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ᠓"),
            bstack1111ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ᠔"): bstack1111ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ᠕")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1111ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ᠖")] = item
        store[bstack1111ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ᠗")] = [uuid]
        if not _11ll11l1l1_opy_.get(item.nodeid, None):
            _11ll11l1l1_opy_[item.nodeid] = {bstack1111ll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ᠘"): [], bstack1111ll1_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ᠙"): []}
        _11ll11l1l1_opy_[item.nodeid][bstack1111ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ᠚")].append(bstack11ll11ll1l_opy_[bstack1111ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩ᠛")])
        _11ll11l1l1_opy_[item.nodeid + bstack1111ll1_opy_ (u"ࠬ࠳ࡳࡦࡶࡸࡴࠬ᠜")] = bstack11ll11ll1l_opy_
        bstack1ll11l1ll1l_opy_(item, bstack11ll11ll1l_opy_, bstack1111ll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ᠝"))
    except Exception as err:
        print(bstack1111ll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪ᠞"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1l1111l111_opy_
        bstack1l1l11l111_opy_ = 0
        if bstack111l1l11l_opy_ is True:
            bstack1l1l11l111_opy_ = int(os.environ.get(bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᠟")))
        if bstack111lll11_opy_.bstack111111ll1_opy_() == bstack1111ll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᠠ"):
            if bstack111lll11_opy_.bstack1l11ll11_opy_() == bstack1111ll1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᠡ"):
                bstack1ll11l1l1l1_opy_ = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᠢ"), None)
                bstack1ll11ll111_opy_ = bstack1ll11l1l1l1_opy_ + bstack1111ll1_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣᠣ")
                driver = getattr(item, bstack1111ll1_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᠤ"), None)
                bstack1ll11l11ll_opy_ = getattr(item, bstack1111ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᠥ"), None)
                bstack111lllll1_opy_ = getattr(item, bstack1111ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᠦ"), None)
                PercySDK.screenshot(driver, bstack1ll11ll111_opy_, bstack1ll11l11ll_opy_=bstack1ll11l11ll_opy_, bstack111lllll1_opy_=bstack111lllll1_opy_, bstack1111l1111_opy_=bstack1l1l11l111_opy_)
        if getattr(item, bstack1111ll1_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩᠧ"), False):
            bstack11llll1l_opy_.bstack1ll11ll1ll_opy_(getattr(item, bstack1111ll1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᠨ"), None), bstack1l1111l111_opy_, logger, item)
        if not bstack1l1111l11_opy_.on():
            return
        bstack11ll11ll1l_opy_ = {
            bstack1111ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩᠩ"): uuid4().__str__(),
            bstack1111ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᠪ"): bstack11l1lll1ll_opy_().isoformat() + bstack1111ll1_opy_ (u"࡚࠭ࠨᠫ"),
            bstack1111ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬᠬ"): bstack1111ll1_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᠭ"),
            bstack1111ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᠮ"): bstack1111ll1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᠯ"),
            bstack1111ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᠰ"): bstack1111ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᠱ")
        }
        _11ll11l1l1_opy_[item.nodeid + bstack1111ll1_opy_ (u"࠭࠭ࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᠲ")] = bstack11ll11ll1l_opy_
        bstack1ll11l1ll1l_opy_(item, bstack11ll11ll1l_opy_, bstack1111ll1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᠳ"))
    except Exception as err:
        print(bstack1111ll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰ࠽ࠤࢀࢃࠧᠴ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1l1111l11_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1lll111l1ll_opy_(fixturedef.argname):
        store[bstack1111ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨᠵ")] = request.node
    elif bstack1lll11l11ll_opy_(fixturedef.argname):
        store[bstack1111ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨᠶ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1111ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᠷ"): fixturedef.argname,
            bstack1111ll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᠸ"): bstack111l11l11l_opy_(outcome),
            bstack1111ll1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᠹ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1111ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫᠺ")]
        if not _11ll11l1l1_opy_.get(current_test_item.nodeid, None):
            _11ll11l1l1_opy_[current_test_item.nodeid] = {bstack1111ll1_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᠻ"): []}
        _11ll11l1l1_opy_[current_test_item.nodeid][bstack1111ll1_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᠼ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1111ll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭ᠽ"), str(err))
if bstack1ll11l1lll_opy_() and bstack1l1111l11_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11ll11l1l1_opy_[request.node.nodeid][bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᠾ")].bstack111l1lll_opy_(id(step))
        except Exception as err:
            print(bstack1111ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࡀࠠࡼࡿࠪᠿ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11ll11l1l1_opy_[request.node.nodeid][bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᡀ")].bstack11lll1lll1_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1111ll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫᡁ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11lll1111l_opy_: bstack11lll1ll1l_opy_ = _11ll11l1l1_opy_[request.node.nodeid][bstack1111ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᡂ")]
            bstack11lll1111l_opy_.bstack11lll1lll1_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1111ll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭ᡃ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll11l1llll_opy_
        try:
            if not bstack1l1111l11_opy_.on() or bstack1ll11l1llll_opy_ != bstack1111ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᡄ"):
                return
            global bstack11llll1lll_opy_
            bstack11llll1lll_opy_.start()
            driver = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᡅ"), None)
            if not _11ll11l1l1_opy_.get(request.node.nodeid, None):
                _11ll11l1l1_opy_[request.node.nodeid] = {}
            bstack11lll1111l_opy_ = bstack11lll1ll1l_opy_.bstack1ll1lll11ll_opy_(
                scenario, feature, request.node,
                name=bstack1lll11l1l11_opy_(request.node, scenario),
                bstack11ll1lllll_opy_=bstack111lll1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1111ll1_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧᡆ"),
                tags=bstack1lll11l11l1_opy_(feature, scenario),
                bstack11lll1ll11_opy_=bstack1l1111l11_opy_.bstack11ll1llll1_opy_(driver) if driver and driver.session_id else {}
            )
            _11ll11l1l1_opy_[request.node.nodeid][bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᡇ")] = bstack11lll1111l_opy_
            bstack1ll111lll11_opy_(bstack11lll1111l_opy_.uuid)
            bstack1l1111l11_opy_.bstack11lll11111_opy_(bstack1111ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᡈ"), bstack11lll1111l_opy_)
        except Exception as err:
            print(bstack1111ll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪᡉ"), str(err))
def bstack1ll111lll1l_opy_(bstack11lll1llll_opy_):
    if bstack11lll1llll_opy_ in store[bstack1111ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᡊ")]:
        store[bstack1111ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᡋ")].remove(bstack11lll1llll_opy_)
def bstack1ll111lll11_opy_(bstack11lll1l1l1_opy_):
    store[bstack1111ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᡌ")] = bstack11lll1l1l1_opy_
    threading.current_thread().current_test_uuid = bstack11lll1l1l1_opy_
@bstack1l1111l11_opy_.bstack1ll1l1lll1l_opy_
def bstack1ll111llll1_opy_(item, call, report):
    global bstack1ll11l1llll_opy_
    bstack1l111l1l1l_opy_ = bstack111lll1l_opy_()
    if hasattr(report, bstack1111ll1_opy_ (u"ࠬࡹࡴࡰࡲࠪᡍ")):
        bstack1l111l1l1l_opy_ = bstack111l11ll11_opy_(report.stop)
    elif hasattr(report, bstack1111ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࠬᡎ")):
        bstack1l111l1l1l_opy_ = bstack111l11ll11_opy_(report.start)
    try:
        if getattr(report, bstack1111ll1_opy_ (u"ࠧࡸࡪࡨࡲࠬᡏ"), bstack1111ll1_opy_ (u"ࠨࠩᡐ")) == bstack1111ll1_opy_ (u"ࠩࡦࡥࡱࡲࠧᡑ"):
            bstack11llll1lll_opy_.reset()
        if getattr(report, bstack1111ll1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᡒ"), bstack1111ll1_opy_ (u"ࠫࠬᡓ")) == bstack1111ll1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᡔ"):
            if bstack1ll11l1llll_opy_ == bstack1111ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᡕ"):
                _11ll11l1l1_opy_[item.nodeid][bstack1111ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᡖ")] = bstack1l111l1l1l_opy_
                bstack1ll11l111ll_opy_(item, _11ll11l1l1_opy_[item.nodeid], bstack1111ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᡗ"), report, call)
                store[bstack1111ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᡘ")] = None
            elif bstack1ll11l1llll_opy_ == bstack1111ll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᡙ"):
                bstack11lll1111l_opy_ = _11ll11l1l1_opy_[item.nodeid][bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᡚ")]
                bstack11lll1111l_opy_.set(hooks=_11ll11l1l1_opy_[item.nodeid].get(bstack1111ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᡛ"), []))
                exception, bstack11lll111ll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11lll111ll_opy_ = [call.excinfo.exconly(), getattr(report, bstack1111ll1_opy_ (u"࠭࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠬᡜ"), bstack1111ll1_opy_ (u"ࠧࠨᡝ"))]
                bstack11lll1111l_opy_.stop(time=bstack1l111l1l1l_opy_, result=Result(result=getattr(report, bstack1111ll1_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩᡞ"), bstack1111ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᡟ")), exception=exception, bstack11lll111ll_opy_=bstack11lll111ll_opy_))
                bstack1l1111l11_opy_.bstack11lll11111_opy_(bstack1111ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᡠ"), _11ll11l1l1_opy_[item.nodeid][bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᡡ")])
        elif getattr(report, bstack1111ll1_opy_ (u"ࠬࡽࡨࡦࡰࠪᡢ"), bstack1111ll1_opy_ (u"࠭ࠧᡣ")) in [bstack1111ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᡤ"), bstack1111ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᡥ")]:
            bstack11llll1111_opy_ = item.nodeid + bstack1111ll1_opy_ (u"ࠩ࠰ࠫᡦ") + getattr(report, bstack1111ll1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᡧ"), bstack1111ll1_opy_ (u"ࠫࠬᡨ"))
            if getattr(report, bstack1111ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᡩ"), False):
                hook_type = bstack1111ll1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᡪ") if getattr(report, bstack1111ll1_opy_ (u"ࠧࡸࡪࡨࡲࠬᡫ"), bstack1111ll1_opy_ (u"ࠨࠩᡬ")) == bstack1111ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᡭ") else bstack1111ll1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᡮ")
                _11ll11l1l1_opy_[bstack11llll1111_opy_] = {
                    bstack1111ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩᡯ"): uuid4().__str__(),
                    bstack1111ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᡰ"): bstack1l111l1l1l_opy_,
                    bstack1111ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᡱ"): hook_type
                }
            _11ll11l1l1_opy_[bstack11llll1111_opy_][bstack1111ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᡲ")] = bstack1l111l1l1l_opy_
            bstack1ll111lll1l_opy_(_11ll11l1l1_opy_[bstack11llll1111_opy_][bstack1111ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᡳ")])
            bstack1ll11l1ll1l_opy_(item, _11ll11l1l1_opy_[bstack11llll1111_opy_], bstack1111ll1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᡴ"), report, call)
            if getattr(report, bstack1111ll1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᡵ"), bstack1111ll1_opy_ (u"ࠫࠬᡶ")) == bstack1111ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᡷ"):
                if getattr(report, bstack1111ll1_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧᡸ"), bstack1111ll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ᡹")) == bstack1111ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᡺"):
                    bstack11ll11ll1l_opy_ = {
                        bstack1111ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᡻"): uuid4().__str__(),
                        bstack1111ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ᡼"): bstack111lll1l_opy_(),
                        bstack1111ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᡽"): bstack111lll1l_opy_()
                    }
                    _11ll11l1l1_opy_[item.nodeid] = {**_11ll11l1l1_opy_[item.nodeid], **bstack11ll11ll1l_opy_}
                    bstack1ll11l111ll_opy_(item, _11ll11l1l1_opy_[item.nodeid], bstack1111ll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭᡾"))
                    bstack1ll11l111ll_opy_(item, _11ll11l1l1_opy_[item.nodeid], bstack1111ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ᡿"), report, call)
    except Exception as err:
        print(bstack1111ll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡾࢁࠬᢀ"), str(err))
def bstack1ll11l1lll1_opy_(test, bstack11ll11ll1l_opy_, result=None, call=None, bstack1l111111ll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11lll1111l_opy_ = {
        bstack1111ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᢁ"): bstack11ll11ll1l_opy_[bstack1111ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᢂ")],
        bstack1111ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨᢃ"): bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᢄ"),
        bstack1111ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᢅ"): test.name,
        bstack1111ll1_opy_ (u"࠭ࡢࡰࡦࡼࠫᢆ"): {
            bstack1111ll1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᢇ"): bstack1111ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᢈ"),
            bstack1111ll1_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᢉ"): inspect.getsource(test.obj)
        },
        bstack1111ll1_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᢊ"): test.name,
        bstack1111ll1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪᢋ"): test.name,
        bstack1111ll1_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᢌ"): bstack11lll1lll_opy_.bstack11ll111111_opy_(test),
        bstack1111ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᢍ"): file_path,
        bstack1111ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᢎ"): file_path,
        bstack1111ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᢏ"): bstack1111ll1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᢐ"),
        bstack1111ll1_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᢑ"): file_path,
        bstack1111ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᢒ"): bstack11ll11ll1l_opy_[bstack1111ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᢓ")],
        bstack1111ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᢔ"): bstack1111ll1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᢕ"),
        bstack1111ll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫᢖ"): {
            bstack1111ll1_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭ᢗ"): test.nodeid
        },
        bstack1111ll1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᢘ"): bstack11111l1l1l_opy_(test.own_markers)
    }
    if bstack1l111111ll_opy_ in [bstack1111ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᢙ"), bstack1111ll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᢚ")]:
        bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"࠭࡭ࡦࡶࡤࠫᢛ")] = {
            bstack1111ll1_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᢜ"): bstack11ll11ll1l_opy_.get(bstack1111ll1_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᢝ"), [])
        }
    if bstack1l111111ll_opy_ == bstack1111ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᢞ"):
        bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᢟ")] = bstack1111ll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᢠ")
        bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᢡ")] = bstack11ll11ll1l_opy_[bstack1111ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᢢ")]
        bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᢣ")] = bstack11ll11ll1l_opy_[bstack1111ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᢤ")]
    if result:
        bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᢥ")] = result.outcome
        bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᢦ")] = result.duration * 1000
        bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᢧ")] = bstack11ll11ll1l_opy_[bstack1111ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᢨ")]
        if result.failed:
            bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩᢩࠬ")] = bstack1l1111l11_opy_.bstack11l11ll1ll_opy_(call.excinfo.typename)
            bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᢪ")] = bstack1l1111l11_opy_.bstack1ll1ll111l1_opy_(call.excinfo, result)
        bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ᢫")] = bstack11ll11ll1l_opy_[bstack1111ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᢬")]
    if outcome:
        bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᢭")] = bstack111l11l11l_opy_(outcome)
        bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ᢮")] = 0
        bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᢯")] = bstack11ll11ll1l_opy_[bstack1111ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᢰ")]
        if bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᢱ")] == bstack1111ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᢲ"):
            bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᢳ")] = bstack1111ll1_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫᢴ")  # bstack1ll111ll1l1_opy_
            bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᢵ")] = [{bstack1111ll1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᢶ"): [bstack1111ll1_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪᢷ")]}]
        bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᢸ")] = bstack11ll11ll1l_opy_[bstack1111ll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᢹ")]
    return bstack11lll1111l_opy_
def bstack1ll111ll1ll_opy_(test, bstack11ll1ll1l1_opy_, bstack1l111111ll_opy_, result, call, outcome, bstack1ll11l1l11l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11ll1ll1l1_opy_[bstack1111ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᢺ")]
    hook_name = bstack11ll1ll1l1_opy_[bstack1111ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᢻ")]
    hook_data = {
        bstack1111ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩᢼ"): bstack11ll1ll1l1_opy_[bstack1111ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪᢽ")],
        bstack1111ll1_opy_ (u"࠭ࡴࡺࡲࡨࠫᢾ"): bstack1111ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᢿ"),
        bstack1111ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᣀ"): bstack1111ll1_opy_ (u"ࠩࡾࢁࠬᣁ").format(bstack1lll111llll_opy_(hook_name)),
        bstack1111ll1_opy_ (u"ࠪࡦࡴࡪࡹࠨᣂ"): {
            bstack1111ll1_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᣃ"): bstack1111ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᣄ"),
            bstack1111ll1_opy_ (u"࠭ࡣࡰࡦࡨࠫᣅ"): None
        },
        bstack1111ll1_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭ᣆ"): test.name,
        bstack1111ll1_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᣇ"): bstack11lll1lll_opy_.bstack11ll111111_opy_(test, hook_name),
        bstack1111ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᣈ"): file_path,
        bstack1111ll1_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᣉ"): file_path,
        bstack1111ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᣊ"): bstack1111ll1_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ᣋ"),
        bstack1111ll1_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᣌ"): file_path,
        bstack1111ll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᣍ"): bstack11ll1ll1l1_opy_[bstack1111ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᣎ")],
        bstack1111ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᣏ"): bstack1111ll1_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬᣐ") if bstack1ll11l1llll_opy_ == bstack1111ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᣑ") else bstack1111ll1_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬᣒ"),
        bstack1111ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᣓ"): hook_type
    }
    bstack1ll1ll11l1l_opy_ = bstack11l1ll11ll_opy_(_11ll11l1l1_opy_.get(test.nodeid, None))
    if bstack1ll1ll11l1l_opy_:
        hook_data[bstack1111ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬᣔ")] = bstack1ll1ll11l1l_opy_
    if result:
        hook_data[bstack1111ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᣕ")] = result.outcome
        hook_data[bstack1111ll1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᣖ")] = result.duration * 1000
        hook_data[bstack1111ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᣗ")] = bstack11ll1ll1l1_opy_[bstack1111ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᣘ")]
        if result.failed:
            hook_data[bstack1111ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᣙ")] = bstack1l1111l11_opy_.bstack11l11ll1ll_opy_(call.excinfo.typename)
            hook_data[bstack1111ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᣚ")] = bstack1l1111l11_opy_.bstack1ll1ll111l1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1111ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᣛ")] = bstack111l11l11l_opy_(outcome)
        hook_data[bstack1111ll1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᣜ")] = 100
        hook_data[bstack1111ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᣝ")] = bstack11ll1ll1l1_opy_[bstack1111ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᣞ")]
        if hook_data[bstack1111ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᣟ")] == bstack1111ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᣠ"):
            hook_data[bstack1111ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᣡ")] = bstack1111ll1_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨᣢ")  # bstack1ll111ll1l1_opy_
            hook_data[bstack1111ll1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᣣ")] = [{bstack1111ll1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᣤ"): [bstack1111ll1_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧᣥ")]}]
    if bstack1ll11l1l11l_opy_:
        hook_data[bstack1111ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᣦ")] = bstack1ll11l1l11l_opy_.result
        hook_data[bstack1111ll1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᣧ")] = bstack1111l111ll_opy_(bstack11ll1ll1l1_opy_[bstack1111ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᣨ")], bstack11ll1ll1l1_opy_[bstack1111ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᣩ")])
        hook_data[bstack1111ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᣪ")] = bstack11ll1ll1l1_opy_[bstack1111ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᣫ")]
        if hook_data[bstack1111ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᣬ")] == bstack1111ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᣭ"):
            hook_data[bstack1111ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᣮ")] = bstack1l1111l11_opy_.bstack11l11ll1ll_opy_(bstack1ll11l1l11l_opy_.exception_type)
            hook_data[bstack1111ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᣯ")] = [{bstack1111ll1_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᣰ"): bstack1111llllll_opy_(bstack1ll11l1l11l_opy_.exception)}]
    return hook_data
def bstack1ll11l111ll_opy_(test, bstack11ll11ll1l_opy_, bstack1l111111ll_opy_, result=None, call=None, outcome=None):
    bstack11lll1111l_opy_ = bstack1ll11l1lll1_opy_(test, bstack11ll11ll1l_opy_, result, call, bstack1l111111ll_opy_, outcome)
    driver = getattr(test, bstack1111ll1_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᣱ"), None)
    if bstack1l111111ll_opy_ == bstack1111ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᣲ") and driver:
        bstack11lll1111l_opy_[bstack1111ll1_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᣳ")] = bstack1l1111l11_opy_.bstack11ll1llll1_opy_(driver)
    if bstack1l111111ll_opy_ == bstack1111ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᣴ"):
        bstack1l111111ll_opy_ = bstack1111ll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᣵ")
    bstack11ll1lll11_opy_ = {
        bstack1111ll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ᣶"): bstack1l111111ll_opy_,
        bstack1111ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ᣷"): bstack11lll1111l_opy_
    }
    bstack1l1111l11_opy_.bstack11l1llll1l_opy_(bstack11ll1lll11_opy_)
def bstack1ll11l1ll1l_opy_(test, bstack11ll11ll1l_opy_, bstack1l111111ll_opy_, result=None, call=None, outcome=None, bstack1ll11l1l11l_opy_=None):
    hook_data = bstack1ll111ll1ll_opy_(test, bstack11ll11ll1l_opy_, bstack1l111111ll_opy_, result, call, outcome, bstack1ll11l1l11l_opy_)
    bstack11ll1lll11_opy_ = {
        bstack1111ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ᣸"): bstack1l111111ll_opy_,
        bstack1111ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ᣹"): hook_data
    }
    bstack1l1111l11_opy_.bstack11l1llll1l_opy_(bstack11ll1lll11_opy_)
def bstack11l1ll11ll_opy_(bstack11ll11ll1l_opy_):
    if not bstack11ll11ll1l_opy_:
        return None
    if bstack11ll11ll1l_opy_.get(bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭᣺"), None):
        return getattr(bstack11ll11ll1l_opy_[bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ᣻")], bstack1111ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ᣼"), None)
    return bstack11ll11ll1l_opy_.get(bstack1111ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᣽"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l1111l11_opy_.on():
            return
        places = [bstack1111ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭᣾"), bstack1111ll1_opy_ (u"ࠨࡥࡤࡰࡱ࠭᣿"), bstack1111ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᤀ")]
        bstack11ll11ll11_opy_ = []
        for bstack1ll11l1l1ll_opy_ in places:
            records = caplog.get_records(bstack1ll11l1l1ll_opy_)
            bstack1ll11l11l1l_opy_ = bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᤁ") if bstack1ll11l1l1ll_opy_ == bstack1111ll1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᤂ") else bstack1111ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᤃ")
            bstack1ll11l11l11_opy_ = request.node.nodeid + (bstack1111ll1_opy_ (u"࠭ࠧᤄ") if bstack1ll11l1l1ll_opy_ == bstack1111ll1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᤅ") else bstack1111ll1_opy_ (u"ࠨ࠯ࠪᤆ") + bstack1ll11l1l1ll_opy_)
            bstack11lll1l1l1_opy_ = bstack11l1ll11ll_opy_(_11ll11l1l1_opy_.get(bstack1ll11l11l11_opy_, None))
            if not bstack11lll1l1l1_opy_:
                continue
            for record in records:
                if bstack1111l1l111_opy_(record.message):
                    continue
                bstack11ll11ll11_opy_.append({
                    bstack1111ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᤇ"): bstack1111ll11ll_opy_(record.created).isoformat() + bstack1111ll1_opy_ (u"ࠪ࡞ࠬᤈ"),
                    bstack1111ll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᤉ"): record.levelname,
                    bstack1111ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᤊ"): record.message,
                    bstack1ll11l11l1l_opy_: bstack11lll1l1l1_opy_
                })
        if len(bstack11ll11ll11_opy_) > 0:
            bstack1l1111l11_opy_.bstack1l1111l1_opy_(bstack11ll11ll11_opy_)
    except Exception as err:
        print(bstack1111ll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡤࡱࡱࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡀࠠࡼࡿࠪᤋ"), str(err))
def bstack1l11l1lll_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11lll111_opy_
    bstack1l1l1l111l_opy_ = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᤌ"), None) and bstack1llll1l11_opy_(
            threading.current_thread(), bstack1111ll1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᤍ"), None)
    bstack11l111l1_opy_ = getattr(driver, bstack1111ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩᤎ"), None) != None and getattr(driver, bstack1111ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪᤏ"), None) == True
    if sequence == bstack1111ll1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᤐ") and driver != None:
      if not bstack11lll111_opy_ and bstack1111l1ll11_opy_() and bstack1111ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᤑ") in CONFIG and CONFIG[bstack1111ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᤒ")] == True and bstack1l1lll1l_opy_.bstack11llllll_opy_(driver_command) and (bstack11l111l1_opy_ or bstack1l1l1l111l_opy_) and not bstack1l1l11l11l_opy_(args):
        try:
          bstack11lll111_opy_ = True
          logger.debug(bstack1111ll1_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡻࡾࠩᤓ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1111ll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ࠭ᤔ").format(str(err)))
        bstack11lll111_opy_ = False
    if sequence == bstack1111ll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᤕ"):
        if driver_command == bstack1111ll1_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧᤖ"):
            bstack1l1111l11_opy_.bstack1ll111lll1_opy_({
                bstack1111ll1_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪᤗ"): response[bstack1111ll1_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫᤘ")],
                bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᤙ"): store[bstack1111ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᤚ")]
            })
def bstack11lll1111_opy_():
    global bstack111lll1ll_opy_
    bstack1111111ll_opy_.bstack1111l111l_opy_()
    logging.shutdown()
    bstack1l1111l11_opy_.bstack11l1ll1lll_opy_()
    for driver in bstack111lll1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll111lllll_opy_(*args):
    global bstack111lll1ll_opy_
    bstack1l1111l11_opy_.bstack11l1ll1lll_opy_()
    for driver in bstack111lll1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll111l111_opy_(self, *args, **kwargs):
    bstack111ll1l1_opy_ = bstack1lll11l1l1_opy_(self, *args, **kwargs)
    bstack1l1111l11_opy_.bstack1ll111l11_opy_(self)
    return bstack111ll1l1_opy_
def bstack1lll1l1ll_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11l11l1ll_opy_ = Config.bstack1111l1lll_opy_()
    if bstack11l11l1ll_opy_.get_property(bstack1111ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬᤛ")):
        return
    bstack11l11l1ll_opy_.bstack11llllll1_opy_(bstack1111ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭ᤜ"), True)
    global bstack1ll1l11ll_opy_
    global bstack1l1l11l1ll_opy_
    bstack1ll1l11ll_opy_ = framework_name
    logger.info(bstack1111l11l_opy_.format(bstack1ll1l11ll_opy_.split(bstack1111ll1_opy_ (u"ࠪ࠱ࠬᤝ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1111l1ll11_opy_():
            Service.start = bstack1l1lll11ll_opy_
            Service.stop = bstack1lll1l11_opy_
            webdriver.Remote.__init__ = bstack1ll11111ll_opy_
            webdriver.Remote.get = bstack11l1ll11l_opy_
            if not isinstance(os.getenv(bstack1111ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬᤞ")), str):
                return
            WebDriver.close = bstack1l1ll1l1l_opy_
            WebDriver.quit = bstack11l1ll111_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack1111l1ll11_opy_() and bstack1l1111l11_opy_.on():
            webdriver.Remote.__init__ = bstack1ll111l111_opy_
        bstack1l1l11l1ll_opy_ = True
    except Exception as e:
        pass
    bstack1lll11l11_opy_()
    if os.environ.get(bstack1111ll1_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪ᤟")):
        bstack1l1l11l1ll_opy_ = eval(os.environ.get(bstack1111ll1_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᤠ")))
    if not bstack1l1l11l1ll_opy_:
        bstack111l11lll_opy_(bstack1111ll1_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤᤡ"), bstack1l1lllll11_opy_)
    if bstack1ll111111l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack111l1l1ll_opy_
        except Exception as e:
            logger.error(bstack1ll1l1l11l_opy_.format(str(e)))
    if bstack1111ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᤢ") in str(framework_name).lower():
        if not bstack1111l1ll11_opy_():
            return
        try:
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
def bstack11l1ll111_opy_(self):
    global bstack1ll1l11ll_opy_
    global bstack11l111ll1_opy_
    global bstack1l111ll11l_opy_
    try:
        if bstack1111ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᤣ") in bstack1ll1l11ll_opy_ and self.session_id != None and bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧᤤ"), bstack1111ll1_opy_ (u"ࠫࠬᤥ")) != bstack1111ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᤦ"):
            bstack1ll11l1ll1_opy_ = bstack1111ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᤧ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1111ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᤨ")
            bstack1ll1l1l11_opy_(logger, True)
            if self != None:
                bstack1ll1l1ll1_opy_(self, bstack1ll11l1ll1_opy_, bstack1111ll1_opy_ (u"ࠨ࠮ࠣࠫᤩ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1111ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᤪ"), None)
        if item is not None and bstack1ll111l11ll_opy_:
            bstack11llll1l_opy_.bstack1ll11ll1ll_opy_(self, bstack1l1111l111_opy_, logger, item)
        threading.current_thread().testStatus = bstack1111ll1_opy_ (u"ࠪࠫᤫ")
    except Exception as e:
        logger.debug(bstack1111ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ᤬") + str(e))
    bstack1l111ll11l_opy_(self)
    self.session_id = None
def bstack1ll11111ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11l111ll1_opy_
    global bstack111111ll_opy_
    global bstack111l1l11l_opy_
    global bstack1ll1l11ll_opy_
    global bstack1lll11l1l1_opy_
    global bstack111lll1ll_opy_
    global bstack1l1lll1lll_opy_
    global bstack1l11l11lll_opy_
    global bstack1ll111l11ll_opy_
    global bstack1l1111l111_opy_
    CONFIG[bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᤭")] = str(bstack1ll1l11ll_opy_) + str(__version__)
    command_executor = bstack1l11lllll1_opy_(bstack1l1lll1lll_opy_)
    logger.debug(bstack11l11l1l_opy_.format(command_executor))
    proxy = bstack11111ll11_opy_(CONFIG, proxy)
    bstack1l1l11l111_opy_ = 0
    try:
        if bstack111l1l11l_opy_ is True:
            bstack1l1l11l111_opy_ = int(os.environ.get(bstack1111ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭᤮")))
    except:
        bstack1l1l11l111_opy_ = 0
    bstack11l1llll_opy_ = bstack1l1lll11_opy_(CONFIG, bstack1l1l11l111_opy_)
    logger.debug(bstack11l1111l_opy_.format(str(bstack11l1llll_opy_)))
    bstack1l1111l111_opy_ = CONFIG.get(bstack1111ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᤯"))[bstack1l1l11l111_opy_]
    if bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᤰ") in CONFIG and CONFIG[bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᤱ")]:
        bstack1ll11lll_opy_(bstack11l1llll_opy_, bstack1l11l11lll_opy_)
    if bstack11l11l111_opy_.bstack1l1l1111_opy_(CONFIG, bstack1l1l11l111_opy_) and bstack11l11l111_opy_.bstack1l1111lll1_opy_(bstack11l1llll_opy_, options, desired_capabilities):
        bstack1ll111l11ll_opy_ = True
        bstack11l11l111_opy_.set_capabilities(bstack11l1llll_opy_, CONFIG)
    if desired_capabilities:
        bstack111l1l111_opy_ = bstack1l11ll11l_opy_(desired_capabilities)
        bstack111l1l111_opy_[bstack1111ll1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᤲ")] = bstack1lll1111l_opy_(CONFIG)
        bstack1lll1111_opy_ = bstack1l1lll11_opy_(bstack111l1l111_opy_)
        if bstack1lll1111_opy_:
            bstack11l1llll_opy_ = update(bstack1lll1111_opy_, bstack11l1llll_opy_)
        desired_capabilities = None
    if options:
        bstack11l1l1ll1_opy_(options, bstack11l1llll_opy_)
    if not options:
        options = bstack1ll1l111ll_opy_(bstack11l1llll_opy_)
    if proxy and bstack111l11ll1_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫᤳ")):
        options.proxy(proxy)
    if options and bstack111l11ll1_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᤴ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack111l11ll1_opy_() < version.parse(bstack1111ll1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᤵ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11l1llll_opy_)
    logger.info(bstack1l11111l_opy_)
    if bstack111l11ll1_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᤶ")):
        bstack1lll11l1l1_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l11ll1_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᤷ")):
        bstack1lll11l1l1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l11ll1_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩᤸ")):
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
        bstack1lllllllll_opy_ = bstack1111ll1_opy_ (u"᤹ࠪࠫ")
        if bstack111l11ll1_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ᤺")):
            bstack1lllllllll_opy_ = self.caps.get(bstack1111ll1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰ᤻ࠧ"))
        else:
            bstack1lllllllll_opy_ = self.capabilities.get(bstack1111ll1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ᤼"))
        if bstack1lllllllll_opy_:
            bstack1l11llll_opy_(bstack1lllllllll_opy_)
            if bstack111l11ll1_opy_() <= version.parse(bstack1111ll1_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ᤽")):
                self.command_executor._url = bstack1111ll1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ᤾") + bstack1l1lll1lll_opy_ + bstack1111ll1_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ᤿")
            else:
                self.command_executor._url = bstack1111ll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ᥀") + bstack1lllllllll_opy_ + bstack1111ll1_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ᥁")
            logger.debug(bstack1lllll111_opy_.format(bstack1lllllllll_opy_))
        else:
            logger.debug(bstack1llllll1ll_opy_.format(bstack1111ll1_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ᥂")))
    except Exception as e:
        logger.debug(bstack1llllll1ll_opy_.format(e))
    bstack11l111ll1_opy_ = self.session_id
    if bstack1111ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭᥃") in bstack1ll1l11ll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1111ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ᥄"), None)
        if item:
            bstack1ll111l1l1l_opy_ = getattr(item, bstack1111ll1_opy_ (u"ࠨࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࡤࡹࡴࡢࡴࡷࡩࡩ࠭᥅"), False)
            if not getattr(item, bstack1111ll1_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ᥆"), None) and bstack1ll111l1l1l_opy_:
                setattr(store[bstack1111ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ᥇")], bstack1111ll1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ᥈"), self)
        bstack1l1111l11_opy_.bstack1ll111l11_opy_(self)
    bstack111lll1ll_opy_.append(self)
    if bstack1111ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᥉") in CONFIG and bstack1111ll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᥊") in CONFIG[bstack1111ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᥋")][bstack1l1l11l111_opy_]:
        bstack111111ll_opy_ = CONFIG[bstack1111ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᥌")][bstack1l1l11l111_opy_][bstack1111ll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᥍")]
    logger.debug(bstack11l111l11_opy_.format(bstack11l111ll1_opy_))
def bstack11l1ll11l_opy_(self, url):
    global bstack1l1llll11_opy_
    global CONFIG
    try:
        bstack1111l1l11_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l11lll1l1_opy_.format(str(err)))
    try:
        bstack1l1llll11_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1111111_opy_ = str(e)
            if any(err_msg in bstack1l1111111_opy_ for err_msg in bstack1111ll1l1_opy_):
                bstack1111l1l11_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l11lll1l1_opy_.format(str(err)))
        raise e
def bstack1l1ll11l_opy_(item, when):
    global bstack1llll11111_opy_
    try:
        bstack1llll11111_opy_(item, when)
    except Exception as e:
        pass
def bstack1llll1ll_opy_(item, call, rep):
    global bstack1lll1lll1_opy_
    global bstack111lll1ll_opy_
    name = bstack1111ll1_opy_ (u"ࠪࠫ᥎")
    try:
        if rep.when == bstack1111ll1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ᥏"):
            bstack11l111ll1_opy_ = threading.current_thread().bstackSessionId
            bstack1ll11l11ll1_opy_ = item.config.getoption(bstack1111ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᥐ"))
            try:
                if (str(bstack1ll11l11ll1_opy_).lower() != bstack1111ll1_opy_ (u"࠭ࡴࡳࡷࡨࠫᥑ")):
                    name = str(rep.nodeid)
                    bstack1l11ll1ll1_opy_ = bstack1ll1ll111_opy_(bstack1111ll1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᥒ"), name, bstack1111ll1_opy_ (u"ࠨࠩᥓ"), bstack1111ll1_opy_ (u"ࠩࠪᥔ"), bstack1111ll1_opy_ (u"ࠪࠫᥕ"), bstack1111ll1_opy_ (u"ࠫࠬᥖ"))
                    os.environ[bstack1111ll1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᥗ")] = name
                    for driver in bstack111lll1ll_opy_:
                        if bstack11l111ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l11ll1ll1_opy_)
            except Exception as e:
                logger.debug(bstack1111ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ᥘ").format(str(e)))
            try:
                bstack1lllll1ll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1111ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᥙ"):
                    status = bstack1111ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᥚ") if rep.outcome.lower() == bstack1111ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᥛ") else bstack1111ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᥜ")
                    reason = bstack1111ll1_opy_ (u"ࠫࠬᥝ")
                    if status == bstack1111ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᥞ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1111ll1_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᥟ") if status == bstack1111ll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᥠ") else bstack1111ll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᥡ")
                    data = name + bstack1111ll1_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫᥢ") if status == bstack1111ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᥣ") else name + bstack1111ll1_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧᥤ") + reason
                    bstack11lllllll1_opy_ = bstack1ll1ll111_opy_(bstack1111ll1_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧᥥ"), bstack1111ll1_opy_ (u"࠭ࠧᥦ"), bstack1111ll1_opy_ (u"ࠧࠨᥧ"), bstack1111ll1_opy_ (u"ࠨࠩᥨ"), level, data)
                    for driver in bstack111lll1ll_opy_:
                        if bstack11l111ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack11lllllll1_opy_)
            except Exception as e:
                logger.debug(bstack1111ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ᥩ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1111ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧᥪ").format(str(e)))
    bstack1lll1lll1_opy_(item, call, rep)
notset = Notset()
def bstack1l1l1lll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1ll1ll1l_opy_
    if str(name).lower() == bstack1111ll1_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫᥫ"):
        return bstack1111ll1_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦᥬ")
    else:
        return bstack1ll1ll1l_opy_(self, name, default, skip)
def bstack111l1l1ll_opy_(self):
    global CONFIG
    global bstack1lll1l1l1_opy_
    try:
        proxy = bstack1lll11llll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1111ll1_opy_ (u"࠭࠮ࡱࡣࡦࠫᥭ")):
                proxies = bstack11l1l1111_opy_(proxy, bstack1l11lllll1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1llll111ll_opy_ = proxies.popitem()
                    if bstack1111ll1_opy_ (u"ࠢ࠻࠱࠲ࠦ᥮") in bstack1llll111ll_opy_:
                        return bstack1llll111ll_opy_
                    else:
                        return bstack1111ll1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ᥯") + bstack1llll111ll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1111ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨᥰ").format(str(e)))
    return bstack1lll1l1l1_opy_(self)
def bstack1ll111111l_opy_():
    return (bstack1111ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᥱ") in CONFIG or bstack1111ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᥲ") in CONFIG) and bstack1l1l11ll_opy_() and bstack111l11ll1_opy_() >= version.parse(
        bstack1lll11l111_opy_)
def bstack11l1ll11_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack111111ll_opy_
    global bstack111l1l11l_opy_
    global bstack1ll1l11ll_opy_
    CONFIG[bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᥳ")] = str(bstack1ll1l11ll_opy_) + str(__version__)
    bstack1l1l11l111_opy_ = 0
    try:
        if bstack111l1l11l_opy_ is True:
            bstack1l1l11l111_opy_ = int(os.environ.get(bstack1111ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᥴ")))
    except:
        bstack1l1l11l111_opy_ = 0
    CONFIG[bstack1111ll1_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ᥵")] = True
    bstack11l1llll_opy_ = bstack1l1lll11_opy_(CONFIG, bstack1l1l11l111_opy_)
    logger.debug(bstack11l1111l_opy_.format(str(bstack11l1llll_opy_)))
    if CONFIG.get(bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ᥶")):
        bstack1ll11lll_opy_(bstack11l1llll_opy_, bstack1l11l11lll_opy_)
    if bstack1111ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᥷") in CONFIG and bstack1111ll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᥸") in CONFIG[bstack1111ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᥹")][bstack1l1l11l111_opy_]:
        bstack111111ll_opy_ = CONFIG[bstack1111ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᥺")][bstack1l1l11l111_opy_][bstack1111ll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᥻")]
    import urllib
    import json
    bstack111l1l1l1_opy_ = bstack1111ll1_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩ᥼") + urllib.parse.quote(json.dumps(bstack11l1llll_opy_))
    browser = self.connect(bstack111l1l1l1_opy_)
    return browser
def bstack1lll11l11_opy_():
    global bstack1l1l11l1ll_opy_
    global bstack1ll1l11ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11l1l1l1l_opy_
        if not bstack1111l1ll11_opy_():
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
def bstack1ll11l11lll_opy_():
    global CONFIG
    global bstack1l1lll1111_opy_
    global bstack1l1lll1lll_opy_
    global bstack1l11l11lll_opy_
    global bstack111l1l11l_opy_
    global bstack1l1111l1l1_opy_
    CONFIG = json.loads(os.environ.get(bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧ᥽")))
    bstack1l1lll1111_opy_ = eval(os.environ.get(bstack1111ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ᥾")))
    bstack1l1lll1lll_opy_ = os.environ.get(bstack1111ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪ᥿"))
    bstack111ll11l_opy_(CONFIG, bstack1l1lll1111_opy_)
    bstack1l1111l1l1_opy_ = bstack1111111ll_opy_.bstack11ll11l1_opy_(CONFIG, bstack1l1111l1l1_opy_)
    global bstack1lll11l1l1_opy_
    global bstack1l111ll11l_opy_
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
    except Exception as e:
        pass
    if (bstack1111ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᦀ") in CONFIG or bstack1111ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᦁ") in CONFIG) and bstack1l1l11ll_opy_():
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
        logger.debug(bstack1111ll1_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧᦂ"))
    bstack1l11l11lll_opy_ = CONFIG.get(bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᦃ"), {}).get(bstack1111ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᦄ"))
    bstack111l1l11l_opy_ = True
    bstack1lll1l1ll_opy_(bstack1l1ll111l1_opy_)
if (bstack1111111lll_opy_()):
    bstack1ll11l11lll_opy_()
@bstack11l1lll111_opy_(class_method=False)
def bstack1ll111l1ll1_opy_(hook_name, event, bstack1ll111ll111_opy_=None):
    if hook_name not in [bstack1111ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᦅ"), bstack1111ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᦆ"), bstack1111ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪᦇ"), bstack1111ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧᦈ"), bstack1111ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᦉ"), bstack1111ll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᦊ"), bstack1111ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᦋ"), bstack1111ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᦌ")]:
        return
    node = store[bstack1111ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᦍ")]
    if hook_name in [bstack1111ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪᦎ"), bstack1111ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧᦏ")]:
        node = store[bstack1111ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬᦐ")]
    elif hook_name in [bstack1111ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᦑ"), bstack1111ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᦒ")]:
        node = store[bstack1111ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧᦓ")]
    if event == bstack1111ll1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᦔ"):
        hook_type = bstack1lll11l1lll_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11ll1ll1l1_opy_ = {
            bstack1111ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩᦕ"): uuid,
            bstack1111ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᦖ"): bstack111lll1l_opy_(),
            bstack1111ll1_opy_ (u"࠭ࡴࡺࡲࡨࠫᦗ"): bstack1111ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᦘ"),
            bstack1111ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᦙ"): hook_type,
            bstack1111ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᦚ"): hook_name
        }
        store[bstack1111ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᦛ")].append(uuid)
        bstack1ll11ll11l1_opy_ = node.nodeid
        if hook_type == bstack1111ll1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᦜ"):
            if not _11ll11l1l1_opy_.get(bstack1ll11ll11l1_opy_, None):
                _11ll11l1l1_opy_[bstack1ll11ll11l1_opy_] = {bstack1111ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᦝ"): []}
            _11ll11l1l1_opy_[bstack1ll11ll11l1_opy_][bstack1111ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᦞ")].append(bstack11ll1ll1l1_opy_[bstack1111ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᦟ")])
        _11ll11l1l1_opy_[bstack1ll11ll11l1_opy_ + bstack1111ll1_opy_ (u"ࠨ࠯ࠪᦠ") + hook_name] = bstack11ll1ll1l1_opy_
        bstack1ll11l1ll1l_opy_(node, bstack11ll1ll1l1_opy_, bstack1111ll1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᦡ"))
    elif event == bstack1111ll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᦢ"):
        bstack11llll1111_opy_ = node.nodeid + bstack1111ll1_opy_ (u"ࠫ࠲࠭ᦣ") + hook_name
        _11ll11l1l1_opy_[bstack11llll1111_opy_][bstack1111ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᦤ")] = bstack111lll1l_opy_()
        bstack1ll111lll1l_opy_(_11ll11l1l1_opy_[bstack11llll1111_opy_][bstack1111ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᦥ")])
        bstack1ll11l1ll1l_opy_(node, _11ll11l1l1_opy_[bstack11llll1111_opy_], bstack1111ll1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᦦ"), bstack1ll11l1l11l_opy_=bstack1ll111ll111_opy_)
def bstack1ll11l11111_opy_():
    global bstack1ll11l1llll_opy_
    if bstack1ll11l1lll_opy_():
        bstack1ll11l1llll_opy_ = bstack1111ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᦧ")
    else:
        bstack1ll11l1llll_opy_ = bstack1111ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᦨ")
@bstack1l1111l11_opy_.bstack1ll1l1lll1l_opy_
def bstack1ll111l1lll_opy_():
    bstack1ll11l11111_opy_()
    if bstack1l1l11ll_opy_():
        bstack1l1l1l1lll_opy_(bstack1l11l1lll_opy_)
    try:
        bstack1llllllllll_opy_(bstack1ll111l1ll1_opy_)
    except Exception as e:
        logger.debug(bstack1111ll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦᦩ").format(e))
bstack1ll111l1lll_opy_()