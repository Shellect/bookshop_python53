import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";

const options = (credentials) => ({
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(credentials)
});

const sendRequest = (endpoint, post) => async (credentials, {rejectWithValue}) => {
    try {
        const response = await fetch('/api/auth/' + endpoint, post && options(credentials));
        const data = await response.json();
        return response.ok ? data : rejectWithValue(data);
    } catch (error) {
        return rejectWithValue({detail: error.message});
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
    rejected: (state) => {
        state.isLoading = false;
    }
}

const slice = createSlice({
    name: 'auth',
    initialState: {
        isLoading: false,
        user: null,
        isAuthenticated: false
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
                rejected: (state) => {
                    state.isLoading = false;
                }
            })
    }
});

export const {localLogout} = slice.actions;
export const authReducer = slice.reducer;
