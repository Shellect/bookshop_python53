import { createSlice } from "@reduxjs/toolkit";

const slice = createSlice({
    name: 'page',
    initialState : {
        value: 0,
        limit: 10,
        total: 500
    },
    reducers: {
        setPage: (state, action) => {
            state.value = action.payload
        },
        setLimit: (state, action) => {
            state.limit = action.payload
        }
    }
});

export const {setPage} = slice.actions;
export const pageReducer =  slice.reducer;