# Git Commands and Concepts

Git is a distributed version control system, and GitHub is a platform that hosts Git repositories. Below is a summary of some essential Git commands and their uses:

### Basic Commands

- **Clone**: Downloads a repository from GitHub to your local machine.
  - **Example**: 
    ```bash
    git clone https://github.com/username/repository.git
    ```

- **Add**: Stages changes for the next commit. This tells Git which files you want to include in your next commit.
  - **Example**:
    ```bash
    git add file.txt          # Stages a specific file
    git add .                 # Stages all changes in the current directory
    ```

- **Commit**: Saves the staged changes to your local repository.
  - **Example**:
    ```bash
    git commit -m "Commit message"
    ```

- **Push**: Uploads your committed changes to a remote repository (e.g., GitHub).
  - **Example**:
    ```bash
    git push origin master    # Pushes changes to the 'master' branch on the 'origin' remote
    ```

- **Pull**: Downloads changes from a remote repository and merges them into your local repository.
  - **Example**:
    ```bash
    git pull origin master    # Pulls changes from the 'master' branch on the 'origin' remote
    ```

- **Git Status**: Displays the state of your working directory and staging area. It shows which files have been modified, which are staged for the next commit, and which are untracked.
  - **Example**:
    ```bash
    git status
    ```

- **Git Init**: Initializes a new Git repository in your current directory.
  - **Example**:
    ```bash
    git init
    ```

### Additional Commands

- **Git Branch**: Manages branches within your repository.
  - **Example**:
    ```bash
    git branch                 # Lists all branches
    git branch new-branch      # Creates a new branch
    ```

- **Git Checkout**: Switches between branches.
  - **Example**:
    ```bash
    git checkout branch-name   # Switches to the specified branch
    ```

- **Git Merge**: Merges changes from one branch into another.
  - **Example**:
    ```bash
    git merge feature-branch   # Merges changes from 'feature-branch' into the current branch
    ```

- **Git Log**: Displays the commit history.
  - **Example**:
    ```bash
    git log
    ```

- **Git Remote**: Manages connections to remote repositories.
  - **Example**:
    ```bash
    git remote                 # Lists all remote repositories
    ```

These commands are fundamental for working with Git and GitHub, enabling you to manage your code effectively and collaborate with others.