# My Self-Analysis of How to Get Back to Posting Every Day

I fell off the wagon with creating a new notebook every day, but it's not too late to get back on. Today's post is for me to figure out how to make this more sustainable. 

## Setup


```python
from datetime import datetime
from fastcore.utils import *
from pathlib import Path
```

## Understand the problems

* I take too long to write each daily post. 
* Often, my objective that I start out with turns out to be over-ambitious and takes me too long to implement. 
* I've gotten around that by leaving my higher objective notebook hanging and creating a new notebook branching off, exploring a sub-problem. 
* Is it just that I need to do that more? Well, let me think. 
* Sometimes, when I'm branching off subproblems, it gets overwhelming after the fifth branch-off notebook. Even after the third, it feels like a bit much. And I feel like I'm getting lost in all the branches. 
* That makes it hard to just get the smallest subproblem out as a daily post within a short amount of time. 
* Related, I also haven't been timeboxing because I've been wanting to let my ideas go free at the end of the day. Well, sort of. I've been starting my blog posts late at night after a long day of coding when I'm tired and perhaps my mind is most divergent at that time. 
* This morning I'm creating this post. First thing I started it at 9:00 a.m., and now it's 9:30 a.m. Let's see if I can get it out by 10:00 a.m.

## Ask AI to clarify the problems

I asked Claude 3.5 Sonnet: 

> Clarify what the key problems are here. 

From the text, there are 3 core problems making daily posting unsustainable:

1. Time management:
   - Posts take too long to complete
   - Starting late at night when tired
   - Not timeboxing the work

2. Scope creep:
   - Initial objectives are too ambitious
   - Projects expand beyond original intent

3. Organization:
   - Too many branching subproblem notebooks
   - Getting lost in the branches
   - Difficulty focusing on smallest complete unit

The root cause appears to be trying to tackle complex topics without sufficient structure and boundaries, during suboptimal times of day.

## Devise a Plan

Continuing to get Claude's help:

> What can I do today to get this blog post out in the next 25 minutes? 

Given it's already 9:30am and you want to finish by 10am, here's what to do in the next 25 minutes:

1. Set a timer for 25 minutes right now
2. Write a quick bullet-point list of 3 concrete actions you'll take tomorrow to address the problems identified (e.g. "Start writing at 9am", "Set 45-min timer", "Pick one small topic")
3. Add a conclusion paragraph summarizing your key realization: that writing at night without timeboxing leads to scope creep
4. Proofread once, publish

Don't add any new sections or analysis - the current content identifying the problems is sufficient for a useful blog post. The goal is to ship it, not perfect it.

## Timebox


```python
datetime.now()
```




    datetime.datetime(2025, 2, 12, 9, 33, 53, 702594)



## Pick one small topic. 

Let's analyze my incomplete drafts in the minutes that remain for today, perhaps. Maybe also analyze my story of what happened and try to find the root cause 

### Wait, is this doable?

So it's a bit tricky to do. I have a catch-all repo that is for random notebooks. Some are blog posts, some are meeting notes, some are private notes, some are notes or random experiments that I create pair programming or on my own to try to figure out things at work. These are definitely not all intended to be blog posts. 

But it's not clear or definitive which ones are blog posts and which ones aren't. Even say a snippet of something interesting from something I do at work could end up turning out as a blog post if it involves only open source code, for example 

### Analyze something to start, anything


```python
nbs = L(Path().glob("*.ipynb")).sorted(reverse=True)
nbs
```




    (#144) [Path('Untitled9.ipynb'),Path('Untitled8.ipynb'),Path('Untitled7.ipynb'),Path('Untitled6.ipynb'),Path('Untitled5.ipynb'),Path('Untitled4.ipynb'),Path('Untitled3.ipynb'),Path('Untitled29.ipynb'),Path('Untitled28.ipynb'),Path('Untitled27.ipynb'),Path('Untitled26.ipynb'),Path('Untitled25.ipynb'),Path('Untitled24.ipynb'),Path('Untitled23.ipynb'),Path('Untitled22.ipynb'),Path('Untitled21.ipynb'),Path('Untitled20.ipynb'),Path('Untitled2.ipynb'),Path('Untitled19.ipynb'),Path('Untitled18.ipynb')...]



Okay, wow 144 notebooks in there. The latest ones are all untitled. I guess I was hoping to lean on my notebook titler pretty heavily. That's where I had left off last when I was getting ready to post something more deliberately. I was taking my old "Untitled" notebook titling experiment and turning it into a more polished  notebook titler tool. 

### Why I've needed a notebook auto-titler

My hands have been getting tired lately, so the typing involved with copying the notebook title to Jupyter Notebooks rename dialog then adding dashes and prepending with the date was getting to be a bit too much typing. I've been using voice dictation for everything lately, and that's one of those things that you can't voice dictate. 

I had been hoping some automation would help up there, and I had been working on the automation. 

### Root Cause Identified! When automation goes wrong

I realize now that I fell off the wagon when I had been almost done creating the ultimate notebook auto-titler, and then I accidentally ran it on itself and accidentally destroyed all my work for the day. You can imagine how frustrating that felt. 

### Where are the latest versions of my auto-titler? 

[Auto-Renaming My Untitled.ipynb Files With Gemini 1.5 Flash](https://audrey.feldroy.com/nbs/2025-02-01-Auto-Renaming-My-Untitled-ipynb-Files-With-Gemini) is the latest public version.

As for the private versions, I have a notebook that I retrieved from a Jupyter notebook checkpoint that is only slightly more advanced than that notebook above.

## Plan for Tomorrow

* Start writing at 9 a.m. sharp. (Or the moment I get my laptop open after dropping off my daughter at school.)
* Time box myself: Import datetime at the start and set a target end time for 10am. 
* Identify a subproblem in that Jupyter Notebook checkpoint notebook and make that my blog topic. 



```python
datetime.now()
```




    datetime.datetime(2025, 2, 12, 10, 1, 27, 65936)


