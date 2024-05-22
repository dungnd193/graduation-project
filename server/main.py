from fastapi import FastAPI, File, HTTPException, Depends, UploadFile, status, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Annotated, List
import be_models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from subprocess import call
import jwt
from datetime import datetime, timedelta
import os
from sqlalchemy.orm import joinedload

from keras.models import load_model
from PIL import Image, ImageChops, ImageEnhance
import numpy as np




SECRET_KEY = "your-secret-key"  # Change this to your secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24 # Adjust the expiration time as needed

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can adjust this based on your needs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

be_models.Base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    id: int = None
    username: str
    password: str
    email: str
    phone_number: str
    role_id: int
    status: str

class UserWithoutPasswordBase(BaseModel):
    id: int
    username: str
    email: str
    phone_number: str
    role_id: int
    status: str

class UserWithoutPasswordList(BaseModel):
    users: list[UserWithoutPasswordBase]

class UserList(BaseModel):
    users: list[UserBase]

class Token(BaseModel):
    access_token: str
    token_type: str
    
class UpdateUserStatus(BaseModel):
    status: str

class RoleBase(BaseModel):
    role: str

class LogInBase(BaseModel):
    username: str
    password: str

class ModelBase(BaseModel):
    id: int = None
    name: str
    path: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    model_type: str
    version: str
    description: str

class HistoryBase(BaseModel):
    id: int = None
    user_id: int
    classification_model_id: int
    localization_model_id: int
    input_img_path: str
    output_img_path: str
    label: str
    accuracy: float

def test_face_image(image_path, model_loaded):
        """
        Custom Model
        :param  image_path
        :return label1[Real , Fake] , acc[class accuracy]
        """
        # model_loaded = load_model(model_path)
        # Read image
        image = Image.open(image_path).convert('RGB')

        # prepare image for testing
        image = np.array(image.resize((256, 256))).flatten() / 255.0
        image = image.reshape(-1, 256, 256, 3)
        

        # Make predictions on the input image
        acc = model_loaded.predict(image)[0]
        idx = np.argmax(acc)

        label = "Fake" if acc < 0.5  else "Real"
        return label, acc[idx]

def convert_to_ela_image(path, quality):
    temp_filename = 'temp_file_name.jpg'
    
    image = Image.open(path).convert('RGB')
    image.save(temp_filename, 'JPEG', quality = quality)
    temp_image = Image.open(temp_filename)
    
    ela_image = ImageChops.difference(image, temp_image)
    
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    os.remove(temp_filename)
    return ela_image

def prepare_image(image_path):
    return np.array(convert_to_ela_image(image_path, 98).resize([128,128])).flatten() / 255.0

def forgery_image_test(image_path, model_loaded):
    """
    Custom Model
    :param  image_path
    :return label1[Real , Fake] , acc[class accuracy]
    """
    X = prepare_image(image_path=image_path)
    X = np.array(X)
    X = X.reshape(-1, 128, 128, 3)
    A = model_loaded(X)
    (label, acc) = ("Fake", A[0][0]) if A[0][1] < A[0][0]  else ("Real", A[0][1])
    acc = A[0][0] if A[0][1] < A[0][0]  else A[0][1]
    return label, acc

# def create_access_token(data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

def create_access_token(id: int, username: str, expires_delta: timedelta):
    to_encode = {"id": id, "username": username}
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
        
        token = token.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("id")
        user = db.query(be_models.User).filter(be_models.User.id == id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        user_without_password = be_models.User(
            id=user.id,
            username=user.username,
            email=user.email,
            phone_number=user.phone_number,
            role_id=user.role_id,
            status=user.status
        )
        return user_without_password
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired, please sign in again!")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token is invalid, please sign in again!")

