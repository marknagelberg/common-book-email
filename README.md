# Commonplace Book Daily Email Update Script

This is a series of scripts to set up daily email updates for a commonplace book system in Google Drive. If you don't know what a commonplace book is or why you should have one, see [this awesome overview by Ryan Holiday](https://ryanholiday.net/how-and-why-to-keep-a-commonplace-book/).

For an overview of the specific commonplace book system these scripts were designed for, see [this blog post](http://www.marknagelberg.com/creating-a-commonplace-book-with-google-drive/).

Here is an overview of what the code does:

* Selects 5 documents at random, choosing across all the files in your commonplace book folder and subfolders
* Builds an email template with links to the five randomly selected commonplace book notes. It does this using the Jinja2 template engine.
* Sends the email of commonplace book notes to review to yourself (and any other recipients you want). See this previous blog post on how to write programs to send automated email updates.

Before you try to run the code, you should follow steps 1 and 2 in this [Python quick-start guide](https://developers.google.com/drive/v3/web/quickstart/python) to turn on the Google Drive API and install the Google Drive client library. This will produce client_secret.json that you will need to place in the top directory of the code.

You’ll also need to make a few substitutions to placeholders in the code:

* Enter in your Gmail email and password in the file email_user_pass.json .
* Enter in the email that will be sending the email update and the list of recipients in the file emails.json.
* In build_email.py, you need to provide a value for COMMONPLACE_BOOK_FOLDER_ID. You can find this by looking in the URL when you navigate to your commonplace book folder in Google Drive.
* Install any of the required packages in build_email.py

You can customize the way that the email looks by modifying templates/email.html.

Note that this code is useful not just for this commonplace book system, but any
system where you need to receive automated email updates that randomly select files in
your Google Drive.
