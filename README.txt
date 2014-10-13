Bath Application is...


It requires the installation of python and virtualenv (with all of its dependencies)

The application uses SQLite as default database manager. The super user name is 'Admin_Bath', the password is "Pass_Bath", the email is jmtovar@gmail.com

So far this project will have dependencies with biopython. The required libraries are already configured in the req.txt file to be loaded by pip. But in linux it also needs some header files in the system so it can compile all the modules. I had to install [g++ libpng-dev libjpeg8-dev libfreetype6-dev] in a linux Mint 17 machine to be able to compile everything correctly.
