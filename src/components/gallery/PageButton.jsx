import {setPage} from "@/slices/pageSlice.js";
import {useDispatch} from "react-redux";

export const PageButton = ({page, children, isCurrent = false}) => {
    const dispatch = useDispatch();
    return (
        <li className={`page-item${isCurrent ? ' active' : ''}`}>
            <button type="button" className="page-link" onClick={() => dispatch(setPage(page))}>
                {children || page + 1}
            </button>
        </li>
    );
}