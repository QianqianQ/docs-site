#!/usr/bin/env bash

# Exit on first error or first use of an undeclared variable
set -o errexit
set -o nounset

# Colorful output
CYAN='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m' # No more coloring

DEPLOY_SERVER="none"

pass() {
    function=$1
    echo -e "\\n  ${GREEN}[DONE] -- $function()${NC}"
}

step() {
    local heading="$1"
    local function="$2"
    echo -e "\\n${CYAN}*** $heading${NC}"
    "$function"
    pass "$function"
}

deployment_server_selection(){
    local PS3='Select the server to be deployed => '
    local options=("s1" "s2")

    select DEPLOY_SERVER in "${options[@]}"; do
        # Check if the selection is valid
        if [[ -n "${DEPLOY_SERVER}" ]]; then
            echo "${DEPLOY_SERVER} is selected to deploy docs"
            return
        else
            echo "Invalid choice. Please select a valid number from the list."
        fi
    done
}

fetch_images_from_remote_server() {
    echo "Fetch static data..."

    local dst_dir="source/_static/images/"
    rm -fr "${dst_dir}"
    mkdir --parents "${dst_dir}"

    local host="host"
    urls=(
        "$host/path/to/images.tar"
    )
    for url in "${urls[@]}"; do
        local filename
        filename=$(basename "$url")
        echo "Fetching ${filename}"
        if curl -o "${dst_dir}/${filename}" "$url"; then
            if [[ "${filename}" == *.tar || "${filename}" == *.tar.gz || "${filename}" == *.tgz ]]; then
                tar -xf "${dst_dir}/${filename}" -C "${dst_dir}";
            fi
        fi
    done
}

build_and_deploy_docs() {
    echo "Build docs and deploy to ${DEPLOY_SERVER}..."
    script_dir=$(dirname "$0")
    deploy_cmd="ansible-playbook ${script_dir}/deploy.yml -i ${script_dir}/inventory.ini -e target_host=${DEPLOY_SERVER} --ask-become-pass --ask-vault-pass"
    echo "Running deployment cmd: ${deploy_cmd}"
    eval "$deploy_cmd"
}

step "Docs deployment server selection" deployment_server_selection
step "Fetch static data from rdlinux213" fetch_images_from_remote_server
step "Start ansible playbook to build and deploy docs" build_and_deploy_docs
