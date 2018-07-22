(function (app) {

    app.controller('MemberController', ['$scope', '$routeParams', 'memberService', function ($scope, $routeParams, memberService) {

        memberService.getAll(true).success(function (members) {
            $scope.members = members;
        });

        $scope.loadMember = function (id) {
            $scope.member = $scope.members[id];
            //memberService.getById(id).success(function (member) {
              //  $scope.member = member;
                // Maybe fetch payments for member here?
            //}
        }

        $scope.del = function (member) {
            if (confirm("Are you sure you want to delete")) {
                memberService.delete(member.id).success(function () {
                    var index = $scope.members.indexOf(member);
                    $scope.members.splice(index, 1);
                });
            }
        };

        $scope.fixMember = function (member) {
            var newId = prompt("Enter new member id");

            if (!isNaN(parseInt(newId))) {
                memberService.fixMember(member.id, newId).success(function () {
                    var index = $scope.members.indexOf(member);
                    $scope.members.splice(index, 1);
                });
            }
        }

    }]);

} (thundersnow));
