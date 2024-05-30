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
# ezdl-utils: Utility functions written for the ezdl tool.


import json
import os
from colorama import (
    Fore,
    Style,
)
from pathlib import Path


# normalise string
def normaliseString(s):
    return s.strip() if s and isinstance(s, str) else s


# resolve provided path
def resolvePath(path):
    return os.path.abspath(os.path.expanduser(path)) if path else None


# create intro title
def createIntro(title, **kwargs):
    return colouriseString("*-*-*-*-*-*-* %s *-*-*-*-*-*-*" % title.upper(), **kwargs)


# colourise string
def colouriseString(s, **kwargs):
    colour = kwargs.get("colour")
    style = kwargs.get("style")
    colour = getattr(Fore, colour.upper()) if colour else ""
    style = getattr(Style, style.upper()) if colour and style else ""
    reset = Style.RESET_ALL if colour else ""
    return "{colour}{style}{s}{reset}".format(colour=colour, style=style, s=s, reset=reset)


# read config file
def readConfig(configFile):
    config = {}
    if configFile and Path(configFile).is_file():
        with open(configFile, "r") as f:
            configContent = f.read()
            config = {normaliseString(x.split("=", 1)[0]): normaliseString(x.split("=", 1)[1]) for x in configContent.splitlines()}
    else:
        print(writeWarning("Config file not found! (%s)" % configFile))
    return config


# get value from config dict
def getConfigValue(config, key, **kwargs):
    default = kwargs.get("default")
    return config.get(key) if config and (config.get(key) or config.get(key) is False) else default


# determine config value which prioritises opts
def determineConfig(config, opts, configKey, optsKey, default=None):
    configValue = getConfigValue(config, configKey, default=default)
    return getConfigValue(opts, optsKey, default=configValue)


# read json file
def readJson(jsonFile, **kwargs):
    required = kwargs.get("required", False)
    silent = kwargs.get("silent", False)
    data = {}
    if Path(jsonFile).is_file():
        with open(jsonFile, "r") as f:
            data = json.load(f)
    else:
        if not silent:
            print(writeWarning("JSON file not found! (%s)" % jsonFile))
        if required:
            exit(1)
    return data


# sync available cookies
def syncCookies(cookiesDir):
    cookiesDict = {}
    # get cookies directory
    cookiesPath = Path(resolvePath(cookiesDir)) if cookiesDir else None
    if cookiesPath and cookiesPath.is_dir():
        # get available cookies
        cookies = os.listdir(cookiesPath)
        for f in cookies:
            # if f is a file and ends with .txt
            if Path(cookiesPath, f).is_file() and f.lower().endswith(".txt"):
                cookie = str(Path(cookiesPath, f))
                cookieName = normaliseString(f.lower().replace(".txt", ""))
                cookiesDict[cookieName] = cookie
    if cookiesDict:
        # add option to not use cookies if the "reserved" key does not exist
        if "anonymous" not in cookiesDict:
            cookiesDict["anonymous"] = None
        # sort cookies alphabetically
        cookiesDict = dict(sorted(cookiesDict.items()))
    return cookiesDict


# validate user choice
def validateChoice(choice, data, **kwargs):
    valueDict = {}
    indexOffset = kwargs.get("offset", 1)
    # ensure dict is not empty and choice is a number
    if data and (isinstance(choice, int) or choice.isdigit()):
        choice = int(choice)
        # get true choice by accounting for index offset
        trueChoice = choice - indexOffset
        # check if choice is within range
        dataKeys = list(data.keys())
        if 0 <= trueChoice < len(dataKeys):
            k = dataKeys[trueChoice]
            v = data[k]
            valueDict = {k: v}
    return valueDict


# create columns
def createColumns(headers, itemsLists, **kwargs):
    colMargin = kwargs.get("margin") if kwargs.get("margin") else 10
    # create a dictionary of columns
    itemDict = dict(zip(headers, itemsLists))
    # count max length of each column including their header
    colMaxLen = {k: max([len(k)] + [len(str(x)) for x in v]) + colMargin for k, v in itemDict.items()}
    # align values to max length
    colDict = {k: [str(x).ljust(colMaxLen[k]) for x in v] for k, v in itemDict.items()}
    return colDict, colMaxLen


# print columns of headers and items
def printColumns(colDict, colMaxLen, **kwargs):
    printHeader = kwargs.get("header", True)
    # align and print column headers
    if printHeader:
        print("".join([k.ljust(colMaxLen[k]) for k in colDict.keys()]))
    # print aligned column items
    for i in range(len(list(colDict.values())[0])):
        print("".join([str(colDict[k][i]) for k in colDict.keys()]))
    print()


