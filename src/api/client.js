import store from "@/store.js";
import {localLogout} from "@/slices/authSlice.js";

const BASE_URL = '/api';

export const apiClient = async (endpoint, options) => {
    const response = await fetch(BASE_URL + endpoint, options);

    if (response.status === 401) {
        store.dispatch(localLogout());
        return;
    }
    return response;
}