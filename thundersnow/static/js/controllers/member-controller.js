(function (app) {

    app.controller('MemberController', ['$scope', '$routeParams', 'memberService', function ($scope, $routeParams, memberService) {

        memberService.getAll().success(function (members) {
            $scope.members = members;
        });

        $scope.loadMember = function (id) {
            $scope.member = $scope.members[id];
            //memberService.getById(id).success(function (member) {
              //  $scope.member = member;
                // Maybe fetch payments for member here?
            //}
        }

    }]);

}(thundersnow));