# write error message
def writeError(message):
    return colouriseString("🚨 %s" % message, colour="red")


# write warning message
def writeWarning(message):
    return colouriseString("⚠️ %s" % message, colour="yellow")


# select from dict
def selectFromDict(data, **kwargs):
    choice = None
    indexOffset = 1
    colMargin = kwargs.get("margin")
    intro = kwargs.get("intro")
    introColour = kwargs.get("introColour")
    introStyle = kwargs.get("introStyle")
    itemColour = kwargs.get("itemColour")
    itemStyle = kwargs.get("itemStyle")
    choiceColour = kwargs.get("choiceColour", itemColour)
    choiceStyle = kwargs.get("choiceStyle", itemStyle)
    descKey = kwargs.get("desc")
    defaultPick = kwargs.get("default")
    yesToDefault = kwargs.get("yes", False)

    # parse data into dict
    if isinstance(data, dict):
        data = {normaliseString(k): normaliseString(v) for k, v in data.items()}
    elif isinstance(data, str):
        # split string data by comma into a list and create dict where key is index and value is item
        data = {"Option %s" % str(i): v for i, (v) in enumerate((x for x in data.split(",") if x), 1)}

    # exit if data is empty or has not be parsed into a dict
    if not data or not isinstance(data, dict):
        return None

    # determine default pick
    if not defaultPick or defaultPick not in list(data.keys()):
        defaultPick = list(data.keys())[0]

    # print intro
    if intro:
        print(createIntro(intro, colour=introColour, style=introStyle), "\n")

    # make headers and choices
    headers = ["INDEX", "ID", "DESCRIPTION"]
    indexes = [str(i) for i in range(1, len(data) + 1)]
    identifiers = [k for k in data.keys()]
    descriptions = [v[descKey] if descKey else v for v in data.values()]

    # create columns
    colDict, colMaxLen = createColumns(headers, [indexes, identifiers, descriptions], margin=colMargin)
    # colourise identifiers
    colDict["ID"] = [colouriseString(i, colour=itemColour, style=itemStyle) for i in colDict["ID"]]
    # print columns
    printColumns(colDict, colMaxLen)

    # get user choice
    if defaultPick:
        if not yesToDefault:
            choice = input("Please select your choice [%s]: " % defaultPick).strip()
        choice = choice if choice and validateChoice(choice, data, offset=indexOffset) else list(data.keys()).index(defaultPick) + indexOffset
    else:
        while not validateChoice(choice, data, offset=indexOffset):
            choice = input("Please select your choice: ").strip()

    # finalise value
    value = validateChoice(choice, data, offset=indexOffset)
    # print value of selected choice
    print(colouriseString("%s" % list(value.keys())[0], colour=choiceColour, style=choiceStyle), "\n")
    return value


# get user list
def getUserList(**kwargs):
    confirm = None
    userList = kwargs.get("list")
    userList = userList if userList and (isinstance(userList, list) or isinstance(userList, str)) else []
    colMargin = kwargs.get("margin")
    intro = kwargs.get("intro")
    introColour = kwargs.get("introColour")
    introStyle = kwargs.get("introStyle")
    itemColour = kwargs.get("itemColour")
    itemStyle = kwargs.get("itemStyle")
    itemName = kwargs.get("item", "Item")
    yesToDefault = kwargs.get("yes", False)

    # print intro
    if intro:
        print(createIntro(intro, colour=introColour, style=introStyle), "\n")

    # get user input
    if not userList:
        loop = True
        index = 0
        while loop:
            index += 1
            item = input("%s %s: " % (itemName.capitalize(), index)).strip()
            if item:
                # split item by whitespace
                for i in item.split(" "):
                    index += 1
                    userList.append(i.strip())
                index -= 1
            else:
                loop = False
    # parse to list if user list is provided as string
    elif isinstance(userList, str):
        userList = [i.strip() for i in userList.split(" ") if i.strip()]

    # print list
    if userList:
        print()
        # make headers and choices
        headers = ["INDEX", itemName.upper()]
        indexes = [str(i) for i in range(1, len(userList) + 1)]
        items = [i for i in userList]

        # create columns
        colDict, colMaxLen = createColumns(headers, [indexes, items], margin=colMargin)
        # colourise items
        colDict[itemName.upper()] = [colouriseString(i, colour=itemColour, style=itemStyle) for i in colDict[itemName.upper()]]
        # print columns
        printColumns(colDict, colMaxLen)

        # get user confirmation
        if not yesToDefault:
            confirm = input("Do you want to proceed with the above list? [Y/n]: ").strip().lower()
            print()
        if yesToDefault or not confirm in ["n", "no"]:
            return userList
    return None
