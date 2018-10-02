# Gus Bot

[![Build status](https://badge.buildkite.com/136ac15e403f9d3be9d1dd3910781e553a17a63b4c44866346.svg?branch=master)](https://buildkite.com/myob/ops-gus-bot)

This is a Slackbot developed by Platform Enablement to help in the education of users in our channel.

## Functionality

### @here plugin

This plugin looks for `@here` and `@channel` messages and replies with a request not to do so as well as a link to Platform Enablement's Slacktiquete.

## Development

This project is written in python and run in Kubernetes. You can find more information about it's deployment in [the pipeline](./.buildkite/pipeline.yml). There are 2 versions of the bot:

- One is continuously deployed into the SIT cluster(`europa-preprod`) as `Gus Bot Edge` and it is used for testing purposes
- The other is deployed on demand (by unblocking the pipeline) in the Prod cluster (`europa`) as `Gus Bot`

## Deployment

- It is setup to be deployed in Buildkite pipeline.
- __! Important__: There is one critical dependency that is NOT deployed automatically for security reasons. Once valid secret _SLACKBOT_API_TOKEN_ is not available to the app, there will be a warning in app's log `settings.API_TOKEN doesn't exist`. In this case, maintainers should:
  - login in to the cluster in CLI, i.e. `myob-auth k -e <env-slug> -n platform-enablement`
  - run kube cmd to verify your secret `kubectl get secret ops-gus-bot -n platform-enablement`
  - If there was a secret in k8s cluster, please run `kubectl delete secret ops-gus-bot -n platform-enablement` prior to run the next step
  - run kube cmd to upload your secret `kubectl create secret generic --from-literal=SLACKBOT_API_TOKEN=<raw slack api token> ops-gus-bot -n platform-enablement`

## How to use

- By default, no one is on the _White List_ which exempts Slack users from being policed by the _Gus Bot_.
- In Slack, talk to _Gus Bot_ directly to configure the _White list_. Common cmd are:
  - list
  - add @<slack-user> to #<channel>
  - remove @<slack-user> to #<channel>
  - sudo rm -rf @<slack-user>

## TODO/Wishlist:

- Add health check + Alerts in case the application suddenly stops working.
- Allow users to be added by Slack User Group. 
- Data migration/import-export 
