import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";
import {showToast} from "@/slices/toastSlice";

const rawBaseQuery = fetchBaseQuery({baseUrl: "/api", timeout: 15_000});

const requestUrl = (args) => (typeof args === "string" ? args : args.url);

const notify = (error, dispatch) => {
    const {status, data} = error;
    if (status === "FETCH_ERROR") {
        dispatch(showToast("danger", "The server is unavailable. Please try again later."));
        return;
    }
    if (status === "TIMEOUT_ERROR") {
        dispatch(showToast("danger", "The request timed out. Please try again."));
        return;
    }
    dispatch(showToast("danger", data?.message ?? "Request failed. Please try again."));
};

const baseQuery = async (args, api, extra) => {
    const result = await rawBaseQuery(args, api, extra);
    if (!result.error) {
        return result;
    }
    // Для гостя 401 на /auth/me — штатная ситуация
    if (result.error.status === 401 && requestUrl(args) === "/auth/me") {
        return result;
    }
    const fields = result.error.data?.fields ?? {};
    if (Object.keys(fields).length === 0) {
        notify(result.error, api.dispatch);
    }
    return result;
};

export const apiSlice = createApi({
    baseQuery,
    reducerPath: "api",
    endpoints: build => ({
        register: build.mutation({
            query: credentials => ({
                url: "/auth/register",
                method: "POST",
                body: credentials
            })
        }),
        login: build.mutation({
            query: credentials => ({
                url: "/auth/login",
                method: "POST",
                body: credentials
            })
        }),
        logout: build.mutation({
            query: () => ({
                url: "/auth/logout",
                method: "POST"
            }),
            async onQueryStarted(_, {dispatch, queryFulfilled}) {
                try {
                    await queryFulfilled;
                    dispatch(apiSlice.util.resetApiState());
                } catch {
                    /* ошибку показывает форма / матчер 401 */
                }
            },
        }),
        me: build.query({
            query: () => "/auth/me"
        })
    })
});

export const {useRegisterMutation, useLoginMutation, useLogoutMutation} = apiSlice;
