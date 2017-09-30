.PHONY: test publish deploy/dev deploy/prod ecr-login

AWS_ACCOUNT_ID := 693429498512
REPO_URL := ${AWS_ACCOUNT_ID}.dkr.ecr.ap-southeast-2.amazonaws.com/platform-enablement/gusbot
BUILD_TAG := ${BUILDKITE_BUILD_NUMBER}-${BUILDKITE_COMMIT}
DCR := docker-compose run --rm

install:
	@pip install -r requirements.txt

test:
	@echo "+++ Testing all the things"

publish: ecr-login
	@echo "--- Building :docker: image [${BUILD_TAG}]"
	docker build -t "${REPO_URL}:${BUILD_TAG}" .
	@echo "+++ Publishing :docker: image [${BUILD_TAG}]"
	docker push "${REPO_URL}:${BUILD_TAG}"

deploy/dev:
	@echo "+++ Deploy to preprod"
	${DCR} helm init --client-only --tiller-namespace platform-enablement
	${DCR} helm upgrade --install ops-gus-bot ./chart \
		--tiller-namespace platform-enablement \
		--namespace platform-enablement \
		--set image.tag=${BUILD_TAG} \
		--set build=${BUILDKITE_BUILD_NUMBER}

deploy/prod:
	@echo "+++ Deploy to prod"
	${DCR} helm init --client-only --tiller-namespace platform-enablement
	${DCR} helm upgrade --install ops-gus-bot ./chart \
		--tiller-namespace platform-enablement \
		--namespace platform-enablement	\
		--set image.tag=${BUILD_TAG} \
		--set build="${BUILDKITE_BUILD_NUMBER}"

ecr-login:
	@echo "--- Docker login"
	${DCR} aws ecr get-login \
	      --no-include-email \
	      --registry-ids ${AWS_ACCOUNT_ID} \
	      --region ap-southeast-2 | tr -d '\r' | bash
