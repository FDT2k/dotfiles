#!/bin/zsh

export KDA_WORK="$HOME/Documents/fastwork/kda-dev"


c2_82_dev () {
	docker run --rm --interactive --tty -e COMPOSER=composer.dev.json -e COMPOSER_HOME=/app/composer   --mount type=bind,source="$(echo $KDA_WORK)",target="$(echo $KDA_WORK)",readonly     --mount type=bind,source="$(pwd)",target=/app -w /app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.2-trixie composer2 "$@"
}

c2_82_prod () {
	docker run --rm --interactive --tty -e COMPOSER=composer.prod.json -e COMPOSER_HOME=/app/composer   --mount type=bind,source="$(echo $KDA_WORK)",target="$(echo $KDA_WORK)",readonly     --mount type=bind,source="$(pwd)",target=/app -w /app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.2-trixie composer2 "$@"
}

alias c2-82="docker run --rm --interactive --tty -e COMPOSER=composer.json -e COMPOSER_HOME=/app/composer   --mount type=bind,source="$(echo $KDA_WORK)",target="$(echo $KDA_WORK)",readonly     --mount type=bind,source="$(pwd)",target=/app -w /app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.2-trixie composer2"

alias c2-82-prod="docker run --rm --interactive --tty -e COMPOSER=composer.prod.json -e COMPOSER_HOME=/app/composer   --mount type=bind,source="$(echo $KDA_WORK)",target="$(echo $KDA_WORK)",readonly     --mount type=bind,source="$(pwd)",target=/app -w /app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.2-trixie composer2"

alias c2-82-shell="docker run --rm --interactive --tty -e COMPOSER=composer.prod.json -e COMPOSER_HOME=/app/composer   --mount type=bind,source="$(echo $KDA_WORK)",target="$(echo $KDA_WORK)",readonly     --mount type=bind,source="$(pwd)",target=/app -w /app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.2-trixie bash"

alias p82="docker run --rm --interactive --tty -e COMPOSER=composer.prod.json -e COMPOSER_HOME=/app/composer   --mount type=bind,source="$(echo $KDA_WORK)",target="$(echo $KDA_WORK)",readonly     --mount type=bind,source="$(pwd)",target=/app -w /app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.2-trixie php"



alias c2-83-dev="docker run --rm --interactive --tty -e COMPOSER=composer.dev.json -e COMPOSER_HOME=/app/composer   --mount type=bind,source="$(echo $KDA_WORK)",target="$(echo $KDA_WORK)",readonly     --mount type=bind,source="$(pwd)",target=/app -w /app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.3-trixie composer2"
alias c2-83-shell="docker run --rm --interactive --tty -e COMPOSER=composer.prod.json -e COMPOSER_HOME=/app/composer   --mount type=bind,source="$(echo $KDA_WORK)",target="$(echo $KDA_WORK)",readonly     --mount type=bind,source="$(pwd)",target=/app -w /app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.3-trixie bash"
# alias p83="docker run --rm --interactive --tty --add-host=host.docker.internal:host-gateway -e COMPOSER=composer.prod.json -e COMPOSER_HOME=/app/composer  -e XDEBUG_CONFIG=\"idekey=vsc client_host=host.docker.internal client_port=9003\" -e XDEBUG_MODE=develop,debug -e XDEBUG_TRIGGER=1   --mount type=bind,source="$(echo $KDA_WORK)",target="$(echo $KDA_WORK)",readonly     --mount type=bind,source="$(pwd)",target=/app -w /app  --user $(id -u):$(id -g) registry.gitlab.com/karsegard/docker-infomaniak:8.3-trixie php"

alias p83='docker run --rm -it \
  --add-host=host.docker.internal:host-gateway \
  -e COMPOSER=composer.prod.json \
  -e COMPOSER_HOME=/app/composer \
  -e XDEBUG_CONFIG="idekey=vsc client_host=host.docker.internal client_port=9003" \
  -e XDEBUG_MODE=debug,develop \
  -e XDEBUG_TRIGGER=1 \
  -e XDEBUG_START_WITH_REQUEST=yes \
  -e XDEBUG_CLIENT_HOST=host.docker.internal \
  -e XDEBUG_CLIENT_PORT=9003 \
  --mount type=bind,source="$KDA_WORK",target="$KDA_WORK",readonly \
  --mount type=bind,source="$(pwd)",target=/app \
  -w /app \
  --user $(id -u):$(id -g) \
  registry.gitlab.com/karsegard/docker-infomaniak:8.3-trixie php'


# Fonction générique
docker_php () {
  local version=$1   # ex: 8.2, 8.3...
  local cmd=$2       # ex: composer2, bash, php...
  local env=$3       # ex: dev, prod (optionnel)

  local image="registry.gitlab.com/karsegard/docker-infomaniak:${version}-trixie"
  local composer_file="composer.${env}.json"

  # Si env est vide => par défaut prod
  if [[ -z "$env" ]]; then
    composer_file="composer.prod.json"
  fi

  docker run --rm -it \
    -e COMPOSER="$composer_file" \
    -e COMPOSER_HOME=/app/composer \
    --mount type=bind,source="$KDA_WORK",target="$KDA_WORK",readonly \
    --mount type=bind,source="$(pwd)",target=/app \
    -w /app \
    --user "$(id -u):$(id -g)" \
    "$image" "$cmd"
}
