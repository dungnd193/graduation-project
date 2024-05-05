import { ThemeProvider } from "@mui/material";
import Button from '@mui/material/Button';
import FormControlLabel from '@mui/material/FormControlLabel';
import Modal from '@mui/material/Modal';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { deleteUser, getAllUsers, updateUserStatus, updateUserInformation, searchUsers } from '../../redux/slices/userInformationSlice';
import classes from "./UserManagement.module.css";
import userManagementTheme from "./user-management.theme";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import { styled } from '@mui/material/styles';

const StyledTableCell = styled(TableCell)(({ theme }) => ({
    [`&.${tableCellClasses.head}`]: {
        backgroundColor: "#57a1f8",
        color: theme.palette.common.white,
    },
    [`&.${tableCellClasses.body}`]: {
        fontSize: 14,
    },
}));

function UserManagement() {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const all_users = useSelector(state => state.userInformationSlice.all_users)
    const [searchValue, setSearchValue] = useState("");
    const [open, setOpen] = React.useState(false);
    const [userPerPage, setUserPerPage] = useState([])
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);
    const [userInfo, setUserInfo] = useState({
        id: NaN,
        username: "",
        password: "",
        email: "",
        phone_number: "",
        role_id: NaN,
        status: ""
    })
    const [roleId, setRoleId] = useState(NaN);

    const handleChangeRoleId = (e) => {
        setRoleId(e.target.value);
    };

    const handleChangePage = (event, newPage) => {
        setUserPerPage(all_users.slice(newPage * rowsPerPage, (newPage + 1) * rowsPerPage))
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
        setUserPerPage(all_users.slice(0, parseInt(event.target.value, 10)))
    };

    const handleSearchUser = () => {
        dispatch(searchUsers(searchValue))
    }

    const handleActiveUser = (user_id) => {
        dispatch(updateUserStatus({ user_id, stt: "ACTIVE" }))
            .then(() => dispatch(getAllUsers()));
    }
    const handleDeactiveUser = (user_id) => {
        dispatch(updateUserStatus({ user_id, stt: "DEACTIVE" }))
            .then(() => dispatch(getAllUsers()));
    }
    const handleOpenUpdateModal = (user) => {
        setOpen(true)
        setUserInfo(state => ({ ...state, ...user }))
        setRoleId(user.role_id)
    }

    const handleUpdateUser = () => {
        const newInfo = {
            ...userInfo,
            role_id: roleId
        }
        dispatch(updateUserInformation(newInfo))
            .then(() => {
                setOpen(false)
                dispatch(getAllUsers())
            });
    }

    const handleDeleteUser = (user_id) => {
        dispatch(deleteUser({ user_id }))
            .then(() => dispatch(getAllUsers()));
    }

    useEffect(() => {
        dispatch(getAllUsers())
    }, [])

    useEffect(() => {
        setUserPerPage(all_users.slice(page*rowsPerPage, (page+1)*rowsPerPage))
    }, [all_users])


    return (
        <ThemeProvider theme={userManagementTheme}>
            <div className={classes.container}>
                <div className={classes.backDashboard} onClick={() => navigate("/dashboard")}>
                    <ArrowBackIcon /> Back to Dashboard
                </div>
                <h2 className={classes.title}>User Management</h2>
                <div className={classes.searchGroup}>
                    <Button variant="contained" sx={{ backgroundColor: '#57a1f8', width: '200px', height: '49px' }} onClick={handleSearchUser}>Search</Button>
                    <input type="text" className={classes.searchInput} value={searchValue} onChange={e => setSearchValue(e.target.value)} />
                </div>
                <TableContainer component={Paper}>
                    <Table sx={{ minWidth: 700 }} aria-label="customized table">
                        <TableHead>
                            <TableRow>
                                <StyledTableCell sx={{ width: '70px' }}>Id</StyledTableCell>
                                <StyledTableCell align="right" sx={{ width: '150px' }}>Username</StyledTableCell>
                                <StyledTableCell align="right" sx={{ width: '250px' }}>Email</StyledTableCell>
                                <StyledTableCell align="right" sx={{ width: '150px' }}>Phone Number</StyledTableCell>
                                <StyledTableCell align="right" sx={{ width: '100px' }}>Role</StyledTableCell>
                                <StyledTableCell align="right" sx={{ width: '100px' }}>Status</StyledTableCell>
                                <StyledTableCell align="right" sx={{ textAlign: 'center' }}>Action</StyledTableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {userPerPage.map((user, idx) => (
                                <TableRow key={idx}>
                                    <StyledTableCell component="th" scope="row">
                                        {user.id}
                                    </StyledTableCell>
                                    <StyledTableCell align="right">{user.username}</StyledTableCell>
                                    <StyledTableCell align="right">{user.email}</StyledTableCell>
                                    <StyledTableCell align="right">{user.phone_number}</StyledTableCell>
                                    <StyledTableCell align="right">{user.role_id == 2 ? "USER" : "ADMIN"}</StyledTableCell>
                                    <StyledTableCell align="right">{user.status}</StyledTableCell>
                                    <StyledTableCell align="right">
                                        <div className={classes.btnActionGroup}>
                                            <button className={classes.btnAction} style={{ backgroundColor: "#4bcd00" }} onClick={() => handleActiveUser(user.id)}>ACTIVE</button>
                                            <button className={classes.btnAction} style={{ backgroundColor: "#d13645" }} onClick={() => handleDeactiveUser(user.id)}>DEACTIVE</button>
                                            <button className={classes.btnAction} style={{ backgroundColor: "#d79f59" }} onClick={() => handleOpenUpdateModal(user)}>UPDATE</button>
                                            <button className={classes.btnAction} style={{ backgroundColor: "#585858" }} onClick={() => handleDeleteUser(user.id)}>DELETE</button>
                                        </div>
                                    </StyledTableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                    <TablePagination
                        rowsPerPageOptions={[5, 10, 15]}
                        component="div"
                        count={all_users.length}
                        rowsPerPage={rowsPerPage}
                        page={page}
                        onPageChange={handleChangePage}
                        onRowsPerPageChange={handleChangeRowsPerPage}
                    />
                </TableContainer>
            </div>

            <Modal
                open={open}
                onClose={() => setOpen(false)}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <div className={classes.updateUserInforModal}>
                    <h3 className={classes.modalTitle}>Update user information</h3>
                    <span className="modalText">Username</span>
                    <input type="text" value={userInfo.username} placeholder="Username" className={classes.inputField} readOnly disabled />

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

                    <span className="modalText">Role</span>
                    <RadioGroup
                        aria-labelledby="demo-radio-buttons-group-label"
                        name="radio-buttons-group"
                        value={roleId}
                        onChange={handleChangeRoleId}
                        row
                        sx={{ columnGap: '30px' }}
                    >
                        <FormControlLabel value={1} control={<Radio />} label="ADMIN" />
                        <FormControlLabel value={2} control={<Radio />} label="USER" />
                    </RadioGroup>

                    <Button variant="contained" sx={{ backgroundColor: '#57a1f8', width: '100%', marginTop: '20px' }} onClick={handleUpdateUser}>Update</Button>
                </div>
            </Modal>
        </ThemeProvider>
    )
}

export default UserManagement;
