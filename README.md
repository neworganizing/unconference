#The Wall

**The Wall** is a Django/Python app built to be deployed on Heroku that allows conferences and unconferences to post their full schedule on a responsive website with a full API backend.  It also allows for users to submit session ideas, vote on session ideas, and schedule sessions once the final sessions have been chosen.

Goals of the app are to allow rapid deployment, low maintainance and a responsive design that allows visitors to quickly view sessions on desktop, tablet and mobile.

##Setup

### General Setup

    django-admin.py startproject mysite
    cd mysite
    add "-e git+git@github.com:neworganizing/unconference.git" to requirements.txt
    pip install -r requirements.txt
    (Add thewall.urls to your urls.py file)
    python manage.py syncdb
    python manage.py migrate
    python manage.py collectstatic
    python manage.py runserver
    
### Heroku

    django-admin.py startproject mysite
    cd mysite
    add "-e git+git@github.com:neworganizing/unconference.git" to requirements.txt
    heroku create
    heroku config:add AWS_STORAGE_BUCKET=bucketnamehere
    heroku config:add AWS_ACCESS_KEY_ID=public_access_key_here
    heroku config:add AWS_SECRET_ACCESS_KEY=secret_key_here
    git push heroku master
    heroku run python manage.py syncdb
    heroku run python manage.py migrate
    heroku run python manage.py collectstatic

Then visit `http://yourappname.herokuapp.com/admin/` to setup the initial data.

## Functionality Overview

### Initial data setup

#### Step 0: Login
If you correctly followed the configuration steps you'll need to login to your control panel at http://yourdomain.com/admin/.

#### Step 1: Name Your Site
The first step is to give your site a name. If you visit /admin/sites/site/ you'll see a single record (Domain name: example.com, Display name exmaple.com.)

Edit this record by clicking on the linked 'Domain name.' Set the domain name to the domain your wall is hosted on and the Display name to what your site is referred to as.

Change the settings to fit your needs then click 'Save'

#### Step 2: Add a venue
Using the 'Home' link on the top of the admin page, find 'Venues' and click the +Add button.

Any fields that are bold are required.

#### Step 3: Add days
Going back to the home screen, click the +Add button next to Days and add the first day of your event. If you have a multi-day event, click 'Save and add another', otherwise save the day and go back to the homescreen.  Typically you can just name the day by the day of the week, but if you have fancier naming conventions those could be used too.

#### Step 4: Add slots
Going back to the home screen, click the +Add button next to Slots. From the dropdown choose a day, enter a name for the slot and then a start time and end time.

Note: Start time and End time are in 24H format (so 1PM is 13:00:00)

#### Step 5: Add tags
Going back to home, click the +Add next to 'Session tags' and start adding tags for your sessions.

#### Step 6: Add rooms
At the home screen, click the +Add next to 'Rooms' to add available rooms. Floor is useful for ordering and is required even if your event is only on a single floor.

#### Step 7: Add your unconference

Again from the home screen, click the +Add next to 'Unconferences' to add your unconference.  The slug will determine the URL for your sessions, such as "http://yourdomain/myunconference/sessions".  The display name will appear on the site, and venue, days, and participants helps determine what options should be displayed when creating a session.  Only users with a paricipant instance associated with them, and who are added to this unconference, will be able to access the sessions page and the wall.

#### Step 8: Add participants
If you are planning on directly importing EventBrite attendees be sure to have that done before adding any sessions or participants. The import system only checks to see if a participant with the same participant ID in EventBrite exists in the 'Participants' database, so manually adding a user and then having that user register in EventBrite will result in that user appearing twice.  Participants are tied to the current Django app's user model, and so that model must have a first name and last name for the participant to be displayed correctly.

#### Step 9: Adding sessions

To add a session through the backend, click on the bolded 'Sessions' link on the Home page. Press 'Add session' on the top right of the screen that appears and enter the relevant information.

The 'Presenters' box is actually an autofill box. If you start typing in the name of an attendee in the system that attendee should appear in a dropdown menu. Use your arrow keys or mouse to select that attendee and add them as a presenter.

If a presenter is not in the system, you can press the '+add' button to the right of the presenters box and a popup window will appear allowing you to add new presenters.

As you add sessions, they will be added to the session voting page.  Any user with staff level access can assign a session to a particular room and slot, thus adding it to the public schedule.

Users can add sessions through the front end, using a similar form.  Sessions added in this way will automatically add the user as a presenter, but the user can add other presenters as well.

### Optional Addons

####EventBrite Integration

This app is setup to allow attendee data (specifically name, organization and unique attendee ID) to be pulled from EventBrite using the [EventBrite API](http://developer.eventbrite.com/).

In order to implement EventBrite functionality you'll need an [API Key](https://www.eventbrite.com/api/key) as well as a private [User Key](https://www.eventbrite.com/userkeyapi/) specific to your EventBrite account (OAuth authentication is also supported, but untested), alongside the EventID (the easiest way to find this is to visit your control panel and look for the ?eid=123456 in the URL)

Set those as environmental variables

    heroku config:add EB_APPKEY=APP_KEY_HERE
    heroku config:add EB_USERKEY=SECRET_USER_KEY_HERE
    heroku config:add EB_EVENTID=12345654321

OAuth tokens can be used instead of USERKEY by using `heroku config:add EB_OAUTHKEY`

To populate your database with new attendees from EventBrite run `heroku run python manage.py pullattendees`

To view a list of all attendees being pulled, use the `--list` flag.

## The API
You can access all the session data by visiting `http://yourappurl.herokuapp.com/api/`. On the bottom of that page there are links to different formats you can request the data in (JSON, JSON-P, XML, etc.)

If you want information about a specific session, simply append the primary key of the session to the URL (so the first session you could be viewed at `http://yourappurl.herokuapp.com/api/1/`)

We expose full name, organization and then EventBrite Attendee ID. For our uses we've found it easier to have third parties that need more data pull any additional demographic data straight from EventBrite, using the Attendee ID as a primary key.

Attendee ID is not a 'secret' field in EventBrite. In fact, any event that exposes their full list of atendees also exposes each attendee's ID to every EventBrite API user, so we're comfortable listing it publicly.

## Final Notes

This app was originally built in-house by the team at [New Organizing Institute](http://neworganizing.com/) led by [Nick Catalano](https://github.com/nickcatal) for the [RootsCamp](http://rootscamp.org/) unconference and is released under an open source Apache 2.0 license.

Bug fixes and feature additions that fit the goals laid out in the start of this README are greatly appreciated.

# Awards App

## Requirements
You need to define ORGANIZATION_MODEL and USER_PROFILE_MODEL in your settings, or use the
models provided in "standalone_models".  The standalone_models.models Models represent
the minimum requirements for models that are compatible with this app.  Additionally there must be a named url called "list_organizations" for the organization autocomplete to work.
