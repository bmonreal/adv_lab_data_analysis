# All About git (OK, a little about git)
Git is basically the modern standard system for *version control*.  What is easiest to explain about version control is what it isn't: it isn't "I wrote some code and saved it as mycode.C.  I emailed that to my colleague who edited it and saved mycode-Edited.C.  I found a bug in that so I emailed her back mycode-Edited-Fixed.C.  But she had been fixing another bug in the meantime and had to find my edits to merge mycode-Edited.C (her version) with mycode-Edited-Fixed.C (my version)."  Nor is it like a Google Doc: "Here is the only copy of the document.  I edited it, then you edited it, then I edited it.  Shoot, three edits ago I accidentally deleted the intro, can you roll it back?  Wait, don't roll it back, we'd lose the most recent edit." 

Instead, Git puts your project under version control.  As you edit your documents, it keeps a record of what changes were made in which order.  At any time, it can spit back a copy of the document with any requested chain of changes---even if that's not the order you made the changes in.  "Bob took mycode.C and made Edit-A and Edit-B to the first subroutine. At the same time Alice had mycode.C and was making Edit-C to the second subroutine.   Git, please show a current master copy as if Edits A and C had been made in that order."

The idea is that git allows one or many people to edit a common project, and allow a single working version---or indeed multiple working versions---of the project to "exist".  I will try to show in a few examples why you want to do that.

## Getting started

Open up a terminal (note: there are ways to do this within, e.g., Emacs, or XCode, but I only know the command line version myself.) and start typing.   Let's pretend we are going to simulate a planet's orbit using Newton's laws.  I will type this stuff in and make obvious coding errors for the sake of showing some of the versioning issues.

Create a directory for your project. Change to that directory and tell `git` to get ready to maintain a project in this directory.  
```
$ mkdir orbitsim
$ cd orbitsim
$ git init
```

Make a new file using your preferred text editor and save it.
``` 
$ emacs sim.py
```

Just to make things clearer later, I will occasionally cat the file so you can see its contents.

```
$ cat sim.py 
import numpy as np
from matplotlib import pyplot as plt
def force(m1,m2,r):
    return Gnewton*m1*m2/r*2

```

We have not told Git what filenames we care about.  From now on, "newton.py" will no longer be a regular file in which you store information.  From now on "newton.py" will be a sort of temporary-view-of-the-file, generated from a master set of diffs stored elsewhere.  

```
$ git add sim.py
```

Finally, let's tell Git that now is a good time to register some of my edits to newton.py and add those edits to the master record of the project.  This is called a "commit".  Every time you commit, you should make a human-readable note or message saying what has happened.

```
$ git commit -m "initial commit; one force function"
[master (root-commit) 9c2119d] initial commit; one force function
 1 file changed, 4 insertions(+)
 create mode 100644 sim.py
```

## Committing code while you debug

Maybe next you realize you forgot to define GNewton.  Let's fix that in our text editor.

```
$ cat sim.py
import numpy as np
from matplotlib import pyplot as plt
Gnewton= 6.67e-11 # SI units
def force(m1,m2,r):
    return Gnewton*m1*m2/r*2
```

We have to tell `git` which files we care about committing---you're allowed to edit multiple files but limit your commit to one or two.  This is called "staging".  Roughly speaking, as a beginner, you will usually stage everything you've edited. 
```
$ git add sim.py
$ git commit -m "m fix, add Gnewton"
```

an alternative syntax for that is `commit -a` which stages everything.  

```
$ git commit -a -m "m fix, add Gnewton"
[master 0df87d1] m fix, add Gnewton
 1 file changed, 1 insertion(+)
```

Maybe at this point, your advisor has asked you to prepare some plots to show at group meeting. You keep working and commit code with a simple plot defined.

```

$ cat sim.py 
import numpy as np
from matplotlib import pyplot as plt
Gnewton= 6.67e-11 # SI units
def force(m1,m2,r):
    return Gnewton*m1*m2/r*2

plt.plot([force(1,1,r) for r in range(1)])

$ git commit -a -m "add first plot"
[master 35a6dd9] add first plot
 1 file changed, 2 insertions(+)
```

And finally, of course, you may keep working.  The first attempt to code up a force law was maybe too inflexible.  You want vector and scalar functions, perhaps.

