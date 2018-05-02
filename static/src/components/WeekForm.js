import React, { Component } from 'react'


class WeekForm extends Component {
    constructor(props) {
        super(props);

        this.onChange = this.onChange.bind(this);
        this.onClick = this.onClick.bind(this);
    }

    onChange(e) {
        this.setState({[e.target.name]: e.target.value});
        this.props.changeWeek(e.target.value);
    }

    onClick(e) {
        e.preventDefault();
        var week = prompt("Please type in the date of the Sunday you'd like to enter payments for using the MM-DD-YYYY format", "4-13-2014");
        fetch('http://localhost:5000/api/weeks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({week: week})
        })
        .then(res => res.json())
        .then(data => {
            this.props.updateWeeks(data);
        });
    }

    render() {
        const weekOptions = this.props.weeks
            .map(week => (
                <option key={week} value={week}>
                    {week}
                </option>
            ));

        return (
            <div>
            <button className="btn btn-default btn-block" onClick={this.onClick}>New Week</button>
            <form id="weekForm" name="weekForm">
                <legend>Add Payment</legend>
                <div className="form-group">
                    <label className="control-label">Week</label>
                    <select className="form-control" name="date" onChange={this.onChange} value={this.props.week} >
                        {weekOptions}
                    </select>
                </div>
            </form>
            </div>
        )
    }
}

export default WeekForm;

