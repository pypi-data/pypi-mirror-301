#!/usr/bin/env bash

CURRENT_BRANCH=$(git symbolic-ref --short HEAD)
PUBLISH_BRANCH="publish"
AUTHOR_NAME="Syseleven"
AUTHOR_MAIL="doc@syseleven.de"

if [ "$CURRENT_BRANCH" = "$PUBLISH_BRANCH" ]; then
  echo "Please use another branch than $PUBLISH_BRANCH before running this script."
  exit 1
fi

# remove previous builds
if [ -d "dist" ]; then
  rm -r "dist"
fi

# stash all changes
git stash -q

# delete previous publishing branch
if git show-ref -q "refs/heads/$PUBLISH_BRANCH"; then
    git branch -q -D "$PUBLISH_BRANCH"
fi

# switch to publishing branch
git checkout -q -b publish

# change author on all commits
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --env-filter "
    GIT_AUTHOR_NAME='$AUTHOR_NAME'
    GIT_AUTHOR_EMAIL='$AUTHOR_MAIL'
    GIT_COMMITTER_NAME='$AUTHOR_NAME'
    GIT_COMMITTER_EMAIL='$AUTHOR_MAIL'
  " HEAD

# build wheel
uv build

# return to initial branch and unstash changes
git checkout -q "$CURRENT_BRANCH"
git stash pop -q

# ask user for confirmation
read -p "Are you sure you want to publish? " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  : "${UV_PUBLISH_URL:=https://upload.pypi.org/legacy/}"

  # upload wheel
  UV_PUBLISH_URL="$UV_PUBLISH_URL" uv publish
fi
