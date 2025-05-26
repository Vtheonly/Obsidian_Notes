#!/bin/bash

# Simple and effective renaming script for both directories and files
# Converts format like "09.Sorting.Algorithms" to "09. Sorting Algorithms"

set -e  # Exit on error

# Simple function to rename items
rename_items() {
    local base_path="$1"
    local dry_run="${2:-true}"  # Default to dry run
    
    echo "=== Renaming Items ==="
    echo "Path: $base_path"
    echo "Dry run: $dry_run"
    echo ""
    
    # Process from deepest level first to avoid issues with changing paths
    find "$base_path" -depth -type f -o -type d | while read -r item; do
        # Skip the base path itself
        [[ "$item" == "$base_path" ]] && continue
        
        local item_basename=$(basename "$item")
        local parent_dir=$(dirname "$item")
        
        # Skip if it already has spaces (already renamed)
        if [[ "$item_basename" == *" "* ]]; then
            continue
        fi
        
        # Skip if it doesn't contain dots (nothing to convert)
        if [[ "$item_basename" != *.* ]]; then
            continue
        fi
        
        local new_name=""
        
        if [[ -d "$item" ]]; then
            # DIRECTORY processing
            if [[ "$item_basename" =~ ^([0-9][0-9]?)\.(.*) ]]; then
                # Numbered directory: "09.Sorting.Algorithms" -> "09. Sorting Algorithms"
                local number="${BASH_REMATCH[1]}"
                local rest="${BASH_REMATCH[2]}"
                new_name="$number. $(echo "$rest" | tr '.' ' ')"
            else
                # Non-numbered directory: "Algorithms.Pattern.Matching" -> "Algorithms Pattern Matching"
                new_name=$(echo "$item_basename" | tr '.' ' ')
            fi
            echo "[DIR]  '$item_basename' -> '$new_name'"
            
        elif [[ -f "$item" ]]; then
            # FILE processing - preserve the last extension
            if [[ "$item_basename" =~ ^(.+)\.([^.]+)$ ]]; then
                local name_without_ext="${BASH_REMATCH[1]}"
                local extension="${BASH_REMATCH[2]}"
                
                if [[ "$name_without_ext" =~ ^([0-9][0-9]?)\.(.*) ]]; then
                    # Numbered file: "01.Algorithm.Binary.Search.md" -> "01. Algorithm Binary Search.md"
                    local number="${BASH_REMATCH[1]}"
                    local rest="${BASH_REMATCH[2]}"
                    new_name="$number. $(echo "$rest" | tr '.' ' ').$extension"
                else
                    # Non-numbered file: "Concepts.Big.O.Notation.md" -> "Concepts Big O Notation.md"
                    new_name="$(echo "$name_without_ext" | tr '.' ' ').$extension"
                fi
                echo "[FILE] '$item_basename' -> '$new_name'"
            fi
        fi
        
        # Perform the rename if not in dry run mode and we have a new name
        if [[ "$dry_run" != "true" && -n "$new_name" ]]; then
            local new_path="$parent_dir/$new_name"
            if mv "$item" "$new_path" 2>/dev/null; then
                echo "  ✓ Renamed successfully"
            else
                echo "  ✗ Failed to rename"
            fi
        fi
    done
}

# Alternative: Use a simple find and rename approach
simple_rename() {
    local base_path="$1"
    local dry_run="${2:-true}"
    
    echo "=== Simple Pattern-Based Rename ==="
    echo "Path: $base_path"
    echo "Dry run: $dry_run"
    echo ""
    
    # Find all items with dots in their names
    find "$base_path" -name "*.*" | sort -r | while read -r item; do
        local basename_item=$(basename "$item")
        local dirname_item=$(dirname "$item")
        
        # Skip if already has spaces
        [[ "$basename_item" == *" "* ]] && continue
        
        local new_name=""
        local item_type=""
        
        if [[ -d "$item" ]]; then
            item_type="DIR"
            # For directories, convert all dots to spaces, but handle numbered ones specially
            if [[ "$basename_item" =~ ^[0-9][0-9]?\. ]]; then
                # Extract number and rest
                local num=$(echo "$basename_item" | cut -d'.' -f1)
                local rest=$(echo "$basename_item" | cut -d'.' -f2- | tr '.' ' ')
                new_name="$num. $rest"
            else
                new_name=$(echo "$basename_item" | tr '.' ' ')
            fi
        elif [[ -f "$item" ]]; then
            item_type="FILE"
            # For files, preserve the last extension
            local extension="${basename_item##*.}"
            local name_part="${basename_item%.*}"
            
            if [[ "$name_part" =~ ^[0-9][0-9]?\. ]]; then
                # Numbered file
                local num=$(echo "$name_part" | cut -d'.' -f1)
                local rest=$(echo "$name_part" | cut -d'.' -f2- | tr '.' ' ')
                new_name="$num. $rest.$extension"
            else
                # Non-numbered file
                new_name="$(echo "$name_part" | tr '.' ' ').$extension"
            fi
        fi
        
        if [[ -n "$new_name" && "$new_name" != "$basename_item" ]]; then
            echo "[$item_type] '$basename_item' -> '$new_name'"
            
            if [[ "$dry_run" != "true" ]]; then
                local new_path="$dirname_item/$new_name"
                if mv "$item" "$new_path" 2>/dev/null; then
                    echo "  ✓ Success"
                else
                    echo "  ✗ Failed"
                fi
            fi
        fi
    done
}

