import {createSlice, isAnyOf, isRejectedWithValue} from "@reduxjs/toolkit";
import {apiSlice} from "@/api";

const {me, login, logout, register} = apiSlice.endpoints;

const slice = createSlice({
    name: 'auth',
    initialState: {
        isLoading: false,
        user: null,
        isAuthenticated: false
    },
    extraReducers: (builder) => {
        builder
            .addMatcher(
                isAnyOf(me.matchPending, login.matchPending, register.matchPending),
                state => {
                    state.isLoading = true
                }
            )
            .addMatcher(
                isAnyOf(me.matchFulfilled, login.matchFulfilled, register.matchFulfilled),
                (state, action) => {
                    state.isLoading = false;
                    state.user = action.payload;
                    state.isAuthenticated = true;
                }
            )
            .addMatcher(
                logout.matchFulfilled,
                state => {
                    state.isLoading = false;
                    state.user = null;
                    state.isAuthenticated = false;
                }
            )
            // 401 на любом запросе API значит, что сессии нет
            .addMatcher(
                action => isRejectedWithValue(action) && action.payload?.status === 401,
                state => {
                    state.isLoading = false;
                    state.user = null;
                    state.isAuthenticated = false;
                }
            )
            .addMatcher(
                isAnyOf(me.matchRejected, login.matchRejected, register.matchRejected),
                state => {
                    state.isLoading = false;
                }
            )
    }
});

export const authReducer = slice.reducer;
