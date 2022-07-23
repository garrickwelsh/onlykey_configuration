# Onlykey Duo

This is the configuration I have used for my onlykey duo. It includes a script to load encryption keys for gpg onto my onlykey to support multiple gpg keys and gpg subkeys.
__NOTE__: This support requires changes to libagent, I have a PR for it so hopefully the changes are accepted.

## Install for Arch Linux
Use your AUR helper to install the OnlyKey app.
```paru -S onlykey```
Install the command line app. Please see [instructions](https://docs.crp.to/command-line.html#arch-linux-install-with-dependencies).
```pacman -S git python python-setuptools libusb python-pip libfido2```
```pip install pgpy onlykey```
Note to upgrade use: ```pip install --upgrade onlykey```

## Steps to get up and running
The OnlyKey Duo had issues communicating over USB with v3.0.0 version for the firmare. Upgrade to v3.0.1 fixed this issue.
The key could communicate via a hub so this was used.

## Set sensible defaults
Place key into configuration mode. Hold button 1 for 10 seconds.
Run the following:
* ```onlykey-cli storedkeymode 1```
* ```onlykey-cli derivedkeymode 1```

To place back into regular mode again unplug then plug back in.

## Configuring ssh
```ssh-keygen -t ed25519-sk -O resident -f ~/.ssh/id_mykey_sk```
This will generate an ssh key.
Run ssh agent. This is what to use in $HOME/.fish/config.fish
```fish
if test -z (pgrep ssh-agent)
  eval (ssh-agent -c)
  set -Ux SSH_AUTH_SOCK $SSH_AUTH_SOCK
  set -Ux SSH_AGENT_PID $SSH_AGENT_PID
  set -Ux SSH_AUTH_SOCK $SSH_AUTH_SOCK
end
```

Add the key to the agent to it can be used.
```ssh-add -K```
List your public to add it to a website
```ssh-add -L```

Now log into ssh.

## Configuring GPG

Get your gpg key. Either get it or generate a new one.

### Generating a key
[Import or Generate a key](https://docs.crp.to/importpgp.html)

```gpg --expert --full-gen-key```
Pick the following options:
* (9) ECC and ECC
* (1) Curve 25519
* Choose key validity
* Name
* Email
```gpg --expert --edit-key <uid>```
Add additional keys.
```gpg --output private.asc --armor --export-secret-key <email address>```
```gpg --output public.asc --armor --export <email address>```
### Importing a key into Only Key
Run onlykey-cli-gpg-add-keys.py [https://github.com/garrickwelsh/onlykey_configuration/blob/master/onlykey-cli-gpg-add-keys.py].
This has been modified from - [https://raw.githubusercontent.com/trustcrypto/python-onlykey/master/tests/PGPparseprivate.py]
This will not find slots and add the keys to them (note this is still more of a proof of concept and only supports RSA and ECC Curve25519).

# Import manually

Run the scripts to manually extract your private key and add them to your only key.
__note__: This requires they keygrip patch to libagent.

Set key to configuration mode (hold button 1 for 10 seconds the key will flash red).
```onlykey-cli setkey 101 x d <32 bytes second key>```
```onlykey-cli setkey 102 x s <32 bytes first key>```
```onlykey-cli setkey 101 label <keygrip second key>```
```onlykey-cli setkey 102 label <keygrip first key>```
```onlykey-cli setkey 103 x d <32 bytes second key>```
```onlykey-cli setkey 104 x s <32 bytes first key>```
```onlykey-cli setkey 103 label <keygrip second key>```
```onlykey-cli setkey 104 label <keygrip first key>```

Next create an onlykey agent to run. The updated libagent will search for keys before applying default keys.
Please see [https://github.com/trustcrypto/OnlyKey-App/issues/166#issuecomment-890157049] for an example.
```onlykey-gpg init "FirstName LastName <emailaddress>" -sk 102 -dk 101 -i public.asc```

### Setup systemd
[Start agent as systemd](https://docs.crp.to/onlykey-agent.html#how-do-i-start-the-agent-as-a-systemd-unit)
Follow the instructions above or look at [my configuration](../dotconfig/systemd/user).
__NOTE__: I had issues signing with running as a systemd service.

### Switch between keys using systemd
Please refer to [shell scripts](../bin)
```bash
#!/bin/bash

systemctl --user stop onlykey-gpg-agent.service
pushd $HOME/.gnupg
rm onlykey
ln -s gmail onlykey
popd
systemctl --user start onlykey-gpg-agent.service
```

## Configuring FIDO2 websites
Just press the button when required.

