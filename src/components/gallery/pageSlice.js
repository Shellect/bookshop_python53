import { createSlice } from "@reduxjs/toolkit";

const slice = createSlice({
    name: 'page',
    initialState : {
        value: 0
    },
    reducers: {
        setPage: (state, action) => {
            state.value = action.payload
        }
    }
});

export const {setPage} = slice.actions;
export default slice.reducer;