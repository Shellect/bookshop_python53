import React from "react";
import {Route, Routes} from "react-router";
import {connect} from "react-redux";
import {BookCard, OrderForm, Nav} from "@/components";
import {Profile, Registration, BookGallery, Login} from "@/pages";
import {checkAuth} from "@/slices/authSlice.js";

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
        this.props.checkAuth();
    }

    componentDidUpdate(prevProps) {
        if (prevProps.page !== this.props.page) {
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
        this.setState({bookName, quantity: this.state.quantity + 1});
    }

    render() {
        return (
            <>
                <Nav/>
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
                                }/>
                                <Route path="/profile" element={<Profile/>}/>
                                <Route path="/cart" element={
                                    <OrderForm bookName={this.state.bookName} quantity={this.state.quantity}/>
                                }/>
                                <Route path="/registration" element={<Registration/>}/>
                                <Route path="/login" element={<Login/>}/>
                            </Routes>
                        </div>
                    </div>
                </div>
            </>
        )
    }
}

const mapStateToProps = (state) => ({page: state.page.value});
const mapDispatchToProps = (dispatch) => ({checkAuth: () => dispatch(checkAuth())});

export default connect(mapStateToProps, mapDispatchToProps)(App);