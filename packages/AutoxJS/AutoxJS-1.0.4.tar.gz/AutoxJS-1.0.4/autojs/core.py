# -*-coding:utf-8;-*-
from json import dumps
from os import getenv, mkdir, remove
from os.path import abspath, dirname, exists, isfile, join
from socket import socket, AF_INET, SOCK_STREAM
from subprocess import run
from tempfile import gettempprefix
from time import time_ns
from typing import Tuple


def createSocket() -> Tuple[socket, int]:
    oServer = socket(AF_INET, SOCK_STREAM)
    oPort = 16384
    while True:
        oAddressTemp = ("localhost", oPort)
        try:
            oServer.bind(oAddressTemp)
        except Exception:
            oPort += 1
        else:
            break
    oServer.listen(1)
    return oServer, oPort


def createTempFile(isString: bool, iPort: int) -> str:
    oPath = abspath(join(getenv("EXTERNAL_STORAGE", "/sdcard"), "Android/data/com.termux/cache"))
    if not exists(oPath):
        mkdir(oPath)
    oFile = abspath(join(oPath, "%s%d.js" % (gettempprefix(), time_ns())))
    if isString:
        open(oFile, "w", encoding="utf-8").write(
            open(join(dirname(__file__), "execute_string.js"), "r", encoding="utf-8").read() % (iPort,))
    else:
        open(oFile, "w", encoding="utf-8").write(
            open(join(dirname(__file__), "execute_file.js"), "r", encoding="utf-8").read() % (iPort,))
    return oFile


def runTempFile(iFile: str) -> bool:
    return run(("am", "start", "-W", "-a", "android.intent.action.VIEW", "-d", "file://%s" % (iFile,), "-t",
                "application/x-javascript", "--grant-read-uri-permission", "--grant-write-uri-permission",
                "--grant-prefix-uri-permission", "--include-stopped-packages", "--activity-exclude-from-recents",
                "--activity-no-animation", "org.autojs.autojs/.external.open.RunIntentActivity")).returncode == 0


def sendScript(isString: bool, iServer: socket, iStringOrFile: str, iTitleOrPath: str):
    oClient, oAddress = iServer.accept()
    if isString:
        oClient.send((dumps({"name": iTitleOrPath, "script": iStringOrFile}, ensure_ascii=False,
                            separators=(",", ":")) + "\n").encode("utf-8"))
    else:
        oClient.send((dumps({"file": iStringOrFile, "path": iTitleOrPath}, ensure_ascii=False,
                            separators=(",", ":")) + "\n").encode("utf-8"))
    oClient.close()


def runFile(iFile: str) -> bool:
    if type(iFile) != str:
        raise TypeError("The path of script must be a string.")
    oFile = abspath(iFile)
    if not (exists(oFile) and isfile(oFile)):
        raise FileNotFoundError("The script must be an existing file.")
    oServer, oPort = createSocket()
    oTempFile = createTempFile(False, oPort)
    if runTempFile(oTempFile):
        sendScript(False, oServer, oFile, dirname(oFile))
        oServer.close()
        remove(oTempFile)
        return True
    else:
        oServer.close()
        remove(oTempFile)
        return False


def runString(iString: str, iTitle: str = "script") -> bool:
    if type(iString) != str:
        raise TypeError("The script must be a string.")
    if type(iTitle) != str:
        raise TypeError("The name of script must be a string.")
    if iTitle == "":
        raise ValueError("The name of script shouldn't be void.")
    oServer, oPort = createSocket()
    oTempFile = createTempFile(True, oPort)
    if runTempFile(oTempFile):
        sendScript(True, oServer, iString, iTitle)
        oServer.close()
        remove(oTempFile)
        return True
    else:
        oServer.close()
        remove(oTempFile)
        return False
