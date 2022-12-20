name=kpipe
repo=cmantas/$(name)

test:
	@echo $(name) $(repo)

build:
# Builds a local "testing" image
# In case build is ran on a mac M1 family chip, we can use docker "buildx"
	docker buildx build --platform=linux/amd64 . -t $(name):testing
tag-latest:
# Tagging the "testing" as "latest"
	docker image tag $(name):testing $(repo):latest
push-latest:
# Push the local image tagged as "latest" to the docker registry
	docker push $(repo):latest
