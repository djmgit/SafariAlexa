# SafariAlexa

SafariAlexa is an Alexa skill focussed on tourism. The purpose of this skill is to help people to gather various
information on different tourist places from Alexa. This skill will allow Alexa to answer queries like what is the
location of a particulat spot, what is the best time of the year to visit that spot, what are the special attractions
of that place, etc. Instead of searching all these information from various sources on the Internet, users can simply
ask their queries to Alexa and Alexa will answer them.

## How to use the skill
The **invocation phrase** for this skill is **go safari**. So in order to use this skill preceed all your queries with
the phrase go safari.
For example:

**ask go safari what is the location of manali**

or

**ask go safari to give information on manali**

or

**ask go safari what are the things I should do at manali**

or

**ask go safari what are the speacial attractions at manali**

or

**ask go safari to tell me the most suitable time to visit manali**

or

**ask go safari to name some places in manali**

or

**ask go safari to tell me some places similar to manali**

or

**ask go safari how should I reach manali**

## Technology Stack
- Alexa NodeJS kit
- NodeJS
- AWS Lambda
- Python
- Flask
- Flask-admin
- Postgres
- BeautifulSoup
- Heroku

## How the project works
The skill works at three stages, the **Alexa voice user interface (VUI)** stage, the client interacts with Alexa using VUI,
that **lambda function** which runs the app logic for generating alexa response and finally the web app which provides
the REST API from where Alexa fetches all its data.

When the user procvides a voice input, Alexa uses its VUI to handle the user input, and it finds out a particular
**intent** which can serve the user query. Alexa, after determining the appropriate intent and parameter, sends a request
to the lambda function. The lambda function uses the appropriate **handler** to serve the request. The handler actually
makes a API call to the above mentioned REST API to get the required data, generates the response and sends it back to Alexa
VUI.

### The REST API
The REST API provides the neccessary data to server the user requests. The data is provided from a database which needs
to be maintained by an admin.

Example of the REST API:

```
curl 'http://alexasafari.herokuapp.com/api/query_spot?spot=manali&query_type=info'
{
  "info": "Circled by towering peaks in the rich verdant valley of the Beas River, with mountain ventures waving from all directions, Manali is a year-round attraction. Travelers assemble here to hang out in the hippie villages around the main town; adventure seekers come for trekking, climbing, mountain biking, canyoning, paragliding, rafting and skiing; and much more.", 
  "spot_name": "manali", 
  "status": "FOUND"
}
```
**Basic format**

```
http://alexasafari.herokuapp.com/api/query_spot?spot=[name_of_the_spot]&query_type=[type_of_query]
```

where query_type can be any one of the following values

- location
- info
- things_to_do
- special_attraction
- time_to_visit
- near_by_places
- similar_places
- how_to_reach

The webapp maintains a database of tourist spots. The data is added by the admin. The server has two types of provision
to server the requests it receives about spots and query type. If the information about the spot is available in its
database, then it can return the data immidietely. Otherwise the server can employ scrapers to scrape the required
information from the web. Presently the project contains one such scraper, the **bttv_scraper** which finds out the best
time of the year to visit a particular place in case that particular place is not present in the data base.
In future more such scrapers will be added.

The webapp provides a simple and easy to use admin interface to add and maintain the data base. Admin has to login using
his credentials and an authorised admin can add other admins.

<table>
<tr>
<td><img src="images/admin.png"></td>
</tr>
</table>

<table>
<tr>
<td><img src="images/add.png"></td>
</tr>
</table>

## How to build the project

In order to build the skill along with the backend app and lambda functions, follow the below instructions

### Creating the skill

- Firstly, create a new ALexa skill by following the instructions present over 
  <a href='https://developer.amazon.com/alexa-skills-kit/tutorials/fact-skill-1'>here</a>
  
- Once the skill is created, open the tab for interaction model from the skill dash board, open the JSON edittor 
  and paste the model from <a href='InteractionModel.json'>here</a>
  
- Next create a lambda function by following the instructions present over 
  <a href="https://developer.amazon.com/alexa-skills-kit/tutorials/fact-skill-2">here</a>
  
- Do not forget to save and build your skill
  
- In the edittor for the lambda function code, paste the content from <a href="lambda/custom/index.js">here</a>

- Save your lambda function

- Connect your lambda function to Alexa VUI

### Building the backend app

Follow the below instructions to build the REST API locally

- Enter into the directory called webapp

- The API is build using python3, so you must have python3 installed

- Execute ``` pip install -r requirements.txt ```
  This will install all the dependencies for this app.
  If you encounter permission issues, please execute the above command with superuser access. For debian based systems like
  Ubuntu the command will be-
  ``` sudo pip install -r requirements.txt ```
  You may use virtualenv for building this app if you do not want to install dependencies in your global space.

### Installing the database

Execute the following to install Postgres on your system-
```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```
This will install Postgres on your system.
Next you need to create a database where you will be creating tables for this project.
By default Postgres creates a role (user) named after your system username (the username by which you are currently logged in) and a database names postgres.
In order to create a new database and get familiar with Postgres follow this article-
[Setting up Postgres onn Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04)

After Postgres is up and running you will have to apply migrations for your app and create tables.
For this execute the following from the project root.

```
python app/manage.py db init
python app/manage.py db migrate
python app/manage.py db upgrade

```

This will create tables and apply migrations.

### Running the app
Finally run the app using the following:
```
python app/main.py
```
This will start the development server at 127.0.0.1 (localhost) and port 5000

Now visit the following URL in your browser:
```
htttp://127.0.0.1:5000
```

The admin interface can be accessed at ```/admin```
However for that you need to create an admin manually from your Postgres console. This will be improved in the future

## Future goals

SafariAlexa is at the very early stages of development. Below are some future goals

- Adding more data to the database
- Adding more scrapers and data mining strategies for dynamically building a strong database
- Improving interaction experience by adding more utterances
