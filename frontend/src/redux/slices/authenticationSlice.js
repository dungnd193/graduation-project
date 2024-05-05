import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { toast } from 'react-toastify';
import API from "../../api/api"
import axiosInstance, { getAccessToken, removeAccessToken, setAccessToken } from "../../api/axios.js";


export const signInThunk = createAsyncThunk(
    "auth/login",
    async ({ username, password }) => {
        try {
            const response = await axiosInstance.post(API.LOGIN, {
                username,
                password
            });
            return response.data;
        } catch (err) {
            throw new Error(err.response.data.detail)
        }
    }
);

export const signUpThunk = createAsyncThunk(
    "auth/signup",
    async ({
        username,
        password,
        email,
        phoneNumber,
    }) => {
        try {
            const response = await axiosInstance.post(API.SIGN_UP, {
                username,
                password,
                email,
                phone_number: phoneNumber,
                status: "ACTIVE",
                role_id: 2
            });
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);


export const authenticationSlice = createSlice({
    name: "authenticationSlice",
    initialState: {
        accessToken: getAccessToken(),
        error: false,
        loading: false,
        user: {
            email: "",
            id: 0,
            phone_number: "",
            role_id: 0,
            status: "",
            userName: "",
        },
    },
    reducers: {
        logout: (state) => {
            state.accessToken = "";
            removeAccessToken();
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(signInThunk.pending, (state) => {
                state.loading = true;
            })
            .addCase(signInThunk.fulfilled, (state, action) => {
                state.loading = false;
                state.accessToken = action.payload['access_token'];
                state.user = action.payload.user
                setAccessToken(state.accessToken);
                toast.success('Sign in successfully!', {
                    position: "bottom-right",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: false,
                    draggable: true,
                    progress: undefined,
                    theme: "light",
                });
            })
            .addCase(signInThunk.rejected, (state, action) => {
                state.loading = false;
                state.error = true;
                toast.error(action.error.message || 'Something wrong! Please try again!', {
                    position: "bottom-right",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: false,
                    draggable: true,
                    progress: undefined,
                    theme: "light",
                });
            });
        builder
            .addCase(signUpThunk.pending, (state) => {
                state.loading = true;
            })
            .addCase(signUpThunk.fulfilled, (state, action) => {
                state.loading = false;
                toast.success('Sign up account successfully!', {
                    position: "bottom-right",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: false,
                    draggable: true,
                    progress: undefined,
                    theme: "light",
                });
            })
            .addCase(signUpThunk.rejected, (state, action) => {
                state.loading = false;
                state.error = true;
                toast.error('Something wrong! Please try again!', {
                    position: "bottom-right",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: false,
                    draggable: true,
                    progress: undefined,
                    theme: "light",
                });
            });
    },
});

export const { logout } = authenticationSlice.actions;
export default authenticationSlice.reducer;
