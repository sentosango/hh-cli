# HH.ru CLI Tool Makefile

.PHONY: build install uninstall clean help

.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@echo "  build     - Build wheel package"
	@echo "  install   - Install package to system"
	@echo "  uninstall - Uninstall package from system"
	@echo "  clean     - Clean build artifacts"

build:
	uv build --wheel --clear

install: build
	uv tool install dist/hh-*.whl

uninstall:
	uv tool uninstall hh

clean:
	rm -rf dist/ build/ *.egg-info/