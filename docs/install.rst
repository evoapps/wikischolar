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
