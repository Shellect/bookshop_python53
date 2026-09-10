import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";

export const register = createAsyncThunk(
    'auth/register',
    async (credentials, {rejectWithValue}) => {
        try {
            const response = await fetch('/api/auth/register', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(credentials)
            });
            if (!response.ok) {
                return rejectWithValue(await response.json());
            }
            return await response.json();
        } catch (error) {
            return rejectWithValue({detail: error.message});
        }
    }
);

export const login = createAsyncThunk(
    'auth/login',
    async (credentials, {rejectWithValue}) => {
        try {
            const response = await fetch('/api/auth/login', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(credentials)
            });
            if (!response.ok) {
                return rejectWithValue(await response.json());
            }
            return await response.json();
        } catch (error) {
            return rejectWithValue({detail: error.message});
        }
    }
);

export const checkAuth = createAsyncThunk(
    'auth/check',
    async (_, {rejectWithValue}) => {
        try {
            const response = await fetch('/api/auth/me');
            if (!response.ok) {
                return rejectWithValue(null);
            }
            return await response.json();
        } catch (error) {
            return rejectWithValue({detail: error.message});
        }
    }
);

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
        state.user = null;
        state.isAuthenticated = false;
    }
}

const slice = createSlice({
    name: 'auth',
    initialState: {
        isLoading: false,
        user: null,
        isAuthenticated: false
    },
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addAsyncThunk(login, reducers)
            .addAsyncThunk(register, reducers)
            .addAsyncThunk(checkAuth, reducers)
    }
});

export const authReducer = slice.reducer;
