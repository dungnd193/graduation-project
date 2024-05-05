import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import "./App.css";
import SignIn from "./components/SignIn/SignIn";
import SignUp from "./components/SignUp/SignUp";
import Dashboard from "./components/Dashboard/Dashboard";
import UserManagement from "./components/UserManagement/UserManagement";
import ModelManagement from "./components/ModelManagement/ModelManagement";
import ViewHistoryPrediction from "./components/ViewHistoryPrediction/ViewHistoryPrediction";
import PredictImage from "./components/PredictImage/PredictImage";

function App() {

  return (
    <BrowserRouter>
      <Routes>
      <Route path="*" element={<Navigate to="/dashboard" replace={true} />} />
        <Route path="sign-in" element={<SignIn />} />
        <Route path="sign-up" element={<SignUp />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="user-management" element={<UserManagement />} />
        <Route path="model-management" element={<ModelManagement />} />
        <Route path="view-history-prediction" element={<ViewHistoryPrediction />} />
        <Route path="predict" element={<PredictImage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

