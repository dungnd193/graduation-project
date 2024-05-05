import { createTheme } from "@mui/material/styles";

const signUpTheme = createTheme({
    components: {
        MuiOutlinedInput: {
            styleOverrides: {
                root: {
                    borderRadius: '0px',
                },
            },
        },
        MuiButtonBase: {
            styleOverrides: {
                root: {
                    '&:hover': {
                        backgroundColor: '#57a1f8 !important',
                    },
                },
            },
        }
    },
});

export default signUpTheme;
