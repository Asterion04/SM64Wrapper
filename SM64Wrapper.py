import psutil
import time
import datetime
import pymem
import pymem.process
import pymem.memory
from colorama import Fore, init
init()


class RAM:

    def __init__(self, debugMode: bool = False):
        self.pid: int = None
        self.pm: pymem = None
        self.isEmuOpen: bool = False
        self.basePtr: int = None
        self.debugMode = debugMode

        self.__memoryMap = {
            'level': 0x8033B249,
            'lives': 0x8033B21E,
            'stars': 0x8033B218,
            'coins': 0x8033B21A,
            'health': 0x8033B21D,
            'restartLevel': 0x8033B24B,
            'xPos': 0x8033B1AC,
            'yPos': 0x8033B1B0,
            'zPos': 0x8033B1B4
        }

    def debugLog(self, message: str, addr: str = None):
        if addr:
            print(Fore.YELLOW + f"[DEBUG {datetime.datetime.now().time()}]" + Fore.RESET + f" {message} " +
                  Fore.GREEN + f"{hex(int(addr, 16))}" + Fore.RESET)
        else:
            print(Fore.YELLOW + f"[DEBUG {datetime.datetime.now().time()}]" + Fore.RESET + f" {message}")

    def openEmu(self, emu_name: str = '') -> bool:
        if emu_name:
            if emu_name in ['Project64']:
                for Process in psutil.process_iter():
                    if emu_name in Process.name():
                        self.pid = Process.pid
                        self.pm = pymem.Pymem()
                if self.pid:
                    self.pm.open_process_from_id(self.pid)
                    self.isEmuOpen = True
                    self.basePtr = hex(self.pm.read_int(0x7C640000) & (2 ** 32 - 1))

                    if self.debugMode:
                        self.debugLog(f"Process pid {self.pid} has been opened")
                        self.debugLog(f"Base Pointer of SM64 is {self.basePtr}")

                else:
                    raise Exception('RAM: Emulator not running')

            else:
                raise Exception('RAM: Emulator name not compatible')

        return True

    ''' Read value from SM64 '''

    def currentLevel(self) -> str:
        if self.isEmuOpen:
            addrStr = hex(int(self.basePtr, 0) + self.__memoryMap.get('level'))[3:]
            if self.debugMode:
                self.debugLog("Address of the current level :", addrStr)

            level_dict = {
                0x00: "None",
                0x04: "Haunted House",
                0x05: "Cool Cool Mountain",
                0x06: "Inside Castle",
                0x07: "Hazy Maze Cave",
                0x08: "Shifting Sand Land",
                0x09: "Bob-Omb's Battlefield",
                0x0A: "Snow Man's land",
                0x0B: "Wet Dry World",
                0x0C: "Jolly Roger Bay",
                0x0D: "Tiny Huge Island",
                0x0E: "Tick Tock Clock",
                0x0F: "Rainbow Ride",
                0x10: "Castle Grounds",
                0x11: "Bowser First Course",
                0x12: "Vanish Cap",
                0x13: "Bowser's Fire Sea",
                0x14: "Secret Aquarium",
                0x15: "Bowser Third Course",
                0x16: "Lethal Lava Land",
                0x17: "Dire Dire Docks",
                0x18: "Whomp's Fortress",
                0x19: "Picture at the end",
                0x1A: "Castle Courtyard",
                0x1B: "Peach's Secret Slide",
                0x1C: "Metal Cap",
                0x1D: "Wing Cap",
                0x1E: "Bowser First Battle",
                0x1F: "Rainbow Clouds",
                0x21: "Bowser Second Battle",
                0x22: "Bowser Third Battle",
                0x24: "Tall Tall Mountain"
            }

            level_number = self.pm.read_bytes(int(addrStr, 16), 2)[1]
            return level_dict.get(level_number)

        else:
            raise Exception("RAM: Emulator not open")

    def getLives(self) -> int:
        if self.isEmuOpen:
            addrStr = hex(int(self.basePtr, 0) + self.__memoryMap.get('lives'))[3:]
            if self.debugMode:
                self.debugLog("Address of the lives :", addrStr)

            return self.pm.read_int(int(addrStr, 16))
        else:
            raise Exception("RAM: Emulator not open")

    def getStars(self) -> int:
        if self.isEmuOpen:
            addrStr = hex(int(self.basePtr, 0) + self.__memoryMap.get('stars'))[3:]
            if self.debugMode:
                self.debugLog("Address of the stars :", addrStr)
            return int.from_bytes(self.pm.read_bytes(int(addrStr, 16), 1), "big")
        else:
            raise Exception("RAM: Emulator not open")

    def getCoins(self) -> int:
        if self.isEmuOpen:
            addrStr = hex(int(self.basePtr, 0) + self.__memoryMap.get('coins'))[3:]
            if self.debugMode:
                self.debugLog("Address of the coins :", addrStr)
            return int.from_bytes(self.pm.read_bytes(int(addrStr, 16), 1), "big")
        else:
            raise Exception("RAM: Emulator not open")

    def getHealth(self) -> int:
        if self.isEmuOpen:
            addrStr = hex(int(self.basePtr, 0) + self.__memoryMap.get('health'))[3:]
            if self.debugMode:
                self.debugLog("Address of the health :", addrStr)
            return int.from_bytes(self.pm.read_bytes(int(addrStr, 16), 1), "big")
        else:
            raise Exception("RAM: Emulator not open")

    ''' Write value to SM64 '''

    def setCoins(self, coins: int = None):
        if coins is not None:
            if self.isEmuOpen:
                addrStr = hex(int(self.basePtr, 0) + self.__memoryMap.get('coins'))[3:]
                self.pm.write_uchar(int(addrStr, 16), coins)
            else:
                raise Exception("RAM: Emulator not open")

    def setLives(self, lives: int = None):
        if lives is not None:
            if self.isEmuOpen:
                addrStr = hex(int(self.basePtr, 0) + self.__memoryMap.get('lives'))[3:]
                self.pm.write_int(int(addrStr, 16), lives)
            else:
                raise Exception("RAM: Emulator not open")

    def setStars(self, stars: int = None):
        if stars is not None:
            if self.isEmuOpen:
                addrStr = hex(int(self.basePtr, 0) + self.__memoryMap.get('stars'))[3:]
                self.pm.write_uchar(int(addrStr, 16), stars)
            else:
                raise Exception("RAM: Emulator not open")

    def setHealth(self, health: int = None):
        if health is not None:
            if self.isEmuOpen:
                addrStr = hex(int(self.basePtr, 0) + self.__memoryMap.get('health'))[3:]
                self.pm.write_uchar(int(addrStr, 16), health)
            else:
                raise Exception("RAM: Emulator not open")

    ''' Event '''

    def restartLevel(self):
        if self.isEmuOpen:
            addrStr = hex(int(self.basePtr, 0) + self.__memoryMap.get('restartLevel'))[3:]
            self.pm.write_uchar(int(addrStr, 16), 2)
        else:
            raise Exception("RAM: Emulator not open")


    def killMario(self):
        if self.isEmuOpen:
            addrStr = hex(int(self.basePtr, 0) + self.__memoryMap.get('health'))[3:]
            self.pm.write_uchar(int(addrStr, 16), 0)
        else:
            raise Exception("RAM: Emulator not open")

    def freezePos(self, timer: int = 3):
        if self.isEmuOpen:
            addrX = hex(int(self.basePtr, 0) + self.__memoryMap.get('xPos'))[3:]
            addrY = hex(int(self.basePtr, 0) + self.__memoryMap.get('yPos'))[3:]
            addrZ = hex(int(self.basePtr, 0) + self.__memoryMap.get('zPos'))[3:]
            x = self.pm.read_int(int(addrX, 16))
            y = self.pm.read_int(int(addrY, 16))
            z = self.pm.read_int(int(addrZ, 16))

            t_end = time.time() + timer
            while time.time() < t_end:
                self.pm.write_int(int(addrX, 16), x)
                self.pm.write_int(int(addrY, 16), y)
                self.pm.write_int(int(addrZ, 16), z)
        else:
            raise Exception("RAM: Emulator not open")


