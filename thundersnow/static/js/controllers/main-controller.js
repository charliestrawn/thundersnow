(function (app) {

    app.controller('MainController', ['$scope', '$location', 'paymentService', 'dateService', 'memberService', 'AuthService', function ($scope, $location, paymentService, dateService, memberService, AuthService) {

        $scope.isAdmin = function() {
            return AuthService.isAdmin();
        };

        $scope.loadPayments = function loadPayments(year) {
            if (typeof year != 'undefined') {
                dateService.getWeeks(year).success(function (weeks) {
                    $scope.weeks = weeks;
                    $scope.week = weeks[0];
                    $scope.getWeeklyPayments($scope.week);
                });
            } else {
                dateService.getWeeks(2017).success(function (weeks) {
                    $scope.weeks = _.map(weeks, function(week) {
                        return week.month + '-' + week.day + '-' + week.year;
                    });
                    $scope.week = $scope.weeks[0];
                    $scope.getWeeklyPayments($scope.week);
                });
            }
        };

        // onLoad call load payments with undefined, server will default to
        // current year.  Probably a better way to do this.
        $scope.loadPayments();

        memberService.getAll().success(function (members) {
            $scope.names = _.map(members, 'name');
        });

        $scope.newWeek = function () {
            var week = prompt("Please type in the date of the Sunday you'd like to enter payments for using the MM-DD-YYYY format", "4-13-2014");
            dateService.createWeek({'week': week}).success(function (week) {
                $scope.week = week;
                $scope.weeks.unshift(week);
                $scope.payments = [];
            });
        };

        $scope.getWeeklyPayments = function (week) {
            if (typeof week != 'undefined') {
                $scope.week = week;
                paymentService.getWeeklyPayments($scope.week).success(function (payments) {
                    $scope.payments = payments;
                });
            }
        };

        $scope.createPayment = function (payment) {
            payment.date = $scope.week;

            if ($scope.shouldUpdate) {
                paymentService.updatePayment(payment).success(function (data) {
                    $scope.shouldUpdate = false;
                });
            } else {
                paymentService.createPayment(payment).success(function (payment) {
                    $scope.payments.push(payment);
                });
            }

            if ($scope.names.indexOf(payment.name) === -1)
                $scope.names.push(payment.name);

            $scope.payment = '';
            $scope.addForm.$setPristine();
        };

        $scope.populateUpdateForm = function (payment) {
            $scope.payment = payment;
            $scope.shouldUpdate = true;
        };

        $scope.del = function (payment) {
            if (confirm("Are you sure you want to delete")) {
                paymentService.deletePayment(payment.id).success(function () {
                    var index = $scope.payments.indexOf(payment);
                    $scope.payments.splice(index, 1);
                });
            }
        };

        $scope.logout = function() {
           AuthService.logout().then(function () {
               $location.path('/login');
           });
        };
    }]);

    app.filter('encodeURIComponent', function() {
        return window.encodeURIComponent;
    });

}(thundersnow));
