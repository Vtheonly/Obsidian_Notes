# Git Session Postmortem — Making `Pizza2` The Default And Single Timeline

## Clarify the Ask (Context Correction)

You asked for an Obsidian note that captures everything that happened here and turns it into a clean, repeatable process. The core goals were:

- Push the local project to GitHub.
    
- Make `Pizza2` the default branch on the remote.
    
- Collapse history so that `Pizza2` effectively becomes “the one and only head” (a single linear timeline for the repo).
    
- Fix HTTPS auth issues by switching to SSH.
    
- Resolve “unrelated histories” and merge conflicts (notably `.gitignore`).
    
- Verify that the remote reflects `Pizza2` as the canonical state.
    

This note documents what happened, why, and how to do it safely next time.

---

## Quick Timeline (What Happened)

1. Initialized a repo and tried to push over HTTPS.
    
    - Error: “Invalid username or token. Password authentication is not supported…”
        
2. Switched the remote to SSH:
    
    ```bash
    git remote remove Pizza_Stores_Tamplates
    git remote add origin git@github.com:Vtheonly/Pizza_Stores_Tamplates.git
    ```
    
3. Staged and committed; pushed `Pizza2`:
    
    ```bash
    git add .
    git commit -m "Initial commit"
    git push -u origin Pizza2
    ```
    
4. Tried to merge `Pizza2` into `main` locally, then push `main`.
    
    - Remote `main` had different history → pull/merge failed with “unrelated histories”.
        
5. Resolved by allowing unrelated histories and favoring local changes.
    
    - Conflict in `.gitignore` resolved by keeping local (`--ours`).
        
6. Installed GitHub CLI (`gh`), authenticated, and set the default branch to `Pizza2`:
    
    ```bash
    sudo apt install gh
    gh auth login
    gh repo edit Vtheonly/Pizza_Stores_Tamplates --default-branch Pizza2
    ```
    
7. Final state: `Pizza2` exists on remote and is set as the default. Push confirmation showed everything up-to-date.
    

---

## Root Causes And Fixes

### 1) HTTPS Push Failing

- Reason: GitHub disabled password-based HTTPS pushes. You must use a Personal Access Token or SSH.
    
- Fix chosen: use SSH remote. This leverages your existing SSH key and avoids token friction.
    

### 2) Divergent Histories On `main`

- Reason: The remote `main` had an independent history (e.g., a README created on GitHub UI) while local history came from a fresh init.
    
- Symptom: `git pull` or `git merge origin/main` complained about unrelated histories.
    
- Fix: Explicitly allow unrelated histories, then resolve conflicts. You chose to keep your local content as canonical.
    

### 3) “Make `Pizza2` The One And Only Head”

This had two interpretations:

- A) Keep `main` as the canonical branch, but overwrite its content/history with `Pizza2` (force-update).
    
- B) Keep `Pizza2` as the canonical branch and make it the default branch (no need to touch `main` immediately).
    

You executed B: set `Pizza2` as the default branch on GitHub. If you also want a truly single branch (no `main` at all), see the “Single-Timeline Options” section.

---

## Recommended Final Shapes (Pick One)

### Option A — `Pizza2` remains default, delete `main` (single branch repo)

Pros: clean, no confusion.  
Cons: any integrations expecting `main` will need updating.

Commands:

```bash
# Ensure Pizza2 is fully up to date
git checkout Pizza2
git pull --ff-only

# Delete local main if present
git branch -D main || true

# Delete remote main
git push origin --delete main
```

Verification:

```bash
git ls-remote --heads origin
# Should show only refs/heads/Pizza2
```

### Option B — Make `main` the single branch by force-updating it to `Pizza2`

Pros: aligns with common defaults that expect `main`.  
Cons: force push rewrites remote history of `main` (destructive).

Commands:

```bash
# From Pizza2, force-update remote main to match Pizza2 exactly
git checkout Pizza2
git push origin +Pizza2:main

# Optionally set default back to main
gh repo edit Vtheonly/Pizza_Stores_Tamplates --default-branch main

# Optionally delete Pizza2 if you truly want a single branch
git push origin --delete Pizza2
```

Verification:

```bash
git fetch origin
git ls-remote --heads origin
git rev-parse origin/main
git rev-parse origin/Pizza2  # If you kept Pizza2
```