async def forgery_image_predict(upload_file: UploadFile, user_id, classification_model_id, localization_model_id, model_loaded, loc_model_path, db: Session):
    try:
        input_images_directory = "D:\\dungnd\\GraduationProject\\server\\input_images"
        masks_directory="D:\\dungnd\\GraduationProject\\server\\masks"

        if not os.path.exists(input_images_directory):
            os.makedirs(input_images_directory)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename, file_extension = os.path.splitext(upload_file.filename)
        unique_filename = f"{timestamp}_{filename}{file_extension}"

        file_path = os.path.join(input_images_directory, unique_filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await upload_file.read())
        
        label, acc = forgery_image_test(image_path=file_path, model_loaded=model_loaded)
        
        mask_file_name = os.path.splitext(os.path.basename(file_path))[0]+"_mask.png"
        mask_path = os.path.join(masks_directory, mask_file_name)
        call(["python", 
            r"D:\dungnd\GraduationProject\MMFusion-IML\inference.py", 
            "--exp", r'D:\dungnd\GraduationProject\MMFusion-IML\experiments\ec_example_phase2.yaml',
            "--ckpt", loc_model_path,
            "--path", file_path])
        
        history = be_models.History(
            user_id=user_id,
            classification_model_id=classification_model_id,
            localization_model_id=localization_model_id,
            input_img_path=unique_filename,
            output_img_path=mask_file_name,
            label=label,
            classification_accuracy="%.5f" % np.abs(acc*100)
        )
        db.add(history)
        db.commit()

        return {
            "message": "Predicted successfully", 
            "label": label,
            "accuracy": "%.5f" % np.abs(acc*100),
            "file_path": file_path, 
            "mask_path": mask_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def ai_generated_predict(upload_file: UploadFile, user_id, classification_model_id, localization_model_id, model_loaded, loc_model_path, db: Session):
    try:
        input_images_directory = "D:\\dungnd\\GraduationProject\\server\\input_images"
        masks_directory="D:\\dungnd\\GraduationProject\\server\\masks"

        if not os.path.exists(input_images_directory):
            os.makedirs(input_images_directory)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename, file_extension = os.path.splitext(upload_file.filename)
        unique_filename = f"{timestamp}_{filename}{file_extension}"

        file_path = os.path.join(input_images_directory, unique_filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await upload_file.read())
        
        label, acc = test_face_image(image_path=file_path, model_loaded=model_loaded)
        
        mask_file_name = os.path.splitext(os.path.basename(file_path))[0]+"_mask.png"
        mask_path = os.path.join(masks_directory, mask_file_name)
        call(["python", 
            r"D:\dungnd\GraduationProject\MMFusion-IML\inference.py", 
            "--exp", r'D:\dungnd\GraduationProject\MMFusion-IML\experiments\ec_example_phase2.yaml',
            "--ckpt", loc_model_path,
            "--path", file_path])
        
        history = be_models.History(
            user_id=user_id,
            classification_model_id=classification_model_id,
            localization_model_id=localization_model_id,
            input_img_path=unique_filename,
            output_img_path=mask_file_name,
            label=label,
            classification_accuracy="%.5f" % np.abs(acc*100)
        )
        db.add(history)
        db.commit()

        return {
            "message": "Predicted successfully", 
            "label": label,
            "accuracy": "%.5f" % np.abs(acc*100),
            "file_path": file_path, 
            "mask_path": mask_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/login")
async def login(credentials: LogInBase, db: db_dependency):
    user = db.query(be_models.User).filter(be_models.User.username == credentials.username).first()
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        id=user.id,
        username=user.username,
        expires_delta=access_token_expires
    )


    user_without_password = be_models.User(
        id=user.id,
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        role_id=user.role_id,
        status=user.status
    )

    return {"user": user_without_password, "access_token": access_token, "token_type": "bearer"}

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = be_models.User(**user.dict())
    db.add(db_user)
    db.commit()
    return {"message": "Sign Up successfully!"}

@app.get("/users/", status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency) -> UserList:
    users = db.query(be_models.User).all()
    users = [
        UserBase(
            id=user.id,
            username=user.username,
            email=user.email,
            phone_number=user.phone_number,
            role_id=user.role_id,
            status=user.status,
            password=user.password
        ) 
        for user in users
    ]
    # users_without_password = [
    #     UserWithoutPasswordBase(
    #         id=user.id,
    #         username=user.username,
    #         email=user.email,
    #         phone_number=user.phone_number,
    #         role_id=user.role_id,
    #         status=user.status
    #     ) 
    #     for user in users
    # ]
    return UserList(users=users)

@app.get("/user/current")
async def protected_route(user: be_models.User = Depends(get_current_user)):
    return {"message": "Access granted for user: {}".format(user.username), "user": user}

@app.get("/users/user_search/")
async def search_users(db: Session = Depends(get_db), search_string: str = None) -> UserList:
    if search_string:
        users = db.query(be_models.User).filter(
            (be_models.User.username.contains(search_string)) |
            (be_models.User.email.contains(search_string)) |
            (be_models.User.phone_number.contains(search_string))
        ).all()
    else:
        users = db.query(be_models.User).all()

    users = [
        UserBase(
            id=user.id,
            username=user.username,
            email=user.email,
            phone_number=user.phone_number,
            role_id=user.role_id,
            status=user.status,
            password=user.password
        ) 
        for user in users
    ]
    return UserList(users=users)

@app.get("/users/search/")
async def get_users_by_username(db: db_dependency, username: str = None) -> List[UserBase]:
    if username:
        users = db.query(be_models.User).filter(be_models.User.username.contains(username)).all()
        if not users:
            return []
    else:
        users = db.query(be_models.User).all()
    return users
    
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id:int , db: db_dependency):
    user = db.query(be_models.User).filter(be_models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    
    user_without_password = be_models.User(
        id=user.id,
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        role_id=user.role_id,
        status=user.status
    )

    return user_without_password

@app.put("/users/{user_id}/status", status_code=status.HTTP_200_OK)
async def update_user_status(user_id: int, status_update: UpdateUserStatus, db: db_dependency):
    user = db.query(be_models.User).filter(be_models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = status_update.status
    db.commit()
    return {"message": "User status updated successfully"}

@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(updated_user: UserBase, db: db_dependency):
    existing_user = db.query(be_models.User).filter(be_models.User.id == updated_user.id).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.username = updated_user.username
    existing_user.password = updated_user.password
    existing_user.email = updated_user.email
    existing_user.phone_number = updated_user.phone_number
    existing_user.role_id = updated_user.role_id
    existing_user.status = updated_user.status

    db.commit()

    user_without_password = be_models.User(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        phone_number=updated_user.phone_number,
        role_id=updated_user.role_id,
        status=updated_user.status
    )

    return {"user": user_without_password}

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: db_dependency):
    user = db.query(be_models.User).filter(be_models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "Delete user successfully!"}

@app.post("/roles/", status_code=status.HTTP_201_CREATED)
async def create_role(role: RoleBase, db: db_dependency):
    db_role = be_models.Role(**role.dict())
    db.add(db_role)
    db.commit()

@app.get("/roles/{role_id}", status_code=status.HTTP_200_OK)
async def get_role(role_id:int , db: db_dependency):
    role = db.query(be_models.Role).filter(be_models.Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found!")
    return role

@app.post("/models/", status_code=status.HTTP_201_CREATED)
async def create_model(model: ModelBase, db: db_dependency):
    db_model = be_models.Model(**model.dict())
    db.add(db_model)
    db.commit()

@app.get("/models/", status_code=status.HTTP_200_OK)
async def get_all_models(db: db_dependency) -> list[ModelBase]:
    mods = db.query(be_models.Model).all()
    return mods

@app.get("/models/search/")
async def get_models_by_name(db: db_dependency, name: str = None) -> List[ModelBase]:
    if name:
        mods = db.query(be_models.Model).filter(be_models.Model.name.contains(name)).all()
        if not mods:
            return []
    else:
        mods = db.query(be_models.Model).all()
    return mods

@app.put("/models/{classification_model_id}", status_code=status.HTTP_200_OK)
async def update_model(classification_model_id: int, updated_model: ModelBase, db: db_dependency):
    existing_model = db.query(be_models.Model).filter(be_models.Model.id == classification_model_id).first()
    if existing_model is None:
        raise HTTPException(status_code=404, detail="Model not found")

    # Update the existing model with the new information
    existing_model.name = updated_model.name
    existing_model.path = updated_model.path
    existing_model.accuracy = updated_model.accuracy
    existing_model.precision = updated_model.precision
    existing_model.recall = updated_model.recall
    existing_model.f1_score = updated_model.f1_score
    existing_model.model_type = updated_model.model_type
    existing_model.version = updated_model.version

    db.commit()

    return {"message": "Model updated successfully"}

@app.delete("/models/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model(model_id: int, db: db_dependency):
    existing_model = db.query(be_models.Model).filter(be_models.Model.id == model_id).first()
        
    if existing_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    if os.path.isfile(existing_model.path):
        os.remove(existing_model.path)

    db.delete(existing_model)
    db.commit()

    return {"message": "Model deleted successfully"}


@app.post("/history/", status_code=status.HTTP_201_CREATED)
async def create_history(hist: HistoryBase, db: db_dependency):
    db_history = be_models.History(**hist.dict())
    db.add(db_history)
    db.commit()

#async def get_all_history(db: db_dependency) -> list[HistoryBase]:
#    hist = db.query(be_models.History).all()
#    return hist
@app.get("/history/", status_code=status.HTTP_200_OK)
async def get_all_history(db: db_dependency):
    hist = db.query(be_models.History).all()
    
    result = []
    for h in hist:
        result.append({
            "id": h.id,
            "username": h.user.username,
            "classification_model_id": h.classification_model_id,
            "localization_model_id": h.localization_model_id,
            "input_img_path": h.input_img_path,
            "output_img_path": h.output_img_path,
            "label": h.label,
            "classification_accuracy": h.classification_accuracy,
            "creat_at": h.creat_at
        })
    return result

@app.get("/history/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_hist_by_user_id(user_id:int , db: db_dependency):
    hist = db.query(be_models.History).filter(be_models.History.user_id == user_id).all()

    result = []
    for history in hist:
        result.append({
            "id": history.id,
            "username": history.user.username,
            "classification_model_id": history.classification_model_id,
            "localization_model_id": history.localization_model_id,
            "input_img_path": history.input_img_path,
            "output_img_path": history.output_img_path,
            "label": history.label,
            "classification_accuracy": history.classification_accuracy,
            "creat_at": history.creat_at
        })
    return result

@app.get("/history/id/{id}", status_code=status.HTTP_200_OK)
async def get_hist_by_id(id:int , db: db_dependency):
    hist = db.query(be_models.History).filter(be_models.History.id == id).all()
    if hist is None:
        return []
    
    return hist


@app.post("/predict/")
async def create_prediction(user_id: int, classification_model_id: int, localization_model_id: int, db: db_dependency, input_image: UploadFile = File(...)):
    localization_model_selected = db.query(be_models.Model).filter(be_models.Model.id == localization_model_id).first()
    classification_model_selected = db.query(be_models.Model).filter(be_models.Model.id == classification_model_id).first()
    
    classification_model_loaded = load_model(classification_model_selected.path)
    if (classification_model_selected.model_type == "FORGERY CLASSIFICATION"):
        result = await forgery_image_predict(input_image, user_id, classification_model_id, localization_model_id, classification_model_loaded, localization_model_selected.path, db)
        return result
    if (classification_model_selected.model_type == "AI GENERATED CLASSIFICATION"):
        result = await ai_generated_predict(input_image, user_id, classification_model_id, localization_model_id, classification_model_loaded, localization_model_selected.path, db)
        return result

@app.get("/images/{type}/{image_filename}", response_class=FileResponse)
async def get_image(type: str, image_filename: str):
    dir = "D:\\dungnd\\GraduationProject\\server"
    image_path = os.path.join(dir, type, image_filename)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path)  
