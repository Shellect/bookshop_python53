import { configureStore } from "@reduxjs/toolkit";
import {pageReducer} from './components/gallery';
import {authReducer} from "./slices/authSlice.js";

export default configureStore({
    reducer: {
        page: pageReducer,
        auth: authReducer
    }
})