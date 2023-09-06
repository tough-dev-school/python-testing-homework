# testing_homework

This project was generated with [`wemake-django-template`](https://github.com/wemake-services/wemake-django-template). Current template version is: [4e5b885](https://github.com/wemake-services/wemake-django-template/tree/4e5b8853c7f2d263302421229b5ed7981229b954). See what is [updated](https://github.com/wemake-services/wemake-django-template/compare/4e5b8853c7f2d263302421229b5ed7981229b954...master) since then.


[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake-services.github.io)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)


## What does this app do?

This app serves just one main purpose:
showing pictures and saving your favoirutes ones.

To do that we also have supporting features, like:
- User registration and login / logout mechanics
- Integration with other external "services"
- Admin panel
- All the required infrastructure code: including CI/CD and build scripts

We also care about:
- Code quality
- Naming conventions
- Architecture
- Typing
- Tooling

### Glossary

See https://github.com/sobolevn/testing_homework/blob/master/docs/pages/project/glossary.rst


## Prerequisites

You will need:

- `python3.11` (see `pyproject.toml` for full version)
- `postgresql` with version `15`
- Latest `docker`


## Development

When developing locally, we use:

- [`editorconfig`](http://editorconfig.org/) plugin (**required**)
- [`poetry`](https://github.com/python-poetry/poetry) (**required**)
- [`pyenv`](https://github.com/pyenv/pyenv)


## 🚀 Quickstart

One time setup:
1. `git clone tough-dev-school/python-testing-homework`
2. `cd python-testing-homework`
3. Create your own `config/.env` file: `cp config/.env.template config/.env` and then update it with your own value

Run tests with:
1. `docker compose run --rm web pytest`

To start the whole project:
1. Run `docker compose run --rm web python manage.py migrate` (only once)
2. `docker compose up`


## Documentation

Full documentation is available here: [`docs/`](docs).
