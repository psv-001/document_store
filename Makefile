APP_NAME = 'apiservice/document_store_api'
VERSION = '0.0.1'

.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


build: ## Build command.
	@docker build -t $(APP_NAME):$(VERSION) .

run:  ## Run command.
	@docker run -td --name=$(APP_NAME) -p 17736:8000 $(APP_NAME):$(VERSION)

remove-image: ## Remove image
	@docker rmi -f $(APP_NAME):$(VERSION)

remove: ## Remove container
	@docker rm -f $(APP_NAME)

clean: ## clean egg-info
	@rm -rf *.egg-info
