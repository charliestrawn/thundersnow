(function (app) {
    'use strict';

    app.factory('reportService', ['$http', function ($http) {
        return {
            getForYear: function (year) {
                return $http.get('/api/reports/annual/' + year);
            }
        };
    }]);

}(thundersnow));
