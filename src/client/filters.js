
// FILTERS

angular.module('myApp.filters', [])

/* Select List to List Attributes
 *
 * Checks that the 'filteredObj' contains at least one of the 'categories' in
 * filterObj[attributeList]
 *
 * @param objects: the list of objects that is bing evaluated for filtering
 * @param attributeList: The attribute of the filteredObj that is being checked to confirm
 *                  it contains >=1 of the 'categories'
 * @param categories: the lists of checkbox options corresponding to 'attributeList'.
 * @param requireAll: indicates whether the object should posses all or >=1 of the selected
 *                  attributes
 */
.filter('selectListToListAttribute', function () {
    return function (objects, attribute, categories, requireAll) {
        var categoriesAreChecked = false,
            filteredObjects = objects.slice(0);     // copy object array

        for (var cat in categories) {
            if (categories[cat]) {
                categoriesAreChecked = true;
            }
        }

        if (!categoriesAreChecked) {
            return filteredObjects;
        }

        objectLoop:
        // iterate through the objects backwards
        for (var objIndex = filteredObjects.length-1; objIndex > -1; objIndex--) {  
            var removeObj = true;   // assume we'll be removing the obj

            categoryLoop:
            for (var catIndex in categories) {      // iterate through the categories
                if (categories[catIndex] && filteredObjects[objIndex][attribute]){   // obj selected & obj has the attribute
                    var categoryExists = filteredObjects[objIndex][attribute].indexOf(catIndex);
                    if (categoryExists === -1 && requireAll) {
                        removeObj = true;
                        break categoryLoop;
                    } else if (categoryExists !== -1) {
                        removeObj = false;
                    }
                }
            }
            if (removeObj) { // remove obj from array
                filteredObjects.splice(objIndex, 1);
            }
        }
        return filteredObjects;
    };
})

.filter('regionsFilter', function (stateToRegion) {
    return function (objects, regions) {
        if (regions == []) {
            return objects;
        }

        var filteredObjects = objects.slice(0);     // copy object array

        for (var objIndex = filteredObjects.length-1; objIndex > -1; objIndex--){
            removeObj = false;

            // check that state exists
            if (filteredObjects[objIndex].PhysicalAddress && filteredObjects[objIndex].PhysicalAddress.State != "") {
                // check that the state is in a region is selected
                var objRegion = stateToRegion[filteredObjects[objIndex].PhysicalAddress.State] || null;
                if (regions.indexOf(objRegion) == -1) {
                    removeObj = true;
                }
            } else {
                removeObj = true;
            }

            if (removeObj) {
                filteredObjects.splice(objIndex, 1);
            }
        }

        return filteredObjects;
    };
});

