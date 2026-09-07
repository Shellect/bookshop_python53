import {Link} from 'react-router';

export const Registration = () => {
    return (
        <form action="" className="mt-3 p-3 rounded bg-body-tertiary shadow col-12 col-md-8 offset-md-2 col-lg-6 offset-lg-3">
            <h2 className="text-center mb-3">Registration</h2>
            <div className="row mb-3">
                <div className="col-2"><label htmlFor="username" className="form-label">Login:</label></div>
                <div className="col-10"><input id="username" type="text" className="form-control" name="login"/></div>
            </div>
            <div className="row mb-3">
                <div className="col-2"><label htmlFor="email" className="form-label"></label>Email:</div>
                <div className="col-10"><input id="email" type="email" className="form-control" name="email"/></div>
            </div>
            <div className="row mb-3">
                <div className="col-2"><label htmlFor="password" className="form-label"></label>Password:</div>
                <div className="col-10"><input id="password" type="password" className="form-control" name="password"/></div>
            </div>
            <div className="row mb-3">
                <div className="col-2"><label htmlFor="confirm-password" className="form-label">Confirm password:</label></div>
                <div className="col-10"><input id="confirm-password" type="password" className="form-control" name="confirm_password"/></div>
            </div>
            <div className="row mb-3 justify-content-end">
                <span>Already have an account? <Link to="/login" >Login</Link></span>
            </div>
        </form>
    );
}