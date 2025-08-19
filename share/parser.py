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
# ezdl-parser: Parsing functions written for the ezdl tool.


import re


# sanitise video list
def sanitiseVideoList(videoList):
    # reformat vimeo links
    videoList = ["https://player.vimeo.com/video/%s" % re.search(r'vimeo\.com/(\d+)', l).group(1) if l.startswith("https://vimeo.com") else l for l in videoList]
    # reformat xitter links
    videoList = [l.replace("x.com/", "twitter.com/").strip().rstrip("/") if l.startswith("https://x.com") else l for l in videoList]
    # clean instagram links
    videoList = [l.split("?")[0].strip().rstrip("/") if "instagram.com" in l else l for l in videoList]
    return videoList
