const FIELD_NAMES = ["login", "email", "password", "confirm_password"];

const emptyFields = () => ({
    login: "",
    email: "",
    password: "",
    confirm_password: "",
});

const GATEWAY_STATUSES = new Set([502, 503, 504]);

const gatewayMessage = (status) => {
    if (status === 504) {
        return "The request timed out. Please try again.";
    }
    if (status === 503) {
        return "The service is temporarily unavailable. Please try again later.";
    }
    return "The server is unavailable. Please try again later.";
};

const locField = (loc) => {
    if (!Array.isArray(loc)) {
        return null;
    }
    const name = [...loc].reverse().find((part) => FIELD_NAMES.includes(part));
    return name ?? null;
};

const appendField = (fields, name, message) => {
    if (!message) {
        return;
    }
    fields[name] = fields[name] ? `${fields[name]} ${message}` : message;
};

export const normalizeAuthError = (payload, status = 0) => {
    const fields = emptyFields();
    let form = "";

    if (payload == null) {
        return {status, fields, form: gatewayMessage(status || 502)};
    }

    if (typeof payload === "string") {
        form = payload;
        return {status, fields, form};
    }

    const detail = payload.detail ?? payload;

    if (Array.isArray(detail)) {
        for (const item of detail) {
            const message = item?.msg ?? "";
            const field = locField(item?.loc);
            if (field) {
                appendField(fields, field, message);
            } else if (typeof message === "string" && /password/i.test(message)) {
                appendField(fields, "password", message);
            } else {
                form = form ? `${form} ${message}` : message;
            }
        }
        return {status, fields, form};
    }

    if (detail && typeof detail === "object") {
        if (detail.field && FIELD_NAMES.includes(detail.field) && detail.message) {
            appendField(fields, detail.field, detail.message);
            return {status, fields, form};
        }
        form = detail.message || detail.error || JSON.stringify(detail);
        return {status, fields, form};
    }

    if (typeof detail === "string") {
        return {status, fields, form: detail};
    }

    return {status, fields, form: "Request failed. Please try again."};
};

export const errorFromResponse = async (response) => {
    const status = response.status;
    const contentType = response.headers.get("content-type") || "";
    const raw = await response.text();

    if (contentType.includes("application/json") && raw) {
        try {
            return normalizeAuthError(JSON.parse(raw), status);
        } catch {
            return {status, fields: emptyFields(), form: "Request failed. Please try again."};
        }
    }

    if (GATEWAY_STATUSES.has(status) || raw.trim().startsWith("<")) {
        return {status, fields: emptyFields(), form: gatewayMessage(status)};
    }

    if (raw) {
        return {status, fields: emptyFields(), form: raw};
    }

    return {status, fields: emptyFields(), form: gatewayMessage(status || 502)};
};

export const errorFromException = (error) => {
    const fields = emptyFields();
    if (error?.name === "AbortError") {
        return {status: 0, fields, form: "Request timed out. Please try again."};
    }
    return {status: 0, fields, form: "The server is unavailable. Please try again later."};
};
