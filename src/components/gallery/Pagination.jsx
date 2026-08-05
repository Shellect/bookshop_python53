import { useDispatch } from "react-redux";
import { setPage } from "./pageSlice";
import { useState } from "react";

export default function Pagination() {
    const [currentPage, setCurrentPage] = useState(2);
    const dispatch = useDispatch();

    return (
        <nav aria-label="Page navigation">
            <ul className="pagination">
                <li className="page-item"><button type="button" className="page-link" onClick={() => dispatch(setPage(1))}>Previous</button></li>
                <li className="page-item"><button type="button" className="page-link" onClick={() => dispatch(setPage(1))}>1</button></li>
                <li className="page-item"><button type="button" className="page-link" onClick={() => dispatch(setPage(2))}>2</button></li>
                <li className="page-item"><button type="button" className="page-link" onClick={() => dispatch(setPage(3))}>3</button></li>
                <li className="page-item"><button type="button" className="page-link" onClick={() => dispatch(setPage(3))}>Next</button></li>
            </ul>
        </nav>
    )
}