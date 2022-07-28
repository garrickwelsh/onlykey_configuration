# Configuring ssh
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
