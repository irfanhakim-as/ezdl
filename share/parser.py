# sanitise video list
def sanitiseVideoList(videoList):
    # reformat vimeo links
    videoList = [l[:l.rfind("/") + 1].replace("vimeo.com/", "player.vimeo.com/video/").rstrip("/") if l.startswith("https://vimeo.com") else l for l in videoList]
    return videoList
