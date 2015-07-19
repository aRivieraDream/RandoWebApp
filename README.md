#RandoWebApp
This is an application primarily designed for the management of employees working on diverse processes in order to track time spent on tasks and also whatever meta-data associated with that task.

The primary assumption is that you want to access this data programmatically rather than storing it in excel/google sheets etc.


This app was designed using a similar structure to [Miguel Grindberg's Flask tutorial]( http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). However, I've modified it for my own use.

##Setup
This was built in a virtualenv
There were a bunch of dependencies setup following the instruction of the [tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). However, for better or worse this repo should be self-contained and have all the dependencies.

##Running the app
- Navigate to the top directory.
- `./run.py`

##Future
* Logout
* Facelift - bootstrap css
* Build functionality for storing info
  - preset preferences based on user (auto prep form)
  - typeahead for quick filling known data
* Create an initialization sequence for easy deployment.
* 
* Admin section for monitoring
