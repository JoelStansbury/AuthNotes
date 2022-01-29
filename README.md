# AuthNotes
Instructions for setting up CLI authentication with github
/

1. Create SSH key `ssh-keygen`
2. Register SSH key here https://github.com/settings/keys
   * Click `New SSH key`
   * Paste the entire contents of your ssh_rsa.pub. In linux the default location is `/home/USERNAME/.ssh/id_rsa.pub` (system username not git username)
3. `git remote set-url origin git@github.com:USERNAME/REPOSITORY.git` (github username)
   * If you run `git config -l` to list out all of the config parameters you'll see something like this
    `remote.origin.url=https://github.com/USERNAME/REPOSITORY.git`
    After running the above command this param will change to the `git@github:` format which is needed for ssh authentication.
   * This may (or may not) need to be replicated for each repo (i've not tested this yet)

(1/28/2021)
```bash
remote: Support for password authentication was removed on August 13, 2021. Please use a personal access token instead.
remote: Please see https://github.blog/2020-12-15-token-authentication-requirements-for-git-operations/ for more information.
fatal: Authentication failed for 'https://github.com/USERNAME/REPOSITORY.git/'
```
That link is useless. If you follow the instructions you'll find that you can create a PAT and it works when you paste it into the password field when pushing up to remote, but it only works once (git cli doesn't remember the token, and github will not show you again so you just need to regenerate a new key everytime you push)

"you must begin using a personal access token over HTTPS (recommended) or SSH key by August 13, 2021, to avoid disruption"

I interpreted this as _if you do not make an SSH key by August 13 you will no longer have that option_. I'm still not convinced that this was not the intended message, but it's not true. You can still use ssh, you just need to take the additional step of correcting the remote origin address. Maybe this isn't new, but I don't remember needing this step before
