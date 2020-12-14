import React from "react"
import Cookies from 'universal-cookie';
import {TEST_UPDATE, AUTH_TOKEN_UPDATE, CURRENT_TASK_UPDATE, TASKS_ALL_UPDATE} from './actions'


const cookies = new Cookies();
let auth_token = cookies.get("auth_token")


export const ContextApp = React.createContext();

export const initialState = {
    app: {
        test: "test_context"
    },
    authToken: auth_token,
    currentTask: null,
    tasks: [],
}

export const testReducer = (state, action) => {
    switch ( action.type) {
        case TEST_UPDATE:
            return {
                ...state,
                ...action.payload
            };
        case AUTH_TOKEN_UPDATE:
            return {
                ...state,
                authToken: action.payload.token
            };
        case CURRENT_TASK_UPDATE:
            return {
                ...state,
                ...action.payload
            };
        case TASKS_ALL_UPDATE:
            return {
                ...state,
                ...action.payload
            }
        default:
            return state
    }
}