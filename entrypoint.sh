#!/bin/bash

# Set environment variables from inputs
export GITHUB_TOKEN="${INPUT_GITHUB_TOKEN}"
export GITHUB_OWNER="${INPUT_GITHUB_OWNER}"
export REPOS="${INPUT_REPOS}"
export VERIFY_ONLY="${INPUT_VERIFY_ONLY}"

# Build command based on inputs
COMMAND="python -m src.main"

if [ "${VERIFY_ONLY}" = "true" ]; then
    COMMAND="${COMMAND} --verify-only"
fi

if [ -n "${REPOS}" ]; then
    COMMAND="${COMMAND} --repos ${REPOS}"
fi

# Execute the command
exec $COMMAND 