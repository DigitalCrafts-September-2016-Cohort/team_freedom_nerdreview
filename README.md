#Nerd Review
######
[Live Project - http://nerdreview.co](https://nerdreview.co)  | [Overview](https://github.com/DigitalCrafts-September-2016-Cohort/team_freedom_nerdreview#overview)  |  [Team](https://github.com/DigitalCrafts-September-2016-Cohort/team_freedom_nerdreview#team-members--roles)  |  [What We Used](https://github.com/DigitalCrafts-September-2016-Cohort/team_freedom_nerdreview#what-we-used)  |  [MVP](https://github.com/DigitalCrafts-September-2016-Cohort/team_freedom_nerdreview#mvp-minimum-viable-product)  |  [Challenges](https://github.com/DigitalCrafts-September-2016-Cohort/team_freedom_nerdreview#challenges--solutions) [Contributing](https://github.com/DigitalCrafts-September-2016-Cohort/team_freedom_nerdreview#contribute-to-nerd-review)

##Overview:
Nerd Review is a centralized platform that brings together product lovers of the obsessive and methodical variety from their respective corners of the internet.  The audience of the dedicated product review bloggers out there can often be limited to existing members of that community.  If you are a nerdy consumer branching into a new area or just researching every major purchase like a PhD thesis, your progress can be slowed by the fact that if you aren't already aware of that particular niche product review blog.  If you don't already know about it, you can't find it.  This web app provides a functioning framework for such a dedicated review site that bridges the gap between professional product reviewers and average consumers.  

**Our conceptual goals for the site:**
* Eliminate any commerce connection to keep site content impartial
* Reviewers are responsible for site content (user-generated content only, no listicles or subjective rankings)
* Primary content (reviews) should meet a minimum threshold of nerdiness
    - Minimum length
* Only registered users of Nerd Review can post reviews
* Reviews are associated with a product which is associated with a company, new products can be added directly by reviewers

##Github Link:
[NerdReview](https://github.com/DigitalCrafts-September-2016-Cohort/team_freedom_nerdreview.git)

##Team Members & Roles:
**Click on each member's name to see their GitHub profile**
All team members are students in the [Digital Crafts](https://digitalcrafts.com) September 2016 cohort. This project was initially completed as the first full-stack project for that curriculum.
<!-- During this project we utilized the Scrum development process and philosophy.  Paired and mob programming were the focus in the initial and final stages, while mid and late stage work was primarily completed through individual but coordinated and co-located programming.   -->

####Team Freedom
* [Che Blankenship](https://github.com/cheblankenship/):  
**Primary team role:** UI/UX evaluation, Quality control  
**Contributions:**  
**Key code portions:**

* [John Coppola](https://github.com/johnnycopes/):  
**Primary team role:** Front-end warrior
**Contributions:** Led the charge on all things visual/client-facing. Built a custom, responsive layout from scratch with focus on clean, robust design. Wrote and refactored HTML/CSS with an emphasis on simplicity, clarity, and flexibility. Organized site navigation. Made sure that we were pulling the right information from the database in the right places.
**Key code portions:** Most of the HTML, CSS and JavaScript. Made tweaks to route handlers on the back end as well.

* [Robert Dunn](https://github.com/robdunn220/):  
**Primary team role:** Back-end ninja  
**Contributions:** Database design and implementation. Route handlers and queries. Just making sure the manipulation and display of the data in the database was working well with the design concept.
**Key code portions:** server.py, Jinja in some of the HTML

* [Jesslyn Landgren](https://github.com/jesslynlandgren/):  
**Primary team role:** Organize all the things, back-end backup  
**Contributions:** Scrum master. Led daily stand up meetings and maintained virtual scrum board.  Provided initial project concept.  Helped Rob build out initial back-end, including route handlers, SQL queries, and placeholder HTML/Jinja for pages.  Helped troubleshoot and tweak SQL queries throughout project.  Developed and implemented drop-down sort throughout site.  
**Key code portions:** Front-end and back-end for drop-down sort elements for tile-grid pages.  Co-wrote user login & signup route handlers, HTML.

##What we used:
**Technologies:**  
* PostGresSQL
* Amazon Web Services EC2
* Apache

**Frameworks:**  
* Flask
* Jinja
* Bootstrap

**Languages:**  
* Python (including the following modules)
  * PyGreSQL
  * datetime
  * os
  * dotenv
* HTML5
* CSS
* JavaScript

##MVP (Minimum Viable Product):
This was the first full-stack project for all team members, therefore our first experience at deciding on an MVP.  One challenge we faced was a blurring the line between our MVP and stretch goals due to a desire to make efficient use of our time, dispatching some members to advanced tasks if troubleshooting an MVP issue was a one person job.

**Initial MVP**
* The following pages: individual review, individual project (with all reviews), list of all reviews, list of all brands, list of all users
* Products organized into a category hierarchy at least three levels deep
* Consistent formatting for all pages including a vertical fixed-right nav bar and a main content area displaying items as grid tiles
* User session tracking (log in, log out, sign up)
* Drop-down sort menu with auto refresh for all pages displaying grid tiles
* Back button

We started incorporating stretch goals about three days before the project deadline (as soon as we knew that we would be able to reach MVP ahead of the deadline), but before our MVP was officially deployed.

**Stretch Goals**
* Site responsiveness
* User log in and sign up without leaving the current page, instead as modal dialogs
* Page title acts as a breadcrumb and supplements back button
* "Add a review" form with select elements showing choices of existing categories, brands, and products.
* Validate inputs on user log in and sign up forms before submission
* Search products (from home page)

## Challenges & Solutions:
**Some of the biggest challenges we faced with this project build included:**
1. Tracking a visitor's current location within the site category hierarchy to maintain the "up a level" or "down a level" on click
2. Sorting grid pages without implementing a significant amount of JavaScript.
3. Reducing redundancies on the back-end

##Code Snippets
```
// NAV MENU SLIDE
// Store nav menu panel position in JS local storage. On page refresh, set it to either open or closed and the mobile menu button to the correct color
function markSliderPosition(position){
    localStorage.setItem('sliderPosition', position);
}
if (localStorage.getItem('sliderPosition') === 'open') {
    $('.nav-menu').css('left', '0');
    $('.js-slide').css('color', '#fff');
} else {
    $('.nav-menu').css('left', '-320');
    $('.js-slide').css('color', '#F4CF6F');
}
// Change the slider position and mobile menu button on click
$('.js-slide').on('click', function(){
    if ($('.nav-menu').position().left === 0) {
        $('.nav-menu').animate({left: -320});
        $(this).css('color', '#F4CF6F');
        markSliderPosition('closed');
    } else {
        $('.nav-menu').animate({left: 0});
        $(this).css('color', '#fff');
        markSliderPosition('open');
    }
});
// If page width is greater than 1000px, set the nav menu on any kind of page resize
$(window).resize(function() {
    if ($(window).width() > 1000) {
        $('.nav-menu').css('left', '0');
        markSliderPosition('open');
    }
});
```

##Screenshots

********

#Contribute to Nerd Review

##Desired Contributions:
While what we *really* would like to see are your passionate rants about the features of big fluffy coats, there are some features we haven't implemented yet in Nerd Review that we think are important:
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
