import { setLang } from "@/slices/languageSlice";
import { useSelector, useDispatch } from "react-redux"

export const LangSwitcher = () => {
    const currentLang = useSelector(store => store.language.value);
    const dispatch = useDispatch();
    const nextLang = currentLang == 'ru' ? 'en' : 'ru';
    const checked = currentLang == 'ru';

    return (
        <div className="form-check form-switch">
            <input
                type="checkbox"
                className="form-check-input"
                id="lang-switch"
                onClick={() => dispatch(setLang(nextLang))}
                checked={checked} />
            <label className="form-check-label" htmlFor="lang-switch">{currentLang}</label>
        </div>
    );
}