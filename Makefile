build:
# In case build is ran on a mac M1 family chip, we can use docker "buildx"
	docker buildx build --platform=linux/amd64 . -t kpipe:testing
tag-latest:
# Tagging the "testing" as "latest"
	docker image tag kpipe:testing cmantas/kpipe:latest
push-latest:
# Push the local image tagged as "latest" to the docker registry
	docker push cmantas/kpipe:latest