class Cap:
    def __init__(self, sm64wrapper):
        if isinstance(sm64wrapper, RAM):
            self.main = sm64wrapper
        else:
            raise Exception("Control: RAM class is needed")

    def reset(self):
        if self.main.isEmuOpen:
            addrStr = hex(int(self.main.basePtr, 0) + 0x8033B174)[3:]
            self.main.pm.write_int(int(addrStr, 16), 17)
        else:
            raise Exception("Control: Emulator not open")

    def wing(self):
        if self.main.isEmuOpen:
            addrStr = hex(int(self.main.basePtr, 0) + 0x8033B174)[3:]
            self.main.pm.write_int(int(addrStr, 16), 280)
        else:
            raise Exception("Control: Emulator not open")

    def no_hat(self):
        if self.main.isEmuOpen:
            addrStr = hex(int(self.main.basePtr, 0) + 0x8033B174)[3:]
            self.main.pm.write_int(int(addrStr, 16), 1)
        else:
            raise Exception("Control: Emulator not open")

    def metal(self):
        if self.main.isEmuOpen:
            addrStr = hex(int(self.main.basePtr, 0) + 0x8033B174)[3:]
            self.main.pm.write_int(int(addrStr, 16), 20)
        else:
            raise Exception("Control: Emulator not open")

    def completely_invisible(self):
        if self.main.isEmuOpen:
            addrStr = hex(int(self.main.basePtr, 0) + 0x8033B174)[3:]
            self.main.pm.write_int(int(addrStr, 16), 136)
        else:
            raise Exception("Control: Emulator not open")


