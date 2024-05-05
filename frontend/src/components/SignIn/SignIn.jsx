import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Navigate, useNavigate } from "react-router-dom";
import classes from "./SignIn.module.css";
import SignInImg from "./login.webp"
import TextField from '@mui/material/TextField';
import { ThemeProvider } from "@mui/material";
import Button from '@mui/material/Button';
import signInTheme from "./signIn.theme"
import { signInThunk } from '../../redux/slices/authenticationSlice';

function SignIn() {
    const accessToken = useSelector(state => state.authenticationSlice.accessToken)
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const loading = useSelector(state => state.authenticationSlice.loading)

    const handleSignIn = () => {
        dispatch(signInThunk({ username, password }))
    }

    const handleNavigateSignUp = () => {
        navigate("/sign-up")
    }

    useEffect(() => {
        if (!accessToken) {
            navigate('/sign-in')
        } else {
            navigate('/')
        }
    }, [])
    return !accessToken ? (
        <ThemeProvider theme={signInTheme}>
            <div className={classes.container}>
                <img src={SignInImg} alt="" />
                <div>
                    <div className={classes.signInGroup}>
                        <h2 className={classes.signInText}>Sign In</h2>
                        <div className={classes.signInInput}>
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
                            <Button variant="contained" sx={{ backgroundColor: '#57a1f8' }} onClick={handleSignIn}>Sign In</Button>
                            <div className={classes.signInBottomText}>
                                <span>Don't have an account?</span>
                                {" "}
                                <span onClick={handleNavigateSignUp}>Register now</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </ThemeProvider>
    ) : (<Navigate to="/" />)
}

export default SignIn;
