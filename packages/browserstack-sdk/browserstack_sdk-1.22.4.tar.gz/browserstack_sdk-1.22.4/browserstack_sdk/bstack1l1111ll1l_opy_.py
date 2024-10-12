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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11lll1111l_opy_ import bstack11lll1l11l_opy_, bstack11lll1ll1l_opy_
from bstack_utils.bstack1111lll11_opy_ import bstack11lll1lll_opy_
from bstack_utils.helper import bstack1llll1l11_opy_, bstack111lll1l_opy_, Result
from bstack_utils.bstack1ll1lllll_opy_ import bstack1l1111l11_opy_
from bstack_utils.capture import bstack11lll11lll_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1l1111ll1l_opy_:
    def __init__(self):
        self.bstack11llll1lll_opy_ = bstack11lll11lll_opy_(self.bstack11lll11l1l_opy_)
        self.tests = {}
    @staticmethod
    def bstack11lll11l1l_opy_(log):
        if not (log[bstack1111ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ෆ")] and log[bstack1111ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ෇")].strip()):
            return
        active = bstack11lll1lll_opy_.bstack11llll1l1l_opy_()
        log = {
            bstack1111ll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭෈"): log[bstack1111ll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ෉")],
            bstack1111ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴ්ࠬ"): bstack111lll1l_opy_(),
            bstack1111ll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ෋"): log[bstack1111ll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ෌")],
        }
        if active:
            if active[bstack1111ll1_opy_ (u"ࠬࡺࡹࡱࡧࠪ෍")] == bstack1111ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ෎"):
                log[bstack1111ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧා")] = active[bstack1111ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨැ")]
            elif active[bstack1111ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧෑ")] == bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࠨි"):
                log[bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫී")] = active[bstack1111ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬු")]
        bstack1l1111l11_opy_.bstack1l1111l1_opy_([log])
    def start_test(self, attrs):
        bstack11lll1l1l1_opy_ = uuid4().__str__()
        self.tests[bstack11lll1l1l1_opy_] = {}
        self.bstack11llll1lll_opy_.start()
        driver = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ෕"), None)
        bstack11lll1111l_opy_ = bstack11lll1ll1l_opy_(
            name=attrs.scenario.name,
            uuid=bstack11lll1l1l1_opy_,
            bstack11ll1lllll_opy_=bstack111lll1l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1111ll1_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣූ"),
            framework=bstack1111ll1_opy_ (u"ࠨࡄࡨ࡬ࡦࡼࡥࠨ෗"),
            scope=[attrs.feature.name],
            bstack11lll1ll11_opy_=bstack1l1111l11_opy_.bstack11ll1llll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[bstack11lll1l1l1_opy_][bstack1111ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬෘ")] = bstack11lll1111l_opy_
        threading.current_thread().current_test_uuid = bstack11lll1l1l1_opy_
        bstack1l1111l11_opy_.bstack11lll11111_opy_(bstack1111ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫෙ"), bstack11lll1111l_opy_)
    def end_test(self, attrs):
        bstack11lll1l1ll_opy_ = {
            bstack1111ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤේ"): attrs.feature.name,
            bstack1111ll1_opy_ (u"ࠧࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥෛ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11lll1111l_opy_ = self.tests[current_test_uuid][bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩො")]
        meta = {
            bstack1111ll1_opy_ (u"ࠢࡧࡧࡤࡸࡺࡸࡥࠣෝ"): bstack11lll1l1ll_opy_,
            bstack1111ll1_opy_ (u"ࠣࡵࡷࡩࡵࡹࠢෞ"): bstack11lll1111l_opy_.meta.get(bstack1111ll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨෟ"), []),
            bstack1111ll1_opy_ (u"ࠥࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ෠"): {
                bstack1111ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ෡"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11lll1111l_opy_.bstack11llll11l1_opy_(meta)
        bstack11lll1111l_opy_.bstack11llll11ll_opy_(bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ෢"), []))
        bstack11llll1l11_opy_, exception = self._11lll11l11_opy_(attrs)
        bstack11lll11ll1_opy_ = Result(result=attrs.status.name, exception=exception, bstack11lll111ll_opy_=[bstack11llll1l11_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ෣")].stop(time=bstack111lll1l_opy_(), duration=int(attrs.duration)*1000, result=bstack11lll11ll1_opy_)
        bstack1l1111l11_opy_.bstack11lll11111_opy_(bstack1111ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ෤"), self.tests[threading.current_thread().current_test_uuid][bstack1111ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ෥")])
    def bstack111l1lll_opy_(self, attrs):
        bstack11lll1l111_opy_ = {
            bstack1111ll1_opy_ (u"ࠩ࡬ࡨࠬ෦"): uuid4().__str__(),
            bstack1111ll1_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫ෧"): attrs.keyword,
            bstack1111ll1_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫ෨"): [],
            bstack1111ll1_opy_ (u"ࠬࡺࡥࡹࡶࠪ෩"): attrs.name,
            bstack1111ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ෪"): bstack111lll1l_opy_(),
            bstack1111ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ෫"): bstack1111ll1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ෬"),
            bstack1111ll1_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ෭"): bstack1111ll1_opy_ (u"ࠪࠫ෮")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ෯")].add_step(bstack11lll1l111_opy_)
        threading.current_thread().current_step_uuid = bstack11lll1l111_opy_[bstack1111ll1_opy_ (u"ࠬ࡯ࡤࠨ෰")]
    def bstack1lll111ll_opy_(self, attrs):
        current_test_id = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ෱"), None)
        current_step_uuid = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫෲ"), None)
        bstack11llll1l11_opy_, exception = self._11lll11l11_opy_(attrs)
        bstack11lll11ll1_opy_ = Result(result=attrs.status.name, exception=exception, bstack11lll111ll_opy_=[bstack11llll1l11_opy_])
        self.tests[current_test_id][bstack1111ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫෳ")].bstack11lll1lll1_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11lll11ll1_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11l1lllll_opy_(self, name, attrs):
        try:
            bstack11lll1llll_opy_ = uuid4().__str__()
            self.tests[bstack11lll1llll_opy_] = {}
            self.bstack11llll1lll_opy_.start()
            scopes = []
            driver = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ෴"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1111ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ෵")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11lll1llll_opy_)
            if name in [bstack1111ll1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ෶"), bstack1111ll1_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣ෷")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1111ll1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ෸"), bstack1111ll1_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ෹")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1111ll1_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩ෺")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack11lll1l11l_opy_(
                name=name,
                uuid=bstack11lll1llll_opy_,
                bstack11ll1lllll_opy_=bstack111lll1l_opy_(),
                file_path=file_path,
                framework=bstack1111ll1_opy_ (u"ࠤࡅࡩ࡭ࡧࡶࡦࠤ෻"),
                bstack11lll1ll11_opy_=bstack1l1111l11_opy_.bstack11ll1llll1_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1111ll1_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦ෼"),
                hook_type=name
            )
            self.tests[bstack11lll1llll_opy_][bstack1111ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠢ෽")] = hook_data
            current_test_id = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠧࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤ෾"), None)
            if current_test_id:
                hook_data.bstack11llll111l_opy_(current_test_id)
            if name == bstack1111ll1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ෿"):
                threading.current_thread().before_all_hook_uuid = bstack11lll1llll_opy_
            threading.current_thread().current_hook_uuid = bstack11lll1llll_opy_
            bstack1l1111l11_opy_.bstack11lll11111_opy_(bstack1111ll1_opy_ (u"ࠢࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠣ฀"), hook_data)
        except Exception as e:
            logger.debug(bstack1111ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤ࡭ࡵ࡯࡬ࠢࡨࡺࡪࡴࡴࡴ࠮ࠣ࡬ࡴࡵ࡫ࠡࡰࡤࡱࡪࡀࠠࠦࡵ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠪࡹࠢก"), name, e)
    def bstack1l1l1ll1l_opy_(self, attrs):
        bstack11llll1111_opy_ = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ข"), None)
        hook_data = self.tests[bstack11llll1111_opy_][bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ฃ")]
        status = bstack1111ll1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦค")
        exception = None
        bstack11llll1l11_opy_ = None
        if hook_data.name == bstack1111ll1_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣฅ"):
            self.bstack11llll1lll_opy_.reset()
            bstack11llll1ll1_opy_ = self.tests[bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ฆ"), None)][bstack1111ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪง")].result.result
            if bstack11llll1ll1_opy_ == bstack1111ll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣจ"):
                if attrs.hook_failures == 1:
                    status = bstack1111ll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤฉ")
                elif attrs.hook_failures == 2:
                    status = bstack1111ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥช")
            elif attrs.bstack11lll111l1_opy_:
                status = bstack1111ll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦซ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1111ll1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩฌ") and attrs.hook_failures == 1:
                status = bstack1111ll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨญ")
            elif hasattr(attrs, bstack1111ll1_opy_ (u"ࠧࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠧฎ")) and attrs.error_message:
                status = bstack1111ll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣฏ")
            bstack11llll1l11_opy_, exception = self._11lll11l11_opy_(attrs)
        bstack11lll11ll1_opy_ = Result(result=status, exception=exception, bstack11lll111ll_opy_=[bstack11llll1l11_opy_])
        hook_data.stop(time=bstack111lll1l_opy_(), duration=0, result=bstack11lll11ll1_opy_)
        bstack1l1111l11_opy_.bstack11lll11111_opy_(bstack1111ll1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫฐ"), self.tests[bstack11llll1111_opy_][bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ฑ")])
        threading.current_thread().current_hook_uuid = None
    def _11lll11l11_opy_(self, attrs):
        try:
            import traceback
            bstack1ll111l1l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11llll1l11_opy_ = bstack1ll111l1l_opy_[-1] if bstack1ll111l1l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1111ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡴࡶࡲࡱࠥࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࠣฒ"))
            bstack11llll1l11_opy_ = None
            exception = None
        return bstack11llll1l11_opy_, exception