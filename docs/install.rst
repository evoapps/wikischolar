Installing wikischolar
======================

- Clone the wikischolar package.
- Create a new python virtualenv.
- Install python requirements.

Install python requirements
---------------------------

First install pywikibot::

    pip install pywikibot --pre

Then configure pywikibot by modifying user-config.py with your accounts.

After that, you can install the remaining requirements with::

    pip install -r requirements.txt

Install wikischolarlib
======================

wikischolarlib is an R package for bundling up data collected
using wikischolar. To install the wikischolarlib you can use the
R package devtools and install it from github::

    devtools::install_github("evoapps/wikischolar", subdir = "wikischolarlib")

Right now, wikischolarlib is included with the wikischolar project.
If you want to modify your local copy of wikischolarlib, you can install
the modified version using devtools::

    # working directory is wikischolar project root
    devtools::install("wikischolarlib")
