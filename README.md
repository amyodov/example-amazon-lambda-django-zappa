# Example Amazon Lambda Django app (using Zappa)

This is the basic (example/template) project for running a Django app on
Amazon Lambda, completely serverless. Uses Zappa Python library for
deployment.

This is a very minimal environment; it has no static files serving and no DB.
Depending on your needs, feel free to enhance it with S3/CloudFront serving
and probably DB (maybe even Amazon RDS / Aurora Serverless).

For the test purposes, though, it already contains the Django-Rest-Framework
configured for DB-less access as well.

For the purposes of easier usage as a template for other projects, this
example has two different parts: setting up just the Django app server on
Amazon Lambda (so you could use it, probably, for REST APIs), without any static files;
and, if you really need it - configuring the extra S3 bucket for static files.

## App server on Amazon Lambda

### Initial setup

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

### Configuring Amazon Lambda

(No configuration in AWS control panel is normally required!)

For using the Amazon AWS/Lambda environment, the Python package `zappa` is
used (it is already installed as a requirement).
But it needs to learn about your Amazon credentials.

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

and it configures all the Amazon Lambda settings needed for deployment
(asking you some questions in the process).

It will generate the `zappa_settings.json` file in the process, which
configures your settings for deployment. By default, this file won't be
committed to Git (as it is mentioned in Gitignore); depending on your
project security rules, you may want to remove it from Gitignore and commit
your file, or generate it dynamically from other deployment settings (like
Ansible Vault), or use some other way of handling it. Investigate the data
in the file yourself and choose for yourself if you want to commit it in
your repository or not.

### Deploying to Amazon Lambda for the first time

Just run:

~~~sh
zappa deploy dev
~~~

and you are done!

(In the example, `dev` is the name of the environment for Lambda; you may
use multiple environments if you want).

### Update the Amazon Lambda deployment

If you updated your code and need to re-deploy the latest codebase to Amazon
Lambda, just use:

~~~sh
zappa update dev
~~~


## Using S3 for static files

### Configuring S3

For static files, we will be using S3. Configuring it is (a little bit) more
involved, and you cannot get rid of visiting the Amazon AWS control panel.

So go to the AWS control panel, and create a new S3 bucket. Note you cannot
use the same bucket that is used for zappa deployment - you need a different
bucket for static files.

For example, you create an S3 bucket with the name `zappa-static` (in fact
you'll have to find a globally unique name for the bucket). During
the creation/configuring, you probably want to leave most settings on
default. But note: when setting up the permissions of this bucket, you will
be asked if you want to "_Block all public access_" (and some other
suboptions, like "_Block public access to buckets and objects granted through new access control lists
(ACLs)_"). In fact, you want to set all these "blocks" to "Off" (so the
files in this bucket will be publicly visible!)

After you created this S3 bucket and made sure to "Unblock" it, you should go
to the CORS configuration for this bucket, press "Add CORS configuration",
and add the following one:

~~~xml
<CORSConfiguration>
  <CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <MaxAgeSeconds>3000</MaxAgeSeconds>
    <AllowedHeader>Authorization</AllowedHeader>
  </CORSRule>
</CORSConfiguration>
~~~

After this, you are basically done with configuring S3. Now you need to
teach the Django site to use it.

### Configuring Django site to use S3 for static files

By default, the `lambdatest` site has it `settings.py` which tries to load
the extra (site-specific) settings from from `settings_local.py`, which
should be in the same directory as the `settings.py` file.

To store the static files on Amazon S3, you need to use the `django-s3-storage`
module (already added in the dependencies) and configure it accordingly; so
put at least the lines like this (with your actual values) into the
`settings_local.py`:

~~~python
STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'
AWS_S3_BUCKET_NAME_STATIC = 'zappa-static'
# use the real name of your S3 bucket; we've used "zappa-static" in the example
# but it should be globally unique

# These next two lines will serve the static files directly
# from the s3 bucket
AWS_S3_CUSTOM_DOMAIN = f'{AWS_S3_BUCKET_NAME_STATIC}.s3.amazonaws.com'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

# OR...if you create a fancy custom domain for your static files use:
#AWS_S3_PUBLIC_URL_STATIC = "https://static.yourdomain.com/"
~~~

### Deploying the static files

Now, as you configured the static files storage engine to use
`StaticS3Storage`, every run of `collectstatic` will upload them to S3.

Interestingly, you can both run it locally, as

~~~sh
python lambdatest/manage.py collectstatic --noinput
~~~

, but also you can run it even on the Amazon Lambda environment!

~~~sh
zappa manage dev "collectstatic --noinput"
~~~

Note that using `zappa manage` will imply the extra costs for running Amazon
Lambda for this.

## Summary: redeploy everything

~~~sh
python lambdatest/manage.py collectstatic --noinput
zappa update dev
~~~


## Setting up CloudFront for delivering the static files from CDN

Left as an exercise for the reader.


---

(C) 2020 Alex Myodov