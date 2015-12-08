![Paypyrus](http://i.imgur.com/VcunvJc.png)
### money, reimagined.

[screenshots](http://imgur.com/a/4EEkX)

### Summary:

Paypyrus is a web application based on QR codes that allows users to send each other
money electronically, but with a physical component.

Paypyruses are paper bills fitted with a QR code. This QR code can be scanned,
which will bring the user to a redemption phase during which the user can receive
the money in their Venmo accounts.

Through Paypyrus, you can send a given amount of money through Venmo without first knowing
who is to redeem this money. In short, you can pre-allocate a certain amount of money by printing
it on a Paypyrus bill, give it to someone, who can decide how to redeem it. The recipient can even
give the bill to yet another person, who can redeem it in turn without hassle.

##### Paypyrus is versatile like cash, but simple and direct like Venmo.

Paypyrus uses the Venmo API, Python Flask for the web app, and MySQL for the backend.
We use SVGs to generate the printable Paypyrus bills.

### Usage:
 - User 1 (Amy) decides to print a bill for a dollar
 - Amy goes on Paypyrus and selects $1, then prints out of printer
 - Amy gives Paypyrus to Ricky, who gives it to Chaoyi
 - Chaoyi gives the money to Mani who decides to cash in the funds.
 - Mani scans the code, puts in his Venmo username, and receives funds directly from Amy

### Running:
 - Install Python dependencies: `pip install -r requirements.txt`
 - Modify `pp/config.py` with correct credentials
 - Start MySQL and create DB
 - Create tables: `python create_db.py`
 - Run: `python runpp.py`

### Authors:
 - [@amy-shu](https://github.com/amy-shu)
 - [@tsmanikandan](https://github.com/tsmanikandan)
 - [@rickyliang](https://github.com/rickyliang)
 - [@cydrobolt](https://github.com/cydrobolt)

<!-- https://paypyrus.org -->
