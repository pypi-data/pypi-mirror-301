#! /usr/bin/env bash

function CV_action_git_before_push() {
    [[ "$(abcli_git get_branch)" != "main" ]] &&
        return 0

    CV pypi build
}
