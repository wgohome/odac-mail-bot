#Customised Email Sender

Before running the main.py script, ensure dependencies are present. In the dependencies directory, there should be the following files:

1. message.html
This is the template for the email body. The html file can be editted to your needs.

2. mailing_list.txt
This is a tab-delimited .txt file containing the information of the mailing list and the customised strings to be included in the email body.
This file can be edited in Microsoft Excel.

3. test.pdf
This can be any pdf file that is intended to be sent as an attachment. The size has to be at most 25 MB based on the email client restriction.

Also ensure that there is a directory named ./output to collect the email progress log .txt file.

Before running the main.py script, edit the email address in line 23 to the email you will be sending from. Also ensure that the email setting has been set to allow third party applications.

Run the script in the terminal.

contact: wirriamm@gmail.com
