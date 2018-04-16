(function (app) {
    'use strict';
    
    app.factory('AuthService', ['$q', '$timeout', '$http', function ($q, $timeout, $http) {

    // create user variable
    var user = null;
    var admin = null;

    // return available functions for use in controllers
    return ({
      isLoggedIn: isLoggedIn,
      isAdmin: isAdmin,
      login: login,
      logout: logout,
      getUserStatus: getUserStatus
    });

    function isLoggedIn() {
      if(user) {
        return true;
      } else {
        return false;
      }
    }

    function isAdmin() {
        if (admin) {
            return true;
        } else {
            return false;
        }
    }

    function login(email, password) {
        var deferred = $q.defer();

        $http.post('/api/login', {email: email, password: password}).success(function (data, status) {
            if(status === 200 && data.result){
                user = true;
                admin = data.admin;
                deferred.resolve();
            } else {
                clearUser();
                deferred.reject();
            }
        }).error(function (data) {
            clearUser();
            deferred.reject();
        });

        return deferred.promise;
    }

    function logout() {
        var deferred = $q.defer();

        $http.get('/api/logout').success(function (data) {
            clearUser();
            deferred.resolve();
        }).error(function (data) {
            clearUser();
            deferred.reject();
        });

        return deferred.promise;
    }

    function getUserStatus() {
        return $http.get('/api/status').success(function (data) {
            if(data.status){
                user = true;
                admin = data.admin;
            } else {
                user = false;
            }
        }).error(function (data) {
            user = false;
            admin = false;
        });
    }

    function clearUser() {
        user = false;
        admin = false;
    }

}])})(thundersnow);
