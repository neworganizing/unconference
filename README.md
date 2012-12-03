#The Wall

**The Wall** is a Django/Python app built to be deployed on Heroku that allows conferences and unconferences to post their full schedule on a responsive website with a full API backend (which has been used in the past to work with a mobile app.)

Goals of the app are to allow rapid deployment, low maintainance and a responsive design that allows visitors to quickly view sessions on desktop, tablet and mobile.

##Setup Notes

The setup of this app is relatively quick and straightforward.

To save you a bunch of reading, here's the commands that will let you deploy in an instant (works on Mac/Linux.)

    git clone git@github.com:neworganizing/unconference.git
    cd unconference
    heroku create
    heroku config:add AWS_STORAGE_BUCKET=bucketnamehere
    heroku config:add AWS_ACCESS_KEY_ID=public_access_key_here
    heroku config:add AWS_SECRET_ACCESS_KEY=secret_key_here
    git push heroku master
    heroku run python manage.py syncdb
    heroku run python manage.py collectstatic

Then visit `http://yourappname.herokuapp.com/admin/` to setup sessions.

Here are the more detailed instructions 

###Comand Line Setup
These steps are a bit more complicated and will require some command line help. This is where you may want to bring in a bit of outside help if you aren't familiar or comfortable with using your operating system's command prompt.

#####Step 0: Install Heroku Tools
Make sure that you have the [Heroku Toolbelt](https://toolbelt.heroku.com/) installed and an Amazon S3 account and bucket ready for the app.

#####Step 1: Clone the app
Using your operating system's shell, clone into the wall repository by running `git clone git@github.com:neworganizing/unconference.git`

#####Step 2: Create a heroku app
Move into the 'unconference' directory you just cloned into and type `heroku create`. You'll now see a url with the subdomain http://xyz123.herokuapp.com/, this is the heroku URL of our wall.

#####Step 3: Add information for S3
We need to add our s3 information to heroku before we can deploy. Your public and secret keys are available under 'Security Credentials' on the [Amazon Web Services](http://aws.amazon.com/) website, while you'll need to use the Amazon Management Console or a 3rd party app like the Firefox Extension [S3Fox](http://www.s3fox.net/) to create a bucket.

Once you have your credentials and have created a bucket, set the following environmental variables

    heroku config:add AWS_STORAGE_BUCKET=bucketnamehere
    heroku config:add AWS_ACCESS_KEY_ID=public_access_key_here
    heroku config:add AWS_SECRET_ACCESS_KEY=secret_key_here

#####Step 4: Submit app to heroku
We need to send our app to Heroku and launch it. This is done by typing the command `git push heroku master`. This may take a few moments.

#####Step 5: Setup database
We need to setup our database. Type in `heroku run python manage.py syncdb` and follow the prompts to create a new administrative account.

#####Step 6: Send static files to Amazon S3
We need to collect our static files into our S3 bucket. This is done with the command `heroku run python manage.py collectstatic`

At this point you can visit http://yourherokuappurl.herokuapp.com/admin/ and login using the username and password you set during the `syncdb` step.

###Event Configuration

These steps can be handled by a less technically experienced event organizer. Much of the information is only seen via the API and not on the main website (as of right now)

####Step 0: Login
If you correctly followed the configuration steps you'll need to login to your control panel at http://yourherokuapp.herokapp.com/admin/ .

####Step 1: Name Your Site
The first step is to give your site a name. If you visit /admin/sites/site/ you'll see a single record (Domain name: example.com, Display name exmaple.com.)

Edit this record by clicking on the linked 'Domain name.' Set the domain name to the domain your wall is hosted on (in this case http://yourherokuappurl.herokuapp.com/) and the Display name to what your event is referred to as. Display name is used in the template to refer to your event, so it's important you set it properly.

Change the settings to fit your needs then click 'Save'

####Step 2: Add a venue
Using the 'Home' link on the top of the admin page, find 'Venues' and click the +Add button.

Any fields that are bold are required.

####Step 3: Add days
Going back to the home screen, click the +Add button next to Days and add the first day of your event. If you have a multi-day event, click 'Save and add another', otherwise save the day and go back to the homescreen.

####Step 4: Add slots
Going back to the home screen, click the +Add button next to Slots. From the dropdown choose a day, enter a name for the slot and then a start time and end time.

Note: Start time and End time are in 24H format (so 1PM is 13:00:00)

####Step 5: Add tags
Going back to home, click the +Add next to 'Session tags' and start adding tags for your sessions.

####Step 6: Add rooms
At the home screen, click the +Add next to 'Rooms' to add available rooms. Floor is useful for ordering and is required even if your event is only on a single floor.

####Step 7: Add sessions and participants
If you are planning on directly importing EventBrite attendees be sure to have that done before adding any sessions or participants. The import system only checks to see if a participant with the same participant ID in EventBrite exists in the 'Participants' database, so manually adding a user and then having that user register in EventBrite will result in that user appearing twice.

To add a session, click on the bolded 'Sessions' link on the Home page. Press 'Add session' on the top right of the screen that appears and enter the relevant information.

The 'Presenters' box is actually an autofill box. If you start typing in the name of an attendee in the system that attendee should appear in a dropdown menu. Use your arrow keys or mouse to select that attendee and add them as a presenter.

If a presenter is not in the system, you can press the '+add' button to the right of the presenters box and a popup window will appear allowing you to add new presenters.

As you add sessions they will start to appear on your wall in real time.

####Step 8: Check your work
It is important to note that the system as it exists now does no deduping. You can schedule two events in the same room at the same time.

The best way to handle this is to cycle through your data room by room on the public-facing wall and search for duplicates per session. If you are a logged in user you will see an 'Edit this entry' box appear next to sessions which will link you to that sessions entry in the admin.

###Optional Addons

#####Custom Domain/CNAME Suport
Obviously using http://randomname.herokuapp.com/ isn't ideal. Thankfully, Heroku offers support for custom subdomains.

Heroku offers [detailed instructions on custom domains](https://devcenter.heroku.com/articles/custom-domains) which is worth the read. Just note, you'll need access to your registrar or webhost to prepend the wall to your existing domain.

#####Google Analytics
You can add Google Analytics tracking to your wall by setting your Google Analaytics ID as the GA_ID. `heroku config:add GA_ID=UA-12345-1`

If you want to track visitors across your entire domain name, specify your domain with `heroku config:add SITE_DOMAIN='yoursite.com'`

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