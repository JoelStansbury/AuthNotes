# AuthNotes
Instructions for setting up CLI authentication with github
/

#### Info
These are instructions for configuring github to trust a single computer to make operations on your personal repositories without the need to enter your credentials (username and private-access-token) manually.
> Note: The process authenticates a single machine, but you can repeat it for multiple machines.

The process involves creating an _ssh-key pair_ which your git command line interface (CLI) uses to authenticate an operation (e.g. `git push`). GitHub will encrypt some message with your public ssh-key which can only be decrypted by the private key stored on your machine (read more about asymmetric encryption [here](https://www.digitalocean.com/community/tutorials/understanding-the-ssh-encryption-and-connection-process)). Your machine will decrypt the message and send it back to GitHub to confirm your identity.

## Instructions
1. Create SSH key `ssh-keygen` (this command is the same on windows osx and linux) <br> ![image](https://user-images.githubusercontent.com/48299585/151645620-608fd9e6-b4c0-41ed-979c-4fc0d0fee812.png)

2. Register SSH key here https://github.com/settings/keys
   * Click `New SSH key`
   * Paste the entire contents of your (public key) `ssh_rsa.pub` into the key field (the file location was printed out in the previous step)

> TODO: look into adding a `config` file to see what that is used for
### Still not working
* It may be due to the way your local repo is configured.
   * `git config remote.origin.url` should show a url like this `git@github.com:USERNAME/REPOSITORY.git`
   * If you see a url starting with `https` you need to fix it or ssh will not work. Use this command to fix it<br>
    `git remote set-url origin git@github.com:USERNAME/REPOSITORY.git`
   * To avoid this in the future, when cloning a repository make sure to choose the `ssh` url ![image](https://user-images.githubusercontent.com/48299585/151645529-262c1ca5-4ef4-4f99-a64f-e2d7fc1e4c81.png)

### Updates
(1/28/2022)
```bash
remote: Support for password authentication was removed on August 13, 2021. Please use a personal access token instead.
remote: Please see https://github.blog/2020-12-15-token-authentication-requirements-for-git-operations/ for more information.
fatal: Authentication failed for 'https://github.com/USERNAME/REPOSITORY.git/'
```
That link is useless. If you follow the instructions you'll find that you can create a PAT and it works when you paste it into the password field when pushing up to remote, but it only works once (git cli doesn't remember the token, and github will not show you again so you just need to regenerate a new key everytime you push)

"you must begin using a personal access token over HTTPS (recommended) or SSH key by August 13, 2021, to avoid disruption"

I interpreted this as _if you do not make an SSH key by August 13 you will no longer have that option_. I'm still not convinced that this was not the intended message, but either way, it's not true. You can still use ssh.