---

## Safe, Repeatable Procedure (What I’d Do Next Time)

1. Initialize with SSH from the start
    

```bash
git init
git remote add origin git@github.com:USER/REPO.git
```

2. First commit and push a canonical branch (say `main` or `Pizza2`)
    

```bash
git add .
git commit -m "Initial commit"
git push -u origin Pizza2
```

3. Set the default branch early
    

```bash
gh auth login   # once per machine
gh repo edit USER/REPO --default-branch Pizza2
```

4. Avoid unrelated histories
    

- Don’t create files directly on GitHub before your first push. If you did, either:
    
    - Pull first: `git pull --allow-unrelated-histories`, then resolve.
        
    - Or decide which side is canonical and force-update the other.
        

5. If you really want a single branch
    

- Either delete the non-canonical branch (`git push origin --delete main`)
    
- Or force-update it to match your canonical branch (`git push origin +Pizza2:main`).
    

---

## Commands Used (Curated And Correct)

### Switch remote to SSH

```bash
git remote remove origin  # if an origin existed
git remote add origin git@github.com:Vtheonly/Pizza_Stores_Tamplates.git
```

### Push Pizza2 as canonical

```bash
git checkout -B Pizza2
git push -u origin Pizza2
```

### Set default branch (GitHub CLI)

```bash
sudo apt install gh        # once
gh auth login              # once per machine
gh repo edit Vtheonly/Pizza_Stores_Tamplates --default-branch Pizza2
```

### Resolve unrelated histories by keeping your local content

```bash
git checkout main
git fetch origin
git merge origin/main --allow-unrelated-histories
# If conflicts, keep ours (local):
git checkout --ours .gitignore
git add .gitignore
git commit -m "Merge unrelated histories; keep local as canonical"
git push origin main
```

### Force-update remote main to match Pizza2 (destructive)

```bash
git checkout Pizza2
git push origin +Pizza2:main
```

### Delete a remote branch

```bash
git push origin --delete main
```

---

## Why SSH Over HTTPS

- GitHub disabled password-based HTTPS pushes. Access tokens work but must be managed and scoped carefully.
    
- SSH keys are long-lived, easy to rotate, and integrate well with CLI tooling and CI.
    
- Your session shows SSH worked immediately after `gh auth login`.
    

---

## Verification Checklist

- Default branch is `Pizza2`:
    
    ```bash
    gh repo view Vtheonly/Pizza_Stores_Tamplates --json defaultBranchRef -q '.defaultBranchRef.name'
    ```
    
- Remote branches:
    
    ```bash
    git ls-remote --heads origin
    ```
    
- Local-to-remote tracking:
    
    ```bash
    git status
    git branch -vv
    ```
    
- If forcing `main` to match `Pizza2`:
    
    ```bash
    git rev-parse origin/main
    git rev-parse origin/Pizza2
    # Compare hashes; they should be identical.
    ```
    

---

## My Take (Opinionated Guidance)

- If you don’t have external dependencies expecting `main`, keep `Pizza2` as the only branch and delete `main`. It’s the cleanest representation of your intention: one canonical line of development.
    
- If some tooling expects `main`, force-update `main` to match `Pizza2` and make `main` the default, then delete `Pizza2`. Avoid keeping two branches that are supposed to be the same—it invites drift.
    
- Avoid the “allow unrelated histories” path by pushing first from your local repo before creating anything in the GitHub UI.
    

---

## One-Page TL;DR

- Use SSH, not HTTPS passwords.
    
- Push `Pizza2`, set it as default:
    
    ```bash
    git checkout -B Pizza2
    git push -u origin Pizza2
    gh repo edit Vtheonly/Pizza_Stores_Tamplates --default-branch Pizza2
    ```
    
- To make a single branch:
    
    - Delete `main`:
        
        ```bash
        git push origin --delete main
        ```
        
    - Or overwrite `main` with `Pizza2`:
        
        ```bash
        git push origin +Pizza2:main
        gh repo edit Vtheonly/Pizza_Stores_Tamplates --default-branch main
        git push origin --delete Pizza2
        ```
        

That gives you the “one and only head” you wanted, with a clean history and no surprises.