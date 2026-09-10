import {Link, NavLink} from "react-router";
import {useSelector} from "react-redux";

const setActive = ({isActive}) => isActive ? "active nav-link" : "nav-link";

export default function Nav() {
    const {isAuthenticated, user} = useSelector((state) => state.auth);

    return (
        <nav className="navbar navbar-expand-lg bg-warning">
            <div className="container-fluid justify-content-between">
                <Link to="/" className="navbar-brand">Book Shop</Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse justify-content-end" id="navbarNav">
                    <ul className="navbar-nav">
                        <li className="nav-item">
                            <NavLink to="/" className={setActive}><i className="bi bi-house"></i> Главная</NavLink>
                        </li>
                        {isAuthenticated ? (
                            <>
                                <li className="nav-item">
                                    <NavLink to="/profile" className={setActive}><i
                                        className="text-primary bi bi-person-circle"></i> {user.username}</NavLink>
                                </li>
                                <li className="nav-item">
                                    <NavLink to="/cart" className={setActive}><i
                                        className="bi bi-cart"></i> Корзина</NavLink>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href="#">Выход</a>
                                </li>
                            </>
                        ) : (
                            <>
                                <li className="nav-item">
                                    <NavLink to="/login" className={setActive}>Войти</NavLink>
                                </li>
                                <li className="nav-item">
                                    <NavLink to="/register" className={setActive}>Зарегистрироваться</NavLink>
                                </li>
                            </>
                        )}
                    </ul>
                </div>
            </div>
        </nav>
    )
}