import React, { Component } from 'react'


class PaymentForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            name: '',
            checkNumber: '',
            amount: 0.00
        };

        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }

    onChange(e) {
        this.setState({[e.target.name]: e.target.value});
    }

    onSubmit(e) {
        e.preventDefault();

        const payment = {
            name: this.state.name,
            checkNumber: this.state.checkNumber,
            amount: this.state.amount,
            date: this.props.week
        };

        fetch('http://localhost:5000/api/payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payment)
        })
            .then(res => res.json())
            .then(data => this.props.updatePayments(data));
    }

    render() {
        return (
            <div>
                <form id="addForm" name="addForm" onSubmit={this.onSubmit} >
                    <div className="form-group">
                        <label className="control-label">Name</label>
                        <input type="text" className="form-control" name="name" onChange={this.onChange} />
                    </div>
                    <div className="form-group">
                        <label className="control-label">Check Number</label>
                        <input type="text" className="form-control" name="checkNumber" onChange={this.onChange} />
                    </div>
                    <div className="form-group">
                        <label className="control-label">Amount</label>
                        <input type="text" className="form-control" name="amount" onChange={this.onChange} />
                    </div>
                    <div className="form-group">
                        <button type="submit" className="btn btn-primary btn-block">Submit</button>
                    </div>
                </form>
            </div>
        )
    }
}

export default PaymentForm;
