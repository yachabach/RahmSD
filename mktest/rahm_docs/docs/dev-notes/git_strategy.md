# GitHub Strategy for Development

There are two branches in the filter-file-lines repository:

1. **main**:  The main branch is the default branch for the repository.  It contains the latest stable version of the code.  
2. **dev**:  The dev branch is used for development.  It contains the latest changes that are being worked on.  The develop branch is merged into the main branch when the changes are stable.

## Main Branch (In a perfect world)

The main branch is protected, meaning that you cannot push directly to it.  Instead, you must create a pull request and have it reviewed before merging it into the main branch.

Currently this branch is not protected.  This is because the project is in the early stages of development and I don't know what I'm doing yet.  I will protect the main branch when I have a better idea of what I'm doing.

## Dev Branch

Exactly as the name implies.

## Feature Branches (In a world of people who know what they are doing)

Feature branches are created from the dev branch.  They contain the changes for a specific feature.  When the feature is complete, the branch is merged back into the dev branch.

The feature is complete when it passes all its unit tests.  The feature branch is then merged into the dev branch where it can go through integration testing.  If the feature passes integration testing, it is merged into the main branch.

## CI/CD Pipeline

When a branch is synched with the GitHub repository, a GitHub Actions workflow is triggered.  The actions of the workflow depend on what branch from which the update came.  Updates to the dev branch are deployed to a dev host (yachserver or miami_test)

In a perfect world, updated to the main branch happen with a pull request.  The pull request triggers a GitHub Actions workflow that runs the unit tests and integration tests.  If the tests pass, the changes are deployed to the semi-production host (miami_test).

## Process

### Create a New Project and Repository

1. Create a folder for a new project
2. Initinalize a git repository in the folder
3. Create a README.md file
4. Create a .gitignore file
5. Create a LICENSE file

```bash
mkdir new_project
cd new_project
git init
echo "# New Project" > README.md
echo "node_modules" > .gitignore
echo "LICENSE" > LICENSE
```

6. Add the files to the repository
7. Commit the files to the repository
8. Create a new repository on GitHub
9. Add the remote repository to the local repository
10. Push the files to the remote repository

```bash
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/your-repository.git
git push -u origin master
```

The `-u' option sets the upstream branch.  After this, you can use `git push` without any arguments to push changes to the remote repository.

### Create the Dev Branch

1. Create the dev branch
2. Push the dev branch to the remote repository

```bash
git checkout -b dev
git push -u origin dev
```

### Create a Workflow to Test and Deploy the Dev Branch to Dev Hosts

1. Create a new file in the `.github/workflows` folder
2. Add the workflow to the file
3. Commit the file to the repository
4. Push the file to the remote repository

```bash
mkdir .github/workflows
echo "name: Test and Deploy Dev Branch" > .github/workflows/test_deploy_dev.yml
git add .
git commit -m "Add test and deploy workflow for dev branch"
git push
```

[Example Workflow YAML for this Projec](../.github/workflows/test_deploy_dev.yml)

For now, we will commit changes directly to the dev branch.  When we are ready to merge the changes into the main branch, we will merge the dev branch into the main branch.

TODO: Use a pull request to merge the dev branch into the main branch.