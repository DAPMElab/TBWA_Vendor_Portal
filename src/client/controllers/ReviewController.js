
/*
 *  Manages the creation and submission of company reviews
 */

angular.module('myApp.controllers')
.controller('ReviewController', function ($scope, $http, setUpDict, condenseDictionary,
  $modal, jobSizeRanges, flash) {

    $scope.jobSizeRanges = jobSizeRanges;

    /**
     * Function for modal opening
     */
    $scope.open = function () {
        $scope.newReview = {
            Description: null,
            Cost: null,
            Rating: 0,
        };

        $scope.reviewCategoryChoices = setUpDict([], $scope.selectedCompany.Company.Categories);
        $scope.modalInstance = $modal.open({
            templateUrl: 'client/partials/writeReview.html',
            scope: $scope
        });
    };

    $scope.submitReview = function () {
        var data = $scope.newReview;
        data['Company'] = $scope.selectedCompany.Company.id;
        data['Category'] = condenseDictionary($scope.reviewCategoryChoices),

        console.log(data);
        $http.post('/review/create/' + $scope.selectedCompany.Company.id, data)
            .success(function (response) {
                console.log("Review was received.");
                flash.post('Review submitted', 'alert-success');
            })
            .error(function (err) {
                console.log(err);
                flash.post(err.message, 'alert-danger');
            });
        $scope.modalInstance.close();
    };


    /*
     * Rating controller
     */
    $scope.rate = 7;
    $scope.max = 10;
    $scope.isReadonly = false;

    $scope.hoveringOver = function(value) {
        $scope.overStar = value;
        $scope.percent = 100 * (value / $scope.max);
    };

    $scope.ratingStates = [
        {stateOn: 'icon-ok-sign', stateOff: 'icon-ok-circle'},
        {stateOn: 'icon-star', stateOff: 'icon-star-empty'},
        {stateOn: 'icon-heart', stateOff: 'icon-ban-circle'},
        {stateOn: 'icon-heart'},
        {stateOff: 'icon-off'}
    ];

    $scope.getNumberOfFullStars = function(num){
        return new Array(num);
    };

    $scope.getNumberOfEmptyStars = function(num){
        var emptyCount = 5 - num;
        return new Array(emptyCount);
    };
});

