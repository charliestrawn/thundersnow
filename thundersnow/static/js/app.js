(function (global) {
    'use strict';

    global.thundersnow = angular
        .module('thundersnow', ['ngRoute', 'ui.bootstrap'])
        .config(function ($routeProvider) {
            $routeProvider
                .when('/', {
                    templateUrl: '/static/js/template/main.html',
                    controller: 'MainController',
                    access: { restricted: true }
                })
                .when('/login', {
                    templateUrl: '/static/js/template/login.html',
                    controller: 'LoginController',
                    access: { restricted: false }
                })
                .when('/logout', {
                    controller: 'LogoutController',
                    access: { restricted: true }
                })
                .when('/members', {
                    templateUrl: '/static/js/template/members.html',
                    controller: 'MemberController',
                    access: { restricted: true }
                })
                .when('/members/:id/payments', {
                    templateUrl: '/static/js/template/member-payments.html',
                    controller: 'MemberController',
                    access: { restricted: true }
                })
                .when('/reports', {
                    templateUrl: '/static/js/template/reports.html',
                    controller: 'ReportController',
                    access: { restricted: true }
                })
                .when('/report/weekly/:week', {
                    templateUrl: '/static/js/template/weekly-report.html',
                    controller: 'ReportController',
                    access: { restricted: true }
                })
                .when('/report/annual/:year', {
                    templateUrl: '/static/js/template/annual-report.html',
                    controller: 'AnnualReportController',
                    access: { restricted: true }
                })
                .otherwise({
                    redirectTo: '/'
                });
        });

    global.thundersnow.factory('lodash', function () {
        return _;
    });

    global.thundersnow.run(function ($rootScope, $location, $route, AuthService) {
        $rootScope.$on('$routeChangeStart', function (event, next, current) {
            AuthService.getUserStatus().then(function () {
                if (next.access.restricted && !AuthService.isLoggedIn()) {
                    $location.path('/login');
                    $route.reload();
                }
            });
        });
    });

}(this));