# Mass rename using rename command (if available)
mass_rename() {
    local base_path="$1"
    local dry_run="${2:-true}"
    
    echo "=== Mass Rename (using rename command) ==="
    
    if ! command -v rename &> /dev/null; then
        echo "The 'rename' command is not available. Install it with:"
        echo "  Ubuntu/Debian: sudo apt install rename"
        echo "  CentOS/RHEL: sudo yum install prename"
        return 1
    fi
    
    local rename_opts=""
    [[ "$dry_run" == "true" ]] && rename_opts="-n"
    
    echo "Processing directories..."
    find "$base_path" -type d -name "*.*" | while read -r dir; do
        local parent=$(dirname "$dir")
        cd "$parent" || continue
        local basename_dir=$(basename "$dir")
        
        # Skip if already has spaces
        [[ "$basename_dir" == *" "* ]] && continue
        
        # Apply rename patterns
        if [[ "$basename_dir" =~ ^[0-9][0-9]?\. ]]; then
            # Numbered: 09.Word.Word -> 09. Word Word
            rename $rename_opts 's/^([0-9][0-9]?)\.(.*)/$1. $2/; s/\./ /g' "$basename_dir" 2>/dev/null || true
        else
            # Non-numbered: Word.Word -> Word Word
            rename $rename_opts 's/\./ /g' "$basename_dir" 2>/dev/null || true
        fi
    done
    
    echo "Processing files..."
    find "$base_path" -type f -name "*.*" | while read -r file; do
        local parent=$(dirname "$file")
        cd "$parent" || continue
        local basename_file=$(basename "$file")
        
        # Skip if already has spaces
        [[ "$basename_file" == *" "* ]] && continue
        
        # Apply rename patterns for files (preserve last extension)
        if [[ "$basename_file" =~ ^[0-9][0-9]?\. ]]; then
            # Numbered file
            rename $rename_opts 's/^([0-9][0-9]?)\.(.*)\.([^.]+)$/$1. $2.$3/; s/\.([^.]+)$/ $1/; s/ ([^. ]+)$/.$1/; s/\./ /g; s/ ([^. ]+)$/.$1/' "$basename_file" 2>/dev/null || true
        else
            # Non-numbered file
            rename $rename_opts 's/^(.*)\.([^.]+)$/$1 $2/; s/\./ /g; s/ ([^. ]+)$/.$1/' "$basename_file" 2>/dev/null || true
        fi
    done
}

# Main execution
echo "=== Directory and File Renaming Tool ==="
echo "Converts: '09.Sorting.Algorithms' -> '09. Sorting Algorithms'"
echo ""

# Configuration
BASE_DIR="${1:-.}"  # Use first argument or current directory
DRY_RUN="${2:-true}"  # Default to dry run

# Expand tilde in path
BASE_DIR="${BASE_DIR/#\~/$HOME}"

# Validate directory
if [[ ! -d "$BASE_DIR" ]]; then
    echo "Error: Directory '$BASE_DIR' not found!"
    echo "Usage: $0 [directory] [true|false]"
    echo "  directory: path to process (default: current directory)"
    echo "  dry_run: true for preview, false for actual rename (default: true)"
    exit 1
fi

echo "Target directory: $BASE_DIR"
echo "Dry run mode: $DRY_RUN"
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
    echo "*** PREVIEW MODE - No actual changes will be made ***"
    echo "*** Run with 'false' as second argument to perform renames ***"
    echo ""
fi

# Choose which method to use
echo "Choose renaming method:"
echo "1. Advanced rename (recommended)"
echo "2. Simple rename"
echo "3. Mass rename (requires 'rename' command)"
echo ""

# For automatic execution, use method 2 (simple rename)
echo "Using Simple Rename method..."
simple_rename "$BASE_DIR" "$DRY_RUN"

echo ""
echo "=== Summary ==="
if [[ "$DRY_RUN" == "true" ]]; then
    echo "Preview completed. To perform actual renames:"
    echo "  $0 \"$BASE_DIR\" false"
else
    echo "Renaming completed!"
fi

echo ""
echo "Note: Always backup your files before running with dry_run=false"
