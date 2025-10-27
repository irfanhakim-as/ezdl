#!/usr/bin/env bash
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


INSTALL_PFX="$(dirname "$(dirname "$(realpath -s "${0}")")")"
VENV_PATH="${INSTALL_PFX}/share/ezdl/.venv"
SCRIPT_PATH="${INSTALL_PFX}/share/ezdl/bin/main.py"


# ensure venv exists
if [[ ! -f "${VENV_PATH}/bin/python" ]]; then
    echo "ERROR: Virtual environment not found at ${VENV_PATH}"
    exit 1
fi


exec "${VENV_PATH}/bin/python" "${SCRIPT_PATH}" "${@}"
