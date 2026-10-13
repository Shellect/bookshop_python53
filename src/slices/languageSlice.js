import i18n from "@/i18n";
import { createSlice } from "@reduxjs/toolkit";

const slice = createSlice({
    name: 'language',
    initialState: {
        value: 'ru'
    },
    reducers: {
        setLang(state, action){
            state.value = action.payload;
            i18n.changeLanguage(action.payload);
        }
    }
});


export const {setLang} = slice.actions;
export const languageReducer = slice.reducer;