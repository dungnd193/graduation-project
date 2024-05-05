import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Navigate, useNavigate } from "react-router-dom";
import classes from "./SignUp.module.css";
import SignUpImg from "./signup.webp"
import TextField from '@mui/material/TextField';
import { ThemeProvider } from "@mui/material";
import Button from '@mui/material/Button';
import signUpTheme from "./signUp.theme"
import { signUpThunk } from '../../redux/slices/authenticationSlice';

function SignUp() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [email, setEmail] = useState('')
    const [phoneNumber, setPhoneNumber] = useState('')
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const handleSignUp = () => {
        dispatch(signUpThunk({ username, password, email, phoneNumber })).then(() => {
            handleNavigateSignIn()
        })
    }

    const handleNavigateSignIn = () => {
        navigate("/sign-in")
    }
    return (
        <ThemeProvider theme={signUpTheme}>
            <div className={classes.container}>
                <img src={SignUpImg} alt="" />
                <div>
                    <div className={classes.signUpGroup}>
                        <h2 className={classes.signUpText}>Register</h2>
                        <div className={classes.signUpInput}>
                            <TextField
                                id="outlined-basic"
                                label="Username"
                                variant="outlined"
                                sx={{ width: '400px' }}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                            <TextField
                                id="outlined-password-input"
                                label="Password"
                                type="password"
                                autoComplete="current-password"
                                onChange={(e) => setPassword(e.target.value)}

                            />
                            <TextField
                                id="outlined-basic"
                                label="Email"
                                variant="outlined"
                                sx={{ width: '400px' }}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                            <TextField
                                id="outlined-basic"
                                label="Phone number"
                                variant="outlined"
                                sx={{ width: '400px' }}
                                onChange={(e) => setPhoneNumber(e.target.value)}
                            />
                            <Button variant="contained" sx={{ backgroundColor: '#57a1f8' }} onClick={handleSignUp}>Register</Button>
                            <div className={classes.signUpBottomText}>
                                <span>Already have an account?</span>
                                {" "}
                                <span onClick={handleNavigateSignIn}>Sign in now</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </ThemeProvider>
    )
}

export default SignUp;
