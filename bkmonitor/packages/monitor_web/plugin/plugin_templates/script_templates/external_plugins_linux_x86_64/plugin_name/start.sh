#!/bin/bash

export LC_ALL=C
export LANG=C

cd `dirname $0`
source ./parse_yaml.sh
create_variables etc/env.yaml

./{{ collector_json.linux.filename }} ${BK_CMD_ARGS}