```
$ cat sim.py 
import numpy as np
from matplotlib import pyplot as plt
Gnewton= 6.67e-11 # SI units
def scalar_force(m1,m2,r):
    return Gnewton*m1*m2/r*2
def vector_force(m1,m2,r1,r2):
    vector_sep = r1-r2
    scalar_sep = np.norm(r1-r2) # FIXME need to look up this syntax
    return vector_sep/scalar_sep(force(m1,m2,scalar_sep))
plt.plot([force(1,1,r) for r in range(1)])

$ git commit -a -m "refactor into scalar and vector components"
[master de54868] refactor into scalar and vector components
 1 file changed, 7 insertions(+), 2 deletions(-)
```
 
That is enough simple coding that we have a very simple Git history.  Let's see what has happened.

```
$ git log
commit de548687769e81ab5381c6af1280bca97063de3e (HEAD -> master)
Author: Benjamin Monreal <benmonreal@gmail.com>
Date:   Thu Mar 12 00:36:04 2020 -0400

    refactor into scalar and vector components

commit 35a6dd901e90dfc479405b6c5f1d0841dec60554
Author: Benjamin Monreal <benmonreal@gmail.com>
Date:   Thu Mar 12 00:34:05 2020 -0400

    add first plot

commit 0df87d148e80d0ca03193153d88868c6bf231706
Author: Benjamin Monreal <benmonreal@gmail.com>
Date:   Thu Mar 12 00:33:07 2020 -0400

    m fix, add Gnewton

commit 9c2119deafc931c9f1294b5b943ad2f1c3aac10e
Author: Benjamin Monreal <benmonreal@gmail.com>
Date:   Thu Mar 12 00:32:29 2020 -0400

    initial commit; one force function
```

Those four commits have been remembered, and the particular chain "these three edits in order" would result in a file which, as it so happens, is the one you already have a copy of.  BUT your copy is just a working copy.  You can delete it, and git knows how to give it back to you.  In this sense *Git is a useful incremental backup system*.  Asking Git for a clean copy of the current `HEAD` is called 'checking out'.  

```
echo 'some nonsense I am going to accidentally overwrite my file with' > sim.py 
```

In a normal filesystem, that'd be bad right?  You just overwrote your code with nonsense.  But you can ask Git to check out a clean copy.  It'll be recreated from the commit list.

```
git checkout master sim.py
```

## Reverting and branching
Here is an example of where Git's branching and merging features are useful.  "git checkout" lets you get any copy---any state you've ever had.  What happens is that there's a pointer, the "head", which tells git which past-edit-record you want to be looking at.  Notice, for example, that we have STARTED refactoring the vector/scalar code but we haven't finished. What would you do if your advisor, right now, wanted an improved version of the plot you made before?  With axis labels, say?  You can't do it now---you changed other things in the code so the current version won't plot anything.  However, you can tell Git to turn your working-directory back into the state it was in when you made the plot.  Get the long hash from the log that tells you which commit you want.

```
git checkout 35a6dd901e90dfc479405b6c5f1d0841dec60554
```

We're now looking at an old version of the file.  (If you just wanted  to look at this, rather than editing it, you're don---when you are finished just `git checkout HEAD master`.) We want to add axis labels and stuff by editing THIS version.  How do we save that new chain of edits?  It's not edits we want to make to the master version---the one that's in the middle of the vector/scalar rewrite---but it's not edits we want to discard.  We want a new BRANCH of the edit history.  Tell Git to name this new branch:

```
$ git checkout -b "make_plot_prettier"
Switched to a new branch 'make_plot_prettier'
$ git branch
\* make_plot_prettier
master
```

Git is now showing two "branches" of the code: one with an edit history leading to the "master" version ("master" is the default name for the branch you're in at `git init`, it doesn't mean anything special or central about that branch), and one called "make\_plot\_prettier" which your next edit will be appended to---it's the "current HEAD".  Let's do that edit and commit it:

```

$ cat sim.py 
import numpy as np
from matplotlib import pyplot as plt
Gnewton= 6.67e-11 # SI units
def force(m1,m2,r):
    return Gnewton*m1*m2/r*2

plt.plot([range[10],[force(1,1,r) for r in range(10)],xlabel='radius (m)',ylabel='force (N)',title="force between two 1kg masses")

$ git commit -a -m "plot now has labels"
[make_plot_prettier b651978] plot now has labels
 1 file changed, 1 insertion(+), 1 deletion(-)
```