class Animation:

    def __init__(self, sm64wrapper):
        if isinstance(sm64wrapper, RAM):
            self.RAM = sm64wrapper

            self.__oncePunch = True
            self.__onceCrouch = True
            self.__onceDive = True
            self.__onceSpin = True
        else:
            raise Exception("Control: RAM class is needed")

    def punch(self):
        if self.RAM.isEmuOpen:
            addrStr = hex(int(self.RAM.basePtr, 0) + int("0x8033B17C", 0))[3:]
            if self.RAM.debugMode and self.__oncePunch:
                self.RAM.debugLog("Animation of the punch is the value 8389504 at", addrStr)
                self.__oncePunch = False
            self.RAM.pm.write_int(int(addrStr, 16), 8389504)
        else:
            raise Exception("Control: Emulator not open")

    def crouch(self):
        if self.RAM:
            if self.RAM.isEmuOpen:
                addrStr = hex(int(self.RAM.basePtr, 0) + 0x8033B17C)[3:]
                if self.RAM.debugMode and self.__onceCrouch:
                    self.RAM.debugLog("Animation of the crouch is the value 201359904 at", addrStr)
                    self.__onceCrouch = False
                self.RAM.pm.write_int(int(addrStr, 16), 201359904)
            else:
                raise Exception("Control: Emulator not open")

    def dive(self):
        if self.RAM:
            if self.RAM.isEmuOpen:
                addrStr = hex(int(self.RAM.basePtr, 0) + 0x8033B17C)[3:]
                if self.RAM.debugMode and self.__onceDive:
                    self.RAM.debugLog("Animation of the dive is the value 8914006 at", addrStr)
                    self.__onceDive = False
                self.RAM.pm.write_int(int(addrStr, 16), 8914006)
            else:
                raise Exception("Control: Emulator not open")

    def spin_forward(self):
        if self.RAM:
            if self.RAM.isEmuOpen:
                addrStr = hex(int(self.RAM.basePtr, 0) + 0x8033B17C)[3:]
                if self.RAM.debugMode and self.__onceSpin:
                    self.RAM.debugLog("Animation of the spin_forward is the value 16779430 at", addrStr)
                    self.__onceSpin = False
                t_end = time.time() + 0.1
                while time.time() < t_end:
                    self.RAM.pm.write_int(int(addrStr, 16), 16779430)
            else:
                raise Exception("Control: Emulator not open")


class CheckInput:
    def __init__(self, sm64wrapper):
        if isinstance(sm64wrapper, RAM):
            self.RAM = sm64wrapper
            self.__onceA = True
            self.__onceB = True
            self.__onceZ = True
        else:
            raise Exception("Control: RAM class is needed")

    def nothing(self):
        if self.RAM.isEmuOpen:
            addrStr = hex(int(self.RAM.basePtr, 0) + 0x8033AFA0)[3:]
            if self.RAM.debugMode and self.__onceA:
                self.RAM.debugLog("Address of the button A :", addrStr)
                self.__onceA = False

            current_button = hex(self.RAM.pm.read_uint(int(addrStr, 16)))
            return current_button == "0x00000000"
        else:
            raise Exception("RAM: Emulator not open")

    def A(self) -> bool:
        if self.RAM.isEmuOpen:
            addrStr = hex(int(self.RAM.basePtr, 0) + 0x8033AFA0)[3:]
            if self.RAM.debugMode and self.__onceA:
                self.RAM.debugLog("Address of the button A :", addrStr)
                self.__onceA = False

            current_button = hex(self.RAM.pm.read_uint(int(addrStr, 16)))[:5]
            return current_button == "0x800"
        else:
            raise Exception("RAM: Emulator not open")

    def B(self) -> bool:
        if self.RAM.isEmuOpen:
            addrStr = hex(int(self.RAM.basePtr, 0) + 0x8033AFA0)[3:]
            if self.RAM.debugMode and self.__onceB:
                self.RAM.debugLog("Address of the button B :", addrStr)
                self.__onceB = False

            current_button = hex(self.RAM.pm.read_uint(int(addrStr, 16)))[:5]
            return current_button == "0x400"
        else:
            raise Exception("RAM: Emulator not open")

    def Z(self) -> bool:
        if self.RAM.isEmuOpen:
            addrStr = hex(int(self.RAM.basePtr, 0) + 0x8033AFA0)[3:]
            if self.RAM.debugMode and self.__onceZ:
                self.RAM.debugLog("Address of the button Z :", addrStr)
                self.__onceZ = False

            current_button = hex(self.RAM.pm.read_uint(int(addrStr, 16)))
            return current_button[:5] == "0x200" and len(current_button) > 7
        else:
            raise Exception("RAM: Emulator not open")
