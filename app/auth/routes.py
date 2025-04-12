from fastapi import APIRouter , HTTPException, Request, status,Response
from app.config import Config
from app.auth.utils import create_session_token, hash_password, verify_password
from app.models.user_model import UserCreate, UserLogin
from fastapi.responses import JSONResponse




router = APIRouter()

@router.post("/register")
async def register_user(user:UserCreate , request:Request):
    """
    Register a new user in the database.
    """
    ## Get the database from the request state 
    try:
        db = request.app.state.database
        # check if the user already exists
        existing_user = await db.users.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exists")
        # Hash the password
        hashed_password = hash_password(user.password)
        # Create the user in the database
        new_user = {
            "username": user.username,
            "email": user.email,
            "password": hashed_password
        }
        await db.users.insert_one(new_user)
        # Return the response
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User created successfully"})
    except Exception as e:
        print(f"Error registering user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.post("/login")
async def login_user(user:UserLogin , request:Request , response:Response):
    """
    Login a user and create a session token.
    """
    try:
        db = request.app.state.database
        # Check if the user exists
        is_user_existed = await db.users.find_one({"email": user.email})
        if not is_user_existed:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
        # Verify the password
        is_password_verified = verify_password(user.password, is_user_existed["password"])
        if not is_password_verified:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        # Create a session token
        token = create_session_token({"email": user.email})
        # Set the session token in the cookies
        response = JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Login successful"})
        if Config.SESSION_COOKIE_NAME is not None:
             response.set_cookie(key=Config.SESSION_COOKIE_NAME, value=token, httponly=True, max_age=3600)
        # Return the response
        return response
    except Exception as e:
        print(f"Error logging in user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/logout")
def logout_user(request:Request , response:Response):
    """
    Logout a user and remove the session token.
    """
    try:
        # Remove the session token from cookies
        if Config.SESSION_COOKIE_NAME is not None:
            response.delete_cookie(key=Config.SESSION_COOKIE_NAME)
        # Return the response
        return Response(status_code=status.HTTP_200_OK, content={"message":"Logout successful"})
    except Exception as e:
        print(f"Error logging out user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.get("/me")
def get_current_user(request: Request):
    """
    Get the current logged-in user.
    """
    if not request.state.user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return {"user": request.state.user}