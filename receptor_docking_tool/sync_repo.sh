#!/bin/bash

REPO_DIR="/Users/cosmopax/Desktop/webpage/Artificial_Life_Institute"
REPO_URL="https://github.com/cosmopax/artificial-life-institute.github.io.git"

# Navigate to the local repository
cd "$REPO_DIR" || exit

# Pull updates from GitHub
echo "Pulling updates from GitHub..."
git pull origin main

# Stage, commit, and push local changes (if any)
echo "Pushing local changes to GitHub..."
git add .
git commit -m "Automatic sync: $(date)" || echo "No changes to commit."
git push origin main
