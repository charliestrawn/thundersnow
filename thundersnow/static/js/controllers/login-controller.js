(function (app) {
    'use strict';

    app.controller('LoginController', [ '$scope', '$location', 'AuthService', function ($scope, $location, AuthService) {

        $scope.login = function() {
            $scope.error = false;
            $scope.disabled = true;

            AuthService.login($scope.loginForm.email, $scope.loginForm.password)
                .then(function () {
                    $location.path('/');
                    $scope.disabled = false;
                    $scope.loginForm = {};
                }).catch(function () {
                    $scope.error = true;
                    $scope.errorMessage = "Invalid username and/or password.";
                    $scope.disabled = false;
                    $scope.loginForm = {};
                });
        };
    }]);

})(thundersnow)
