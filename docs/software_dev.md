# Capstone Software Dev Introduction

## Overview
In this project, you will be working with Git, Docker and Docker Compose to develop a software solution for a real-world problem. You will be collaborating with your team members in a single GitHub repository, and will be building modular components of a larger application, each of which will be built as a separate Docker container and run in tandem via Docker Compose. 
In short, Git helps to manage and track the codebase changes, Docker helps to deploy and run application in a consistent and portable way and Docker Compose allows developer to easily configure and run multiple containers together. This project will give you an opportunity to gain hands-on experience in the tools and techniques commonly used in industry for version control, containerization and application deployment. Although you may have no prior experience in these areas, do not worry, this introduction will cover the basics of each tool, and guide you on how to use them in the context of this project.

## Git
Git is a distributed version control system that is widely used in software development. It allows multiple developers to work on the same codebase simultaneously, and keeps track of all changes made to the code. Git also allows developers to branch the codebase, which means that different versions of the code can be developed in parallel without affecting the main codebase.

### Basics
Here are some basic Git commands and their uses:

1.  `git init`: This command is used to initialize a new Git repository in the current directory.
    
2.  `git clone <repository>`: This command is used to create a copy of an existing repository on your local machine. The repository can be specified as a URL or a local file path.
    
3.  `git status`: This command is used to check the current status of the repository, including the files that have been modified and the files that have not been committed.
    
4.  `git add <file>`: This command is used to stage changes for a specific file or a group of files. Staging means the file will be included in the next commit.
    
5.  `git commit -m "message"`: This command is used to save the staged changes to the repository, with a message describing the changes.
    
6.  `git push <remote> <branch>`: This command is used to upload the committed changes to a remote repository. The remote repository and the branch can be specified as arguments.
    
7.  `git pull <remote> <branch>`: This command is used to download the latest changes from a remote repository and merge them with the local repository.
    
8.  `git branch`: This command is used to list all the branches in the local repository.
    
9.  `git branch <branch-name>`: This command is used to create a new branch.
    
10.  `git checkout <branch-name>`: This command is used to switch between branches.
    

These are just some of the basic Git commands that you will use when working on this project. There are many more advanced Git commands and features available, but the ones listed here should be enough to get you started.

It's also important to mention that a Git workflow is widely used to manage the development process, Git flow is one such widely used workflow, it is a branching model that helps to manage the different stages of development, and it can be helpful to follow it when working on software projects.

Note: It's recommended to practice Git with a tutorial or a sample project before diving into the real project, it will give you more confidence and understanding when using it.

## Git flow in industry

Git Flow is a branching model for Git that helps to manage the different stages of development in a software project. It was developed by Vincent Driessen and it is based on the idea that the development of a software project should be split into several different branches, each with a specific purpose.

The basic structure of Git Flow consists of five branches:

1.  `main`: The main branch where the production-ready code is kept. It should always be in a releasable state.
    
2.  `develop`: The branch where all the development work happens. It is the integration branch for all feature branches.
    
3.  `feature`: These branches are used for developing new features. They are created off the develop branch and are used to develop and test a new feature before it is merged into the develop branch.
    
4.  `release`: These branches are used for preparing the software for release. They are created off the develop branch and are used to test the new features before they are ready to be shipped.
    
5.  `hotfix`: These branches are used for quick fixes that need to be made in the production code. They are created off the main branch and are used to make critical bug fixes that need to be shipped as soon as possible.
    

Git Flow also recommends a specific workflow for creating and merging these branches, which can help to keep the development process organized and avoid conflicts.

Here is a high-level overview of the workflow:

-   When a new feature is developed, a new feature branch is created off the develop branch. The feature is then developed and tested in that branch, before it is merged back into the develop branch
-   when the development is ready for release, a new release branch is created off the develop branch. Final testing and bug fixing is done in this branch, before it is merged back into develop and main.
-   To fix bugs in the production release, a hotfix branch is created off the main branch and the bug is fixed, and then the branch is merged back into main and develop branch.

The Git Flow model is widely used in software development, and it can be a helpful way to structure your Git branches and workflow when working on a software project. Since you are not a company that is continuously releasing software, you will follow a simplified git flow. This is more suitable for developing your MVP, but will still give you valuable experience that will make you stronger job candidates for industry positions.

### Git Flow for a student project

When working collaboratively on your capstone project to build an MVP, the following parts of Git Flow are relevant:

1.  `develop`: This is the branch where all the development work happens. The students should create feature branches from the develop branch and merge them back in when they are done, so that all the work is integrated together on this branch. This can help ensure that the codebase stays consistent and all the features work together.
    
2.  `feature`: Each student should create their own feature branch, where they can work on the task or functionality assigned to them. The feature branches are created off the develop branch, and the students should merge the feature branches back into the develop branch after they are done.
    
