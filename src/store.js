import { configureStore } from "@reduxjs/toolkit";
import {pageReducer} from '@/slices/pageSlice';
import {authReducer} from "@/slices/authSlice";
import {toastReducer} from "@/slices/toastSlice";
import {apiSlice} from "@/api";
import { languageReducer } from "@/slices/languageSlice";

export default configureStore({
    reducer: {
        page: pageReducer,
        auth: authReducer,
        language: languageReducer,
        toast: toastReducer,
        [apiSlice.reducerPath]: apiSlice.reducer
    },
    middleware: getDefaultMiddleware => getDefaultMiddleware().concat(apiSlice.middleware)
})