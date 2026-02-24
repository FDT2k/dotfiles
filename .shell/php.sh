#!/bin/zsh

export KDA_WORK="$HOME/Documents/fastwork/kda-dev"

_docker_php_run() {
    local version=$1
    local cmd=$2
    local composer_file=$3
    shift 3

    local workspace="${PHP_WORKSPACE:-$KDA_WORK}"
    local debian="${PHP_DEBIAN:-trixie}"
    local image="registry.gitlab.com/karsegard/docker-infomaniak:${version}-${debian}"

    local xdebug_args=()
    if [[ "$cmd" == "php" ]]; then
        xdebug_args=(
            --add-host=host.docker.internal:host-gateway
            -e XDEBUG_CONFIG="idekey=vsc client_host=host.docker.internal client_port=9003"
            -e XDEBUG_MODE=debug,develop
            -e XDEBUG_TRIGGER=1
            -e XDEBUG_START_WITH_REQUEST=yes
            -e XDEBUG_CLIENT_HOST=host.docker.internal
            -e XDEBUG_CLIENT_PORT=9003
        )
    fi

    docker run --rm -it \
        -e COMPOSER="$composer_file" \
        -e COMPOSER_HOME=/app/composer \
        "${xdebug_args[@]}" \
        --mount type=bind,source="$workspace",target="$workspace",readonly \
        --mount type=bind,source="$(pwd)",target=/app \
        -w /app \
        --user "$(id -u):$(id -g)" \
        "$image" "$cmd" "$@"
}

# --- composer wrappers: PHP 8.0 ---
c2_80()       { _docker_php_run 8.0 composer2 composer.json "$@"; }
c2_80_dev()   { _docker_php_run 8.0 composer2 composer.dev.json "$@"; }
c2_80_prod()  { _docker_php_run 8.0 composer2 composer.prod.json "$@"; }
c2_80_agent() { _docker_php_run 8.0 composer2 composer.agents.json "$@"; }
c2_80_all()   { c2_80_dev "$@" && c2_80_prod "$@" && c2_80_agent "$@"; }

# --- composer wrappers: PHP 8.1 ---
c2_81()       { _docker_php_run 8.1 composer2 composer.json "$@"; }
c2_81_dev()   { _docker_php_run 8.1 composer2 composer.dev.json "$@"; }
c2_81_prod()  { _docker_php_run 8.1 composer2 composer.prod.json "$@"; }
c2_81_agent() { _docker_php_run 8.1 composer2 composer.agents.json "$@"; }
c2_81_all()   { c2_81_dev "$@" && c2_81_prod "$@" && c2_81_agent "$@"; }

# --- composer wrappers: PHP 8.2 ---
c2_82()       { _docker_php_run 8.2 composer2 composer.json "$@"; }
c2_82_dev()   { _docker_php_run 8.2 composer2 composer.dev.json "$@"; }
c2_82_prod()  { _docker_php_run 8.2 composer2 composer.prod.json "$@"; }
c2_82_agent() { _docker_php_run 8.2 composer2 composer.agents.json "$@"; }
c2_82_all()   { c2_82_dev "$@" && c2_82_prod "$@" && c2_82_agent "$@"; }

# --- composer wrappers: PHP 8.3 ---
c2_83()       { _docker_php_run 8.3 composer2 composer.json "$@"; }
c2_83_dev()   { _docker_php_run 8.3 composer2 composer.dev.json "$@"; }
c2_83_prod()  { _docker_php_run 8.3 composer2 composer.prod.json "$@"; }
c2_83_agent() { _docker_php_run 8.3 composer2 composer.agents.json "$@"; }
c2_83_all()   { c2_83_dev "$@" && c2_83_prod "$@" && c2_83_agent "$@"; }

# --- composer wrappers: PHP 8.4 ---
c2_84()       { _docker_php_run 8.4 composer2 composer.json "$@"; }
c2_84_dev()   { _docker_php_run 8.4 composer2 composer.dev.json "$@"; }
c2_84_prod()  { _docker_php_run 8.4 composer2 composer.prod.json "$@"; }
c2_84_agent() { _docker_php_run 8.4 composer2 composer.agents.json "$@"; }
c2_84_all()   { c2_84_dev "$@" && c2_84_prod "$@" && c2_84_agent "$@"; }

# --- composer wrappers: PHP 8.5 ---
c2_85()       { _docker_php_run 8.5 composer2 composer.json "$@"; }
c2_85_dev()   { _docker_php_run 8.5 composer2 composer.dev.json "$@"; }
c2_85_prod()  { _docker_php_run 8.5 composer2 composer.prod.json "$@"; }
c2_85_agent() { _docker_php_run 8.5 composer2 composer.agents.json "$@"; }
c2_85_all()   { c2_85_dev "$@" && c2_85_prod "$@" && c2_85_agent "$@"; }

# --- php+xdebug wrappers ---
p80() { _docker_php_run 8.0 php composer.prod.json "$@"; }
p81() { _docker_php_run 8.1 php composer.prod.json "$@"; }
p82() { _docker_php_run 8.2 php composer.prod.json "$@"; }
p83() { _docker_php_run 8.3 php composer.prod.json "$@"; }
p84() { _docker_php_run 8.4 php composer.prod.json "$@"; }
p85() { _docker_php_run 8.5 php composer.prod.json "$@"; }
