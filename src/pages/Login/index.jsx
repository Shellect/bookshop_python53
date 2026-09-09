import {Link, useNavigate} from "react-router";
import {useState} from "react";
import {useDispatch} from "react-redux";
import {login} from "@/slices/authSlice.js";

export const Login = () => {
    const [loginField, setLogin] = useState('');
    const [passwordField, setPassword] = useState('');
    const [errors, setErrors] = useState({login: '', password: ''})

    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleSubmit = async e => {
        e.preventDefault();

        const isLoginError = loginField.length === 0;
        const isPasswordError = passwordField.length === 0;
        if (isLoginError || isPasswordError) {
            setErrors({
                login: isLoginError ? 'Login field is empty' : '',
                password: isPasswordError ? 'Password field is empty' : ''
            })
            return;
        }
        try {
            const user = await dispatch(login({login: loginField, password: passwordField})).unwrap();
            if(user.username === loginField){
                navigate('/profile');
            }
        } catch (error) {
            setErrors({
                'login': error.detail,
                password: ''
            })
        }
    }

    return (
        <form onSubmit={handleSubmit} className="mt-3 p-3 rounded bg-body-tertiary shadow col-12 col-md-8 offset-md-2 col-lg-6 offset-lg-3">
            <h2 className="text-center mb-3">Login</h2>
            <div className="row mb-3">
                <div className="col-2"><label htmlFor="login"><span className="form-label">Login:</span></label></div>
                <div className="col-10">
                    <input id="login" type="text" className="form-control" name="login" onInput={e => setLogin(e.target.value)}/>
                    <small className="form-text text-danger">{errors.login}</small>
                </div>
            </div>
            <div className="row mb-3">
                <div className="col-2"><label htmlFor="password"><span className="form-label"></span></label>Password:</div>
                <div className="col-10">
                    <input id="password" type="password" className="form-control" name="password" onInput={e => setPassword(e.target.value)}/>
                    <small className="form-text text-danger">{errors.password}</small>
                </div>
            </div>
            <div className="row mb-3 text-right">
                <div className="col-6">
                    <button className="btn btn-primary">Login</button>
                </div>
                <div className="col-6">
                    <span>Don't have an account? <Link to="/registration">Register</Link></span>
                </div>
            </div>
        </form>
    )
}