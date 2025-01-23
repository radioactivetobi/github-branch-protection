#!/bin/bash

# Build command based on inputs
COMMAND="python -m src.main"

if [ "${INPUT_VERIFY_ONLY}" = "true" ]; then
    COMMAND="${COMMAND} --verify-only"
fi

if [ -n "${INPUT_REPOS}" ]; then
    COMMAND="${COMMAND} --repos ${INPUT_REPOS}"
fi

if [ -n "${INPUT_REPOS_FILE}" ]; then
    COMMAND="${COMMAND} --repos-file ${INPUT_REPOS_FILE}"
fi

# Execute the command
exec $COMMAND 