.ONESHELL:
PROJECT := parrot_ar_drone

.PHONY: help
help:
	@echo "help ..."

.PHONY: build
build:
	@echo "$@ ..."
	@echo "Building Docker image ..."
	@cd ./"Parrot Environment"/"docker"/"parrot-sdk-ecosystem"
	@ls -l
	@docker build -t $(PROJECT):v1 .
	@cd ..

.PHONY: all
all: build
	@echo "$@ ..."
	@echo "ALL created ..."
		