3.  `merge`: When students finish working on their feature branch, they should submit a pull request to merge their feature branch back into the develop branch. This is where code review and testing will happen, and if everything is good to go, the merge will happen, otherwise, the issues need to be fixed and resubmit the merge request.
    
4.  `pull`: Students should make sure to regularly pull the latest changes from the develop branch to their feature branches. This will ensure that their code is up to date and that they are not working on an outdated version of the codebase.
    
5.  `commit`: When student makes changes to their feature branch, they should commit those changes with a clear and meaningful message describing the changes. This will make it easier for others to understand what changes were made, and how it is impacting the system.
    
6.  `rebase`: Before merging the feature branches back into the develop branch, students should use 'git rebase' command to update their feature branches with the latest changes in the develop branch, this will avoid conflicts during merge and will make sure that the feature branches are based on the latest version of the develop branch.
    
7.  `main`: The main branch is usually not used during the development process, and is only used when the final release is ready. It would be a good idea to make a release every time you hit a project milestone.
    

### Using github

GitHub is a web-based platform that provides hosting for Git repositories, and it is widely used by developers to collaborate on code. When working on a school capstone project, students will be using GitHub to host their project's Git repository and collaborate with each other.

Here is an overview of how students will be using GitHub in the capstone project:

1.  Each group of students will have a single GitHub repository for their project, where all the code will be stored.
    
2.  Each student will clone the main repository to their machine. This will allow them to work independently on their own feature branches.
    
3.  Students will use Git and the command line to work with the repository on their local machine. They will be able to use all the Git commands, such as `git clone`, `git pull`, `git push`, `git branch`, and so on, to manage the codebase.
    
4.  Students will use feature branches to work on their assigned tasks and functionalities. They will be able to push their changes to their own copy of the repository and submit pull requests to merge their changes back into the main repository.
    
5.  When a student finishes working on their feature branch and is ready to merge their changes into the main repository, they will submit a pull request through the GitHub web interface. This will notify the other students and the instructor that changes are ready to be reviewed.
    
6.  The other students and the instructor will be able to review the changes, discuss any issues and make suggestions for improvements before approving and merging the changes into the main repository.
    
7.  By using GitHub, students will be able to collaborate and share their code with each other, as well as keep track of all the changes that are made to the codebase. The version control system (Git) will keep a track of all the commits, branching and merging which will aid in debugging and understanding the codebase.
    
8.  By following Git Flow and using GitHub, students will be able to work together effectively on the capstone project, and will also learn valuable skills that are widely used in the industry.

### VS Code

Visual Studio Code (VScode) is a popular code editor that can be used in conjunction with Git, GitHub, and Git Flow to facilitate development and collaboration on a project.

VScode has built-in support for Git, which means that students can use the Git commands directly from within the editor. This can make it more convenient for them to manage their codebase, as they won't need to switch between the command line and the editor. Students can use the Git commands directly from the VScode terminal or through the Source Control tab on the left sidebar.

VScode also has built-in integration with GitHub, which allows students to easily manage their clone of the main repository and submit pull requests. They can view the status of their pull requests and receive notifications when they are reviewed, which can help them stay on top of the progress of their code review.

VScode can be an effective tool for following Git Flow, where students can create feature branches, check the status of their branches, and submit pull requests. With the help of Git Flow extension, students can visualize the Git Flow process and easily create branches, merge back to develop and finish features.

Additionally, there are a number of extensions available for VScode that can be helpful when working with Git, GitHub, and Git Flow.

1.  GitLens - This extension provides powerful code navigation and visualization features, making it easy to understand the history and evolution of the code.
    
2.  GitHub Pull Requests - This extension provides a convenient way to manage pull requests from within VScode, including the ability to view the pull requests, create new pull requests, and view the discussion on pull requests.
3.  Git Flow - This extension provides an easy way to follow the Git Flow process and automate the creation of branches and merge back, it also provides a visual representation of the Git Flow branches.
    
These are just a few examples of the extensions that are available for VScode, and there are many others that can be helpful in different contexts. I personally just use the first two at work.

## Docker
Docker is a platform that allows developers to easily package and deploy applications in a portable and consistent way. It uses containers, which are lightweight, standalone executables that can run on any machine with a Docker engine installed. Each container runs in isolation and has its own dependencies, which means that the applications running in the containers can be guaranteed to work the same way no matter where they are deployed.

## Docker compose
Docker Compose is a tool that allows developers to easily configure and run multiple containers together. It uses a YAML file to define the configuration of the containers, including their dependencies and networks. With Docker Compose, developers can easily set up complex environments for their applications, and quickly spin up or down different parts of the environment as needed.


