(function (app) {
    'use strict';

    app.factory('memberService', ['$http', function ($http) {
        return {
            getAll: function (withPayments) {
                if (withPayments) {
                    return $http.get('/api/members?with_payments=true');
                }
                return $http.get('/api/members');
            },
            getById: function (id) {
                return $http.get('/api/members/' + id);
            },
            delete: function (id) {
                return $http.delete('/api/members/' + id);
            },
            update: function (id, updateObj) {
                return $http.put('/api/members/' + id, updateObj);
            }
        };
    }]);

} (thundersnow));
