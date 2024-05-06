import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { ThemeProvider } from "@mui/material";
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import Slider from '@mui/material/Slider';
import moment from "moment";
import React, { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { getAllHistory, getHistoryById, getUserHistory } from '../../redux/slices/historyPredictionSlice';
import { getAllModels } from '../../redux/slices/modelSlice';
import classes from "./ViewHistoryPrediction.module.css";
import viewHistoryPredictionTheme from "./view-history-prediction.theme";

import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import { styled } from '@mui/material/styles';

const ROLE = {
    ADMIN: 1,
    USER: 2,
}

const MASKS_DIR = "D:\\dungnd\\GraduationProject\\server\\masks\\"

const StyledTableCell = styled(TableCell)(({ theme }) => ({
    [`&.${tableCellClasses.head}`]: {
        backgroundColor: "#57a1f8",
        color: theme.palette.common.white,
    },
    [`&.${tableCellClasses.body}`]: {
        fontSize: 14,
    },
}));

function ViewHistoryPrediction() {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const all_models = useSelector(state => state.modelSlice.all_models)
    const all_history = useSelector(state => state.historyPredictionSlice.all_history)
    const view_hist = useSelector(state => state.historyPredictionSlice.view_hist)
    const user = useSelector(state => state.userInformationSlice.user)
    const [histPerPage, setHistPerPage] = useState([])
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);
    const [open, setOpen] = useState(false)
    const [opacity, setOpacity] = useState(0.50);
    const [scale, setScale] = useState(1);
    const [position, setPosition] = useState({ x: 0, y: 0 });

    const maskRef = useRef(null)

    const handleZoomIn = () => {
        setScale(scale => scale + 0.1)
    }
    const handleZoomOut = () => {
        setScale(scale => scale - 0.1)
    }
    const handleChangePage = (event, newPage) => {
        setHistPerPage(all_history.slice(newPage * rowsPerPage, (newPage + 1) * rowsPerPage))
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
        setHistPerPage(all_history.slice(0, parseInt(event.target.value, 10)))
    };

    const floatToPercentage = (number) => {
        return (number * 100).toFixed(3) + '%'
    }

    const getHistById = (id) => {
        setOpen(true)
        dispatch(getHistoryById(id))
    }

    const handlePath = (path) => {
        if (path) {
            return path.replaceAll("\\", "\/")
        }
    }

    const handleModelName = (model_id) => {
        const model = all_models.find(model => model.id === model_id)
        return model?.name + " " + model?.version
    }

    useEffect(() => {
        if (user.role_id == ROLE.ADMIN) {
            dispatch(getAllHistory())
        }
        if (user.role_id == ROLE.USER) {
            dispatch(getUserHistory(user.id))
        }
    }, [user])

    useEffect(() => {
        dispatch(getAllModels())
    }, [user])

    useEffect(() => {
        setHistPerPage(all_history.slice(page * rowsPerPage, (page + 1) * rowsPerPage))
    }, [all_history])

    useEffect(() => {
        const mask = maskRef.current
        let isDragging = false
        let prevPosition = { x: 0, y: 0 }

        const handleMousedown = (e) => {
            e.preventDefault()
            isDragging = true
            prevPosition = { x: e.clientX, y: e.clientY }
        }

        const handleMouseMove = (e) => {
            e.preventDefault()
            if (!isDragging) return;
            const deltaX = e.clientX - prevPosition.x
            const deltaY = e.clientY - prevPosition.y
            prevPosition = { x: e.clientX, y: e.clientY }
            setPosition(position => ({
                x: position.x + deltaX,
                y: position.y + deltaY,
            }))
        }

        const handleMouseUp = () => {
            isDragging = false
        }

        mask?.addEventListener("mousedown", handleMousedown)
        mask?.addEventListener("mousemove", handleMouseMove)
        mask?.addEventListener("mouseup", handleMouseUp)


        return () => {
            mask?.removeEventListener("mousedown", handleMousedown)
            mask?.removeEventListener("mousemove", handleMouseMove)
            mask?.removeEventListener("mouseup", handleMouseUp)
        }

    }, [maskRef, scale])

    return (
        <ThemeProvider theme={viewHistoryPredictionTheme}>
            <div className={classes.container}>
                <div className={classes.backDashboard} onClick={() => navigate("/dashboard")}>
                    <ArrowBackIcon /> Back to Dashboard
                </div>
                <h2 className={classes.title}>History Prediction</h2>
                <TableContainer component={Paper}>
                    <Table sx={{ minWidth: 700 }} aria-label="customized table">
                        <TableHead>
                            <TableRow>
                                <StyledTableCell sx={{ width: '70px' }}>Id</StyledTableCell>
                                {user.role_id == ROLE.ADMIN &&<StyledTableCell align="right" sx={{ width: '120px' }}>Username</StyledTableCell>}
                                <StyledTableCell align="right" sx={{ width: '200px' }}>Classification model name</StyledTableCell>
                                <StyledTableCell align="right" sx={{ width: '200px' }}>Localization model name</StyledTableCell>
                                {/* <StyledTableCell align="right" sx={{ width: '100px' }}>Input image path</StyledTableCell> */}
                                <StyledTableCell align="right" sx={{ width: '100px' }}>Mask</StyledTableCell>
                                <StyledTableCell align="right" sx={{ width: '100px' }}>Label</StyledTableCell>
                                <StyledTableCell align="right" sx={{ width: '100px' }}>Classification accuracy</StyledTableCell>
                                <StyledTableCell align="right" sx={{ width: '100px' }}>Result</StyledTableCell>
                                <StyledTableCell align="right" sx={{ width: '150px' }}>Date</StyledTableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {histPerPage.map((hist, idx) => (
                                <TableRow key={idx}>
                                    <StyledTableCell component="th" scope="row">
                                        {hist.id}
                                    </StyledTableCell>
                                    {user.role_id == ROLE.ADMIN && <StyledTableCell align="right">{hist.username}</StyledTableCell>}
                                    <StyledTableCell align="right">{handleModelName(hist.classification_model_id)}</StyledTableCell>
                                    <StyledTableCell align="right">{handleModelName(hist.localization_model_id)}</StyledTableCell>
                                    {/* <StyledTableCell align="right">{hist.input_img_path}</StyledTableCell> */}
                                    <StyledTableCell align="right">{hist.output_img_path}</StyledTableCell>
                                    <StyledTableCell align="right">{hist.label}</StyledTableCell>
                                    <StyledTableCell align="right">{(hist.classification_accuracy)}%</StyledTableCell>
                                    <StyledTableCell
                                        align="right"
                                        onClick={() => getHistById(hist.id)}
                                        style={{ textDecoration: 'underline', color: '#57a1f8', cursor: 'pointer' }}
                                    >
                                        View result
                                    </StyledTableCell>
                                    <StyledTableCell align="right">{moment(hist.creat_at).format('lll')}</StyledTableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                    <TablePagination
                        rowsPerPageOptions={[5, 10, 20]}
                        component="div"
                        count={all_history.length}
                        rowsPerPage={rowsPerPage}
                        page={page}
                        onPageChange={handleChangePage}
                        onRowsPerPageChange={handleChangeRowsPerPage}
                    />
                </TableContainer>
            </div>

            <Modal
                open={open}
                onClose={() => { setOpacity(0.5); setOpen(false); setPosition({ x: 0, y: 0 }); setScale(1) }}
            >
                <div className={classes.resultModal}>
                    <h3 className={classes.modalTitle}>Result</h3>
                    <span className={classes.modalText}>Image: {view_hist.input_img_path}</span>
                    <span className={classes.modalText}>Label: {view_hist.label}</span>
                    <span className={classes.modalText}>Classification accuracy: {view_hist.classification_accuracy}%</span>

                    <div className={classes.modalImg} style={{ overflow: 'hidden', border: '1px solid #c4c4c4' }}>
                        <div className={classes.zoomInBtn} onClick={handleZoomIn}>+</div>
                        <div className={classes.zoomOutBtn} onClick={handleZoomOut}>-</div>
                        <img
                            src={"http:\/\/localhost:8000\/images\/input_images\/" + handlePath(view_hist.input_img_path)}
                            alt="input"
                            style={{
                                transform: `translate(${position.x}px, ${position.y}px) scale(${scale})`
                            }}
                            className={classes.resultInput}
                        />
                        <img
                            ref={maskRef}
                            src={"http:\/\/localhost:8000\/images\/masks\/" + handlePath(view_hist.output_img_path)}
                            alt="mask"
                            style={{
                                cursor: 'move',
                                opacity: opacity,
                                transform: `translate(${position.x}px, ${position.y}px) scale(${scale})`
                            }}
                            className={classes.resultMask}
                        />
                    </div>

                    <Slider defaultValue={opacity * 100} onChange={e => setOpacity(e.target.value / 100)} />

                    <Button variant="contained" sx={{ backgroundColor: '#57a1f8', width: '100%', marginTop: '20px' }} onClick={() => setOpen(false)}>Close</Button>
                </div>
            </Modal>
        </ThemeProvider>
    )
}

export default ViewHistoryPrediction;
