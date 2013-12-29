
/*
 *  Holds constants for the project
 */

angular.module('myApp.constants', [])

.value('mapUrl', "client/img/USMap.svg")

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
})

.constant('availableCategories', [
    "Animation",
    "Casting",
    "Digital Production",
    "Directorial",
    "Distribution",
    "Editorial",
    "Illustration",
    "Music",
    "Post Effects",
    "Print Production",
    "Production",
    "Sound Design",
    "Storyboarding",
    "Translation",
    "Other",
]);

