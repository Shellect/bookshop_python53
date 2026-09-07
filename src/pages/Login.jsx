import {Link} from "react-router";

export const Login = () => {
    return (
        <form action="" className="mt-3 p-3 rounded bg-body-tertiary shadow col-12 col-md-8 offset-md-2 col-lg-6 offset-lg-3">
            <h2 className="text-center mb-3">Login</h2>
            <div className="row mb-3">
                <div className="col-2"><label htmlFor="login"><span className="form-label">Login:</span></label></div>
                <div className="col-10"><input id="login" type="text" className="form-control" name="login"/></div>
            </div>
            <div className="row mb-3">
                <div className="col-2"><label htmlFor="password"><span className="form-label"></span></label>Password:</div>
                <div className="col-10"><input id="password" type="password" className="form-control" name="password"/></div>
            </div>
            <div className="row mb-3 text-right">
                <span>Don't have an account? <Link to="/registration">Register</Link></span>
            </div>
        </form>
    )
}