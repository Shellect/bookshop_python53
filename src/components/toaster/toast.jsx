import {hideToast} from "@/slices/toastSlice";
import {useDispatch} from "react-redux";
import {useEffect} from "react";

export const Toast = ({id, type, message}) => {
    const dispatch = useDispatch();
    useEffect(() => {
        const timer = setTimeout(() => {
            dispatch(hideToast(id))
        }, 5000)
        return () => clearTimeout(timer);
    }, [])

    return (
        <div className={`toast show align-items-center text-bg-${type} border-0`} role="alert">
            <div className="d-flex">
                <div className="toast-body">{message}</div>
                <button type="button" className="btn-close btn-close-white me-2 m-auto" onClick={() => dispatch(hideToast(id))}></button>
            </div>
        </div>
    )
}