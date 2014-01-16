
/*
 *  Holds constants for the project
 */

angular.module('myApp.constants', [
    'site.constants'
])

.value('mapUrl', "client/img/USMap.svg")

.value('jobSizeRanges', [
    {"Range": "< $250k"},
    {"Range": "$250k - $500k"},
    {"Range": "> $500k"}
])

/*
 *  SVG map constants
 *  Represent the highlighted and default states of the map regions.
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

/* 
 *  Regions for the SVG map
 */
.constant('mapRegions', {
    'MW': "midwest",
    'SE': "southeast",
    'NE': "northeast",
    'SW': "southwest",
    'W': "west"
})

/*  
 *  States tied to a region.
 *  Used by the regions filter.
 */
.constant('stateToRegion', {

    // WEST
    "AK": 'W',
    "CA": 'W',
    "CO": 'W',
    "HI": 'W',
    "ID": 'W',
    "MT": 'W',
    "NV": 'W',
    "OR": 'W',
    "WA": 'W',
    "WY": 'W',
    "UT": 'W',

    // SOUTHWEST
    "AZ": 'SW',
    "NM": 'SW',
    "OK": 'SW',
    "TX": 'SW',

    // MIDWEST
    "ND": 'MW',
    "SD": 'MW',
    "NE": 'MW',
    "KS": 'MW',
    "MN": 'MW',
    "IA": 'MW',
    "MO": 'MW',
    "WI": 'MW',
    "IL": 'MW',
    "MI": 'MW',
    "IN": 'MW',
    "OH": 'MW',


    // SOUTHEAST
    "AR": 'SE',
    "AL": 'SE',
    "LA": 'SE',
    "MS": 'SE',
    "GA": 'SE',
    "FL": 'SE',
    "TN": 'SE',
    "SC": 'SE',
    "NC": 'SE',
    "VA": 'SE',
    "WV": 'SE',
    "KY": 'SE',


    // NORTHEAST
    "CT": 'NE',
    "DE": 'NE',
    "DC": 'NE',
    "ME": 'NE',
    "MD": 'NE',
    "MA": 'NE',
    "NH": 'NE',
    "NJ": 'NE',
    "NY": 'NE',
    "PA": 'NE',
    "RI": 'NE',
    "VT": 'NE',
    "VI": 'NE',

    // Territories
    "PR": 'T',
    "PR": 'T',
    "FM": 'T',
    "GU": 'T',
    "MH": 'T',
    "MP": 'T',
    "PW": 'T',
});

