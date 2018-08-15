(function (app) {

    app.controller('MemberController', ['$scope', '$routeParams', 'memberService', 'paymentService', function ($scope, $routeParams, memberService, paymentService) {

        if ($routeParams.id) {
            $scope.payments = [];
            memberService.getById($routeParams.id).success(function (member) {
                $scope.member = member;
                paymentService.getForMember($scope.member.id).success(function (payments) {
                    $scope.payments = payments;
                });
            });
        } else {
            memberService.getAll(true).success(function (members) {
                $scope.members = members;
            });
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
            var newId = prompt("Enter new member id", member.id);

            if (!isNaN(parseInt(newId))) {
                memberService.update(member.id, {'id': newId}).success(function () {
                    var index = $scope.members.indexOf(member);
                    $scope.members.splice(index, 1);
                });
            }
        };

        $scope.updateMember = function (member) {
            var newName = prompt("Enter a new name", member.name);
            memberService.update(member.id, {'name': newName}).success(function () {
            });
        }

    }]);

} (thundersnow));
