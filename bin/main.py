#!/usr/bin/env python
#
#         :::   :::  ::::::::::::::    :::    :::
#       :+:+: :+:+:     :+:    :+:   :+:   :+: :+:
#     +:+ +:+:+ +:+    +:+    +:+  +:+   +:+   +:+  Irfan Hakim (MIKA)
#    +#+  +:+  +#+    +#+    +#++:++   +#++:++#++:  https://sakurajima.social/@irfan
#   +#+       +#+    +#+    +#+  +#+  +#+     +#+   https://github.com/irfanhakim-as
#  #+#       #+#    #+#    #+#   #+# #+#     #+#    https://gitlab.com/irfanhakim
# ###       #################    ######     ###
#
# ezdl: Video downloader script for YouTube, Instagram, Tik Tok, and more.


import argparse
import os
import sys
import yt_dlp as youtube_dl
project_path = "../share/ezdl"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), project_path)))
from metadata import (
    __name__ as __app_name__,
    __version__ as __app_version__,
)
from parser import (
    sanitiseVideoList,
)
from utils import (
    colouriseString,
    createColumns,
    getConfigValue,
    getUserList,
    printColumns,
    readJson,
    resolvePath,
    selectFromDict,
    syncCookies,
    writeError,
    writeWarning,
)


# get user arguments
def get_args(arguments):
    parser = argparse.ArgumentParser()
    for arg in arguments:
        if "names" in arg and "kwargs" in arg:
            parser.add_argument(*arg["names"], **arg["kwargs"])
    args, unknown = parser.parse_known_args()
    # indicate unknown arguments have been provided
    if unknown:
        warningMessage = "%(app_name)s: invalid option(s) -- %(unknown)s\nTry '%(app_name)s --help' for more information." % {"app_name": __app_name__, "unknown": " ".join(unknown)}
        print(writeWarning(warningMessage))
        # parser.print_help()
        exit(1)
    return parser, args


# get user input
def getUserInput(config, **kwargs):
    args = kwargs.get("args")
    colMargin = kwargs.get("margin")
    # list user cookies
    cookiesDict = syncCookies(getConfigValue(config, "cookies_dir", default="~/.ezdl/cookies"))
    # list user sources
    sourceFile = resolvePath("~/.config/ezdl/source.json")
    sourceDict = readJson(sourceFile, required=True)

    # get source selection
    source = selectFromDict(
        sourceDict,
        default=getConfigValue(config, "default_source"),
        intro="source",
        introColour="red",
        introStyle="bright",
        itemColour="yellow",
        itemStyle="bright",
        choiceColour="green",
        choiceStyle="bright",
        desc="pretty_name",
        margin=colMargin,
        yes=getattr(args, "yes", None),
    )
    # get download path selection
    downloadPath = selectFromDict(
        getConfigValue(config, "download_paths", default={"default": "~/Downloads"}),
        default=getConfigValue(config, "default_download_path"),
        intro="path",
        introColour="blue",
        introStyle="bright",
        itemColour="yellow",
        itemStyle="bright",
        choiceColour="green",
        choiceStyle="bright",
        margin=colMargin,
        yes=getattr(args, "yes", None),
    )
    # get cookie selection
    cookie = selectFromDict(
        cookiesDict,
        default=getConfigValue(config, "default_cookie"),
        intro="cookie",
        introColour="green",
        introStyle="bright",
        itemColour="yellow",
        itemStyle="bright",
        choiceColour="green",
        choiceStyle="bright",
        margin=colMargin,
        yes=getattr(args, "yes", None),
    )
    # get video selection
    videoLinks = getUserList(
        intro="video",
        introColour="magenta",
        introStyle="bright",
        itemColour="green",
        itemStyle="bright",
        itemName="video",
        margin=colMargin,
        yes=getattr(args, "yes", None),
        list=getattr(args, "video", None),
    )

    return {
        "source": source,
        "download": downloadPath,
        "cookie": cookie,
        "video": videoLinks
    }


