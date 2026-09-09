import { configureStore } from "@reduxjs/toolkit";
import {pageReducer} from '@/slices/pageSlice';
import {authReducer} from "@/slices/authSlice";

export default configureStore({
    reducer: {
        page: pageReducer,
        auth: authReducer
    }
})