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
)

const slice = createSlice({
    name: 'auth',
    initialState: {
        user: null,
        isLoading: false
    },
    reducers: {},
    extraReducers: (builder) => {
        builder.addAsyncThunk(login, {
            pending: (state) => {
                state.isLoading = true;
                state.error = null
            },
            fulfilled: (state, action) => {
                state.isLoading = false;
                state.user = action.payload
            },
            rejected: (state) => {
                state.isLoading = false;
            }
        })
    }
})

export const selectUser = state => state.auth.user;

export const authReducer = slice.reducer;