# download videos
def downloadVideos(config, queue, **kwargs):
    failedDownloads = {}
    colMargin = kwargs.get("margin")
    skipSanitise = getConfigValue(config, "skip_sanitise", default=False)

    # get raw queue dicts
    sourceDict = getConfigValue(queue, "source")
    downloadPathDict = getConfigValue(queue, "download")
    cookieDict = getConfigValue(queue, "cookie")
    # videoList = queue.get("video")
    videoList = getConfigValue(queue, "video")

    # get normalised queue values
    source = list(sourceDict.values())[0] if sourceDict else None
    sourceEmbedder = getConfigValue(source, "embedder")
    sourceOpts = getConfigValue(source, "opts")
    downloadPath = list(downloadPathDict.values())[0] if downloadPathDict else None
    cookiePath = list(cookieDict.values())[0] if cookieDict else None
    videoList = sanitiseVideoList(videoList) if not skipSanitise else videoList

    # quit if any of the required values are missing
    if not (sourceOpts and downloadPath and videoList):
        print("\n", writeError("Invalid queue!"))
        exit(1)

    # add cookie to opts if available
    if cookiePath:
        sourceOpts["cookiefile"] = cookiePath
    # add download path to output template
    sourceOpts["outtmpl"] = sourceOpts["outtmpl"].format(path=downloadPath)
    # add embedder if applicable: https://github.com/ytdl-org/youtube-dl/issues/13009#issuecomment-375724086
    if sourceEmbedder:
        youtube_dl.utils.std_headers["Referer"] = sourceEmbedder

    # create columns
    headers = ["ORDER", "VIDEO"]
    orders = ["%s/%s" % (i, len(videoList)) for i in range(1, len(videoList) + 1)]
    colDict, colMaxLen = createColumns(headers, [orders, videoList], margin=colMargin)

    # colourise orders
    colDict["ORDER"] = [colouriseString(i, colour="yellow", style="bright") if int(i.split("/")[0].strip()) != len(videoList) else colouriseString(i, colour="green", style="bright") for i in colDict["ORDER"]]
    # colourise videos
    colDict["VIDEO"] = [colouriseString(i, colour="yellow", style="bright") for i in colDict["VIDEO"]]

    # print column values and download videos
    for i in range(len(list(colDict.values())[0])):
        # print column value
        print("".join([str(colDict[k][i]) for k in colDict.keys()]))
        # start download
        try:
            # get video
            video = videoList[i]
            # download video
            with youtube_dl.YoutubeDL(sourceOpts) as ydl:
                ydl.download([video])
        except Exception as e:
            # add failed download
            failedDownloads[i + 1] = video
        print()

    # print failed downloads
    if failedDownloads:
        errorMessage = "%s had trouble downloading these videos:" % __app_name__
        print(writeError(errorMessage), "\n")
        # create columns
        colDict, colMaxLen = createColumns(headers, [failedDownloads.keys(), failedDownloads.values()], margin=colMargin)
        # print column items
        printColumns(colDict, colMaxLen, header=False)
        # write failed downloads to log
        installPrefix = getConfigValue(config, "install_pfx", default="~/.local")
        logFile = resolvePath("%s/share/ezdl/log/ezdl.log" % installPrefix)
        with open(logFile, "a") as f:
            f.write("\n" + errorMessage + " " + " ".join(failedDownloads.values()))
    # print success message
    else:
        print("✌️ All videos downloaded successfully!")


# ================= DO NOT EDIT BEYOND THIS LINE =================

if __name__ == "__main__":
    try:
        # predefined values
        margin = 5
        # get user arguments
        arguments = [
            {
                "names": ["-v", "--version"],
                "kwargs": {
                    "help": "return the version of the script",
                    "action": "store_true",
                }
            },
            {
                "names": ["-l", "--video"],
                "kwargs": {
                    "help": "provide a list of video links to download",
                    "type": str,
                    "nargs": "+",
                }
            },
            {
                "names": ["-y", "--yes"],
                "kwargs": {
                    "help": "say yes to all defaults",
                    "action": "store_true",
                }
            },
        ]
        parser, args = get_args(arguments)
        # return script version
        if args.version:
            print("%s: %s" % (__app_name__, __app_version__))
            exit(0)
        # read user config
        configFile = resolvePath("~/.config/ezdl/ezdl.json")
        config = readJson(configFile, required=True)
        # get user queue
        queue = getUserInput(config, args=args, margin=margin)
        # download videos
        downloadVideos(config, queue, margin=margin, skipSanitise=False)
    except KeyboardInterrupt:
        print("\n\n%s" % "👋 Goodbye!")
        exit(0)
    except Exception as e:
        print("\n\n%s" % writeError("ERROR: %s" % e))
        exit(1)
