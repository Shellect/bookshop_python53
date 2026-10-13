import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";

export const apiSlice = createApi({
    baseQuery: fetchBaseQuery({baseUrl: "/api"}),
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
