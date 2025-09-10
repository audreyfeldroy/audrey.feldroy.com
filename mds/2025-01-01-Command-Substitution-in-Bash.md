# Command Substitution in Bash

## Simple Command Substitution

Use `$()` not backticks


```bash
%%bash
echo "Current directory is $(pwd)"
```

It also works with backticks, but it's not the best way:


```bash
%%bash
echo "Current directory is `pwd`"
```

(Because when you nest these, you have to escape the backticks)

## Example: Moving Untracked Files to `_drafts` Folder


```bash
%%bash
git ls-files --others --exclude-standard
```


```bash
%%bash
mv $(git ls-files --others --exclude-standard) ./_drafts
```

It works for me and I'd be happy stopping here, but in the real world where files have spaces, it'll break.

## Fancy Command Substitution With `xargs`

`xargs` lets you map a list to any command. Here I would use it like:


```bash
%%bash
git ls-files --others --exclude-standard | xargs -I {} mv {} ./_drafts/
```

The untracked files list is piped to `xargs`, which lets us run a command for each line in the list. Then `mv` is run for each file in the list. 

`-I {}` is needed to put the filename somewhere other than the end of the `mv` command. Here, `-I` enables string replacement, and `{}` is the placeholder string that gets replaced.
