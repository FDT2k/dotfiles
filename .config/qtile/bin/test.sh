#!/bin/bash
terminator -e "eval $(docker-machine env wedplan-manager-2); $SHELL; lazydocker"
terminator -e "eval $(docker-machine env wedplan-worker-3); $SHELL; lazydocker"

terminator -e "eval $(docker-machine env wedplan-worker-4); $SHELL; lazydocker"
