import React from "react";
import {BookGallery , BookCard} from "./components/gallery";
import { OrderForm as OrderForm } from "./components/OrderForm";
import Nav from "./components/Nav";
import { Route, Routes } from "react-router";
import {Profile} from "./components/Profile";
import { connect } from "react-redux";

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            books: [],
            bookName: '',
            quantity: 0
        }
        this.setBookName = this.setBookName.bind(this);
    }

    componentDidMount() {
        this.loadBooks();
    }

    componentDidUpdate(prevProps) {
        if(prevProps.page !== this.props.page) {
            this.loadBooks();
        }
    }

    async loadBooks() {
        const response = await fetch('/api/books?' + new URLSearchParams({page: this.props.page}).toString());
        if (!response.ok) {
            console.log("Network error");
            return;
        }
        const data = await response.json();
        this.setState({books: data});
    }

    setBookName(bookName) {
        this.setState({ bookName, quantity: this.state.quantity + 1 });
    }

    render() {
        return (
            <>
                <Nav />
                <div className="container">
                    <div className="row mt-3">
                        <div className="col-12">
                            <Routes>
                                <Route path="/" element={
                                    <BookGallery>
                                        {this.state.books.map((book, i) => <BookCard
                                            key={i}
                                            title={book.title}
                                            author={book.author}
                                            poster={book.poster}
                                            price={book.price}
                                            setBookName={this.setBookName}
                                        />)}
                                    </BookGallery>
                                } />
                                <Route path="/profile" element={
                                    <Profile />
                                } />
                                <Route path="/cart" element={
                                    <OrderForm bookName={this.state.bookName} quantity={this.state.quantity} />
                                } />
                            </Routes>
                        </div>
                    </div>
                </div>
            </>
        )
    }
}

function mapStateToProps(state) {
    return {
        page: state.page.value
    }
}

export default connect(mapStateToProps)(App);