import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { toast } from 'react-toastify';
import API from "../../api/api.js";
import axiosInstance from "../../api/axios.js";

export const predictImage = createAsyncThunk(
    "predictImage/predict",
    async ({ formData, user_id, classification_model_id, localization_model_id }) => {
        try {
            const response = await axiosInstance.post(API.PREDICT_IMAGE, formData, {
                params: { user_id, classification_model_id, localization_model_id },
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);


export const predictImageSlice = createSlice({
    name: "predictImage",
    initialState: {
        error: false,
        loading: false,
        result: {
            message: '',
            file_path: '',
            mask_path: '',
            label: '',
            classification_accuracy: 0,
            localization_accuracy: 0,
        }
    },
    reducers: {
        resetResult: (state) => {
            state.result = {
                message: '',
                file_path: '',
                mask_path: '',
                label: '',
                accuracy: 0
            };
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(predictImage.pending, (state) => {
                state.loading = true;
            })
            .addCase(predictImage.fulfilled, (state, action) => {
                state.loading = false;
                console.log(action.payload)
                state.result = action.payload
                toast.success("Predicted successfully!", {
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
            .addCase(predictImage.rejected, (state) => {
                state.loading = false;
                state.error = true;
                toast.error("Predicted error!", {
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
    },
});

export const { resetResult } = predictImageSlice.actions;
export default predictImageSlice.reducer;
