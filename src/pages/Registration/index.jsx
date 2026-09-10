import {useState} from "react";
import {useDispatch} from "react-redux";
import {Link, useNavigate} from 'react-router';
import {register} from "@/slices/authSlice.js";

export const Registration = () => {
    const [loginField, setLoginField] = useState('');
    const [emailField, setEmailField] = useState('');
    const [passwordField, setPasswordField] = useState('');
    const [confirmPasswordField, setConfirmPasswordField] = useState('');
    const [errors, setErrors] = useState({login: '', email: '', password: ''});

    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleSubmit = async e => {
        e.preventDefault();

        const loginErrorMessage = loginField.length === 0 ? 'Login field is empty' : '';
        const isEmailErrorMessage = emailField.length === 0 ? 'Email field is empty' : '';
        const isPasswordMessage = passwordField.length === 0 ? 'Password field is empty' : '';
        if (loginErrorMessage || isEmailErrorMessage || isPasswordMessage) {
            setErrors({
                login: loginErrorMessage,
                email: isEmailErrorMessage,
                password: isPasswordMessage
            });
            return;
        }
        try {
            const user = await dispatch(register({
                login: loginField,
                email: emailField,
                password: passwordField,
                confirm_password: confirmPasswordField
            })).unwrap();
            if (user.username === loginField) {
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
        <form onSubmit={handleSubmit}
              className="mt-3 p-3 rounded bg-body-tertiary shadow col-12 col-md-8 offset-md-2 col-lg-6 offset-lg-3">
            <h2 className="text-center mb-3">Registration</h2>
            <div className="row mb-3">
                <div className="col-2"><label htmlFor="username" className="form-label">Login:</label></div>
                <div className="col-10">
                    <input id="username" type="text" className="form-control" name="login"
                           onInput={e => setLoginField(e.target.value)}/>
                    <small className="form-text text-danger">{errors.login}</small>
                </div>
            </div>
            <div className="row mb-3">
                <div className="col-2"><label htmlFor="email" className="form-label"></label>Email:</div>
                <div className="col-10">
                    <input id="email" type="email" className="form-control" name="email"
                           onInput={e => setEmailField(e.target.value)}/>
                    <small className="form-text text-danger">{errors.email}</small>
                </div>
            </div>
            <div className="row mb-3">
                <div className="col-2"><label htmlFor="password" className="form-label"></label>Password:</div>
                <div className="col-10">
                    <input id="password" type="password" className="form-control" name="password"
                           onInput={e => setPasswordField(e.target.value)}/>
                    <small className="form-text text-danger">{errors.password}</small>
                </div>
            </div>
            <div className="row mb-3">
                <div className="col-2"><label htmlFor="confirm-password" className="form-label">Confirm
                    password:</label></div>
                <div className="col-10">
                    <input id="confirm-password" type="password" className="form-control"
                           name="confirm_password"
                           onInput={e => setConfirmPasswordField(e.target.value)}/>
                </div>
            </div>
            <div className="row mb-3 justify-content-end">
                <span>Already have an account? <Link to="/login">Login</Link></span>
            </div>
        </form>
    );
}