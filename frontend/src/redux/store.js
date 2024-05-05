import { configureStore } from '@reduxjs/toolkit'
import authenticationSlice from "./slices/authenticationSlice"
import userInformationSlice from "./slices/userInformationSlice"
import modelSlice from "./slices/modelSlice"
import historyPredictionSlice from "./slices/historyPredictionSlice"
import predictImageSlice from "./slices/predictImageSlice"
const reducer = {
    authenticationSlice,
    userInformationSlice,
    modelSlice,
    historyPredictionSlice,
    predictImageSlice
};

export const store = configureStore({ reducer })