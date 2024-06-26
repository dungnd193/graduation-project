import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { toast } from 'react-toastify';
import API from "../../api/api.js";
import axiosInstance, { removeAccessToken } from "../../api/axios.js";


export const getUserInformation = createAsyncThunk(
    "userInfor/get",
    async () => {
        try {
            const response = await axiosInstance.get(API.USER_INFO);
            return response.data;
        } catch (err) {
            throw new Error(err.response.data.detail)
        }
    }
);

export const updateUserInformation = createAsyncThunk(
    "userInfor/update",
    async (user) => {
        try {
            const response = await axiosInstance.put(API.UPDATE_USER_INFO + user.id, user);
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);

export const getAllUsers = createAsyncThunk(
    "users/getAll",
    async () => {
        try {
            const response = await axiosInstance.get(API.GET_ALL_USER);
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);

export const searchUsers = createAsyncThunk(
    "users/search",
    async (search) => {
        try {
            const response = await axiosInstance.get(API.SEARCH_USER + "?search_string=" + search);
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);

export const updateUserStatus = createAsyncThunk(
    "userInfor/update/status",
    async ({ user_id, stt }) => {
        try {
            const body = { status: stt }
            const response = await axiosInstance.put(API.UPDATE_USER_STATUS + user_id + "/status", body);
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);
export const deleteUser = createAsyncThunk(
    "userInfor/update/status",
    async ({ user_id }) => {
        try {
            const response = await axiosInstance.delete(API.DELETE_USER + user_id);
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);

export const getAllRoles = createAsyncThunk(
    "roles/getAll",
    async () => {
        try {
            const response = await axiosInstance.get(API.GET_ALL_ROLES);
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);

export const createRole = createAsyncThunk(
    "role/create",
    async ({ role }) => {
        try {
            const response = await axiosInstance.post(API.CREATE_ROLE, { role });
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);

export const createGroup = createAsyncThunk(
    "group/create",
    async ({ group }) => {
        try {
            const response = await axiosInstance.post(API.CREATE_GROUP, { group });
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);



export const getAllGroups = createAsyncThunk(
    "groups/getAll",
    async () => {
        try {
            const response = await axiosInstance.get(API.GET_ALL_GROUPS);
            return response.data;
        } catch (err) {
            throw new Error(err)
        }
    }
);

export const userInformationSlice = createSlice({
    name: "userInfoSlice",
    initialState: {
        error: false,
        redirectToSignIn: false,
        loading: false,
        user: {
            email: "",
            id: 0,
            phone_number: "",
            role_id: 0,
            status: "",
            userName: "",
        },
        all_users: [],
        all_roles: [],
        all_groups: [],
    },
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(getUserInformation.pending, (state) => {
                state.loading = true;
            })
            .addCase(getUserInformation.fulfilled, (state, action) => {
                state.loading = false;
                state.redirectToSignIn = false;
                state.user = action.payload.user;
            })
            .addCase(getUserInformation.rejected, (state, action) => {
                state.loading = false;
                state.error = true;
                state.redirectToSignIn = true;
                removeAccessToken()
                toast.error(action.error.message, {
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
            .addCase(updateUserInformation.pending, (state) => {
                state.loading = true;
            })
            .addCase(updateUserInformation.fulfilled, (state, action) => {
                state.loading = false;
                state.user = action.payload.user;
                toast.success('Change your information successfully!', {
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
            .addCase(updateUserInformation.rejected, (state) => {
                state.loading = false;
                state.error = true;
                toast.error('Change your information error. Please try again!', {
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
            .addCase(getAllUsers.pending, (state) => {
                state.loading = true;
            })
            .addCase(getAllUsers.fulfilled, (state, action) => {
                state.loading = false;
                action.payload.users.forEach(u => {
                    u.password = ""
                });
                state.all_users = action.payload.users;
            })
            .addCase(getAllUsers.rejected, (state) => {
                state.loading = false;
                state.error = true;
            })
            .addCase(getAllRoles.pending, (state) => {
                state.loading = true;
            })
            .addCase(getAllRoles.fulfilled, (state, action) => {
                state.loading = false;
                state.all_roles = action.payload;
            })
            .addCase(getAllRoles.rejected, (state) => {
                state.loading = false;
                state.error = true;
            })
            .addCase(getAllGroups.pending, (state) => {
                state.loading = true;
            })
            .addCase(getAllGroups.fulfilled, (state, action) => {
                state.loading = false;
                state.all_groups = action.payload;
            })
            .addCase(getAllGroups.rejected, (state) => {
                state.loading = false;
                state.error = true;
            })
            .addCase(searchUsers.pending, (state) => {
                state.loading = true;
            })
            .addCase(searchUsers.fulfilled, (state, action) => {
                state.loading = false;
                state.all_users = action.payload.users;
            })
            .addCase(searchUsers.rejected, (state) => {
                state.loading = false;
                state.error = true;
            })
            .addCase(updateUserStatus.pending, (state) => {
                state.loading = true;
            })
            .addCase(updateUserStatus.fulfilled, (state, action) => {
                state.loading = false;
                toast.success('Update user status succesfully!', {
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
            .addCase(updateUserStatus.rejected, (state) => {
                state.loading = false;
                state.error = true;
                toast.error('Update user status error. Please try again!', {
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
            .addCase(createRole.pending, (state) => {
                state.loading = true;
            })
            .addCase(createRole.fulfilled, (state, action) => {
                state.loading = false;
                toast.success('Created new role succesfully!', {
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
            .addCase(createRole.rejected, (state) => {
                state.loading = false;
                state.error = true;
                toast.error('Created new role error. Please try again!', {
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
            .addCase(createGroup.pending, (state) => {
                state.loading = true;
            })
            .addCase(createGroup.fulfilled, (state, action) => {
                state.loading = false;
                toast.success('Created new group succesfully!', {
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
            .addCase(createGroup.rejected, (state) => {
                state.loading = false;
                state.error = true;
                toast.error('Created new group error. Please try again!', {
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

// export const { logout } = userInformationSlice.actions;
export default userInformationSlice.reducer;
