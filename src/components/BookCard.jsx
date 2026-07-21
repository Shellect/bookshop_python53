import { useState } from "react";
import styles from "./BookCard.module.css";

export default function BookCard({ title, author, poster, price, setBookName }) {
    return (
        <div className={"card p-3 " + styles.bookCard} >
            <img src={poster} alt="..." className="card-img-top" />
            <div className="card-body">
                <h5 className="card-text">{title}</h5>
                <p className="card-text">
                    <small className="text-body-secondary">{author}</small>
                </p>
                <p className="card-text">{price}</p>
            </div>
            <div className="d-grid">
                <button
                    type="button"
                    className="btn btn-warning"
                    onClick={() => setBookName(title)}>В корзину</button>
            </div>
        </div>
    );

}