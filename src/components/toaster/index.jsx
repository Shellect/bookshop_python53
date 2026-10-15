import {useSelector} from "react-redux";
import {Toast} from "@/components/toaster/toast.jsx";

export const Toaster = () => {
    const items = useSelector((state) => state.toast.items);

    return (
        <div className="toast-container position-fixed top-0 end-0 p-3">
            {items.map(({id, type, message}) => <Toast key={id} id={id} type={type} message={message} />)}
        </div>
    );
};
