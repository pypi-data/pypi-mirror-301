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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111l1l111l_opy_
from browserstack_sdk.bstack1l111111_opy_ import bstack11llll1l_opy_
def _1111111l11_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1llllllllll_opy_:
    def __init__(self, handler):
        self._1lllllllll1_opy_ = {}
        self._1lllllll1l1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11llll1l_opy_.version()
        if bstack111l1l111l_opy_(pytest_version, bstack1111ll1_opy_ (u"ࠨ࠸࠯࠳࠱࠵ࠧᑺ")) >= 0:
            self._1lllllllll1_opy_[bstack1111ll1_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᑻ")] = Module._register_setup_function_fixture
            self._1lllllllll1_opy_[bstack1111ll1_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑼ")] = Module._register_setup_module_fixture
            self._1lllllllll1_opy_[bstack1111ll1_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑽ")] = Class._register_setup_class_fixture
            self._1lllllllll1_opy_[bstack1111ll1_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᑾ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1lllllll11l_opy_(bstack1111ll1_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑿ"))
            Module._register_setup_module_fixture = self.bstack1lllllll11l_opy_(bstack1111ll1_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᒀ"))
            Class._register_setup_class_fixture = self.bstack1lllllll11l_opy_(bstack1111ll1_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᒁ"))
            Class._register_setup_method_fixture = self.bstack1lllllll11l_opy_(bstack1111ll1_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᒂ"))
        else:
            self._1lllllllll1_opy_[bstack1111ll1_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᒃ")] = Module._inject_setup_function_fixture
            self._1lllllllll1_opy_[bstack1111ll1_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᒄ")] = Module._inject_setup_module_fixture
            self._1lllllllll1_opy_[bstack1111ll1_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᒅ")] = Class._inject_setup_class_fixture
            self._1lllllllll1_opy_[bstack1111ll1_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᒆ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1lllllll11l_opy_(bstack1111ll1_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᒇ"))
            Module._inject_setup_module_fixture = self.bstack1lllllll11l_opy_(bstack1111ll1_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᒈ"))
            Class._inject_setup_class_fixture = self.bstack1lllllll11l_opy_(bstack1111ll1_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᒉ"))
            Class._inject_setup_method_fixture = self.bstack1lllllll11l_opy_(bstack1111ll1_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᒊ"))
    def bstack1llllllll1l_opy_(self, bstack11111111ll_opy_, hook_type):
        meth = getattr(bstack11111111ll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1lllllll1l1_opy_[hook_type] = meth
            setattr(bstack11111111ll_opy_, hook_type, self.bstack1llllll1ll1_opy_(hook_type))
    def bstack1lllllll111_opy_(self, instance, bstack1llllll1lll_opy_):
        if bstack1llllll1lll_opy_ == bstack1111ll1_opy_ (u"ࠤࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᒋ"):
            self.bstack1llllllll1l_opy_(instance.obj, bstack1111ll1_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦᒌ"))
            self.bstack1llllllll1l_opy_(instance.obj, bstack1111ll1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣᒍ"))
        if bstack1llllll1lll_opy_ == bstack1111ll1_opy_ (u"ࠧࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᒎ"):
            self.bstack1llllllll1l_opy_(instance.obj, bstack1111ll1_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠧᒏ"))
            self.bstack1llllllll1l_opy_(instance.obj, bstack1111ll1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠤᒐ"))
        if bstack1llllll1lll_opy_ == bstack1111ll1_opy_ (u"ࠣࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᒑ"):
            self.bstack1llllllll1l_opy_(instance.obj, bstack1111ll1_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠢᒒ"))
            self.bstack1llllllll1l_opy_(instance.obj, bstack1111ll1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠦᒓ"))
        if bstack1llllll1lll_opy_ == bstack1111ll1_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᒔ"):
            self.bstack1llllllll1l_opy_(instance.obj, bstack1111ll1_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠦᒕ"))
            self.bstack1llllllll1l_opy_(instance.obj, bstack1111ll1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠣᒖ"))
    @staticmethod
    def bstack111111111l_opy_(hook_type, func, args):
        if hook_type in [bstack1111ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᒗ"), bstack1111ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᒘ")]:
            _1111111l11_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1llllll1ll1_opy_(self, hook_type):
        def bstack1llllllll11_opy_(arg=None):
            self.handler(hook_type, bstack1111ll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩᒙ"))
            result = None
            exception = None
            try:
                self.bstack111111111l_opy_(hook_type, self._1lllllll1l1_opy_[hook_type], (arg,))
                result = Result(result=bstack1111ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᒚ"))
            except Exception as e:
                result = Result(result=bstack1111ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᒛ"), exception=e)
                self.handler(hook_type, bstack1111ll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᒜ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1111ll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᒝ"), result)
        def bstack1111111111_opy_(this, arg=None):
            self.handler(hook_type, bstack1111ll1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧᒞ"))
            result = None
            exception = None
            try:
                self.bstack111111111l_opy_(hook_type, self._1lllllll1l1_opy_[hook_type], (this, arg))
                result = Result(result=bstack1111ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᒟ"))
            except Exception as e:
                result = Result(result=bstack1111ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᒠ"), exception=e)
                self.handler(hook_type, bstack1111ll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᒡ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1111ll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᒢ"), result)
        if hook_type in [bstack1111ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᒣ"), bstack1111ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᒤ")]:
            return bstack1111111111_opy_
        return bstack1llllllll11_opy_
    def bstack1lllllll11l_opy_(self, bstack1llllll1lll_opy_):
        def bstack1lllllll1ll_opy_(this, *args, **kwargs):
            self.bstack1lllllll111_opy_(this, bstack1llllll1lll_opy_)
            self._1lllllllll1_opy_[bstack1llllll1lll_opy_](this, *args, **kwargs)
        return bstack1lllllll1ll_opy_