If this plot makes your advisor happy, you want to return to the master branch where you were doing the vector/scalar edits.  Your "version of the code that makes the plot for group meeting" will not be forgotten, it's stored nicely in the branch you created while working on it.  You can return to that and fiddle with the plot aesthetics as many times as you want, then jump right back into your force-law-calculation editing work:

```
$ git checkout master
Switched to branch 'master'
```

## Merging two branches
Here's the particular magic of git.  You can *merge branches*.  Getting that plot command rihgt was a lot of work!  Can we pull that work *back into* the master branch?  We sure can.  You have master checked out.  This gets exciting.  Run this:

```
$ git merge make_plot_prettier
Auto-merging sim.py
CONFLICT (content): Merge conflict in sim.py
Automatic merge failed; fix conflicts and then commit the result.
```

OK, whoa, a conflict!  Is that scary?  No, it's normal.  The master branch of `sim.py` shows the `plt.plot` line of code looking one way,  the `make\_plot\_prettier` branch shows it looking another way.  Git is going to show you the two side by side so you can decide which is the one to keep in the merge.

What does it show you?  It shows you a MANGLED VERSION OF SIM.PY with both versions shown as a sort of comparison.  This is scary if you were not expecting it, but it's normal. Look at it:

```
$ cat sim.py 
import numpy as np
from matplotlib import pyplot as plt
Gnewton= 6.67e-11 # SI units
def scalar_force(m1,m2,r):
    return Gnewton*m1*m2/r*2
<<<<<<< HEAD
def vector_force(m1,m2,r1,r2):
    vector_sep = r1-r2
    scalar_sep = np.norm(r1-r2) # FIXME need to look up this syntax
    return vector_sep/scalar_sep(force(m1,m2,scalar_sep))
    
plt.plot([force(1,1,r) for r in range(1)])

=======

plt.plot([range[10],[force(1,1,r) for r in range(10)],xlabel='radius (m)',ylabel='force (N)',title="force between two 1kg masses")
>>>>>>> make_plot_prettier
```

Git has done some things which are worth pointing out.  It recognizes that the import statements and the Gnewton definition are in both edit histories; they're there intact in the new merged chain.  It recognizes that the function "force" was edited to be named to "scalar\_force" and it thinks there is no problem making that edit in the new merged chain (even though it's a pure product of the `master` branch).  When it sees both a new function and a modified plot  command, it's confused.  Were you trying to do this merge to change the plot command?  Or to add the vector\_force function?  Or both?  It doesn't know.  

Git has given you a job: look at everything between the angle-brackets, equals-signs, and other-angle-brackets, and edit away the things you don't want.  There are tools that make this easier, but in simple cases your text editor will do fine---just edit away the unwanted code choices, then the bracket-and-arrow-and-equals lines.  When you're done editing, commit the results.  Here's my edit:

```
 $ cat sim.py 
import numpy as np
from matplotlib import pyplot as plt
Gnewton= 6.67e-11 # SI units
def scalar_force(m1,m2,r):
    return Gnewton*m1*m2/r*2
def vector_force(m1,m2,r1,r2):
    vector_sep = r1-r2
    scalar_sep = np.norm(r1-r2) # FIXME need to look up this syntax
    return vector_sep/scalar_sep(force(m1,m2,scalar_sep))
    
plt.plot([range[10],[force(1,1,r) for r in range(10)],xlabel='radius (m)',ylabel='force (N)',title="force between two 1kg masses")

$ git commit -a -m "merged in pretty plot  command"
[master eec3089] merged in pretty plot  command
```

Remember, if you don't do that `commit` then none of the above is saved.  Did you get confused during the merge-conflict and wish you'd never done it?  Run `git merge --abort` to abandon the attempted merge.

### Aside: what Git-Merge can handle and what it can't
Code, text, datalogs ... these are all files where you can say "this *line* of text changed from version A to version B".  That is not true of image files, PDFs, executables, etc..  If you have PDFs, PNGs, etc., checked into your repository---and you don't have to, they will live in the directory and ignore Git if you never `git add` them---then your merge-conflict-decisions will look like "should I keep ALL of version A or ALL of version B"?  It's still doable, but in general I try not to version-control PDFs and PNGs.

Unfortunately, `.ipynb` files are a mix of code and images.  There are slightly fancier `git` tools allowing you to version-control just the code components, but I am still learning these.

## Your git history

