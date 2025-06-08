#!/bin/bash
set -euo pipefail

# Process files and directories depth-first
find . -depth -print0 | while IFS= read -d '' -r item; do
    # Skip current directory
    if [ "$item" = "." ]; then
        continue
    fi
    
    # Get directory and base name
    dir=$(dirname -- "$item")
    name=$(basename -- "$item")

    # Process directories: replace spaces and dots with underscores
    if [ -d "$item" ]; then
        newname=$(echo "$name" | tr ' .' '_')
        if [ "$name" != "$newname" ]; then
            mv -v -- "$item" "$dir/$newname"
        fi
    
    # Process files: replace spaces and dots (except extension) with underscores
    else
        # Separate filename and extension
        base=${name%.*}
        ext=${name##*.}
        
        # Handle files without extensions
        if [ "$base" = "$name" ]; then
            ext=""
            newbase=$(echo "$base" | tr ' .' '_')
            newname="$newbase"
        else
            newbase=$(echo "$base" | tr ' .' '_')
            newname="$newbase.$ext"
        fi

        # Rename if changed
        if [ "$name" != "$newname" ]; then
            mv -v -- "$item" "$dir/$newname"
        fi
    fi
done

echo "Renaming completed successfully"