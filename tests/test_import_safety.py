import importlib.util
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RuntimeOperationError(RuntimeError):
    pass


class BlockedCallable:
    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        raise RuntimeOperationError(f"blocked runtime operation called during import: {self.name}")

    def __getattr__(self, name):
        return BlockedCallable(f"{self.name}.{name}")


class BlockerModule(types.ModuleType):
    def __init__(self, name, blocked_names):
        super().__init__(name)
        self._blocked_names = set(blocked_names)

    def __getattr__(self, name):
        if name in self._blocked_names:
            return BlockedCallable(f"{self.__name__}.{name}")
        value = types.SimpleNamespace()
        setattr(self, name, value)
        return value


class FilterStub:
    def __and__(self, other):
        return self

    def __or__(self, other):
        return self

    def __invert__(self):
        return self

    def __rand__(self, other):
        return self

    def __ror__(self, other):
        return self


class WorkbookStub:
    active = types.SimpleNamespace()
    sheetnames = []

    def create_sheet(self, *args, **kwargs):
        return types.SimpleNamespace()

    def save(self, *args, **kwargs):
        raise RuntimeOperationError("openpyxl.Workbook.save called during import")

    def __getitem__(self, key):
        return types.SimpleNamespace()


def install_common_stubs(monkeypatch):
    dotenv = types.ModuleType("dotenv")
    dotenv.load_dotenv = lambda *args, **kwargs: None
    monkeypatch.setitem(sys.modules, "dotenv", dotenv)

    replicate = BlockerModule("replicate", {"run", "Client"})
    monkeypatch.setitem(sys.modules, "replicate", replicate)

    requests = BlockerModule("requests", {"get", "post"})
    monkeypatch.setitem(sys.modules, "requests", requests)

    pil = types.ModuleType("PIL")
    monkeypatch.setitem(sys.modules, "PIL", pil)
    for name in ["Image", "ImageDraw", "ImageFont"]:
        module = types.ModuleType(f"PIL.{name}")
        setattr(pil, name, module)
        monkeypatch.setitem(sys.modules, f"PIL.{name}", module)

    google = types.ModuleType("google")
    colab = types.ModuleType("google.colab")
    files = types.SimpleNamespace(download=BlockedCallable("google.colab.files.download"))
    auth = types.SimpleNamespace(authenticate_user=BlockedCallable("google.colab.auth.authenticate_user"))
    colab.files = files
    colab.auth = auth
    google.colab = colab
    monkeypatch.setitem(sys.modules, "google", google)
    monkeypatch.setitem(sys.modules, "google.colab", colab)
    monkeypatch.setitem(sys.modules, "google.colab.files", files)
    monkeypatch.setitem(sys.modules, "google.colab.auth", auth)


def install_telegram_stubs(monkeypatch):
    install_common_stubs(monkeypatch)

    nest_asyncio = types.ModuleType("nest_asyncio")
    nest_asyncio.apply = BlockedCallable("nest_asyncio.apply")
    monkeypatch.setitem(sys.modules, "nest_asyncio", nest_asyncio)

    redis = BlockerModule("redis", {"Redis"})
    redis.ConnectionError = ConnectionError
    monkeypatch.setitem(sys.modules, "redis", redis)

    openai = types.ModuleType("openai")
    openai.error = types.SimpleNamespace(AuthenticationError=Exception, OpenAIError=Exception)
    monkeypatch.setitem(sys.modules, "openai", openai)

    yagmail = BlockerModule("yagmail", {"SMTP"})
    monkeypatch.setitem(sys.modules, "yagmail", yagmail)

    openpyxl = types.ModuleType("openpyxl")
    openpyxl.Workbook = WorkbookStub
    openpyxl.load_workbook = lambda *args, **kwargs: WorkbookStub()
    monkeypatch.setitem(sys.modules, "openpyxl", openpyxl)

    translate = types.ModuleType("translate")
    translate.Translator = object
    monkeypatch.setitem(sys.modules, "translate", translate)

    langdetect = types.ModuleType("langdetect")
    langdetect.detect = lambda text: "en"
    monkeypatch.setitem(sys.modules, "langdetect", langdetect)

    telegram = types.ModuleType("telegram")
    telegram.Update = object
    monkeypatch.setitem(sys.modules, "telegram", telegram)

    telegram_ext = types.ModuleType("telegram.ext")
    telegram_ext.Application = types.SimpleNamespace(
        builder=BlockedCallable("telegram.ext.Application.builder")
    )
    telegram_ext.CommandHandler = object
    telegram_ext.MessageHandler = object
    telegram_ext.ContextTypes = types.SimpleNamespace(DEFAULT_TYPE=object)
    telegram_ext.filters = types.SimpleNamespace(
        TEXT=FilterStub(),
        COMMAND=FilterStub(),
        Regex=lambda *args, **kwargs: FilterStub(),
    )
    monkeypatch.setitem(sys.modules, "telegram.ext", telegram_ext)


def import_from_path(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_backend_scripts_are_import_safe(monkeypatch):
    install_common_stubs(monkeypatch)
    paths = sorted((ROOT / "Project Backend").rglob("*.py"))

    for index, path in enumerate(paths):
        import_from_path(path, f"backend_import_safety_{index}")


def test_telegram_scripts_are_import_safe(monkeypatch):
    install_telegram_stubs(monkeypatch)
    paths = [
        ROOT / "Project Telegram Bot" / "InstaVision_Telegram_Bot.py",
        ROOT / "Project Telegram Bot" / "Telegram Bot Individual Models" / "InstaVision Bot (Dall E3 API)" / "InstaVision_DallE3_API.py",
        ROOT / "Project Telegram Bot" / "Telegram Bot Individual Models" / "InstaVision Bot (Flux Schnell API)" / "InstaVision_Flux-Schnell_API.py",
        ROOT / "Project Telegram Bot" / "Telegram Bot Individual Models" / "InstaVision Bot (Google Imagen3 API)" / "InstaVision_Imagen3_API.py",
        ROOT / "Project Telegram Bot" / "Telegram Bot Individual Models" / "InstaVision Bot (Sdxl Lightning 4Step API)" / "InstaVision_Sdxl-Lightning-4step_API.py",
    ]

    for index, path in enumerate(paths):
        import_from_path(path, f"telegram_import_safety_{index}")
