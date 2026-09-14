import {useSelector} from "react-redux";
import {PageButton} from "@/components/gallery/PageButton.jsx";

export default function Pagination() {
    const {value: currentPage, limit, total} = useSelector(state => state.page);

    const maxVisiblePages = 5;
    const startPage = Math.max(0, currentPage - 2);
    const lastPage = Math.floor(total / limit);

    const buttons = Array.from(
        {length: Math.min(lastPage - startPage, maxVisiblePages)},
        (_, index) => <PageButton key={index} page={startPage + index} isCurrent={startPage + index === currentPage}/>
    );
    if (currentPage - 2 > 0) {
        buttons.unshift(<li><button type="button" className="page-link">...</button></li>);
        buttons.unshift(<PageButton page={0}>First</PageButton>);
    }
    if (currentPage + 3 < total / limit) {
        buttons.push(<li><button type="button" className="page-link">...</button></li>);
        buttons.push(<PageButton page={lastPage - 1}>Last</PageButton>);
    }

    return (
        <nav aria-label="Page navigation">
            {total > limit && <ul className="pagination">{buttons}</ul>}
        </nav>
    )
}