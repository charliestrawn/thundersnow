(function (app) {
    'use strict';

    app.controller('LogoutController', [ '$scope', '$location', 'AuthService', function ($scope, $location, AuthService) {
        AuthService.logout().then(function () {
            $location.path('/login');
        });
    }]);

}) (thundersnow);
