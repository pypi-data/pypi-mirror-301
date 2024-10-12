#!/bin/bash
set -ueo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
readonly DIR

VERSION_FILE="$DIR/../VERSION"
readonly VERSION_FILE

# shellcheck disable=SC1091
source "$DIR/functions.bash"

# Retrieve current git sha
TAG="$(get_git_sha)"
VERSION="$(cat "$VERSION_FILE")"
if [ -z "$(is_dirty)" ]; then
    # Working dir is clean, attempt to use tag
    GITTAG="$(get_tag_at_head)"

    # If git tag found, use it
    if [ -n "$GITTAG" ]; then
        TAG="$GITTAG"
        VERSION="$GITTAG"
    fi
fi
readonly TAG

# Load project name from project manifest
PROJECT_NAME="$(get_project_name)"
readonly PROJECT_NAME

echo "Updating version in '$VERSION_FILE' to: $VERSION"
echo "$VERSION" >"$VERSION_FILE"

echo "Building $PROJECT_NAME:$TAG..."
if ! task build; then
    # Revert the version file if erroring out
    echo "Reverting version to repository value..."
    git checkout -- "$VERSION_FILE"
    echo
    echo "Aborting..." >&2
    exit 1
fi
# Revert the version after the dist/ was built
echo "Reverting version to repository value..."
git checkout -- "$VERSION_FILE"

# Build the image
for ARCH in linux/x86_64 linux/arm64; do
    docker build \
        --build-arg PROJECT_NAME="$PROJECT_NAME" \
        --build-arg VERSION="$VERSION" \
        --platform "$ARCH" \
        -t "$PROJECT_NAME:$TAG" \
        .

    echo "Built $PROJECT_NAME:$TAG for $ARCH..."
done
