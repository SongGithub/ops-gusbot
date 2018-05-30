#!/usr/bin/env bash
# assumptions:
#   - users have authenticated to k8s environment
#   - deployment folder containing deployment templates, envs and scripts exist under root dir.

set -e
environment=$1
application_version=${2:-latest}
usage() { echo "$0 <env name> <optional docker image tag>"; exit 1; }


dc="docker-compose -f deployment/docker-compose.yml"
dcr="$dc run --rm"

die() { printf '%s\n' "$*" >&2; exit 1; }

# clean up existing k8s config files
yaml_clean() {
  if [ -d deployment/_build ]; then
    rm -rf deployment/_build
  fi
}

cleanup() {
  echo "~~~ :docker: Cleaning up after docker-compose"
  $dc rm -f -v
}
trap cleanup EXIT

# without docker images ready, the stdout of ktmpl might be invalid.
prepare() {
  $dc pull
  yaml_clean
}

compile_and_apply() {
  tmp_path="$1"
  mkdir -p "$tmp_path"
  for file in deployment/templates/*.yml ; do
    template=$(echo $file | sed -e 's/deployment\///g')
    filename=$(echo $template | sed -e 's/templates\///g')
    # not using pipe here because it causes intermittent issue
    # "docker network already exists"
    $dcr ktmpl $template \
      --parameter-file envs/defaults.yml \
      --parameter-file envs/"$environment".yml \
      --parameter containerTag $application_version > "$tmp_path"/$filename
    relative_path=$(echo "$tmp_path"/$filename | sed -e 's/deployment\///g')
    $dcr kubectl apply -f "$relative_path"
  done
}


verify() {
  defaults_json=$(cat deployment/envs/defaults.yml | $dcr yaml2json)
  deploy_name=$(echo $defaults_json | $dcr aws-jq jq -r '.name')
  namespace=$(echo $defaults_json | $dcr aws-jq jq -r '.namespace')
  echo "verifying: "deployment/"$deploy_name"
  $dcr kubectl \
    --request-timeout 180s \
    rollout status deployment/"$deploy_name" \
    -n $namespace \
    --watch=true
}

# main
[[ "$#" -lt 1 ]] && usage
echo "~~~ doing some preparation work..."
prepare

echo "~~~ :passenger_ship: compile and apply config files for the Jupiter platforms..."
compile_and_apply "deployment/_build"

# note:
# This next step is important to get a rough idea about if your app is running
# correctly on Jupiter. However, be aware that the AWS/RDS instance
# creation time is not deterministic, so the request-timeout section may cause
# time-out error.

echo "~~~ :sunglasses: verifying your deployment"
verify
