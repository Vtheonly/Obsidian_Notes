Here’s how to set up SSH keys for GitHub on Ubuntu, broken down into commands:

### 1. **Generate SSH Key:**
   Use the `ssh-keygen` command to create an SSH key pair. Replace `your_email@example.com` with the email associated with your GitHub account.

   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```

   When prompted, you can either press Enter to accept the default file location (`~/.ssh/id_rsa`) or specify a different file name.

   ```bash
   Enter file in which to save the key (/home/your_user/.ssh/id_rsa): 
   ```

   You’ll also have the option to enter a passphrase for the key. Press Enter to leave it empty if you don’t want to use one.

   ```bash
   Enter passphrase (empty for no passphrase): 
   ```

### 2. **Check SSH Key Files:**
   Once generated, you’ll have two files: your private key (`id_rsa`) and your public key (`id_rsa.pub`). To list the SSH key files:

   ```bash
   ls ~/.ssh/
   ```

   You should see something like:

   ```bash
   id_rsa  id_rsa.pub
   ```

### 3. **Copy the Public Key to GitHub:**
   Copy the content of your public key (`id_rsa.pub`):

   ```bash
   cat ~/.ssh/id_rsa.pub
   ```

   - Select and copy the entire output of this command.
   - Go to GitHub and navigate to **Settings** > **SSH and GPG keys**, then click **New SSH key**.
   - Paste the copied public key and give it a title.
   - Click **Add SSH key** and confirm your GitHub password if prompted.

### 4. **Configure SSH for Git:**
   Now that the public key is uploaded to GitHub, configure your SSH to use it for Git commands.

   Start the SSH agent:

   ```bash
   eval "$(ssh-agent -s)"
   ```

   Add your private SSH key to the agent:

   ```bash
   ssh-add ~/.ssh/id_rsa
   ```

   Optionally, create or edit the SSH config file to automatically use the key with GitHub:

   ```bash
   nano ~/.ssh/config
   ```

   Add the following content:

   ```bash
   Host *
       AddKeysToAgent yes
       IdentityFile ~/.ssh/id_rsa
   ```

   Save the file and exit the editor (`Ctrl + X`, then `Y` to confirm).

### 5. **Test SSH Connection to GitHub:**
   Verify the SSH connection by running:

   ```bash
   ssh -T git@github.com
   ```

   If everything is set up correctly, you should see a message like:

```bash
   Hi your_username! You've successfully authenticated, but GitHub does not provide shell access.

```

