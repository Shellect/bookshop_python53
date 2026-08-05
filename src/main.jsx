import * as bootstrap from 'bootstrap';
import { createRoot } from 'react-dom/client';
import App from "./App";
import { BrowserRouter } from 'react-router';
import React from 'react';
import store from './store';
import { Provider } from 'react-redux';


const root = createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <BrowserRouter>
            <Provider store={store}>
                <App />
            </Provider>
        </BrowserRouter>
    </React.StrictMode>
);