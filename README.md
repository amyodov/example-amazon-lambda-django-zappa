# Example Amazon Lambda Django app (using Zappa)

This is the basic (example/template) project for running a Django app on
Amazon Lambda, completely serverless. Uses Zappa Python library for
deployment.

This is a very minimal environment; it has no static files serving and no DB.
Depending on your needs, feel free to enhance it with S3/CloudFront serving
and probably DB (maybe even Amazon RDS / Aurora Serverless).

For the test purposes, though, it already contains the Django-Rest-Framework
configured for DB-less access as well.


## Initial setup

For easier maintenance, you should use `pipenv` (as a replacement for both
`pip` and `virtualenv` simultaneously). A new pipenv environment is
configured in this way:

~~~sh
brew install pipenv

pipenv --three
~~~

Having the pipenv environment, you may want to "switch" to it. In `pip`,
you were using something like `source ve/bin/activate.sh`; in pipenv, you do
just:

~~~sh
pipenv shell
~~~

Having "sourced" the pipenv environment, you install all the dependencies:

~~~sh
pipenv install
~~~

## Configuring Amazon Lambda

For using the Amazon AWS/Lambda environment, the Python package `zappa` is
used (it is already installed as a requirement). But it needs to learn about your Amazon credentials.

If you've set up your Amazon credentials before (using `~/.aws/config` and
especially `~/.aws/credentials`), you are basically ready to deploy. If you
haven't, you may want a `~/.aws/credentials` file with the contents like:

~~~ini
[default]
aws_access_key_id = YOUR_AWS_ACCESS_KEY_ID
aws_secret_access_key = YOUR_AWS_SECRET_ACCESS_KEY
~~~

So after this you just run

~~~sh
zappa init
~~~

and it configures all the Amazon Lambda settings needed for deployment.

## Deploying to Amazon Lambda for the first time

Just run

~~~sh
zappa deploy dev
~~~

and you are done!

(In the example, `dev` is the name of the environment for Lambda; you may
use multiple environments if you want).

## Update the Amazon Lambda deployment

~~~sh
zappa update dev
~~~

---

(C) 2020 Alex Myodov