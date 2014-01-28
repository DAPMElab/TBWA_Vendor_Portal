
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
        fill : "#F595A0"
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
    "AZ": 'W',
    "NM": 'W',

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
    "MS": 'MW',

    // SOUTH
    "AR": 'S',
    "AL": 'S',
    "LA": 'S',
    "GA": 'S',
    "FL": 'S',
    "TN": 'S',
    "SC": 'S',
    "NC": 'S',
    "KY": 'S',
    "OK": 'S',
    "TX": 'S',

    // NORTHEAST
    "VA": 'NE',
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
    "WV": 'NE',
});
