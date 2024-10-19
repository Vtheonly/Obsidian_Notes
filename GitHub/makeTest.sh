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
  # Define the 'Lessons' and 'Active Recall Test' subfolders
  lesson_folder="$folder/Lessons"
  active_recall_folder="$folder/Active Recall Test"

  # Check if the 'Lessons' folder exists
  if [ -d "$lesson_folder" ]; then
    # Loop through each markdown file in the first level of the 'Lessons' folder
    for lesson_file in "$lesson_folder"/*.md; do
      # Check if any markdown files exist
      if [ ! -e "$lesson_file" ]; then
        echo "No markdown files found in $lesson_folder"
        break
      fi

      # Get the base filename without the path
      base_filename=$(basename "$lesson_file")

      # Define the corresponding test file name in the 'Active Recall Test' folder
      test_file="$active_recall_folder/Test - $base_filename"

      # Ensure the corresponding subfolder structure exists in the 'Active Recall Test' folder
      mkdir -p "$active_recall_folder"

      # Check if the test file already exists
      if [ ! -f "$test_file" ]; then
        # Create the test markdown file
        touch "$test_file"
        echo "Created $test_file"
      else
        echo "Skipped $test_file, already exists."
      fi
    done

    # Additionally, check for any subfolders in 'Lessons'
    for subfolder in "$lesson_folder"/*/; do
      if [ -d "$subfolder" ]; then
        # Get the subfolder name
        subfolder_name=$(basename "$subfolder")

        # Define the corresponding test file name for the subfolder
        test_file="$active_recall_folder/Test - $subfolder_name"

        # Ensure the corresponding subfolder structure exists in the 'Active Recall Test' folder
        mkdir -p "$active_recall_folder"

        # Check if the test file already exists
        if [ ! -f "$test_file" ]; then
          # Create the test markdown file
          touch "$test_file"
          echo "Created $test_file for subfolder $subfolder_name"
        else
          echo "Skipped $test_file for subfolder $subfolder_name, already exists."
        fi
      fi
    done
  else
    echo "Lessons folder $lesson_folder does not exist!"
  fi
done <<< "$folders"

