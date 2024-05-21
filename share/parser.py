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


# sanitise video list
def sanitiseVideoList(videoList):
    # reformat vimeo links
    videoList = [l[:l.rfind("/") + 1].replace("vimeo.com/", "player.vimeo.com/video/").rstrip("/") if l.startswith("https://vimeo.com") else l for l in videoList]
    # reformat xitter links
    videoList = [l.replace("x.com/", "twitter.com/").rstrip("/") if l.startswith("https://x.com") else l for l in videoList]
    return videoList
