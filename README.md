# DrugInteractionDatabase
Repository for group project in CPS 420, Fall 2026.

## Purpose
The Drug Interactions Database is a web-based application designed to help users quickly identify potential
interactions between two medications. By presenting drug interaction information and severity levels in clear,
non-technical language, the system makes complex medical data more accessible to patients. The information provided
in this database is for educational purposes only and should not be taken as medical advice.

## How-to
The project will be built using Django and Rest with data being handled with the pandas library.

Install Django (run in terminal)
 - pip install django

Create Database Migrations (run in terminal)
- python manage.py migrate

Import Drug Interaction Data
- python manage.py shell
- exec(open("interactions/import_data.py").read())
- exit()


To Start Server (run in terminal)
 - python manage.py runserver

 - Then open http://127.0.0.1:8000/ in browser

## Tests
- Check if downloading the DDInter data works
- Check if passing strings to the database look up returns the right data
- Check if the data passed to the display code works
- Check if a user can acess the website
- Check the autocorrect bar takes input correctly
- Checks if the autocorrect bar interacts with the database correctly

## Branch Strategy
We will be using GitHub Flow for branch managing. Keeps branches to short, single goal ideas. Make sure to merge a branch and retire it after it's intended goal is reached.

## Merge Conflict Handling
In the case of a merge conflict, the team will communicate to discuss which code changes should be kept and which branch should be merged. We will document the reason for these decisions in the merge reviews in the repository.

## Branch Protection
The main branch is protected to prevent unwanted changes. Some examples on how the main branch is protected is by force pushes being disabled and changes must be submitted through pull requests that require at least one teammate's approval before being merged. This allows the team to review changes and catch potential issues before they're introduced into the main branch.

## Ignore

<Rollback comment>