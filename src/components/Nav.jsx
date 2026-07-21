import { NavLink } from "react-router";

export default function Nav() {
    return (
        <nav className="navbar navbar-expand-lg bg-warning">
            <div className="container-fluid justify-content-between">
                <a className="navbar-brand" href="#">Book Shop</a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse justify-content-end" id="navbarNav">
                    <ul className="navbar-nav">
                        <li className="nav-item">
                            <NavLink
                                to="/"
                                className={({ isActive }) => isActive ? "active nav-link" : "nav-link"}
                            ><i class="bi bi-house"></i> Главная</NavLink>
                        </li>
                        <li className="nav-item">
                            <NavLink
                                to="/profile"
                                className={({ isActive }) => isActive ? "active nav-link" : "nav-link"}
                            ><i class="text-primary bi bi-person-circle"></i> Профиль</NavLink>
                        </li>
                        <li className="nav-item">
                            <NavLink
                                to="/cart"
                                className={({ isActive }) => isActive ? "active nav-link" : "nav-link"}
                            ><i class="bi bi-cart"></i> Корзина</NavLink>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href="#">Выход</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    )
}