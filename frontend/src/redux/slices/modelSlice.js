import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { toast } from 'react-toastify';
import API from "../../api/api.js";
import axiosInstance from "../../api/axios.js";


export const getAllModels = createAsyncThunk(
    "model/getAll",
    async () => {
        try {
            const response = await axiosInstance.get(API.GET_ALL_MODELS);
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);

export const createModel = createAsyncThunk(
    "model/create",
    async ({
        name,
        accuracy,
        precision,
        recall,
        f1_score,
        path,
        version,
        model_type
    }) => {
        try {
            const response = await axiosInstance.post(API.CREATE_MODELS, {
                name,
                accuracy,
                precision,
                recall,
                f1_score,
                path,
                version,
                model_type
            });
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);

export const searchModel = createAsyncThunk(
    "model/search",
    async (name) => {
        try {
            const response = await axiosInstance.get(API.SEARCH_MODEL+"?name="+name);
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);

export const updateModel = createAsyncThunk(
    "model/update",
    async (model) => {
        try {
            const response = await axiosInstance.put(API.UPDATE_MODEL+ model.id, model);
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);

export const deleteModel = createAsyncThunk(
    "model/delete",
    async ({ model_id }) => {
        try {
            const response = await axiosInstance.delete(API.UPDATE_MODEL+model_id);
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);



export const modelSlice = createSlice({
    name: "modelSlice",
    initialState: {
        error: false,
        loading: false,
        all_models: []
    },
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(getAllModels.pending, (state) => {
                state.loading = true;
            })
            .addCase(getAllModels.fulfilled, (state, action) => {
                state.loading = false;
                state.all_models = action.payload
            })
            .addCase(getAllModels.rejected, (state) => {
                state.loading = false;
                state.error = true;
            })
            .addCase(searchModel.pending, (state) => {
                state.loading = true;
            })
            .addCase(searchModel.fulfilled, (state, action) => {
                state.loading = false;
                state.all_models = action.payload
            })
            .addCase(searchModel.rejected, (state) => {
                state.loading = false;
                state.error = true;
            })
            .addCase(createModel.pending, (state) => {
                state.loading = true;
            })
            .addCase(createModel.fulfilled, (state) => {
                state.loading = false;
                toast.success("Create model successfully!", {
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
            .addCase(createModel.rejected, (state) => {
                state.loading = false;
                state.error = true;
                toast.error("Create model error!", {
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
            .addCase(updateModel.pending, (state) => {
                state.loading = true;
            })
            .addCase(updateModel.fulfilled, (state) => {
                state.loading = false;
                toast.success("Update model successfully!", {
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
            .addCase(updateModel.rejected, (state) => {
                state.loading = false;
                state.error = true;
                toast.error("Update model error!", {
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
            .addCase(deleteModel.pending, (state) => {
                state.loading = true;
            })
            .addCase(deleteModel.fulfilled, (state) => {
                state.loading = false;
                toast.success("Delete model successfully!", {
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
            .addCase(deleteModel.rejected, (state) => {
                state.loading = false;
                state.error = true;
                toast.error("Delete model error!", {
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

export default modelSlice.reducer;
