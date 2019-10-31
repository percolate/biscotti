# Biscotti
An app for demonstrating functionality of the Percolate Developer Platform, written in
Python 3 using Flask.

Defines a manifest and [a Heroku app](https://pdp-demo-python-app.herokuapp.com/).
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
   command
  - If you see the line
    `Forwarding https://490d31a3.ngrok.io -> http://localhost:8000`, this means that
    the `pdp-demo-python-app.herokuapp.com` domains should be changed to
    `490d31a3.ngrok.io`
1. Upload the modified app manifest in the "App registration" page
1. Install the app in the "Manage apps" page
1. Verify that your local app received callback request to `/install` in the server logs
