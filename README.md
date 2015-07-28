#RandoWebApp
This is an application primarily designed for the management of employees working on diverse processes in order to track time spent on tasks and also whatever meta-data associated with that task.

The primary assumption is that you want to access this data programmatically rather than storing it in excel/google sheets etc.


This app was designed using a similar structure to [Miguel Grindberg's Flask tutorial]( http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). However, I've modified it for my own use.

##Setup
This was built in a virtualenv
There were a bunch of dependencies setup following the instruction of the [tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). However, for better or worse this repo should be self-contained and have all the dependencies. *this will be modified once structure is built*

##Running the app
- Navigate to the top directory.
- `./runp.py` for production mode
- `./run.py` for debugging mode

##Future
* ~~Logout~~
* ~~User generation~~
* ~~Facelift - bootstrap css~~
* Main UI
* Build functionality for storing info
  - preset preferences based on user (auto prep form)
  - typeahead for quick filling known data
* 404 & 500 html pages
* Create an initialization sequence for easy deployment.
* Add `active` call to nav bar if user is on that page  
  - consider passing a variable with the page  
  - or better, consider checking the page in the base.html
  - likely that bootstrap has this functionality built in, I'm just not sure how to access it.
* password hashing
* ~~Basic Admin section for monitoring~~
