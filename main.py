import threading
import time
import tokengraber
import asyncio
import os
import logging
import DiscordManager
import LaunchingUkrainizaciya

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("requests.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
#---------------------ProxySetup---------------------
import winreg as reg

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
#--------------------------------------------------------

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