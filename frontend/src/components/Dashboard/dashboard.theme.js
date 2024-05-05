
import { createTheme } from "@mui/material/styles";

const dashboardTheme = createTheme({
    components: {
        MuiBackdrop: {
            styleOverrides: {
                root: {
                    backgroundColor: 'rgba(0, 0, 0, 0.4);',
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

export default dashboardTheme;
