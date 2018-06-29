(function (app) {

    function controller($scope, $routeParams, reportService, _) {

		$scope.loading = true;
        $scope.year = $routeParams.year;

        var monthNames = [
            "Jan", "Feb", "Mar",
            "Apr", "May", "June",
            "July", "Aug", "Sept",
            "Oct", "Nov", "Dec"
        ];

        reportService.getForYear($scope.year).success(function (grouped) {

			$scope.grouped = _.sortBy(grouped, 'name');

			_.forEach($scope.grouped, function(g) {
				_.forEach(g.payments, function(p) {
					var d = p.date.split('-');
					p.date = new Date(d[2], d[0] - 1, d[1]);
				});
			});

			$scope.loading = false;
        });

        $scope.formatDate = function(date) {
            return monthNames[date.getMonth()] + ' ' + date.getDate();
        };

	}

    app.controller(
        'AnnualReportController',
        ['$scope', '$routeParams', 'reportService', 'lodash', controller]
    );

})(thundersnow);
