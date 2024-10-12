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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11ll11111l_opy_ import RobotHandler
from bstack_utils.capture import bstack11lll11lll_opy_
from bstack_utils.bstack11lll1111l_opy_ import bstack11l1ll1l1l_opy_, bstack11lll1l11l_opy_, bstack11lll1ll1l_opy_
from bstack_utils.bstack1111lll11_opy_ import bstack11lll1lll_opy_
from bstack_utils.bstack1ll1lllll_opy_ import bstack1l1111l11_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1llll1l11_opy_, bstack111lll1l_opy_, Result, \
    bstack11l1lll111_opy_, bstack11l1lll1ll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1111ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩณ"): [],
        bstack1111ll1_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬด"): [],
        bstack1111ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫต"): []
    }
    bstack11ll1ll11l_opy_ = []
    bstack11ll11llll_opy_ = []
    @staticmethod
    def bstack11lll11l1l_opy_(log):
        if not (log[bstack1111ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩถ")] and log[bstack1111ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪท")].strip()):
            return
        active = bstack11lll1lll_opy_.bstack11llll1l1l_opy_()
        log = {
            bstack1111ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩธ"): log[bstack1111ll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪน")],
            bstack1111ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨบ"): bstack11l1lll1ll_opy_().isoformat() + bstack1111ll1_opy_ (u"࡚࠭ࠨป"),
            bstack1111ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨผ"): log[bstack1111ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩฝ")],
        }
        if active:
            if active[bstack1111ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧพ")] == bstack1111ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨฟ"):
                log[bstack1111ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫภ")] = active[bstack1111ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬม")]
            elif active[bstack1111ll1_opy_ (u"࠭ࡴࡺࡲࡨࠫย")] == bstack1111ll1_opy_ (u"ࠧࡵࡧࡶࡸࠬร"):
                log[bstack1111ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨฤ")] = active[bstack1111ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩล")]
        bstack1l1111l11_opy_.bstack1l1111l1_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._11ll11l1ll_opy_ = None
        self._11ll1ll1ll_opy_ = None
        self._11ll11l1l1_opy_ = OrderedDict()
        self.bstack11llll1lll_opy_ = bstack11lll11lll_opy_(self.bstack11lll11l1l_opy_)
    @bstack11l1lll111_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11ll1l11l1_opy_()
        if not self._11ll11l1l1_opy_.get(attrs.get(bstack1111ll1_opy_ (u"ࠪ࡭ࡩ࠭ฦ")), None):
            self._11ll11l1l1_opy_[attrs.get(bstack1111ll1_opy_ (u"ࠫ࡮ࡪࠧว"))] = {}
        bstack11l1ll1111_opy_ = bstack11lll1ll1l_opy_(
                bstack11ll1l11ll_opy_=attrs.get(bstack1111ll1_opy_ (u"ࠬ࡯ࡤࠨศ")),
                name=name,
                bstack11ll1lllll_opy_=bstack111lll1l_opy_(),
                file_path=os.path.relpath(attrs[bstack1111ll1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ษ")], start=os.getcwd()) if attrs.get(bstack1111ll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧส")) != bstack1111ll1_opy_ (u"ࠨࠩห") else bstack1111ll1_opy_ (u"ࠩࠪฬ"),
                framework=bstack1111ll1_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩอ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1111ll1_opy_ (u"ࠫ࡮ࡪࠧฮ"), None)
        self._11ll11l1l1_opy_[attrs.get(bstack1111ll1_opy_ (u"ࠬ࡯ࡤࠨฯ"))][bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩะ")] = bstack11l1ll1111_opy_
    @bstack11l1lll111_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11l1ll111l_opy_()
        self._11l1llll11_opy_(messages)
        for bstack11ll1l1l1l_opy_ in self.bstack11ll1ll11l_opy_:
            bstack11ll1l1l1l_opy_[bstack1111ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩั")][bstack1111ll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧา")].extend(self.store[bstack1111ll1_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨำ")])
            bstack1l1111l11_opy_.bstack11l1llll1l_opy_(bstack11ll1l1l1l_opy_)
        self.bstack11ll1ll11l_opy_ = []
        self.store[bstack1111ll1_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩิ")] = []
    @bstack11l1lll111_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11llll1lll_opy_.start()
        if not self._11ll11l1l1_opy_.get(attrs.get(bstack1111ll1_opy_ (u"ࠫ࡮ࡪࠧี")), None):
            self._11ll11l1l1_opy_[attrs.get(bstack1111ll1_opy_ (u"ࠬ࡯ࡤࠨึ"))] = {}
        driver = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬื"), None)
        bstack11lll1111l_opy_ = bstack11lll1ll1l_opy_(
            bstack11ll1l11ll_opy_=attrs.get(bstack1111ll1_opy_ (u"ࠧࡪࡦุࠪ")),
            name=name,
            bstack11ll1lllll_opy_=bstack111lll1l_opy_(),
            file_path=os.path.relpath(attrs[bstack1111ll1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨู")], start=os.getcwd()),
            scope=RobotHandler.bstack11ll111111_opy_(attrs.get(bstack1111ll1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦฺࠩ"), None)),
            framework=bstack1111ll1_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ฻"),
            tags=attrs[bstack1111ll1_opy_ (u"ࠫࡹࡧࡧࡴࠩ฼")],
            hooks=self.store[bstack1111ll1_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫ฽")],
            bstack11lll1ll11_opy_=bstack1l1111l11_opy_.bstack11ll1llll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1111ll1_opy_ (u"ࠨࡻࡾࠢ࡟ࡲࠥࢁࡽࠣ฾").format(bstack1111ll1_opy_ (u"ࠢࠡࠤ฿").join(attrs[bstack1111ll1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭เ")]), name) if attrs[bstack1111ll1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧแ")] else name
        )
        self._11ll11l1l1_opy_[attrs.get(bstack1111ll1_opy_ (u"ࠪ࡭ࡩ࠭โ"))][bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧใ")] = bstack11lll1111l_opy_
        threading.current_thread().current_test_uuid = bstack11lll1111l_opy_.bstack11ll111lll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1111ll1_opy_ (u"ࠬ࡯ࡤࠨไ"), None)
        self.bstack11lll11111_opy_(bstack1111ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧๅ"), bstack11lll1111l_opy_)
    @bstack11l1lll111_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11llll1lll_opy_.reset()
        bstack11ll11l111_opy_ = bstack11l1ll11l1_opy_.get(attrs.get(bstack1111ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧๆ")), bstack1111ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ็"))
        self._11ll11l1l1_opy_[attrs.get(bstack1111ll1_opy_ (u"ࠩ࡬ࡨ่ࠬ"))][bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ้࠭")].stop(time=bstack111lll1l_opy_(), duration=int(attrs.get(bstack1111ll1_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦ๊ࠩ"), bstack1111ll1_opy_ (u"ࠬ࠶๋ࠧ"))), result=Result(result=bstack11ll11l111_opy_, exception=attrs.get(bstack1111ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ์")), bstack11lll111ll_opy_=[attrs.get(bstack1111ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨํ"))]))
        self.bstack11lll11111_opy_(bstack1111ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ๎"), self._11ll11l1l1_opy_[attrs.get(bstack1111ll1_opy_ (u"ࠩ࡬ࡨࠬ๏"))][bstack1111ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭๐")], True)
        self.store[bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ๑")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11l1lll111_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11ll1l11l1_opy_()
        current_test_id = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧ๒"), None)
        bstack11l1l1lll1_opy_ = current_test_id if bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨ๓"), None) else bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪ๔"), None)
        if attrs.get(bstack1111ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭๕"), bstack1111ll1_opy_ (u"ࠩࠪ๖")).lower() in [bstack1111ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ๗"), bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭๘")]:
            hook_type = bstack11l1llllll_opy_(attrs.get(bstack1111ll1_opy_ (u"ࠬࡺࡹࡱࡧࠪ๙")), bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ๚"), None))
            hook_name = bstack1111ll1_opy_ (u"ࠧࡼࡿࠪ๛").format(attrs.get(bstack1111ll1_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ๜"), bstack1111ll1_opy_ (u"ࠩࠪ๝")))
            if hook_type in [bstack1111ll1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ๞"), bstack1111ll1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ๟")]:
                hook_name = bstack1111ll1_opy_ (u"ࠬࡡࡻࡾ࡟ࠣࡿࢂ࠭๠").format(bstack11ll11l11l_opy_.get(hook_type), attrs.get(bstack1111ll1_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭๡"), bstack1111ll1_opy_ (u"ࠧࠨ๢")))
            bstack11ll1ll1l1_opy_ = bstack11lll1l11l_opy_(
                bstack11ll1l11ll_opy_=bstack11l1l1lll1_opy_ + bstack1111ll1_opy_ (u"ࠨ࠯ࠪ๣") + attrs.get(bstack1111ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ๤"), bstack1111ll1_opy_ (u"ࠪࠫ๥")).lower(),
                name=hook_name,
                bstack11ll1lllll_opy_=bstack111lll1l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1111ll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ๦")), start=os.getcwd()),
                framework=bstack1111ll1_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫ๧"),
                tags=attrs[bstack1111ll1_opy_ (u"࠭ࡴࡢࡩࡶࠫ๨")],
                scope=RobotHandler.bstack11ll111111_opy_(attrs.get(bstack1111ll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ๩"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11ll1ll1l1_opy_.bstack11ll111lll_opy_()
            threading.current_thread().current_hook_id = bstack11l1l1lll1_opy_ + bstack1111ll1_opy_ (u"ࠨ࠯ࠪ๪") + attrs.get(bstack1111ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ๫"), bstack1111ll1_opy_ (u"ࠪࠫ๬")).lower()
            self.store[bstack1111ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ๭")] = [bstack11ll1ll1l1_opy_.bstack11ll111lll_opy_()]
            if bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ๮"), None):
                self.store[bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ๯")].append(bstack11ll1ll1l1_opy_.bstack11ll111lll_opy_())
            else:
                self.store[bstack1111ll1_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭๰")].append(bstack11ll1ll1l1_opy_.bstack11ll111lll_opy_())
            if bstack11l1l1lll1_opy_:
                self._11ll11l1l1_opy_[bstack11l1l1lll1_opy_ + bstack1111ll1_opy_ (u"ࠨ࠯ࠪ๱") + attrs.get(bstack1111ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ๲"), bstack1111ll1_opy_ (u"ࠪࠫ๳")).lower()] = { bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ๴"): bstack11ll1ll1l1_opy_ }
            bstack1l1111l11_opy_.bstack11lll11111_opy_(bstack1111ll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭๵"), bstack11ll1ll1l1_opy_)
        else:
            bstack11lll1l111_opy_ = {
                bstack1111ll1_opy_ (u"࠭ࡩࡥࠩ๶"): uuid4().__str__(),
                bstack1111ll1_opy_ (u"ࠧࡵࡧࡻࡸࠬ๷"): bstack1111ll1_opy_ (u"ࠨࡽࢀࠤࢀࢃࠧ๸").format(attrs.get(bstack1111ll1_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ๹")), attrs.get(bstack1111ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ๺"), bstack1111ll1_opy_ (u"ࠫࠬ๻"))) if attrs.get(bstack1111ll1_opy_ (u"ࠬࡧࡲࡨࡵࠪ๼"), []) else attrs.get(bstack1111ll1_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭๽")),
                bstack1111ll1_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧ๾"): attrs.get(bstack1111ll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭๿"), []),
                bstack1111ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭຀"): bstack111lll1l_opy_(),
                bstack1111ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪກ"): bstack1111ll1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬຂ"),
                bstack1111ll1_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ຃"): attrs.get(bstack1111ll1_opy_ (u"࠭ࡤࡰࡥࠪຄ"), bstack1111ll1_opy_ (u"ࠧࠨ຅"))
            }
            if attrs.get(bstack1111ll1_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩຆ"), bstack1111ll1_opy_ (u"ࠩࠪງ")) != bstack1111ll1_opy_ (u"ࠪࠫຈ"):
                bstack11lll1l111_opy_[bstack1111ll1_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬຉ")] = attrs.get(bstack1111ll1_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭ຊ"))
            if not self.bstack11ll11llll_opy_:
                self._11ll11l1l1_opy_[self._11ll11lll1_opy_()][bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ຋")].add_step(bstack11lll1l111_opy_)
                threading.current_thread().current_step_uuid = bstack11lll1l111_opy_[bstack1111ll1_opy_ (u"ࠧࡪࡦࠪຌ")]
            self.bstack11ll11llll_opy_.append(bstack11lll1l111_opy_)
    @bstack11l1lll111_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11l1ll111l_opy_()
        self._11l1llll11_opy_(messages)
        current_test_id = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪຍ"), None)
        bstack11l1l1lll1_opy_ = current_test_id if current_test_id else bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬຎ"), None)
        bstack11ll111l1l_opy_ = bstack11l1ll11l1_opy_.get(attrs.get(bstack1111ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪຏ")), bstack1111ll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬຐ"))
        bstack11ll111ll1_opy_ = attrs.get(bstack1111ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ຑ"))
        if bstack11ll111l1l_opy_ != bstack1111ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧຒ") and not attrs.get(bstack1111ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຓ")) and self._11ll11l1ll_opy_:
            bstack11ll111ll1_opy_ = self._11ll11l1ll_opy_
        bstack11lll11ll1_opy_ = Result(result=bstack11ll111l1l_opy_, exception=bstack11ll111ll1_opy_, bstack11lll111ll_opy_=[bstack11ll111ll1_opy_])
        if attrs.get(bstack1111ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ດ"), bstack1111ll1_opy_ (u"ࠩࠪຕ")).lower() in [bstack1111ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩຖ"), bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ທ")]:
            bstack11l1l1lll1_opy_ = current_test_id if current_test_id else bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨຘ"), None)
            if bstack11l1l1lll1_opy_:
                bstack11llll1111_opy_ = bstack11l1l1lll1_opy_ + bstack1111ll1_opy_ (u"ࠨ࠭ࠣນ") + attrs.get(bstack1111ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬບ"), bstack1111ll1_opy_ (u"ࠨࠩປ")).lower()
                self._11ll11l1l1_opy_[bstack11llll1111_opy_][bstack1111ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬຜ")].stop(time=bstack111lll1l_opy_(), duration=int(attrs.get(bstack1111ll1_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨຝ"), bstack1111ll1_opy_ (u"ࠫ࠵࠭ພ"))), result=bstack11lll11ll1_opy_)
                bstack1l1111l11_opy_.bstack11lll11111_opy_(bstack1111ll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧຟ"), self._11ll11l1l1_opy_[bstack11llll1111_opy_][bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩຠ")])
        else:
            bstack11l1l1lll1_opy_ = current_test_id if current_test_id else bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡩࡥࠩມ"), None)
            if bstack11l1l1lll1_opy_ and len(self.bstack11ll11llll_opy_) == 1:
                current_step_uuid = bstack1llll1l11_opy_(threading.current_thread(), bstack1111ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬຢ"), None)
                self._11ll11l1l1_opy_[bstack11l1l1lll1_opy_][bstack1111ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬຣ")].bstack11lll1lll1_opy_(current_step_uuid, duration=int(attrs.get(bstack1111ll1_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨ຤"), bstack1111ll1_opy_ (u"ࠫ࠵࠭ລ"))), result=bstack11lll11ll1_opy_)
            else:
                self.bstack11l1lll1l1_opy_(attrs)
            self.bstack11ll11llll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1111ll1_opy_ (u"ࠬ࡮ࡴ࡮࡮ࠪ຦"), bstack1111ll1_opy_ (u"࠭࡮ࡰࠩວ")) == bstack1111ll1_opy_ (u"ࠧࡺࡧࡶࠫຨ"):
                return
            self.messages.push(message)
            bstack11ll11ll11_opy_ = []
            if bstack11lll1lll_opy_.bstack11llll1l1l_opy_():
                bstack11ll11ll11_opy_.append({
                    bstack1111ll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫຩ"): bstack111lll1l_opy_(),
                    bstack1111ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪສ"): message.get(bstack1111ll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫຫ")),
                    bstack1111ll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪຬ"): message.get(bstack1111ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫອ")),
                    **bstack11lll1lll_opy_.bstack11llll1l1l_opy_()
                })
                if len(bstack11ll11ll11_opy_) > 0:
                    bstack1l1111l11_opy_.bstack1l1111l1_opy_(bstack11ll11ll11_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1l1111l11_opy_.bstack11l1ll1lll_opy_()
    def bstack11l1lll1l1_opy_(self, bstack11ll1111ll_opy_):
        if not bstack11lll1lll_opy_.bstack11llll1l1l_opy_():
            return
        kwname = bstack1111ll1_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬຮ").format(bstack11ll1111ll_opy_.get(bstack1111ll1_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧຯ")), bstack11ll1111ll_opy_.get(bstack1111ll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ະ"), bstack1111ll1_opy_ (u"ࠩࠪັ"))) if bstack11ll1111ll_opy_.get(bstack1111ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨາ"), []) else bstack11ll1111ll_opy_.get(bstack1111ll1_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫຳ"))
        error_message = bstack1111ll1_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠤࢁࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡠࠧࢁ࠲ࡾ࡞ࠥࠦິ").format(kwname, bstack11ll1111ll_opy_.get(bstack1111ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ີ")), str(bstack11ll1111ll_opy_.get(bstack1111ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຶ"))))
        bstack11ll1lll1l_opy_ = bstack1111ll1_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠢື").format(kwname, bstack11ll1111ll_opy_.get(bstack1111ll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴຸࠩ")))
        bstack11ll1111l1_opy_ = error_message if bstack11ll1111ll_opy_.get(bstack1111ll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨູࠫ")) else bstack11ll1lll1l_opy_
        bstack11ll1l1l11_opy_ = {
            bstack1111ll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶ຺ࠧ"): self.bstack11ll11llll_opy_[-1].get(bstack1111ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩົ"), bstack111lll1l_opy_()),
            bstack1111ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧຼ"): bstack11ll1111l1_opy_,
            bstack1111ll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ຽ"): bstack1111ll1_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧ຾") if bstack11ll1111ll_opy_.get(bstack1111ll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ຿")) == bstack1111ll1_opy_ (u"ࠪࡊࡆࡏࡌࠨເ") else bstack1111ll1_opy_ (u"ࠫࡎࡔࡆࡐࠩແ"),
            **bstack11lll1lll_opy_.bstack11llll1l1l_opy_()
        }
        bstack1l1111l11_opy_.bstack1l1111l1_opy_([bstack11ll1l1l11_opy_])
    def _11ll11lll1_opy_(self):
        for bstack11ll1l11ll_opy_ in reversed(self._11ll11l1l1_opy_):
            bstack11ll1l111l_opy_ = bstack11ll1l11ll_opy_
            data = self._11ll11l1l1_opy_[bstack11ll1l11ll_opy_][bstack1111ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨໂ")]
            if isinstance(data, bstack11lll1l11l_opy_):
                if not bstack1111ll1_opy_ (u"࠭ࡅࡂࡅࡋࠫໃ") in data.bstack11l1l1ll1l_opy_():
                    return bstack11ll1l111l_opy_
            else:
                return bstack11ll1l111l_opy_
    def _11l1llll11_opy_(self, messages):
        try:
            bstack11ll1ll111_opy_ = BuiltIn().get_variable_value(bstack1111ll1_opy_ (u"ࠢࠥࡽࡏࡓࡌࠦࡌࡆࡘࡈࡐࢂࠨໄ")) in (bstack11l1lllll1_opy_.DEBUG, bstack11l1lllll1_opy_.TRACE)
            for message, bstack11ll1l1111_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1111ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ໅"))
                level = message.get(bstack1111ll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨໆ"))
                if level == bstack11l1lllll1_opy_.FAIL:
                    self._11ll11l1ll_opy_ = name or self._11ll11l1ll_opy_
                    self._11ll1ll1ll_opy_ = bstack11ll1l1111_opy_.get(bstack1111ll1_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦ໇")) if bstack11ll1ll111_opy_ and bstack11ll1l1111_opy_ else self._11ll1ll1ll_opy_
        except:
            pass
    @classmethod
    def bstack11lll11111_opy_(self, event: str, bstack11l1ll1l11_opy_: bstack11l1ll1l1l_opy_, bstack11ll111l11_opy_=False):
        if event == bstack1111ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ່࠭"):
            bstack11l1ll1l11_opy_.set(hooks=self.store[bstack1111ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴ້ࠩ")])
        if event == bstack1111ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪ໊ࠧ"):
            event = bstack1111ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥ໋ࠩ")
        if bstack11ll111l11_opy_:
            bstack11ll1lll11_opy_ = {
                bstack1111ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ໌"): event,
                bstack11l1ll1l11_opy_.bstack11ll1l1lll_opy_(): bstack11l1ll1l11_opy_.bstack11l1lll11l_opy_(event)
            }
            self.bstack11ll1ll11l_opy_.append(bstack11ll1lll11_opy_)
        else:
            bstack1l1111l11_opy_.bstack11lll11111_opy_(event, bstack11l1ll1l11_opy_)
class Messages:
    def __init__(self):
        self._11l1l1llll_opy_ = []
    def bstack11ll1l11l1_opy_(self):
        self._11l1l1llll_opy_.append([])
    def bstack11l1ll111l_opy_(self):
        return self._11l1l1llll_opy_.pop() if self._11l1l1llll_opy_ else list()
    def push(self, message):
        self._11l1l1llll_opy_[-1].append(message) if self._11l1l1llll_opy_ else self._11l1l1llll_opy_.append([message])
class bstack11l1lllll1_opy_:
    FAIL = bstack1111ll1_opy_ (u"ࠩࡉࡅࡎࡒࠧໍ")
    ERROR = bstack1111ll1_opy_ (u"ࠪࡉࡗࡘࡏࡓࠩ໎")
    WARNING = bstack1111ll1_opy_ (u"ࠫ࡜ࡇࡒࡏࠩ໏")
    bstack11ll1l1ll1_opy_ = bstack1111ll1_opy_ (u"ࠬࡏࡎࡇࡑࠪ໐")
    DEBUG = bstack1111ll1_opy_ (u"࠭ࡄࡆࡄࡘࡋࠬ໑")
    TRACE = bstack1111ll1_opy_ (u"ࠧࡕࡔࡄࡇࡊ࠭໒")
    bstack11l1ll1ll1_opy_ = [FAIL, ERROR]
def bstack11l1ll11ll_opy_(bstack11ll11ll1l_opy_):
    if not bstack11ll11ll1l_opy_:
        return None
    if bstack11ll11ll1l_opy_.get(bstack1111ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ໓"), None):
        return getattr(bstack11ll11ll1l_opy_[bstack1111ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ໔")], bstack1111ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ໕"), None)
    return bstack11ll11ll1l_opy_.get(bstack1111ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩ໖"), None)
def bstack11l1llllll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1111ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ໗"), bstack1111ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ໘")]:
        return
    if hook_type.lower() == bstack1111ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭໙"):
        if current_test_uuid is None:
            return bstack1111ll1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ໚")
        else:
            return bstack1111ll1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ໛")
    elif hook_type.lower() == bstack1111ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬໜ"):
        if current_test_uuid is None:
            return bstack1111ll1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧໝ")
        else:
            return bstack1111ll1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩໞ")