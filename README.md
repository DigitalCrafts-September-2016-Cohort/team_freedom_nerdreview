#Nerd Review

##Overview:
Nerd Review is a centralized platform that brings together product lovers of the obsessive and methodical variety from their respective corners of the internet.  The audience of the dedicated product review bloggers out there can often be limited to existing members of that community.  If you are a nerdy consumer branching into a new area or just researching every major purchase like a PhD thesis, your progress can be slowed by the fact that if you aren't already aware of that particular niche product review blog.  If you don't already know about it, you can't find it.  This web app provides a functioning framework for such a dedicated review site that bridges the gap between professional product reviewers and average consumers.  

*Our main conceptual goals:*
* Eliminate any commerce connection to keep site content impartial
* Reviewers are responsible for site content (user-generated content only, no listicles or subjective rankings)
* Primary content (reviews) should meet a minimum threshold of nerdiness
    - Minimum length
* Only registered users of Nerd Review can post reviews
* Reviews are associated with a product which is associated with a company, new products can be added directly by reviewers


##Live Project:
[NerdReview](https://nerdreview.co)

##Github Link:
[NerdReview](https://github.com/DigitalCrafts-September-2016-Cohort/team_freedom_nerdreview.git)

##Team Members & Roles:
####Click on each member's name to see their github profile
All team members are students in the [Digital Crafts](https://digitalcrafts.com) September 2016 cohort. This project was initially completed as the first full-stack project for that curriculum.

* [Che Blankenship](https://github.com/cheblankenship/):
*Primary team role:* UI/UX evaluation, Quality control
*Contributions:*
*Key code portions:*

* [John Coppola](https://github.com/johnnycopes/):
*Primary team role:* Front-end dreamer
*Contributions:*
*Key code portions:*

* [Robert Dunn](https://github.com/robdunn220/):
*Primary team role:* Back-end ninja
*Contributions:*
*Key code portions:*

* [Jesslyn Landgren](https://github.com/jesslynlandgren/):
*Primary team role:* Organize all the things, back-end backup
*Contributions:* Scrum master. Led daily stand up meetings and maintained virtual scrum board.  Provided initial project concept.  Helped Rob build out initial back-end, including route handlers, SQL queries, and place holder HTML/Jinja for pages.  Helped troubleshoot and tweak SQL queries throughout project.  Developed and implemented drop-down sort throughout site.
*Key code portions:* Front-end and back-end for drop-down sort elements for tile-grid pages.  Co-wrote user login & signup route handlers, HTML.

During this project we utilized the Scrum development process and philosophy.  Paired and mob programming were the focus in the initial and final stages, while mid and late stage work was primarily completed through individual but coordinated and co-located programming.  


##What was used:
* *Technologies*:
- PostGresSQL
- Amazon Web Services EC2
- Apache

* *Frameworks*:
- Flask
- Jinja
- Bootstrap

* *Languages*:
- Python (including the following modules)
* PyGreSQL
* datetime
* os
* dotenv
- HTML5
- CSS
- Javascript

##MVP:
* The following pages:
- individual review
- individual project (with all reviews)
- list all reviews
- list all brands
- list all users
* Organize reviews into at least 3 category levels
* User login and site membership
* Site navigation through a fixed-right vertical nav bar with hierarchy links
* Sort list pages

## Challenges:
* Tracking a visitor's current location within the site category hierarchy to maintain the "up a level" or "down a level" on click
* Sorting grid pages without implementing a significant amount of JavaScript.
* Reducing redundancies on the back-end

##Code Snippets

##Screenshots

********

#Contribute to Nerd Review

##Desired Contributions:
While what we really would like to see are your passionate rants about the features of big fluffy coats, there are some features we haven't implemented yet in Nerd Review that we think are important:
* User upload of product images
* Advanced text-editor for new reviews
* Community evaluation of a review through a voting system
* Assigning a reputation to a reviewer based on the scores of their posted reviews
* Nerd-tastic improvements to our UI

##Contributing
1. Fork it
2. Create a new feature branch (named after your intended feature): `git checkout -b new-feature-name`
3. Commit your changes: `git commit -am 'Added the feature!'`
4. Push to your feature branch: `git push origin new-feature-name`
5. Submit a pull request!

##Project History
10/24/2016 - Project Completion and Deployment
10/18/2016 - Project Start
