# NBClassic Keyboard Shortcuts: Command and Dual-Mode

I'm taking inventory of all the Command Mode and dual-mode nbclassic keyboard shortcuts on macOS, with my random musings about each. This is part of my deliberate practice to master all of the useful ones, and will serve as a reference for myself later.

## From Command Mode

Press `Esc` to get out of editing a cell (Edit Mode), then:

`p`: Open the Command Palette

This opens the little dialog with commands. Then you can press up or down arrows to select commands.

* There's a scroll bug so when you go down past the bottom edge, the whole window doesn't scroll. When I go past the bottom edge, I can only see command names and not their shortcuts. It basically means the commands not shown by default are hardly usable unless I already know them. The ones shown by default are also not that useful: I rarely want to press number keys to convert a cell to a heading when Markdown `#` is so easy.
* It would be nice if this dialog took up the whole screen. So much wasted space where I wish I could just see more commands. Beyond taking up the whole screen, it would be nice if it were multi-column so you could see tons of commands all at once. 
* Oh! I can rename a notebook from here without using my mouse! That's game-changing for me.

Change cell type:

* `M`: Markdown. I use it often.
* `Y`: Code. I use it often, but I usually accidentally type C instead of Y. Y on the other hand feels like it should yank, which is sort of what C does.
* `R`: Raw. I've never used this. Let's try it now. Oh, that's a good one. 
    * Probably useful for frontmatter in blog apps that require it. This may actually be one of the key pieces that ends up converting me over to the frontmatter side.
    * Occasionally I have other code that I want to stick into a notebook without it being interpreted, and I use fenced no-syntax code blocks within Markdown to do it. Advent of Code puzzle inputs come to mind, stuff like:
aa
bb
  cc
  d e
    e
`f`: Find and replace. I've never used this. I always use Cmd F and use Chrome or Firefox's search. I'm trying it. That's cool that it can take regular expressions! I tried `\w+` and that was fun. To get those to work, I had to toggle the button off and then on again.

`k` or `Up arrow`: Select previous cell

`j` or `Down arrow`: Select next cell

* I always use the arrows, never `k` and `j`, but I'll try them since they're nice Vim workalikes.

`Shift` `k` or `Shift` `Up arrow`: Add previous cell to selection

`Shift` `j` or `Shift` `Down arrow`: Add next cell to selection

* I use `Shift` with up and down arrows sometimes. I didn't know I could use those with `k` and `j`. I'll try to use those.
* "Extend selected cells" in the docs didn't make sense to me until I tried it.

`Cmd` `a`: Select all cells. I never use this and it seems not very useful. Could I be wrong? Copy-pasting cells between notebook browser tabs doesn't work for me, and it may be related to that use case. 

`a` / `b`: Insert cell above/below. I use this often.

Copy-pasting:

* `x` / `c` / `v`: Cut/copy/paste selected cells. I use this often.
* `Shift` `v`: Paste above current cell. I never use this but it feels incredibly useful.
* `Cmd` `v`: Dialog for paste from system clipboard. Sometimes I accidentally press this. I never use this deliberately, because pasting from my system clipboard into Edit Mode works fine. Would I want to paste in Command Mode? I'll look out for the opportunity. Oh wait, this looks like it would be useful in conjunction with `Cmd` `a` to bring a whole notebook over into a new one.

`d` then `d` again: Delete cell. I mostly use `x` instead of this, out of muscle memory not intentionality.

`z`: Undo cell deletion. This usually doesn't work for me because I press `x`. I can press `Shift` `v` when that happens, I now know.

`Shift` `m`: Merge cells. I occasionally do this by accident. 

* Every time that happens, I think, "Oh, that's useful, I should do that on purpose sometimes." Then I try to undo with `z` and it doesn't work, because `z` only undoes `dd`. Then I re-split the cells with `Ctrl` `Shift` `-`.
* But I never actually do it on purpose. My need to merge cells these days is rare enough that I don't remember this. I suppose with imports maybe it'll be good.
* That's cool that if you have only 1 cell selected, it'll merge with the next cell.

`s` or `Ctrl` `s`: Save and checkpoint. I use `Ctrl` `s` often. I didn't realize `s` does the same exact thing. That saves my pinky a bit.

`l`: Toggle line numbers. I rarely use this other than when [Danny](https://daniel.feldroy.com) asks me to turn the line numbers on.

`o`: Toggle output of selected cells. I never use this, but I'll try it now on the time cell. Okay, I could see that being useful if a cell's output is huge, I can't truncate it, and the output iframe doesn't turn on, which happens occasionally for me.

`Shift` `o`: Toggle output scrolling of selected cells. I never use this. Maybe it'll solve my pain point of not being able to see the full version via keyboard of an iframe-truncated output. Oh, wow, I'll use this all the time now that I know about it. Wow, this would have saved me a lot of trackpad scrolling pain yesterday.

Kernel problem sequences:

* `i` then `i`: Interrupt the kernel. I never use this but plan to. But AI tells me it's essential to stop deep learning training runs early, or to stop overfitting as soon as I see it happening. Yeah, I'll try that then.
* `0` then `0`: Restart the kernel. I rarely use this but should do it more.

Commands I don't understand, or that are broken for me, possibly due to my customizations or nbextensions:

* `Esc` or `q` from Command Mode to "Close the pager". Does that mean to close Command Palette? If I have Command Palette open, that's what it does. If I have regular Command Mode open, it doesn't seem to do anything.
* `h`: The [docs](https://jupyter-tutorial.readthedocs.io/en/24.1.0/notebook/shortcuts.html) say it'll "show keyboard shortcuts", but nothing shows for me.

## From Both Modes

Running cells:

* `Shift` `Enter`: Run the current cell and create a new one below, or select the existing one below. I use this often. "Run cell, select below" in the docs isn't quite right.
* `Cmd` `Enter` or `Ctrl` `Enter`: Run the current cell, keep it selected, and switch to Command Mode if not already there. I never use this. 
    * I sort of like it better than my current habit of `Esc` then `Shift` `Enter`, so I'll start using it. 
    * Oh, that's also cool that you can multi-select cells via keyboard and run them all. After you do that, the last cell gets selected.


## Cells for Testing


```python
print(datetime.now().strftime('%I:%M:%S %p'))
```

Here I print the time in a test cell. That way I can see if the cell is actually run.


```python
[i for i in range(1000)]
```

Here's a cell with long output, to test `Shift` `o`.
