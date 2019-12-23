# UCI WebReg Python API

Everything you need to create a UCI WebReg Bot within 5 minutes!

## Introduction
Designed for UC Irvine WebReg, 
WebReg API is a Python API you need to create your own enrollment bot script within less than 10 lines of code!

Unlike other bots, it is deeply integrated with WebReg and takes advantage of Selenium technology
which makes it robust, fast, and secure. 

### Highlights
* **Secure.** The top priority is that you'll never get banned because of using this. 
The bot simulates that a real person and a real browser would do so any kind of behavioral detection will not be able to distinguish you from other people.
* **Robust.** The API keeps track of the WebReg login status. So it won't crash due to exceptions like maintenance or unopened enrollment window. 
* **Versatile.** The API helps you not only enroll in classes, but also check study lists, waitlists, and so on.

## Prerequisite

* Chrome browser and Python 3.6+

## Working Functions

* Add/Change/Drop courses
* Add/Drop wait list courses
* See open sections of a course
* Fetch study list and wait list
* Auto-logout

## Deployment

* Install Selenium

```bash
pip3 install selenium
```

* Download WebDriver and make it executable

<https://sites.google.com/a/chromium.org/chromedriver/downloads>

```bash
chmod +x ./webdriver
```

* Make it yours

```bash
git clone https://github.com/maao666/UCI_WebReg_API.git
```

* Example

```python
form WebReg import WebReg
from pprint import pprint # Not required

# Replace username and password with yours
wr = WebReg().login('username', 'password')

# Add a course
wr.add_course('16570')

# Change to Pass/No Pass
wr.change_course('16570', letter_grade=False)

# Drop a course
wr.drop_course('16570')

# See available sections
pprint(wr.list_open_sections('16570'))

# Get study list
pprint(wr.get_study_list())

#It automatically logs out so no logout operation required
```

## We humbly ask you for a star if this helps you.

**To UCI Registrar**: The technology you use for WebReg is so lame! I can't believe you use a Shell script for load-balancing and redirecting. Such a shame on you and OIT for creating such a terrible user experience! I'm confident that you are not smart enough to catch my bot till I graduate. We'll see.
