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
const QUERY_TYPE = {};
QUERY_TYPE['location'] = 'location';
QUERY_TYPE['info'] = 'info';
QUERY_TYPE['things_to_do'] = 'things_to_do';
QUERY_TYPE['special_attraction'] = 'special_attraction';
QUERY_TYPE['time_to_visit'] = 'time_to_visit';
QUERY_TYPE['near_by_places'] = 'near_by_places';
QUERY_TYPE['similar_places'] = 'similar_places';
QUERY_TYPE['how_to_reach'] = 'how_to_reach';

const notFoundMessage = [
    'Sorry, I do not know the answer to this',
    'I am not sure',
    'Unfortunately, I dont know the answer',
    'Sorry, I dont know',
    'Not sure',
    'Please ask me something else',
    'I have no answer to this',
    'Please try some other question',
    'I have not got this one'
]

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
        var myPath = '/api/query_state?state=' + encodeURIComponent(state)
        console.log(state);

        httpsGet(myPath,  (myResult) => {
                console.log("received : " + myResult.places_to_visit);

                this.response.speak(myResult.places_to_visit);
                this.emit(':responseReady');

            }
        );
    },
    'GetLocationIntent': function () {

        var spot = this.event.request.intent.slots.spot.value;
        var myPath = '/api/query_spot?spot=' + encodeURIComponent(spot) + '&query_type=' + encodeURIComponent(QUERY_TYPE.location);

        httpsGet(myPath,  (myResult) => {
                this.response.speak(myResult.location);
                this.emit(':responseReady');

            }
        );
    },
    'GetInfoIntent': function () {

        var spot = this.event.request.intent.slots.spot.value;
        var myPath = '/api/query_spot?spot=' + encodeURIComponent(spot) + '&query_type=' + encodeURIComponent(QUERY_TYPE.info);

        httpsGet(myPath,  (myResult) => {
                this.response.speak(myResult.info);
                this.emit(':responseReady');

            }
        );
    },
    'GetThingsToDoIntent': function () {

        var spot = this.event.request.intent.slots.spot.value;
        var myPath = '/api/query_spot?spot=' + encodeURIComponent(spot) + '&query_type=' + encodeURIComponent(QUERY_TYPE.things_to_do);

        httpsGet(myPath,  (myResult) => {
                this.response.speak(myResult.things_to_do);
                this.emit(':responseReady');

            }
        );
    },
    'GetSpecialAttractionIntent': function () {

        var spot = this.event.request.intent.slots.spot.value;
        var myPath = '/api/query_spot?spot=' + encodeURIComponent(spot) + '&query_type=' + encodeURIComponent(QUERY_TYPE.special_attraction);

        httpsGet(myPath,  (myResult) => {
                this.response.speak(myResult.special_attraction);
                this.emit(':responseReady');

            }
        );
    },
    'GetTimeToVisitIntent': function () {

        var spot = this.event.request.intent.slots.spot.value;
        var myPath = '/api/query_spot?spot=' + encodeURIComponent(spot) + '&query_type=' + encodeURIComponent(QUERY_TYPE.time_to_visit);

        httpsGet(myPath,  (myResult) => {
                this.response.speak(myResult.time_to_visit);
                this.emit(':responseReady');

            }
        );
    },
    'GetNearByPlacesIntent': function () {

        var spot = this.event.request.intent.slots.spot.value;
        var myPath = '/api/query_spot?spot=' + encodeURIComponent(spot) + '&query_type=' + encodeURIComponent(QUERY_TYPE.near_by_places);

        httpsGet(myPath,  (myResult) => {
                this.response.speak(myResult.near_by_places);
                this.emit(':responseReady');

            }
        );
    },
    'GetSimilarPlacesIntent': function () {

        var spot = this.event.request.intent.slots.spot.value;
        var myPath = '/api/query_spot?spot=' + encodeURIComponent(spot) + '&query_type=' + encodeURIComponent(QUERY_TYPE.similar_places);

        httpsGet(myPath,  (myResult) => {
                this.response.speak(myResult.similar_places);
                this.emit(':responseReady');

            }
        );
    },
    'GetHowToReachIntent': function () {

        var spot = this.event.request.intent.slots.spot.value;
        var myPath = '/api/query_spot?spot=' + encodeURIComponent(spot) + '&query_type=' + encodeURIComponent(QUERY_TYPE.how_to_reach);

        httpsGet(myPath,  (myResult) => {
                this.response.speak(myResult.how_to_reach);
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

function httpsGet(myPath, callback) {

    // create the options object to make the API call
    var options = {
        host: API_BASE,
        path: myPath,
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
