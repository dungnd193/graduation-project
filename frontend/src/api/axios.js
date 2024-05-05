import axios from "axios";
import API from "./api";

export const setAccessToken = (value) =>
    localStorage.setItem("accessToken", value);

export const getAccessToken = () => localStorage.getItem("accessToken");

export const removeAccessToken = () => localStorage.removeItem("accessToken");


const axiosInstance = axios.create({
    baseURL: API.BASE_API_URL,
    timeout: 500000,
    headers: {
        "Content-Type": "application/json",
    },
});
axiosInstance.interceptors.request.use((request) => {
    const accessToken = getAccessToken();
    const accessHeader = `Bearer ${accessToken}`;
    if (request.headers) {
        request.headers["Authorization"] = accessHeader;
    }
    return request;
});
export default axiosInstance;
