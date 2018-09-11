#!/usr/bin/env bash
# assumptions:
#   - users have authenticated to k8s environment
#   - deployment folder containing deployment templates, envs and scripts exist under root dir.

set -e
environment=$1
application_version=${2:-latest}
usage() { echo "$0 <env name> <optional docker image tag>"; exit 1; }
die() { printf '%s\n' "$*" >&2; exit 1; }

# clean up existing k8s config files
yaml_clean() {
  if [ -d deployment/_build ]; then
    rm -rf deployment/_build
  fi
}
prepare() {
  yaml_clean
}

compile_and_apply() {
  tmp_path="$1"
  mkdir -p "$tmp_path"

  for file in deployment/templates/*.yml ; do
    filename=$(echo $file | sed -e 's/deployment\///g' | sed -e 's/templates\///g')
    ktmpl $file \
      --parameter-file deployment/envs/defaults.yml \
      --parameter-file deployment/envs/${environment}.yml \
      --parameter containerTag $application_version > ${tmp_path}/$filename
    kubectl apply -f ${tmp_path}/$filename
  done
}

# main
[[ "$#" -lt 1 ]] && usage
echo "~~~ doing some preparation work..."
prepare

echo "~~~ :passenger_ship: compile and apply config files for the Jupiter platforms..."
compile_and_apply "deployment/_build"
