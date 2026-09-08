import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";

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
        builder
            .addCase(login.pending, (state) => {
                state.isLoading = true;
                state.error = null
            })
            .addCase(login.fulfilled, (state, action) => {
                state.isLoading = false;
                state.user = action.payload
            })
            .addCase(login.rejected, (state) => {
                state.isLoading = false;
            })
    }
})

export const selectUser = state => state.auth.user;

export const authReducer = slice.reducer;
