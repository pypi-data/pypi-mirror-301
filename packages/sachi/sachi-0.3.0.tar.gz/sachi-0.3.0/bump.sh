#!/bin/sh -xe
if [ -z "$1" ]; then
  echo "Usage: $0 <version>"
  exit 1
fi

VERSION=$1
DEV_VERSION=$(echo $VERSION | awk -F. '{print $1 "." $2 "." $3+1 "-dev"}')

git switch --detach
sed -i.bak "s/^version = \".*\"/version = \"$VERSION\"/" pyproject.toml
git commit -am $VERSION
git tag $VERSION

git switch main
sed -i.bak "s/^version = \".*\"/version = \"$DEV_VERSION\"/" pyproject.toml
git commit -am $DEV_VERSION -m '[skip ci]'

git push origin $VERSION main
rm pyproject.toml.bak
