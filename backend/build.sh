#!/bin/bash

PROFILE="default"

usage() {
    echo "Usage: $0 [-p profile] [build|deploy|start|test]"
    exit 1
}

copy_to_requirement() {
    poetry export --without-hashes > src/requirements.txt
    if [ $? -ne 0 ]; then
        exit 1
    fi
}

run_test() {
    poetry run pytest -s tests
    if [ $? -ne 0 ]; then
        exit 1
    fi
}

run_format() {
    poetry run black --target-version=py35 . --line-length 80
    poetry run pre-commit run --all-files
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
    sam local start-api --profile $PROFILE
    if [ $? -ne 0 ]; then
        exit 1
    fi
}

run_deploy() {
    sam deploy --profile $PROFILE
    if [ $? -ne 0 ]; then
        exit 1
    fi
}

while getopts ":p:" opt; do
  case $opt in
    p)
      PROFILE=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      usage
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      usage
      ;;
  esac
done

echo "Set profile to $PROFILE"

shift $((OPTIND - 1))

if [ $# -eq 0 ]; then
    echo "No action specified."
    usage
fi

ACTION=$1

if [ $# -eq 0 ]; then
    echo "Usage: $0 {start|test|build|deploy}..."
    exit 1
fi

case $ACTION in
    start)
        echo "Building and running the project locally..."
        copy_to_requirement
        # run_test
        run_build
        run_local
        ;;
    format)
        echo "Formatting..."
        run_format
        ;;
    test)
        echo "Testing project..."
        run_test
        ;;
    build)
        echo "Building the project..."
        copy_to_requirement
        run_format
        run_test
        run_build
        ;;
    deploy)
        echo "Building and deploying the project..."
        copy_to_requirement
        run_format
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
