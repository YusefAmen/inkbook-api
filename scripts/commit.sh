#!/bin/bash

# Check if a message was provided
if [ -z "$1" ]; then
    echo "Usage: ./commit.sh \"your commit message\""
    echo "Commit message should follow conventional commits format:"
    echo "  feat: add new feature"
    echo "  fix: resolve bug"
    echo "  docs: update documentation"
    echo "  style: format code"
    echo "  refactor: restructure code"
    echo "  test: add tests"
    echo "  chore: update dependencies"
    exit 1
fi

# Get the commit message from the first argument
COMMIT_MSG="$1"

# Add all changes
git add .

# Commit with the provided message
git commit -m "$COMMIT_MSG"

# Push to the current branch
git push origin HEAD

echo "✅ Changes committed and pushed successfully!"
echo "Commit message: $COMMIT_MSG" 
