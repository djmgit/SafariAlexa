
var https = require('https');
// https is a default part of Node.JS.  Read the developer doc:  https://nodejs.org/api/https.html
// try other APIs such as the current bitcoin price : https://btc-e.com/api/2/btc_usd/ticker  returns ticker.last

state = 'west bengal'
const API_BASE = 'alexasafari.herokuapp.com';


httpsGet(state,  (myResult) => {
                console.log("received : " + myResult.places_to_visit);

                console.log(myResult.places_to_visit);

            }
        );
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
