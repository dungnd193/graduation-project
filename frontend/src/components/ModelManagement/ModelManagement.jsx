import { ThemeProvider } from "@mui/material";
import Button from '@mui/material/Button';
import FormControlLabel from '@mui/material/FormControlLabel';
import Modal from '@mui/material/Modal';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { getAllModels, createModel, searchModel, updateModel, deleteModel } from '../../redux/slices/modelSlice';
import classes from "./ModelManagement.module.css";
import modelManagementTheme from "./model-management.theme";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import Box from '@mui/material/Box';
import LinearProgress from '@mui/material/LinearProgress';
import CircularProgress from '@mui/material/CircularProgress';
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

function ModelManagement() {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const all_models = useSelector(state => state.modelSlice.all_models)
    const loading = useSelector(state => state.modelSlice.loading)
    const [searchValue, setSearchValue] = useState("");
    const [open, setOpen] = React.useState(false);
    const [modelPerPage, setModelPerPage] = useState([])
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);
    const [modelInfo, setModelInfo] = useState({
        id: NaN,
        name: "",
        accuracy: 0,
        precision: 0,
        recall: 0,
        f1_score: 0,
        path: "",
        description: "",
        version: "",
        model_type: "",
    })
    const [modelType, setModelType] = useState("Add");


    const handleChangePage = (event, newPage) => {
        setModelPerPage(all_models.slice(newPage * rowsPerPage, (newPage + 1) * rowsPerPage))
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
        setModelPerPage(all_models.slice(0, parseInt(event.target.value, 10)))
    };

    const handleSearchModel = () => {
        dispatch(searchModel(searchValue))
    }

    const handleOpenAddModal = () => {
        setOpen(true)
        setModelType("Add")
    }

    const handleOpenUpdateModal = (model) => {
        setOpen(true)
        setModelType("Update")
        setModelInfo(state => ({ ...state, ...model }))
    }

    const handleCloseModal = () => {
        setOpen(false)
        setModelInfo({
            id: NaN,
            name: "",
            accuracy: 0,
            precision: 0,
            recall: 0,
            f1_score: 0,
            path: "",
            description: "",
            version: "",
            model_type: ""
        })
    }


    const handleModalBtn = () => {
        console.log(modelInfo)
        if (modelType == "Add") {
            delete modelInfo.id
            dispatch(createModel(modelInfo)).then(() => {
                dispatch(getAllModels())
                handleCloseModal()
            })
        }

        if (modelType == "Update") {
            dispatch(updateModel(modelInfo)).then(() => {
                dispatch(getAllModels())
                handleCloseModal()
            })
        }
    }

    const handleDeleteModel = (model_id) => {
        dispatch(deleteModel({ model_id }))
            .then(() => {
                dispatch(getAllModels())
            });
    }

    const floatToPercentage = (number) => {
        return (number * 100).toFixed(3) + '%'
    }


    useEffect(() => {
        dispatch(getAllModels())
    }, [])

    useEffect(() => {
        setModelPerPage(all_models.slice(page * rowsPerPage, (page + 1) * rowsPerPage))
    }, [all_models])


    return (
        <ThemeProvider theme={modelManagementTheme}>
            <div className={classes.container}>
                <div className={classes.backDashboard} onClick={() => navigate("/dashboard")}>
                    <ArrowBackIcon /> Back to Dashboard
                </div>
                <h2 className={classes.title}>Model Management</h2>
                <div className={classes.searchGroup}>
                    <Button variant="contained" sx={{ backgroundColor: '#57a1f8', width: '200px', height: '49px' }} onClick={handleSearchModel}>Search by name</Button>
                    <input type="text" className={classes.searchInput} value={searchValue} onChange={e => setSearchValue(e.target.value)} />
                    <Button variant="contained" sx={{ backgroundColor: '#57a1f8', width: '200px', height: '49px' }} onClick={handleOpenAddModal}>Add Model</Button>
                </div>
                {loading && <div className={classes.overlay}>
                    <svg width={0} height={0}>
                        <defs>
                            <linearGradient id="my_gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" stopColor="#e01cd5" />
                                <stop offset="100%" stopColor="#1CB5E0" />
                            </linearGradient>
                        </defs>
                    </svg>
                    <CircularProgress
                        sx={{
                            'svg circle': { stroke: 'url(#my_gradient)' },
                            position: 'absolute',
                            top: '50%',
                            left: '50%',
                            transform: 'translate(-50%, -50%)',
                            width: '80px',
                        }}
                    />
                </div>}
                {!loading && <TableContainer component={Paper}>
                    <div style={{ overflowX: 'auto' }}>
                        <Table sx={{ minWidth: 700 }} aria-label="customized table" >
                            <TableHead>
                                <TableRow>
                                    <StyledTableCell sx={{ width: '70px' }}>Id</StyledTableCell>
                                    <StyledTableCell align="right" sx={{ width: '200px' }}>Model name</StyledTableCell>
                                    <StyledTableCell align="right" sx={{ width: '100px' }}>Accuracy</StyledTableCell>
                                    <StyledTableCell align="right" sx={{ width: '100px' }}>Precision</StyledTableCell>
                                    <StyledTableCell align="right" sx={{ width: '100px' }}>Recall</StyledTableCell>
                                    <StyledTableCell align="right" sx={{ width: '100px' }}>F1 Score</StyledTableCell>
                                    <StyledTableCell align="right" sx={{ width: '100px' }}>Version</StyledTableCell>
                                    <StyledTableCell align="right" sx={{ width: '100px' }}>Model type</StyledTableCell>
                                    <StyledTableCell align="right" sx={{ width: '500px' }}>Path</StyledTableCell>
                                    <StyledTableCell align="right" sx={{ width: '350px' }}>Description</StyledTableCell>
                                    <StyledTableCell align="right" sx={{ textAlign: 'center' }}>Action</StyledTableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {modelPerPage.map((model, idx) => (
                                    <TableRow key={idx}>
                                        <StyledTableCell component="th" scope="row">
                                            {model.id}
                                        </StyledTableCell>
                                        <StyledTableCell align="right">{model.name}</StyledTableCell>
                                        <StyledTableCell align="right">{floatToPercentage(model.accuracy)}</StyledTableCell>
                                        <StyledTableCell align="right">{floatToPercentage(model.precision)}</StyledTableCell>
                                        <StyledTableCell align="right">{floatToPercentage(model.recall)}</StyledTableCell>
                                        <StyledTableCell align="right">{floatToPercentage(model.f1_score)}</StyledTableCell>
                                        <StyledTableCell align="right">{model.version}</StyledTableCell>
                                        <StyledTableCell align="right">{model.model_type}</StyledTableCell>
                                        <StyledTableCell align="right">{model.path}</StyledTableCell>
                                        <StyledTableCell align="right">{model.description}</StyledTableCell>
                                        <StyledTableCell align="right">
                                            <div className={classes.btnActionGroup}>
                                                <button className={classes.btnAction} style={{ backgroundColor: "#d79f59" }} onClick={() => handleOpenUpdateModal(model)}>UPDATE</button>
                                                <button className={classes.btnAction} style={{ backgroundColor: "#585858" }} onClick={() => handleDeleteModel(model.id)}>DELETE</button>
                                            </div>
                                        </StyledTableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>
                    <TablePagination
                        rowsPerPageOptions={[5, 10, 15]}
                        component="div"
                        count={all_models.length}
                        rowsPerPage={rowsPerPage}
                        page={page}
                        onPageChange={handleChangePage}
                        onRowsPerPageChange={handleChangeRowsPerPage}
                    />
                </TableContainer>}
            </div>

            <Modal
                open={open}
                onClose={handleCloseModal}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <div className={classes.updateUserInforModal}>
                    <h3 className={classes.modalTitle}>{modelType} model</h3>
                    <span className="modalText">Model name</span>
                    <input
                        type="text"
                        placeholder="Type your model name"
                        className={classes.inputField}
                        value={modelInfo.name}
                        onChange={e =>
                            setModelInfo((state) => ({ ...state, name: e.target.value }))
                        }
                    />

                    <span className="modalText">Accuracy</span>
                    <input
                        type="text"
                        placeholder="Type your model's accuracy"
                        className={classes.inputField}
                        value={modelInfo.accuracy}
                        onChange={e =>
                            setModelInfo((state) => ({ ...state, accuracy: e.target.value }))
                        }
                    />

                    <span className="modalText">Precision</span>
                    <input
                        type="text"
                        placeholder="Type your model's precision"
                        className={classes.inputField}
                        value={modelInfo.precision}
                        onChange={e =>
                            setModelInfo((state) => ({ ...state, precision: e.target.value }))
                        }
                    />

                    <span className="modalText">Recall</span>
                    <input
                        type="text"
                        placeholder="Type your model's recall"
                        className={classes.inputField}
                        value={modelInfo.recall}
                        onChange={e =>
                            setModelInfo((state) => ({ ...state, recall: e.target.value }))
                        }
                    />

                    <span className="modalText">F1 Score</span>
                    <input
                        type="text"
                        placeholder="Type your model's f1 score"
                        className={classes.inputField}
                        value={modelInfo.f1_score}
                        onChange={e =>
                            setModelInfo((state) => ({ ...state, f1_score: e.target.value }))
                        }
                    />

                    <span className="modalText">Version</span>
                    <input
                        type="text"
                        placeholder="Type your model's version"
                        className={classes.inputField}
                        value={modelInfo.version}
                        onChange={e =>
                            setModelInfo((state) => ({ ...state, version: e.target.value }))
                        }
                    />

                    <span className="modalText">Model type</span>
                    <RadioGroup
                        aria-labelledby="demo-radio-buttons-group-label"
                        name="radio-buttons-group"
                        value={modelInfo.model_type}
                        onChange={(e) => setModelInfo(state => {
                            console.log(e.target.value)
                            return ({ ...state, model_type: e.target.value })
                        })}
                        sx={{ columnGap: '30px' }}
                    >
                        <FormControlLabel value={"FORGERY CLASSIFICATION"} control={<Radio />} label="FORGERY CLASSIFICATION" />
                        <FormControlLabel value={"AI GENERATED CLASSIFICATION"} control={<Radio />} label="AI GENERATED CLASSIFICATION" />
                        <FormControlLabel value={"LOCALIZATION"} control={<Radio />} label="LOCALIZATION" />
                    </RadioGroup>

                    <span className="modalText">Description</span>
                    <input
                        type="text"
                        placeholder="Type your model's description"
                        className={classes.inputField}
                        value={modelInfo.description}
                        onChange={e =>
                            setModelInfo((state) => ({ ...state, description: e.target.value }))
                        }
                    />

                    <span className="modalText">Path</span>
                    <input
                        type="text"
                        placeholder="Type your model's path"
                        className={classes.inputField}
                        value={modelInfo.path}
                        onChange={e =>
                            setModelInfo((state) => ({ ...state, path: e.target.value }))
                        }
                    />

                    <Button variant="contained" sx={{ backgroundColor: '#57a1f8', width: '100%', marginTop: '20px' }} onClick={handleModalBtn}>{modelType}</Button>
                </div>
            </Modal>
        </ThemeProvider>
    )
}

export default ModelManagement;
