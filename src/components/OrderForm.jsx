import React from "react";

export class OrderForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "John Psina",
        }
    }

    usernameChange(e) {
        this.setState({ username: e.target.value });
    }

    render() {
        return (
            <form action="" className="border rounded p-3" style={{ minHeight: "36rem" }}>
                <div className="row mt-3">
                    <div className="col-4">
                        <label htmlFor="bookName" className="form-label">Book:</label>
                    </div>
                    <div className="col-8">
                        <input id="bookName" type="text" className="form-control" value={this.props.bookName} disabled/>
                    </div>
                </div>
                <div className="row mt-3">
                    <div className="col-4"><label htmlFor="bookQuantity" className="form-label">Quantity:</label></div>
                    <div className="col-8">
                        <input id="bookQuantity" type="text" className="form-control" value={this.props.quantity}/>
                        </div>
                </div>
                <div className="row mt-3">
                    <div className="col-4"><label htmlFor="userName" className="form-label">Name</label></div>
                    <div className="col-8">
                        <input
                            id="userName"
                            type="text"
                            className="form-control"
                            value={this.state.username}
                            onInput={e => this.usernameChange(e)}
                        />
                    </div>
                </div>
                <div className="row mt-3">
                    <div className="col-4"><label htmlFor="userAddress" className="form-label">Delivery address:</label></div>
                    <div className="col-8"><textarea className="form-control" id="userAddress"></textarea></div>
                </div>
                <div className="d-grid mt-3"><button className="btn btn-warning">Оформить заказ</button></div>
            </form>
        )
    }

}