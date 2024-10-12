#! /usr/bin/env bash

function kamangir_action_git_before_push() {
    kamangir build_README
    [[ $? -ne 0 ]] && return 1

    [[ "$(abcli_git get_branch)" == "main" ]] &&
        kamangir pypi build
}
