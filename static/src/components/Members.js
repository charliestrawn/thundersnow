import React, { Component } from 'react'

class Members extends Component {
    constructor (props) {
        super(props);
        this.state = {
            members: []
        };
    }

    componentWillMount () {
        fetch('http://localhost:5000/api/members')
        .then(res => res.json())
        .then(members => {
                this.setState({members: members});
        });
    }

    render() {
        const membersItems = this.state.members.sort(function(a, b){
            var nameA=a.name.toLowerCase(), nameB=b.name.toLowerCase();
            if (nameA < nameB) return -1;
            if (nameA > nameB) return 1;
            return 0;
           })
           .map(member => (<li key={member.id}>{member.name}</li>));
        return (
            <div className="container">
                <ul>{membersItems}</ul>
            </div>
        )
    }
}

export default Members;