You now have a nontrivial git history; you can view it like this:
```
$ git log --pretty=format:"%h %s" --graph

*   eec3089 merged in pretty plot  command
|\  
| * b651978 plot now has labels
* | de54868 refactor into scalar and vector components
|/  
* 35a6dd9 add first plot
* 0df87d1 m fix, add Gnewton
* 9c2119d initial commit; one force function
```

Your code developed for a while in a single version, then split in two different directions, then recombined.  That is objectively different than a file with an undo history.  That is version control.

The industry-adoption-driving power of version control is that people can collaborate.  Two people can work together on a software project, even the same file, by letting their individual edit histories pile up in different "branches" (each branch looking like a solo-coding project with an undo history) which periodically "merge" when a given branch is deemed to have fixed a bug, or added a feature, which other coders will want to base their own next efforts on.

## Summary of solo workflows
### Minimal version
As a solo script-hacking-y coder most of the time you will be doing the same thing repetitively.

0) Get into your repository and `git checkout master` (or otherwise get into the right state)
1) Edit your code; get to a minor stopping point
2) Run `git commit -a -m "type_a_commit_message_here"`

### Branch-early, branch-often version
A notably better workflow is "branch early, branch often".  The nice thing about this is that, in your git log, the "master branch" has a small-ish, understandable commit history; and anything checked out from master is "sort of working code".  All of the tiny debugging commits, syntax errors, typos, etc., are committed in the branches.

0) Get into your repository and `git checkout master` (or otherwise get into the right state)
1) Think about what you want to work on next.
2) Start a branch with `git checkout -b todays_branch_name`
    1) Edit your code and work on this feature
    2) Run `git commit -a -m "type_a_commit_message_here"` regularly
3) When the feature basically works, merge and commit
	1) Run `git checkout master`
	2) Run `git merge todays_branch_name`
	3) Resolve any merge conflicts (should be minimal in this workflow)
	4) `git commit -a -m "describe the new feature"`

### Pull request version
The common thing you'll run into in collaborative settings is *like* branch-early, but there is also a sense that the master branch is *curated*.  A `merge` into the master branch is a notably bigger deal than a `commit -m "ongoing debugging of force() func"`.  Maybe the master branch is something that five or ten or a thousand other users are counting on being able to run.

In terms of `git` terminology, there are two separate actions that result in a `merge` onto the master branch.  One action is taken by the coder.  It is called a *pull request*, meaning "please pull my code into the master branch", and there is a certain syntax.  When a pull request has been made, it is visible to the master-branch-owner, who has a chance to review it before running `merge`.

We will talk about this more after we are doing team analysis using github.

# Connecting to github.com

Go to github.com and create an account.  Follow all the instructions for getting git software installed on your computer.

## Getting a copy of an existing repo
On the left side of your browser window is a list of your repositories.  I have added you as a collaborator to a repository called `bmonreal/adv_lab_data_analysis`.  Click on that.

There are a series of tabs.  "<> code" is usually visible by default.  Click on code, then look for a green button called "Clone or download" on the right.  Copy the string you see there; it may look  like

```
https://github.com/bmonreal/adv_lab_data_analysis.git
```
or like
```
git@github.com:bmonreal/adv_lab_data_analysis.git
```

Now, you are going to tell your computer to (a) get a copy of the entire Git  history from this site, and (b) remember the URL so you can push your bits of history back onto it.  You are getting the whole history---the master branch, other branches, everything that anyone else has pushed.

Instructions for what to do next are here:

https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository

Now that this is set up, there is a small change to your typical workflow.

To start a block of work, run

```
$ git pull
```

This downloads anything that has changed on the GitHub repo---i.e, work that other people have done---since the last time you pulled.  It then tries to merge all of that (i.e, apply that chain of edits) to the repo you have locally.  Notice that this can cause trouble (i.e. merge conflicts) if you did some edits before running `pull`---better practice is "don't touch any files between last night's last `push` and this morning's `pull`.

You spend a few hours coding, something useful gets done, and you want your code to be available to your collaborators.  There are a few specific use cases, depending on whether you're trying to commit to the remote master branch or to another branch.  For this class, I will assume you are *typically* working on a branch (not master) you made yourself, but that you want to go to github so I can see it.  

```
$ git push origin --all
```

Where does "origin" come from?  That's the name of the connection to the remote repo (i.e. GitHub).  If you are unsure of what that second argument is, run `git remote -v` to see a list of what your local repo is connected to.











