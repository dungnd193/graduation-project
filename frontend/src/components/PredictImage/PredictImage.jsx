import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { ThemeProvider } from "@mui/material";
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import FormControl from '@mui/material/FormControl';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import Slider from '@mui/material/Slider';
import { styled } from '@mui/material/styles';
import React, { useEffect, useState, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from 'react-router-dom';
import { getAllModels } from '../../redux/slices/modelSlice';
import { predictImage, resetResult } from '../../redux/slices/predictImageSlice';
import classes from "./PredictImage.module.css";
import predictImageTheme from "./predictImage.theme";

const VisuallyHiddenInput = styled('input')({
    clip: 'rect(0 0 0 0)',
    clipPath: 'inset(50%)',
    height: 1,
    overflow: 'hidden',
    position: 'absolute',
    bottom: 0,
    left: 0,
    whiteSpace: 'nowrap',
    width: 1,
});

function PredictImage() {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const all_models = useSelector(state => state.modelSlice.all_models)
    const user = useSelector(state => state.userInformationSlice.user)
    const { loading, result } = useSelector(state => state.predictImageSlice)
    const [opacity, setOpacity] = useState(1);
    const [selectedFile, setSelectedFile] = useState(null);
    const [imageUrl, setImageUrl] = useState('');
    const [imgInfo, setImgInfo] = useState({
        width: '',
        height: '',
        fileSize: 0,
        fileType: ''
    })

    const [clsModelId, setClsModelId] = React.useState();
    const [locModelId, setLocModelId] = React.useState();

    const [scale, setScale] = useState(1);
    const [position, setPosition] = useState({ x: 0, y: 0 });
    const maskRef = useRef(null)

    const handleZoomIn = () => {
        setScale(scale => scale + 0.1)
    }
    const handleZoomOut = () => {
        setScale(scale => scale - 0.1)
    }

    const handleChangeClsModel = (event) => {
        setClsModelId(event.target.value);
    };
    const handleChangeLocalizationModel = (event) => {
        setLocModelId(event.target.value);
    };

    const handleFileChange = (event) => {
        setPosition({ x: 0, y: 0 }); setScale(1)
        // Access the selected file from event.target.files
        const file = event.target.files[0];
        setSelectedFile(file);

        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                const width = img.width;
                const height = img.height;
                const fileType = file.type;
                const fileSize = file.size;

                setImgInfo({
                    width,
                    height,
                    fileType,
                    fileSize
                });
            };

            img.src = e.target.result;
            setImageUrl(reader.result);
        };
        reader.readAsDataURL(file);
        dispatch(resetResult())
    };

    const handlePredict = () => {
        const formData = new FormData();
        formData.append("input_image", selectedFile);
        dispatch(predictImage({ formData, user_id: user.id, classification_model_id: clsModelId, localization_model_id: locModelId }))
    }

    const handleMaskPath = (mask_path) => {
        return mask_path.replace("D:\\dungnd\\GraduationProject\\server", "http:\/\/localhost:8000\/images").replaceAll("\\", "\/")
    }

    const floatToPercentage = (number) => {
        return (number * 100).toFixed(3) + '%'
    }

    useEffect(() => {
        dispatch(getAllModels())
    }, [])

    useEffect(() => {
        const loc_models = all_models.filter(model => model.model_type == "LOCALIZATION") || []
        const cls_models = all_models.filter(model => model.model_type !== "LOCALIZATION") || []

        setClsModelId(cls_models[0]?.id)
        setLocModelId(loc_models[0]?.id)
    }, [all_models])

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
        <ThemeProvider theme={predictImageTheme}>
            <div className={classes.container}>
                <div className={classes.backDashboard} onClick={() => { dispatch(resetResult()); navigate("/dashboard") }}>
                    <ArrowBackIcon /> Back to Dashboard
                </div>
                <h2 className={classes.title}>Image Prediction</h2>
                <div className={classes.row}>
                    <span className={classes.rowText}>Classification Model</span>
                    <Box sx={{ flex: 1 }}>
                        <FormControl fullWidth>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                value={clsModelId || ""}
                                onChange={handleChangeClsModel}
                                defaultValue={all_models[0]?.id}
                            >
                                {all_models.filter(model => model.model_type !== "LOCALIZATION").map(model => (
                                    <MenuItem value={model.id}>{model.name + " " + model.version}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Box>
                </div>
                <div className={classes.row}>
                    <span className={classes.rowText}>Localization Model</span>
                    <Box sx={{ flex: 1 }}>
                        <FormControl fullWidth>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                value={locModelId || ""}
                                onChange={handleChangeLocalizationModel}
                                defaultValue={all_models[0]?.id}
                            >
                                {all_models.filter(model => model.model_type == "LOCALIZATION").map(model => (
                                    <MenuItem value={model.id}>{model.name + " " + model.version}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Box>
                </div>
                <div className={classes.row}>
                    <span className={classes.rowText}>Image Name</span>
                    <input
                        type="text"
                        className={classes.inputField}
                        readOnly
                        disabled
                        value={selectedFile?.name || ""}
                    />
                    <Button
                        component="label"
                        role={undefined}
                        variant="contained"
                        tabIndex={-1}
                        startIcon={<CloudUploadIcon />}
                        sx={{
                            width: '200px',
                            height: '48px',
                            marginLeft: '20px',
                            backgroundColor: '#57a1f8',
                        }}
                    >
                        Browse
                        <VisuallyHiddenInput type="file" onChange={handleFileChange} />
                    </Button>
                </div>

                <div className={classes.row} style={{ marginBottom: 0 }}>
                    <h3 className={classes.h3text} style={{ marginRight: '10px' }}>Image information</h3>
                    <h3 className={classes.h3text} style={{ marginLeft: '10px' }}>Image</h3>
                </div>
                <div className={classes.imgGroup}>
                    <div className={classes.boxLeft}>
                        {imageUrl && <h3>Resolution: {imgInfo.width}x{imgInfo.height}</h3>}
                        {imageUrl && <h3>Image type: {imgInfo.fileType}</h3>}
                        {imageUrl && <h3>Image size: {(imgInfo.fileSize / 1024).toFixed(2) + ' KB'}</h3>}
                        {result.label && <h3>Label: {result.label}</h3>}
                        {result.classification_accuracy ? <h3>Classification accuracy: {(result.classification_accuracy / 1).toFixed(3)}%</h3> : <></>}
                        {result.localization_accuracy && result.localization_accuracy > 0.0 ? <h3>Localization accuracy: {(result.localization_accuracy / 1).toFixed(3)}%</h3> : <></>}
                    </div>
                    <div className={classes.boxRight} style={{ overflow: 'hidden'}}>
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
                        {result.mask_path && <div className={classes.zoomInBtn} onClick={handleZoomIn}>+</div>}
                        {result.mask_path && <div className={classes.zoomOutBtn} onClick={handleZoomOut}>-</div>}
                        {imageUrl && <img src={imageUrl} alt="Selected" style={{
                                transform: `translate(${position.x}px, ${position.y}px) scale(${scale})`,
                                width: '100%', height: '100%'
                            }}/>}
                        {result.mask_path && <img
                            ref={maskRef}
                            src={handleMaskPath(result.mask_path)}
                            alt="Mask Path"
                            className={classes.maskPath}
                            style={{
                                cursor: 'move',
                                opacity: opacity,
                                transform: `translate(${position.x}px, ${position.y}px) scale(${scale})`
                            }}
                        />}
                    </div>
                </div>
                {false && result.mask_path && <div className={classes.imgGroup}>
                    <div className={classes.boxLeft2}>
                    </div>
                    <div className={classes.boxRight2}>
                        <Slider defaultValue={opacity * 100} onChange={e => setOpacity(e.target.value / 100)} />
                    </div>
                </div>}

                <div style={{ textAlign: 'center' }}>
                    <Button variant="contained" disabled={loading} sx={{ backgroundColor: '#57a1f8', marginTop: '16px', width: '120px' }} onClick={handlePredict}>Predict</Button>
                </div>

            </div>
        </ThemeProvider>
    )
}

export default PredictImage;
