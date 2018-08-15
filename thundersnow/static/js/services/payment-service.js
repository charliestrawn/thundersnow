(function (app) {
    'use strict';

    app.factory('paymentService', ['$http', function ($http) {
        return {
            getAll: function (year) {
                return $http.get('/api/payment');
            },
            getForYear: function (year) {
                return $http.get('/api/payment?year=' + year);
            },
            getWeeklyPayments: function (week) {
                var encodedWeek = encodeURIComponent(week);
                if (encodedWeek === week) {
                    return $http.get('/api/payment?week=' + week);
                } else {
                    return $http.get('/api/payment?week=' + encodedWeek);
                }
            },
            getForMember: function (member_id) {
                return $http.get('/api/payment?member_id=' + member_id);
            },
            getForMemberAndYear: function (member_id, year) {
                return $http.get('/api/member/' + member_id + '/payments?year=' + year);
            },
            createPayment: function (payment) {
                return $http.post('/api/payment', payment);
            },
            updatePayment: function (payment) {
                return $http.put('/api/payment/' + payment.id, payment);
            },
            deletePayment: function(id) {
                return $http.delete('/api/payment/' + id);
            }
        };
    }]);

}(thundersnow));
