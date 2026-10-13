import { configureStore } from "@reduxjs/toolkit";
import {pageReducer} from '@/slices/pageSlice';
import {authReducer} from "@/slices/authSlice";
import {apiSlice} from "@/api";

export default configureStore({
    reducer: {
        page: pageReducer,
        auth: authReducer,
        [apiSlice.reducerPath]: apiSlice.reducer
    },
    middleware: getDefaultMiddleware => getDefaultMiddleware().concat(apiSlice.middleware)
})