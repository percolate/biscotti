# Biscotti
An app for demonstrating functionality of the Percolate Developer Platform, written in
Python 3 using Flask.

Defines a manifest and [a Heroku app](https://prclt-biscotti.herokuapp.com/).
The manifest defines both lifecycle callback and UI extension URLs, which are served by
the app.

## Running the app locally

To create an application server running on your own machine instead of Heroku, use the
following guide.

### Run the server

1. Create a virtualenv: `python3 -m venv venv`
1. Activate it: `./venv/bin/activate`
1. Install the required modules: `pip install -r requirements.txt`
1. Run the server: `python app.py` (the default port is `8000`)
1. Verify it's working by navigating to [http://localhost:8000](http://localhost:8000),
   you should see the string `hi`

### Expose the app publicly with ngrok

1. Install [ngrok](https://ngrok.com/)
1. Expose the running local server publicly: `ngrok http 8000`
1. Change the URL domains in the manifest to use the URL displayed by the `ngrok`
   command. If you see the line `Forwarding https://490d31a3.ngrok.io ->
   http://localhost:8000`, this means that the `prclt-biscotti.herokuapp.com` domains
   should be changed to `490d31a3.ngrok.io`
1. Upload the modified app manifest in the "App registration" page
1. Install the app in the "Manage apps" page
1. Verify that your local app received callback request to `/install` in the server logs

### Update the app secret

1. Stop the app if it is running
1. Navigate to the app details by clicking on the app in the "App registration" page
1. Click the "Show app secret" button to view the secret
1. Start the app back up with the `APP_SECRET` environment variable set to the value
   shown, and the `APP_AUDIENCE` variable set to the `ngrok` domain provided in the
   previous section, an example of this command:
  ```
  APP_SECRET=c12de0430670c1e251e0502aa3afb385374df5337bdd20b27b0e77fc702c9b1a \
  APP_SECRET=5406e8ce.ngrok.io \
  python app.py
  ```
1. Navigate to a page with a UI component served by the app and verify that the JWT
   payload is properly decoded - you should see a JSON payload under the "decoded"
   header
