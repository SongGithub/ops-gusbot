#!/usr/bin/env bash
set -ex
image_tag=$1
dcr="docker-compose -f deployment/docker-compose.yml run --rm"

usage() { echo "usage: $0 <image_tag>" && exit 1; }

die() { echo "$*" >&2; exit 1; }

# get image_name from deployment/env/defaults.yml
get_image_name() {
  defaults_json=$(cat deployment/envs/defaults.yml | $dcr yaml2json)
  image_name=$(echo $defaults_json | $dcr aws-jq jq -r '.dockerImage')
  echo "$image_name"
}

# extract aws_account_id and region from image_name
get_ecr_details() {
  image_name=$1
  REGEX_ECR='^([0-9]{12}).dkr.ecr.([a-z0-9-]*).amazonaws.com/[.]*'
  if [[ "$image_name" =~ $REGEX_ECR ]]; then
    echo ${BASH_REMATCH[1]}_${BASH_REMATCH[2]}
  else
    die "there was something wrong with docker image path set in deployment/env/defaults.yml"
  fi
}

ecr_login() {
  echo "  trying to login ECR...."
  image_name=$(get_image_name)
  ecr_details=$(get_ecr_details "$image_name")
  aws_account_id=${ecr_details%%_*}
  region=${ecr_details##*_}
  ecr_auth_token=$($dcr aws-jq aws ecr get-authorization-token \
    --region "$region" \
    --output text \
    --query 'authorizationData[].authorizationToken' | base64 --decode | cut -d: -f2)
  echo $ecr_auth_token | docker login -u \
    AWS https://"$aws_account_id".dkr.ecr."$region".amazonaws.com \
    --password-stdin
}


build_and_push_image() {
  tag=$1
  full_image_name=$(get_image_name):"$tag"
  docker build --quiet -t "$full_image_name" .
  docker push "$full_image_name"
}

check_aws_token() {
  $dcr aws-jq aws sts get-caller-identity &>/dev/null || die "unable to connect to AWS"
}

# main
[ "$#" -ne 1 ] && usage
docker-compose -f deployment/docker-compose.yml pull
check_aws_token
ecr_login
build_and_push_image "$image_tag"
