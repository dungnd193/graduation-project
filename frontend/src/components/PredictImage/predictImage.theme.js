import { createTheme } from "@mui/material/styles";

const predictImageTheme = createTheme({
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
        },
        MuiMenuItem: {
            styleOverrides: {
                root: {
                    '&:hover': {
                        color: '#fff',
                    },
                },
            },
        },
        MuiCircularProgress: {
            styleOverrides: {
                root: {
                    width: "60px !important",
                    height: "60px !important",
                },
            },
        },
    },
});

export default predictImageTheme;
