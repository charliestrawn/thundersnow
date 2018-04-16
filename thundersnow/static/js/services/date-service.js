(function (app) {
    'use strict';

    app.factory('dateService', ['$http', function ($http) {
        return {
            getWeeks: function (year) {
                return $http.get('/api/weeks?year=' + year );
            },
            createWeek: function(week) {
                return $http.post('/api/weeks', week);
            }
        };
    }]);

}(thundersnow));
