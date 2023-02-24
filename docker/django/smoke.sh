#!/usr/bin/env sh

# This file is executed to run sanity checks
# on production image.
# Please, don't put any test logic here.

set -o errexit
set -o nounset

# Initializing global variables and functions:
: "${DJANGO_ENV:=production}"

# Fail CI if `DJANGO_ENV` is not set to `production`:
if [ "$DJANGO_ENV" != 'production' ]; then
  echo 'DJANGO_ENV is not set to production. Running tests is not safe.'
  exit 1
fi

echo '[smoke started]'
set -x

# Ensure that Django sanity check works,
# this also catches most invalid dependencies and configuration:
python manage.py check --deploy --fail-level WARNING

set +x
echo '[smoke finished]'
