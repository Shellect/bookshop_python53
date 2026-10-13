import {useEffect, useRef} from "react";
import {useDispatch, useSelector} from "react-redux";
import {hideToast} from "@/slices/toastSlice";

const TOAST_TTL_MS = 5000;

export const Toaster = () => {
    const items = useSelector((state) => state.toast.items);
    const dispatch = useDispatch();
    const timers = useRef(new Map());

    useEffect(() => {
        for (const t of items) {
            if (timers.current.has(t.id)) {
                continue;
            }
            timers.current.set(t.id, setTimeout(() => {
                timers.current.delete(t.id);
                dispatch(hideToast(t.id));
            }, TOAST_TTL_MS));
        }
    }, [items, dispatch]);

    useEffect(() => () => {
        timers.current.forEach(clearTimeout);
    }, []);

    const close = (id) => {
        clearTimeout(timers.current.get(id));
        timers.current.delete(id);
        dispatch(hideToast(id));
    };

    return (
        <div className="toast-container position-fixed top-0 end-0 p-3">
            {items.map((t) => (
                <div key={t.id} className={`toast show align-items-center text-bg-${t.type} border-0`} role="alert">
                    <div className="d-flex">
                        <div className="toast-body">{t.message}</div>
                        <button type="button" className="btn-close btn-close-white me-2 m-auto"
                                onClick={() => close(t.id)}></button>
                    </div>
                </div>
            ))}
        </div>
    );
};
