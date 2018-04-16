(function (app) {
    'use strict';

    app.factory('memberService', ['$http', function ($http) {
        return {
            getAll: function () {
                return $http.get('/api/members');
            },
            getById: function (id) {
                return $http.get('/api/members/' + id);
            }
        };
    }]);

} (thundersnow));
