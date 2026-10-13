import {createSlice} from "@reduxjs/toolkit";

let nextId = 1;

const slice = createSlice({
    name: "toast",
    initialState: {items: []},
    reducers: {
        showToast: {
            reducer(state, action) {
                state.items.push(action.payload);
            },
            prepare: (type, message) => ({
                payload: {id: nextId++, type, message},
            }),
        },
        hideToast(state, action) {
            state.items = state.items.filter((t) => t.id !== action.payload);
        },
    },
});

export const {showToast, hideToast} = slice.actions;
export const toastReducer = slice.reducer;
