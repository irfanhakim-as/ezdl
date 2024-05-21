# `ezdl`: Easy (Video) Download

## About

**ezdl** is an Easy (Video) Download tool written in Python and uses readily available libraries in order to simplify the process of downloading videos from varying sources right from the terminal.

## Requirements

### System software

- `bash` 5.0+
- `ffmpeg` 6.1.1+
- `python` 3.0+

### Python library (pip)

- `colorama` 0.4.4+
- `yt-dlp` 2023.7.6+

## Features

- Simple yet useful [configuration](#configurations) options to get things done the way you want it and to have that process reproducible.

    Examples:

    - Set a location where your cookies are stored and **ezdl** will recognise them and prompt you to pick one, if any, when you're downloading videos.
    - Define several download path options for **ezdl** to allow you to choose from when downloading.
    - Configure custom source _profiles_ on top or in place of the ones provided by default i.e. Create a new `instagram` source profile with **yt-dlp** options to use when downloading from Instagram.
    - Set defaults for each option (i.e. source, download path, cookie) or don't and **ezdl** will determine a default for you.

- Easy to use with essentially nothing to remember or recall when you need to download a video.
- Very fast downloads and compatible with videos from a huge list of sources thanks to the [**yt-dlp**](https://github.com/yt-dlp/yt-dlp) project.
- Custom sanitisation/parsing options for video links i.e. automatically changing `vimeo.com` links to `player.vimeo.com`, `x.com` links to `twitter.com`, and so on. **[EXPERIMENTAL]**

## Installation

1. Ensure that you have met all of the project [requirements](#requirements).

2. Clone the repository:

    ```sh
    git clone https://github.com/irfanhakim-as/ezdl.git ~/.ezdl
    ```

3. Get into the local repository:

    ```sh
    cd ~/.ezdl
    ```

4. Use the installer script:

    Use the help option to see other available options:

    ```sh
    ./installer.sh --help
    ```

    For the most basic installation, simply run the script as is:

    ```sh
    ./installer.sh
    ```

    By default, the installer will install the project to the `~/.local` prefix. Please ensure that the `~/.local/bin` directory is in your `PATH` environment variable.

## Configurations

There are two configuration files available that are provided by default after installation:

- `ezdl.json`: Configuration options pertaining to the **ezdl** tool. All supported options are detailed below.

- `source.json`: Source profile configurations that are primarily used as **yt-dlp** download options you could pick from when you are downloading videos. They are meant to be set up for different sources or modes of downloading i.e. one profile for downloading YouTube videos as `mp4` files while another profile for downloading YouTube videos as `mp3` files. Examples can be found in the provided [`source.json`](config/source.json) file.

They are both installed to `~/.config/ezdl` by default.

### ezdl.json

| **Option** | **Description** | **Sample Value** | **Default Value** |
| --- | --- | --- | --- |
| `cookies_dir` | The directory where your cookie(s) are stored, if any. | `~/Downloads/cookies` | `~/.ezdl/cookies` |
| `default_cookie` | The default cookie (`.txt`) file name to use/suggest. | `cookies` if the file name is `cookies.txt` | `anonymous` or the first available cookie if any |
| `default_download_path` | The default download path name to use/suggest. | `current` | `downloads` or the first available download path |
| `default_source` | The default source profile name to use/suggest. | `twitter` | `yt_best` or the first available source profile |
| `download_paths` | A dictionary of download path options comprised of their name and path. | `{"videos": "~/Videos", "movies": "~/Movies"}` | `{"downloads": "~/Downloads", "current": "."}` |
| `install_pfx` | The prefix where **ezdl** was installed. Update this if it's been changed. | `/usr/local` | `~/.local` |
| `skip_sanitise` | Specifies whether or not **ezdl** should skip sanitising video links. | `true` | `false` |

## Usage

1. Ensure that you have [installed](#installation) the project successfully.

2. The easiest way to use **ezdl** is to use the `ezdl` command as is:

    ```sh
    ezdl
    ```

    This will walk you through picking a source profile, a download path, and a cookie (if available) before then getting the video links from you and downloading them accordingly.

3. You may also use the help option to see other (optional) options available to **ezdl**:

    ```sh
    ezdl --help
    ```
