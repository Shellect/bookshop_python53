import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {errorFromException, errorFromResponse} from "@/utils/authErrors.js";

const REQUEST_TIMEOUT_MS = 15_000;

const options = (credentials) => ({
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(credentials)
});

const sendRequest = (endpoint, post) => async (credentials, {rejectWithValue}) => {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
    try {
        const response = await fetch("/api/auth/" + endpoint, {
            ...(post ? options(credentials) : {}),
            signal: controller.signal,
        });
        if (response.ok) {
            if (response.status === 204) {
                return null;
            }
            const text = await response.text();
            return text ? JSON.parse(text) : null;
        }
        return rejectWithValue(await errorFromResponse(response));
    } catch (error) {
        return rejectWithValue(errorFromException(error));
    } finally {
        clearTimeout(timer);
    }
}

export const register = createAsyncThunk('auth/register', sendRequest('register', true));
export const login = createAsyncThunk('auth/login', sendRequest('login', true));
export const logout = createAsyncThunk('auth/logout', sendRequest('logout', true));
export const checkAuth = createAsyncThunk('auth/check', sendRequest('me'));

const reducers = {
    pending: (state) => {
        state.isLoading = true;
        state.error = null
    },
    fulfilled: (state, action) => {
        state.isLoading = false;
        state.user = action.payload;
        state.isAuthenticated = true;
    },
    rejected: (state, action) => {
        state.isLoading = false;
        state.error = action.payload ?? null;
    }
}

const slice = createSlice({
    name: 'auth',
    initialState: {
        isLoading: false,
        user: null,
        isAuthenticated: false,
        error: null,
    },
    reducers: {
        localLogout(state) {
            state.user = null;
            state.isAuthenticated = false;
        }
    },
    extraReducers: (builder) => {
        builder
            .addAsyncThunk(login, reducers)
            .addAsyncThunk(register, reducers)
            .addAsyncThunk(checkAuth, reducers)
            .addAsyncThunk(logout, {
                pending: (state) => {
                    state.isLoading = true;
                    state.error = null
                },
                fulfilled: (state) => {
                    state.isLoading = false;
                    state.user = null;
                    state.isAuthenticated = false;
                },
                rejected: (state, action) => {
                    state.isLoading = false;
                    state.error = action.payload ?? null;
                }
            })
    }
});

export const {localLogout} = slice.actions;
export const authReducer = slice.reducer;
