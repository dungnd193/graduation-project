import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import API from "../../api/api.js";
import axiosInstance from "../../api/axios.js";


export const getAllHistory = createAsyncThunk(
    "historyPrediction/getAll",
    async () => {
        try {
            const response = await axiosInstance.get(API.GET_ALL_HISTORY);
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);
export const getUserHistory = createAsyncThunk(
    "historyPrediction/userHist",
    async (user_id) => {
        try {
            const response = await axiosInstance.get(API.GET_HISTORY_BY_USER+user_id);
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);
export const getHistoryById = createAsyncThunk(
    "historyPrediction/id",
    async (id) => {
        try {
            const response = await axiosInstance.get(API.GET_HISTORY_BY_ID+id);
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);


export const historyPredictionSlice = createSlice({
    name: "historyPrediction",
    initialState: {
        error: false,
        loading: false,
        all_history: [],
        view_hist: {}
    },
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(getAllHistory.pending, (state) => {
                state.loading = true;
            })
            .addCase(getAllHistory.fulfilled, (state, action) => {
                state.loading = false;
                state.all_history = action.payload
            })
            .addCase(getAllHistory.rejected, (state) => {
                state.loading = false;
                state.error = true;
            })
            .addCase(getUserHistory.pending, (state) => {
                state.loading = true;
            })
            .addCase(getUserHistory.fulfilled, (state, action) => {
                state.loading = false;
                state.all_history = action.payload
            })
            .addCase(getUserHistory.rejected, (state) => {
                state.loading = false;
                state.error = true;
            })
            .addCase(getHistoryById.pending, (state) => {
                state.loading = true;
            })
            .addCase(getHistoryById.fulfilled, (state, action) => {
                state.loading = false;
                state.view_hist = action.payload[0]
            })
            .addCase(getHistoryById.rejected, (state) => {
                state.loading = false;
                state.error = true;
            })
    },
});

export default historyPredictionSlice.reducer;
