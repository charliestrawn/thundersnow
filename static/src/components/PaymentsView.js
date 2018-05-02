import React, { Component } from 'react';

import WeekForm from './WeekForm';
import PaymentForm from './PaymentForm';
import PaymentsTable from './PaymentsTable';


class PaymentsView extends Component {

    constructor(props) {
        super(props);
        this.state = {
            weeks: [],
            payments: []
        };
        this.changeWeek = this.changeWeek.bind(this);
        this.updatePayments = this.updatePayments.bind(this);
        this.updateWeeks = this.updateWeeks.bind(this);
    }

    componentWillMount () {
        this.initialize();
    }

    initialize () {
        fetch('http://localhost:5000/api/weeks?year=2017')
        .then(res => res.json())
        .then(
            weeksData => {
                const sortedWeeks = this.sortWeeks(weeksData);
                this.setState({weeks: sortedWeeks, week: sortedWeeks[0]});
                this.fetchPayments(this.state.week);
            });
    }

    fetchPayments (week) {
        fetch('http://localhost:5000/api/payment?week=' + week)
            .then(res => res.json())
            .then(paymentData => this.setState({payments: paymentData}))
    }

    changeWeek (week) {
        this.setState({week: week})
        this.fetchPayments(this.state.week);
    }

    updatePayments (payment) {
        this.setState({payments: [...this.state.payments, payment]})
    }

    updateWeeks(week) {
        this.setState({weeks: this.sortWeeks([...this.state.weeks, week])});
        this.changeWeek(week)
    }

    sortWeeks(weeks) {
        return weeks.sort(function(a, b){
            var monthA = parseInt(a.split('-')[0], 10);
            var monthB = parseInt(b.split('-')[0], 10);
            if (monthB < monthA) //sort string ascending
                return -1;
            if (monthB > monthA)
                return 1;
            return 0; //default return value (no sorting)
        });
    }

    render() {
        return (
            <div className="container">
            <div className="row">
            </div>
            <div className="row">
            <div className="col-sm-4">
                <WeekForm week={this.state.week} weeks={this.state.weeks} changeWeek={this.changeWeek} updateWeeks={this.updateWeeks} />
                <PaymentForm week={this.state.week} updatePayments={this.updatePayments}/>
            </div>
            <div className="col-sm-8">
                <h3>Payments for the week of {this.state.week}</h3>
                <PaymentsTable payments={this.state.payments} />
            </div>
            </div>
        </div>
        );
    }
}

export default PaymentsView;
