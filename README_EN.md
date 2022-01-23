# Kleps

Kleps is an academic project that consists of a social network based on vocal messages.

It was realized as an end of first semester project, during our first year in engineering school, and it was developed by:

- [ASSING Norman](https://github.com/nassing) (Project Manager)
- COUCHEVELLOU Clément
- COUVRAT--PAILLE Titouan
- SEDEKI Khalyl

## Features
- Account system : account creation, connection, constraints verification
- Audio Messages : message recording, server uploading, possibility to make the user listen to the message, possibility to give a title to the message
- Debates : Creation, display of all the debates, display of the proposals of each debate, sorting by recency and popularity
- Features constrained by the type of account: "publish a comment or a proposition" limited to connected users, "create a debate" limited to administrators
- Possibility to reply to a proposition
- Possibility to quote a proposition
- Statistics : number of tokens used for each debate and each proposition, number of propositions that quoted another one, number of comments for each proposition
- Contact and About Pages

## Installation
In its current state, Kleps was only ever used in a local server, and this part will only detail how to setup the server locally. To host the website online, please visit the [Flask documentation](https://flask.palletsprojects.com/en/2.0.x/deploying/).

If you haven't already, install [Python 3.10](https://www.python.org/downloads/) (or a later versino) for your operating system.
Then install the Flask library by typing this command line:
```
$ pip install flask
```
Finally, clone this project and launch ```flask_serv.bat``` if you are on Windows and launch ```flask_serv.sh``` if you are on Linux. The website will be available at ```127.0.0.1:5000```


## Contact
You can contact each of the project's members using the following e-mails :
- Norman : [norman.assing@hotmail.com](mailto:norman.assing@hotmail.com)
- Clément :
- Titouan :
- Khalyl :

## Contributions
This GitHub repository is more about showcasing the team's knowledge at a point of their curriculum rather than actually creating a complete product.

However, you are free to get the source course and modify it as long as you respect the license below.

## Licence
This project is under the Apache 2.0 license.

Main conditions require preservation of copyright and license notices. Contributors provide an express grant of patent rights. Licensed works, modifications, and larger works may be distributed under different terms and without source code.
