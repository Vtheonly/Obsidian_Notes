#!/bin/bash

# Find all directories in the current location, excluding hidden ones
folders=$(find . -maxdepth 1 -type d -not -path '*/\.*')

# Remove the current directory (.) from the list
folders=$(echo "$folders" | sed 's|^\./||' | tail -n +2)

# Check if any folders are found
if [ -z "$folders" ]; then
  echo "No folders found in the current directory."
  exit 1
fi

# Display the folders found
echo "Folders found:"
echo "$folders"

# Ask the user if they want to process these folders
echo "Do you want to process these folders? (y/n)"
read -r user_confirmation

# Check if the user agrees to process the folders
if [[ "$user_confirmation" != "y" && "$user_confirmation" != "Y" ]]; then
  echo "Operation cancelled by the user."
  exit 0
fi

# Loop through each folder found
while IFS= read -r folder; do
  # Create the 'Lessons' and 'Active Recall Test' subfolders if they don't exist
  mkdir -p "$folder/Lessons" "$folder/Active Recall Test"

  # Find all files directly inside the folder, excluding subdirectories
  files=$(find "$folder" -maxdepth 1 -type f)

  # Check if any files are found
  if [ -z "$files" ]; then
    echo "No files found in $folder."
  else
    echo "Files found in $folder:"

    # Loop through each file found
    while IFS= read -r file; do
      # Display the file and prompt the user for confirmation
      echo "Move file: $file? (y/n)"
      read -r answer

      # Check if the answer is 'y' or 'Y'
      if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
        # Move the file to the 'Lessons' folder
        mv "$file" "$folder/Lessons/"
        echo "Moved $file to '$folder/Lessons/'"
      else
        echo "Skipped $file"
      fi
    done <<< "$files"
  fi

  echo "Created 'Active Recall Test' in $folder"
done <<< "$folders"
