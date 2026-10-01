import { configureStore } from "@reduxjs/toolkit";
import {pageReducer} from '@/slices/pageSlice';
import {authReducer} from "@/slices/authSlice";
import { languageReducer } from "@/slices/languageSlice";

export default configureStore({
    reducer: {
        page: pageReducer,
        auth: authReducer,
        language: languageReducer
    }
})