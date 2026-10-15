import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";
import {showToast} from "@/slices/toastSlice";

const rawBaseQuery = fetchBaseQuery({baseUrl: "/api", timeout: 15_000});

const baseQuery = async (args, api, extra) => {
    const result = await rawBaseQuery(args, api, extra);
    if (!result.error) {
        return result;
    }

    const {status, data} = result.error;

    // Для гостя 401 на /auth/me — штатная ситуация
    if (status === 401 && args === "/auth/me") {
        return result;
    }

    // Ошибки валидации показываем в самой форме
    if (data?.error === "REQUEST_VALIDATION_ERROR") {
        return result;
    }

    let message;
    if (status === "FETCH_ERROR") {
        message = "The server is unavailable. Please try again later.";
    } else if (status === "TIMEOUT_ERROR") {
        message = "The request timed out. Please try again.";
    } else {
        message = data?.message ?? "Request failed. Please try again.";
    }
    api.dispatch(showToast("danger", message));

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
