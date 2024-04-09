#!/usr/bin/env bash


# constants
APP_NAME="ezdl"
APP_NAMESPACE="ezdl"


# print help message
function print_help() {
    echo "Usage: ${0} [options]"; echo
    echo "OPTIONS:"
    echo "  -h, --help                           Print help message"
    # echo "  -c, --config-prefix <prefix>         Specify a config prefix"
    echo "  -i, --install-prefix <prefix>        Specify an installation prefix"
    echo "  -l, --link-install                   Perform a symlink installation"
    echo "  -u, --uninstall                      Uninstall application"
}


# get optional arguments
while [[ ${#} -gt 0 ]]; do
    case "${1}" in
        -h|--help)
            print_help
            exit 0
            ;;
        # -c|--config-prefix)
        #     if [ -z "${2}" ]; then
        #         echo "ERROR: Please specify a config prefix"
        #         exit 1
        #     fi
        #     CONFIG_PFX="${2}"
        #     shift
        #     ;;
        -i|--install-prefix)
            if [ -z "${2}" ]; then
                echo "ERROR: Please specify a install prefix"
                exit 1
            fi
            INSTALL_PFX="${2}"
            shift
            ;;
        -l|--link-install)
            LINK_INSTALL=1
            ;;
        -u|--uninstall)
            UNINSTALL_APP=1
            ;;
        *)
            echo "ERROR: Invalid argument (${1})"
            exit 1
            ;;
    esac
    shift
done


# set default prefixes
if [ -z "${CONFIG_PFX}" ]; then
    CONFIG_PFX="${HOME}/.config"
fi
CONFIG_PFX=$(realpath "${CONFIG_PFX}") || exit 1

if [ -z "${INSTALL_PFX}" ]; then
    INSTALL_PFX="${HOME}/.local"
fi
INSTALL_PFX=$(realpath "${INSTALL_PFX}") || exit 1


# associative array of required files and their target locations
declare -A required_files=(
    ["bin/main.py"]="${INSTALL_PFX}/bin/${APP_NAME}"
    ["share/metadata.py"]="${INSTALL_PFX}/share/${APP_NAMESPACE}/"
    ["share/parser.py"]="${INSTALL_PFX}/share/${APP_NAMESPACE}/"
    ["share/utils.py"]="${INSTALL_PFX}/share/${APP_NAMESPACE}/"
    ["log/${APP_NAME}.log"]="${INSTALL_PFX}/share/${APP_NAMESPACE}/log/"
    ["config/${APP_NAME}.json"]="${CONFIG_PFX}/${APP_NAMESPACE}/"
    ["config/source.json"]="${CONFIG_PFX}/${APP_NAMESPACE}/"
)


# determine required directories
declare -a required_directories=()
for dir in "${required_files[@]}"; do
    # check if directory not already in required_directories array
    if [[ ! " ${required_directories[@]} " =~ " ${dir%/*} " ]]; then
        required_directories+=("${dir%/*}")
    fi
done


# install script
function install() {
    echo "Installing ${APP_NAME} to ${INSTALL_PFX}"
    # create required directories
    for dir in "${required_directories[@]}"; do
        echo "Creating directory ${dir}"
        mkdir -p "${dir}"
    done
    # copy required files
    for file in "${!required_files[@]}"; do
        if [ "${LINK_INSTALL}" != 1 ] || [[ "${file}" =~ ^(config|log)/ ]]; then
            echo "Copying ${file} to ${required_files[${file}]}"
            cp -i "${file}" "${required_files[${file}]}"
        else
            echo "Symlinking ${file} to ${required_files[${file}]}"
            ln -s "$(realpath "${file}")" "${required_files[${file}]}"
        fi
    done
}


# uninstall script
function uninstall() {
    echo "Uninstalling ${APP_NAME} from ${INSTALL_PFX}"
    # remove target locations
    for file in "${!required_files[@]}"; do
        echo "Removing ${required_files[${file}]}"
        rm -f "${required_files[${file}]}" || rm -rf "${required_files[${file}]}"
    done
}


# install or uninstall
if [ "${UNINSTALL_APP}" == "1" ]; then
    uninstall
else
    install
fi
