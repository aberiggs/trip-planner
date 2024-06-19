#!/bin/bash

start() {
    echo "Building and running the project locally..."
    # sam build
    poetry run sam build --use-container
    sam local start-api --profile willytripplanner
}

build() {
    echo "Building the project..."
    poetry run sam build --use-container
}

deploy() {
    echo "Building and deploying the project..."
    poetry run sam build --use-container
    sam deploy
}

if [ $# -eq 0 ]; then
    echo "Usage: $0 {start|build|deploy}..."
    exit 1
fi

# Process each command
for command in "$@"; do
    case $command in
        start)
            start
            ;;
        build)
            build
            ;;
        deploy)
            deploy
            ;;
        *)
            echo "Invalid command: $command"
            echo "Usage: $0 {start|build|deploy}..."
            exit 1
            ;;
    esac
done