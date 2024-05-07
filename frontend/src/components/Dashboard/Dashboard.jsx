import React, { useState, useEffect } from "react";
import classes from "./Dashboard.module.css";
import DashboardImg from "./bg.webp";
import Button from '@mui/material/Button';
import { logout } from '../../redux/slices/authenticationSlice';
import { getUserInformation, updateUserInformation } from '../../redux/slices/userInformationSlice';
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import Modal from '@mui/material/Modal';
import { ThemeProvider } from "@mui/material";
import dashboardTheme from "./dashboard.theme"
import { getAccessToken } from "../../api/axios";

function Dashboard() {
    const ADMIN = 1
    const USER = 2
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const user = useSelector(state => state.userInformationSlice.user)
    const redirectToSignIn = useSelector(state => state.userInformationSlice.redirectToSignIn)
    const [open, setOpen] = React.useState(false);

    const [userInfo, setUserInfo] = useState({
        id: user.id,
        username: user.username,
        password: "",
        email: user.email,
        phone_number: user.phone_number,
        role_id: 2,
        status: "ACTIVE"
    })

    const handleLogOut = () => {
        dispatch(logout())
        navigate("/sign-in")
    }

    const handleUpdateUserInfo = () => {
        dispatch(updateUserInformation(userInfo)).then(() => {
            setUserInfo(state => ({
                ...state,
                password: ""
            }))
            setOpen(false)
        })
    }


    useEffect(() => {
        dispatch(getUserInformation()).then((res) => {
            setUserInfo(state => ({
                ...state,
                id: res?.payload?.user?.id,
                username: res?.payload?.user?.username,
                password: "",
                email: res?.payload?.user?.email,
                phone_number: res?.payload?.user?.phone_number
            }))
        })
    }, [])






    return (
        <ThemeProvider theme={dashboardTheme}>
            <div className={classes.container}>
                <img src={DashboardImg} alt="dashboard-img" className={classes.dashboardImg} />
                {!redirectToSignIn && user.role_id == ADMIN && <div className={classes.dashboardBtnGroup}>
                    <Button variant="contained" sx={{ backgroundColor: '#57a1f8' }} onClick={() => navigate("/user-management")}>User Management</Button>
                    <Button variant="contained" sx={{ backgroundColor: '#57a1f8' }} onClick={() => navigate("/model-management")}>Model Management</Button>
                    <Button variant="contained" sx={{ backgroundColor: '#57a1f8' }} onClick={() => navigate("/view-history-prediction")}>View history prediction</Button>
                    <Button variant="contained" sx={{ backgroundColor: '#57a1f8' }} onClick={handleLogOut}>Log out</Button>
                </div>}
                {!redirectToSignIn && user.role_id == USER && <div className={classes.dashboardBtnGroup}>
                    <Button variant="contained" sx={{ backgroundColor: '#57a1f8' }} onClick={() => setOpen(true)}>Update Information</Button>
                    <Button variant="contained" sx={{ backgroundColor: '#57a1f8' }} onClick={() => navigate("/predict")}>Predict Image</Button>
                    <Button variant="contained" sx={{ backgroundColor: '#57a1f8' }} onClick={() => navigate("/view-history-prediction")}>View history prediction</Button>
                    <Button variant="contained" sx={{ backgroundColor: '#57a1f8' }} onClick={handleLogOut}>Log out</Button>
                </div>}
                {redirectToSignIn && <Button variant="contained" sx={{ backgroundColor: '#57a1f8', marginTop: '20px', width: '240px' }} onClick={() => navigate("/sign-in")}>Sign In</Button>}

                <Modal
                    open={open}
                    onClose={() => setOpen(false)}
                    aria-labelledby="modal-modal-title"
                    aria-describedby="modal-modal-description"
                >
                    <div className={classes.updateUserInforModal}>
                        <h3 className={classes.modalTitle}>Update user information</h3>
                        <span className="modalText">Username</span>
                        <input type="text" value={user.username} placeholder="Username" className={classes.inputField} readOnly disabled />

                        <span className="modalText">Password</span>
                        <input
                            type="password"
                            placeholder="Type your password"
                            className={classes.inputField}
                            value={userInfo.password}
                            onChange={e =>
                                setUserInfo((state) => ({ ...state, password: e.target.value }))
                            }
                        />

                        <span className="modalText">Email</span>
                        <input
                            type="text"
                            placeholder="Type your email address"
                            className={classes.inputField}
                            value={userInfo.email}
                            onChange={e =>
                                setUserInfo((state) => ({ ...state, email: e.target.value }))
                            }
                        />

                        <span className="modalText">Phone Number</span>
                        <input
                            type="text"
                            placeholder="Type your phone number"
                            className={classes.inputField}
                            value={userInfo.phone_number}
                            onChange={e =>
                                setUserInfo((state) => ({ ...state, phone_number: e.target.value }))
                            }
                        />

                        <Button variant="contained" sx={{ backgroundColor: '#57a1f8', width: '100%', marginTop: '20px' }} onClick={handleUpdateUserInfo}>Update</Button>
                    </div>
                </Modal>
            </div>
        </ThemeProvider>
    )
}

export default Dashboard;
