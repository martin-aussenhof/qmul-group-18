# Cloud Computing Project - Group 18

This repository contains the code for Group 18's Cloud Computing Project.

## Installation

This Guide is for absolute beginners. If you are more experienced, you might want to skip some of the steps.

### Clone Repository

1. Open _cmd.exe_ (Windows) or _terminal_ (MacOS/Linux/Unix) on your local machine or preferred development environment. _cmd.exe_ will be refered to as Terminal in these instructions.
2. Ensure that Git is installed by executing `git --version`. If it returns a line with your version, you are good to go to the next steps. Otherwise, please install Git following the guide [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) first.
3. Clone repository using `git clone git@github.com:martin-aussenhof/qmul-group-18.git` in your local console or preferred development environment. It will create a new sub directory in your current sub directory, so be aware of your current path.
4. Open the directory `qmul-group-18` in your favourite editor to view the code.

## Contributing

All contributions by the team members should be done on a branch and only merged to the remote _master_ branch after a Pull Request Review of another team member. This ensures that we have a working version at all times.

Follow the following steps to contribute code via a new branch.

1. Open a Terminal and cd into the `qmul-group-18` directory.
2. Run `git checkout -b name-of-your-branch` where `name-of-your-branch` is replaced with the name of your choice.
3. You are now working on a new branch. Add whatever you want to add. Once completed go to the next step.
4. Run `git add .` to at all files or use `git add` to pick individual files. This will add your new files to the index and ensure that Git takes them into account for your commit.
5. Run `git status` and check if all the changes you want to push are included in the commit.
6. Run `git commit -m "Your commit message"` where _"Your commit message"_ is replaced with a meaningful message about what you are adding. This will commit the changes you made.
7. Pushing your code to Github:
   - If you push this branch the first time run `git push --set-upstream origin name-of-your-branch` where `name-of-your-branch` is replaced with the name of your branch. This will tell Git that your remote branch is `origin` and push your code.
   - If you have pushed this branch before, run `git push origin name-of-your-branch`. This will push your code.
8. Go to the repository on Github ([here](https://github.com/martin-aussenhof/qmul-group-18)).
9. There now should be a green button saying `Compare & pull request`. Click this button.
10. On the next page. Add any further comments if you want (optional) and click `Create pull request`.
11. Send the link of the next page to another team member and ask them to review your changes. They can then click `Merge pull request` to merge the changes into `master`. Should there be any conflicts during merge, please ask an experienced member of the team to help you as these require a bit more experience and are hard to explain in a simple instruction manual like this.

Note: You do not have to merge your code to save it. You can follow steps 1-7 to save your code on github within your branch. This also enables other users to pull this branch and work on this. Merges should only be done when something is working and somewhat final. Please ask Martin, if you are unsure.

## Run Locally

1. Open a terminal and navigate to the parent directory where you want to have the repository.
1. Clone repository (see above).
1. Change directory to the repository folder `cd qmul-group-18`.
1. Run `git checkout master` to switch to the master branch.
1. Run `git pull` to get latest master branch from remote.
1. Run `export FLASK_APP=app` to set the environment variable for flask. If using Windows, use `set FLASK_APP=app` in CMD or `$env:FLASK_APP = "app"` in Powershell
1. Run `export FLASK_ENV=development` to enable debug mode (if you want it). If using Windows, use `set FLASK_ENV=development` in CMD or `$env:FLASK_ENV = "development"` in Powershell
1. Run `pip install requirements.txt` to install all required packages.
1. Run `flask run` to start the server and navigate to the url presented in terminal.

## Get Token

1. Log in at: http://127.0.0.1:5000/authentication (e.g. username: 200123471, password: hello).
1. Use as follows in curl `curl -X GET -H "Authorization: Bearer <token>" http://localhost:5000/studentids`

## Deploy to AWS Lightsail

1. Build docker image with `docker build . -t thesispicker`.
1. Run and test locally with `docker run -p 5000:5000 thesispicker`.
1. If previous step had no errors, create container service with `aws lightsail create-container-service --service-name thesispicker-service \ --power small --scale 1`.
1. Push image to service with `aws lightsail push-container-image --service-name thesispicker-service --label thesispicker-container --image thesispicker`
1. Deploy with `aws lightsail create-container-service-deployment --service-name thesispicker-service --containers file://containers.json --public-endpoint file://public-endpoint.json`
