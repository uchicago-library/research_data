# Research Data
This website has a development database with test images. Follow the setup instructions below to get it running.

## Installation and setup
1. Clone the repo and go to the site root.
2. Create a virtualenv: `python3 -m venv venv`
3. Activate the virtualenv: `source venv/bin/activate` 
4. Install the requirements: `pip install -r requirements.txt && pip install -r requirements-dev.txt`
5. Create the database: `./manage.py migrate`
6. Load the dev database: `./manage.py loaddata dev/fixtures/dev.json`
7. Load the dev images: `./manage.py load_dev_images`

## Run the site
1. `./manage.py runserver 0.0.0.0:8000`
2. Go to `http://localhost:8000/`

### Dev database login
Username: `admin`
Password: `test`

### Generating fixtures
If you make a change in the dev database that you'd like to maintain, you'll need to generate fixtures. This will also need to be done when you make changes to the models and new migrations.
- `./manage.py dumpdata --natural-foreign --exclude wagtailsearch > dev/fixtures/dev.json`

## Linting
### Python
The following packages are installed in `requirements-dev.py`. You will need to setup your editor to use them.
- autopep8
- black
- flake8
- isort

### HTML
With the virtualenv activated, you can lint HTML files with the following commands:
- `curlylint --parse-only path/to/template.html`
- `djhtml path/to/template.html`
