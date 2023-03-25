# testing_homework

This project was generated with [`wemake-django-template`](https://github.com/wemake-services/wemake-django-template). Current template version is: [85e91cdc9ac0f1d35b81f37bc7da170ce746d521](https://github.com/wemake-services/wemake-django-template/tree/85e91cdc9ac0f1d35b81f37bc7da170ce746d521). See what is [updated](https://github.com/wemake-services/wemake-django-template/compare/85e91cdc9ac0f1d35b81f37bc7da170ce746d521...master) since then.


[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake-services.github.io)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)


## What does this app do?

This app surves one main purpose: show pictures and save your favoirutes ones.

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

- `python3.9` (see `pyproject.toml` or `.python-version` for full version)
- `postgresql` with version `13`
- `docker` with [version at least](https://docs.docker.com/compose/compose-file/#compose-and-docker-compatibility-matrix) `18.02`


## Development

When developing locally, we use:

- [`editorconfig`](http://editorconfig.org/) plugin (**required**)
- [`poetry`](https://github.com/python-poetry/poetry) (**required**)
- [`pyenv`](https://github.com/pyenv/pyenv)
- `pycharm 2017+` or `vscode`


## TLDR

```bash
cp config/.env.template config/.env
# edit config/.env
# set DJANGO_SECRET_KEY to
# python3 -c 'from django.utils.crypto import get_random_string; print(get_random_string(50))'

docker compose up --build

docker compose exec web bash -c 'pytest'
# or faster tests without coverage
docker compose exec web bash -c 'ptw . --runner ./fast-pytest --now --delay 0.1'
```


## Documentation

Full documentation is available here: [`docs/`](docs).
