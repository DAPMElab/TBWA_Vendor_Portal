

angular.module('myApp.constants', [])

.value('jobSizeRanges', [
    {"Range": "< $250k"},
    {"Range": "$250k - $500k"},
    {"Range": "> $500k"}
])

/*
 * SVG map constants
 * Represent the highlighted and default states of the map regions.
 */
.constant('mapColors', {
    highlighted :{
        opacity :"1.0",
        fillOpacity : "1.0",
        fill : "#66CCFF"
    },
    defaultState:{
        opacity :"1.0",
        fillOpacity : "1.0",
        fill : "#FFFFFF"
    }
})

/* Regions for the SVG map
 */
.constant('mapRegions', {
    'MW': "midwest",
    'SE': "southeast",
    'NE': "northeast",
    'SW': "southwest",
    'W': "west"
});

