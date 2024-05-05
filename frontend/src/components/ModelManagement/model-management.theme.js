
import { createTheme } from "@mui/material/styles";

const modelManagementTheme = createTheme({
    components: {
        MuiTableCell: {
            styleOverrides: {
                head: {
                    textAlign: 'left;',
                    borderRight: '1px solid #c4c4c4'
                },
                body: {
                    textAlign: 'left;',
                    borderRight: '1px solid #c4c4c4'
                },
            },
        },
        MuiTablePagination: {
            styleOverrides: {
                toolbar: {
                    borderRight: '1px solid #c4c4c4'
                },
            },
        },
        MuiButtonBase: {
            styleOverrides: {
                root: {
                    borderRadius: "0px !important",
                    '&:hover': {
                        backgroundColor: '#57a1f8 !important',
                    },
                },
            },
        },
        MuiRadio: {
            styleOverrides: {
                root: {
                    borderRadius: "0px !important",
                    '&:hover': {
                        backgroundColor: 'unset !important',
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
        MuiFormControlLabel : {
            styleOverrides: {
                label: {
                    fontSize: "14px",
                },
            },
        },
    },
});

export default modelManagementTheme;
