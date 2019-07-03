# Django Homework Checker 

This is an example project to illustrate an implementation of multiple user types. In this Django app, teachers can create, update, delete themes for students and students can sign up and take one of them and solve it. Also on this site you can cmpile online code and check if there are similar projects.


## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/alex.andur/django-multiple-user-types-example.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Creating and activate the virtual environment:

```bash
pip install virtualenv
source bin/activate
```

Create the database:

```bash
python manage.py migrate
```

Finally, run the development server:

```bash
python manage.py runserver
```

The project will be available at **localhost:8000/**.


## License

The source code is released under the [MIT License](https://github.com/alexandur/django-multiple-user-types-example/blob/master/LICENSE).
