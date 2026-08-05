import { configureStore } from "@reduxjs/toolkit";
import {pageReducer} from './components/gallery';

export default configureStore({
    reducer: {
        page: pageReducer
    }
})