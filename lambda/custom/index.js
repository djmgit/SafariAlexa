'use strict';
const Alexa = require('alexa-sdk');
var https = require('https');

const APP_ID = 'amzn1.ask.skill.942a196b-77a0-4c60-b0cf-a719bca78855';
const SKILL_NAME = 'Safari';
const HELP_MESSAGE = 'You can say tell me a space fact, or, you can say exit... What can I help you with?';
const HELP_REPROMPT = 'What can I help you with?';
const STOP_MESSAGE = 'Goodbye!';
const ABOUT_MESSAGE = 'You can ask about various tourist places and I will provide you with necessary information';

const API_BASE = 'alexasafari.herokuapp.com';

exports.handler = function(event, context, callback) {
    var alexa = Alexa.handler(event, context);
    alexa.appId = APP_ID;
    alexa.registerHandlers(handlers);
    alexa.execute();
};

const handlers = {
    'LaunchRequest': function () {
        this.emit('AboutIntent');
    },
    'GetTouristPlaces': function () {
        
        
        var state = this.event.request.intent.slots.state.value;
        console.log(state);

        httpsGet(state,  (myResult) => {
                console.log("received : " + myResult.places_to_visit);

                this.response.speak(myResult.places_to_visit);
                this.emit(':responseReady');

            }
        );
    },
    'AboutIntent': function () {
        const speechOutput = ABOUT_MESSAGE;
        
        this.response.cardRenderer(SKILL_NAME, speechOutput);
        this.response.speak(speechOutput);
        this.emit(':responseReady');
    },
    'AMAZON.HelpIntent': function () {
        const speechOutput = HELP_MESSAGE;
        const reprompt = HELP_REPROMPT;

        this.response.speak(speechOutput).listen(reprompt);
        this.emit(':responseReady');
    },
    'AMAZON.CancelIntent': function () {
        this.response.speak(STOP_MESSAGE);
        this.emit(':responseReady');
    },
    'AMAZON.StopIntent': function () {
        this.response.speak(STOP_MESSAGE);
        this.emit(':responseReady');
    },
};

// function to call external API to fetch data

function httpsGet(myData, callback) {

    // create the options object to make the API call
    var options = {
        host: API_BASE,
        path: '/api/query_state?state=' + encodeURIComponent(myData),
        method: 'GET',
    };

    var req = https.request(options, res => {
        res.setEncoding('utf8');
        var returnData = "";

        res.on('data', chunk => {
            console.log(chunk)
            returnData = returnData + chunk;
        });

        res.on('end', () => {
            // we have now received the raw return data in the returnData variable.
            // We can see it in the log output via:
            // console.log(JSON.stringify(returnData))
            // we may need to parse through it to extract the needed data

            var pop = JSON.parse(returnData)

            callback(pop);  // this will execute whatever function the caller defined, with one argument

        });

    });
    req.end();

}
