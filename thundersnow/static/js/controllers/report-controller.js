(function (app) {

    app.controller('ReportController', ['$scope', '$routeParams', 'paymentService', function ($scope, $routeParams, paymentService) {

        $scope.week = $routeParams.week;

        paymentService.getWeeklyPayments($scope.week).success(function (payments) {
            $scope.payments = payments;
            var sum = 0;
            var i = 0;
            for (i; i < payments.length; i++) {
                sum += payments[i].amount;
                if (!payments[i].checkNumber)
                    payments[i].checkNumber = "CASH";
            }

            $scope.total = sum.toFixed(2);
        });
    }]);

}(thundersnow));
