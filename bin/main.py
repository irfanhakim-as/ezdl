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


import os
import sys
import yt_dlp as youtube_dl
project_path = "../share/ezdl"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), project_path)))
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
    selectFromDict,
    syncCookies,
    writeError,
)


# get user input
def getUserInput(config, **kwargs):
    colMargin = kwargs.get("margin")
    # list user cookies
    cookiesDict = syncCookies(getConfigValue(config, "cookies_dir", default="~/.ezdl/cookies"))
    # list user sources
    sourceFile = os.path.expanduser("~/.config/ezdl/source.json")
    sourceDict = readJson(sourceFile)

    # get source selection
    source = selectFromDict(
        sourceDict,
        intro="source",
        introColour="red",
        introStyle="bright",
        itemColour="yellow",
        itemStyle="bright",
        choiceColour="green",
        choiceStyle="bright",
        desc="pretty_name",
        margin=colMargin,
    )
    # get download path selection
    downloadPath = selectFromDict(
        getConfigValue(config, "download_paths", default={"default": "~/Downloads"}),
        intro="path",
        introColour="blue",
        introStyle="bright",
        itemColour="yellow",
        itemStyle="bright",
        choiceColour="green",
        choiceStyle="bright",
        margin=colMargin,
    )
    # get cookie selection
    cookie = selectFromDict(
        cookiesDict,
        intro="cookie",
        introColour="green",
        introStyle="bright",
        itemColour="yellow",
        itemStyle="bright",
        choiceColour="green",
        choiceStyle="bright",
        margin=colMargin,
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
        errorMessage = "ezdl had trouble downloading these videos:"
        print(writeError(errorMessage), "\n")
        # create columns
        colDict, colMaxLen = createColumns(headers, [failedDownloads.keys(), failedDownloads.values()], margin=colMargin)
        # print column items
        printColumns(colDict, colMaxLen, header=False)
        # write failed downloads to log
        installPrefix = getConfigValue(config, "install_pfx", default="~/.local")
        logFile = os.path.expanduser("%s/share/ezdl/log/ezdl.log" % installPrefix)
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
        # read user config
        configFile = os.path.expanduser("~/.config/ezdl/ezdl.json")
        config = readJson(configFile)
        # get user queue
        queue = getUserInput(config, margin=margin)
        # download videos
        downloadVideos(config, queue, margin=margin, skipSanitise=False)
    except KeyboardInterrupt:
        print("\n\n", "👋 Goodbye!")
        exit(0)
    except Exception as e:
        print("\n\n", writeError("ERROR: %s" % e))
        exit(1)
