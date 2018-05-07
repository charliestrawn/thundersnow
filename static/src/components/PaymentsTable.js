import React, { Component } from 'react'

class PaymentsTable extends Component {

    render() {
        const paymentItems = this.props.payments.sort(function(a, b){
            var nameA=a.name.toLowerCase(),
                nameB=b.name.toLowerCase();
            if (nameA < nameB) //sort string ascending
                return -1;
            if (nameA > nameB)
                return 1;
            return 0; //default return value (no sorting)
           }).map(payment => (
            <tr key={payment.id}>
                <td className="text-left">{payment.name}</td>
                <td className="text-right">{payment.checkNumber}</td>
                <td className="text-right">{payment.amount}</td>
                <td></td>
                <td><span className="glyphicon glyphicon-pencil" onClick={() => this.props.editPaymentClick(payment)}></span> </td>
                <td><span className="glyphicon glyphicon-remove"></span> </td>
            </tr>
        ))
        return (
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th className="text-right">Check #</th>
                        <th className="text-right">Amount</th>
                        <th></th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {paymentItems}
                </tbody>
        </table>
        )
    }
}

export default PaymentsTable;
