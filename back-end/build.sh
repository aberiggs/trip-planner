#!/bin/bash

copy_to_requirement() {
    poetry export --without-hashes > src/requirements.txt
    if [ $? -ne 0 ]; then
        exit 1
    fi
}

run_test() {
    poetry run pytest -s tests/unit/src/planner
    if [ $? -ne 0 ]; then
        exit 1
    fi
}

run_build() {
    poetry run sam build --use-container
    if [ $? -ne 0 ]; then
        exit 1
    fi
}

run_local() {
    sam local start-api --profile willytripplanner
    if [ $? -ne 0 ]; then
        exit 1
    fi
}

run_deploy() {
    sam deploy
    if [ $? -ne 0 ]; then
        exit 1
    fi
}

if [ $# -eq 0 ]; then
    echo "Usage: $0 {start|test|build|deploy}..."
    exit 1
fi

# Process each command
for command in "$@"; do
    case $command in
        start)
            echo "Building and running the project locally..."
            copy_to_requirement
            run_test
            run_build
            run_local
            ;;
        test)
            echo "Testing project..."
            run_test
            ;;
        build)
            echo "Building the project..."
            copy_to_requirement
            run_test
            run_build
            ;;
        deploy)
            echo "Building and deploying the project..."
            copy_to_requirement
            run_test
            run_build
            run_deploy
            ;;
        *)
            echo "Invalid command: $command"
            echo "Usage: $0 {start|build|deploy}..."
            exit 1
            ;;
    esac
done