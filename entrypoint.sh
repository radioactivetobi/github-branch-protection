#!/bin/bash

# Set environment variables from inputs
export GITHUB_TOKEN="${INPUT_GITHUB_TOKEN}"
export GITHUB_OWNER="${INPUT_GITHUB_OWNER}"
export REPOSITORIES="${INPUT_REPOSITORIES}"
export VERIFY_ONLY="${INPUT_VERIFY_ONLY}"

# Debug information
echo "Setting up environment variables:"
echo "GITHUB_OWNER: ${GITHUB_OWNER}"
echo "REPOSITORIES: ${REPOSITORIES}"
echo "VERIFY_ONLY: ${VERIFY_ONLY}"

# Build command based on inputs
COMMAND="python -m src.main"

if [ "${VERIFY_ONLY}" = "true" ]; then
    COMMAND="${COMMAND} --verify-only"
fi

if [ -n "${REPOSITORIES}" ]; then
    # Convert space-separated list to command line arguments
    COMMAND="${COMMAND} --repos ${REPOSITORIES// / }"
fi

# Debug command
echo "Executing: ${COMMAND}"
exec $COMMAND 