# Django Blog

This Django blog application was initially created following the Django Girls tutorial, available at [https://tutorial.djangogirls.org/en/](https://tutorial.djangogirls.org/en/), with subsequent modifications and enhancements by me :)

The list of enhancements:
* tests configuration

## Running Locally

To run this application locally, follow these steps:

#### Prerequisites

- Python 3 installed on your machine
- Pip package manager installed
- Virtualenv installed

#### Setting up Virtual Environment

1. Clone this repository to your local machine:

   ```bash
   git clone git@github.com:paziolka/dg_blog.git
   ```

2. Navigate to the project directory:

   ```bash
   cd django-blog
   ```

3. Create a virtual environment:

   ```bash
   virtualenv dg_blog_env
   ```

4. Activate the virtual environment:

   ```bash
   source dg_blog_env/bin/activate
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

#### Running the Application

1. Make migrations:

   ```bash
   python manage.py makemigrations
   ```

2. Apply migrations:

   ```bash
   python manage.py migrate
   ```

3. Run the server:

   ```bash
   python manage.py runserver
   ```

4. Access the application in your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Running Tests

To run tests for this application, ensure you have activated the virtual environment (`source dg_blog_env/bin/activate`). Then, run the following command:

```bash
python manage.py test
```

## To-Do List

- Add more tests and a tool to monitor the test coverage
- Add pylint or other tool to make my code consistent and elegant
- Add some github actions to monitor the test coverage and/or style ;)
- Consider containerization with Docker
