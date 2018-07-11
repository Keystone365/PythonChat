
# Git Info

### Git Locations
There are 4 locations you need to be aware of:
- **origin/master** *- (this is the master branch located on [Github](https://github.com/PrincipiaCollege/6-pythonChat.git))*
- **local/master** *- (this is your local version of the master branch)*
- **local/[user]** *- (your local version of your own branch)*
- **origin/[user]** *- (your branch located on [Github](https://github.com/PrincipiaCollege/6-pythonChat.git))*

# Git Flow
```
sample branch: [user] == jbroere
```

## Starting a Project
1. Clone your repository.
```terminal
  $ git clone https://github.com/PrincipiaCollege/6-pythonChat.git
  ...
  $
```

2. Check your current branches and create a branch for yourself.
```terminal
  $ git branch
  * master
  $ git branch jbroere
  $ git branch
  jbroere
  * master
  $
```

3. Check branches and move into your local branch.
```terminal
  $ git checkout jbroere
  Switched to branch 'jbroere'
  $ git branch
  * jbroere
  master
  $
```

4. Happy programming.

5. You need to stage the files for a commit and then make a commit.
```terminal
  $ git add .
  $ git commit -m 'your commit message'
  ...
  $
```

6. Push your local branch local/[user] onto the remote branch origin/[user].
```terminal
  $ git push origin jbroere
  ...
  $
```

7. Now you need to create a pull request. This will allow a team to check your work before you merge origin/[user] into
origin/master. On [Github](https://github.com/PrincipiaCollege/6-pythonChat.git), go to the ```pull request tab``` and
click ```New pull request```. Choose the branch you want to merge into the master and create the pull request. One of your
teammates can then approve and merge the pull request into the origin/master.

## Working on Existing Project
1. When you are ready to work on your project, you need to make sure that your copy of the repository is up-to-date with
origin/master. Start by switching back to the local/master. Once in local/master, pull from origin/master. Now that your
local/master matches the origin/master you can switch back to your local branch. After switching to your local branch you will
need to merge in the local/master.
```terminal
  $ git checkout master
  ...
  $ git pull origin master
  ...
  $ git checkout jbroere
  ...
  $ git merge master
  ...
  $
```
2. Happy programming.

3. You need to stage the files for a commit and then make a commit.
```terminal
  $ git add .
  $ git commit -m 'your commit message'
  ...
  $
```

4. Push your local branch local/[user] onto the remote branch origin/[user].
```terminal
  $ git push origin jbroere
  ...
  $
```

5. Now you need to create a pull request. This will allow a team to check your work before you merge origin/[user] into origin/master. On [Github](https://github.com/PrincipiaCollege/6-pythonChat.git), go to the ```pull request tab``` and click ```New pull request```. Choose the branch you want to merge into the master and create the pull request. One of your teammates can then approve and merge the pull request into the origin/master.

6. loop back to step 1
