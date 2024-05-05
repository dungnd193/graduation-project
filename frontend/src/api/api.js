const API = {
    BASE_API_URL: 'http://localhost:8000',
    LOGIN: '/login',
    SIGN_UP: '/users/',
    USER_INFO: '/user/current',
    UPDATE_USER_INFO: '/users/',
    UPDATE_USER_STATUS: '/users/',
    GET_ALL_USER: '/users/',
    DELETE_USER: '/users/',
    SEARCH_USER: '/users/user_search/',
    GET_ALL_MODELS: '/models/',
    CREATE_MODELS: '/models/',
    SEARCH_MODEL: '/models/search/',
    UPDATE_MODEL: '/models/',
    DELETE_MODEL: '/models/',
    GET_ALL_HISTORY: '/history/',
    GET_HISTORY_BY_USER: '/history/user/',
    GET_HISTORY_BY_ID: '/history/id/',
    PREDICT_IMAGE: '/predict/'
}

export default API