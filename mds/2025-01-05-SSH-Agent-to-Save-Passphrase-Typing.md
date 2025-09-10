# Using SSH Agent to Save Passphrase Typing

In my terminal (Ghostty) when I run shell scripts that update multiple repos, I get asked my SSH key passphrase over and over. It gets annoying with 20+ repos.

To get around this, I use OpenSSH's authentication agent, `ssh-agent`.

## How It Works

`ssh-agent` holds my decrypted SSH key securely in memory for the current terminal session. (And the memory is not swapped to disk.)

Then, when an SSH client (e.g. git) needs it to authenticate, it asks my SSH agent instead of prompting me.

## Start SSH Agent

This is how I start an SSH agent on macOS:


```bash
%%bash
eval "$(ssh-agent -s)"
```

Note: macOS and many Linux desktop distros auto-start one. I don't have one running in my Ghostty terminal session, though.

### Exploring this further

Let's see what `ssh-agent -s` by itself actually outputs:


```bash
%%bash
ssh-agent -s
```

Here, `ssh-agent` starts the SSH agent. `-s` is to get output in Bash syntax.

The `$(...)` captures its output.

`eval` then executes the captured output, which:
   - Sets `SSH_AUTH_SOCK`: The path to the Unix socket the agent uses for communication
   - Sets `SSH_AGENT_PID`: The process ID of the agent
   - Exports both so SSH clients can find the agent
   - Prints confirmation that the agent is running

## Ensure Agent Has Your Key

To list the keys my terminal session's SSH agent has, I run:


```bash
%%bash
ssh-add -l
```

If my SSH key isn't there, I add it:


```bash
%%bash
ssh-add
```

`ssh-add` without arguments defaults to `~/.ssh/id_rsa`, `id_ecdsa`, `id_ed25519`, and `id_dsa`. (Of those, be sure to use Ed25519 or RSA, not deprecated DSA keys.)

## Security and Other Notes

`ssh-agent` is secure because it:
- Keeps keys encrypted on disk
- Only decrypts keys to memory
- Restricts access via Unix socket permissions to your user
- Clears keys when stopped/rebooted 

While slightly less secure than typing passphrases each time, it's far safer than removing passphrases or storing credentials in files.

SSH agent forwarding (`ssh -A`) lets you use your local keys from servers you SSH into. That comes with its own risks, of course.

To explore in the future: macOS has a built in agent that's different from `ssh-agent`, with keychain integration.
