from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from apps.blogs import schemas, models
from helpers.response import ResponseHandler
from sqlalchemy.exc import SQLAlchemyError



class BlogView(ResponseHandler):
    def __init__(self):
        super().__init__()  # Initialize the parent ResponseHandler class
        self.router = APIRouter()  # Create a router for this view
        
        # Add routes to the router
        self._register_routes()

    def _register_routes(self):
        """Private method to add API routes."""
        self.router.add_api_route("/blogs", self.read_blogs, methods=["GET"], tags=["Blogs"])
        self.router.add_api_route("/blogs/{blog_id}", self.read_blog, methods=["GET"], tags=["Blogs"])
        self.router.add_api_route("/blogs", self.create_or_update_blog, methods=["POST"], tags=["Blogs"])

    async def read_blogs(self, db: Session = Depends(get_db)):
        """Endpoint to retrieve all blogs."""
        try:
            blogs = db.query(models.Blog).all()
            return self.response_info(message="Blogs fetched successfully", data=blogs)
        except Exception as e:
            return self.response_info(status=False, status_code=500, message="An error occurred", errors=str(e))

    async def read_blog(self, blog_id: int, db: Session = Depends(get_db)):
        """Endpoint to retrieve a single blog by ID."""
        try:
            blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
            if not blog:
                return self.response_info(status=False, status_code=404, message="Blog not found")
            return self.response_info(message="Blog fetched successfully", data=blog)
        except Exception as e:
            return self.response_info(status=False, status_code=500, message="An error occurred", errors=str(e))


    async def create_or_update_blog(self,blog: schemas.BlogCreate, db: Session = Depends(get_db)):
        try:
            if blog.instance_id is not None:
                instance = db.query(models.Blog).filter(models.Blog.id == blog.instance_id).first()
                if instance:
                    instance.title = blog.title
                    instance.content = blog.content
                    db.commit()
                    db.refresh(instance)
                    return self.response_info(status=True, status_code=201,message="Blog Updated successfully", data=instance)
                else:
                    # If instance_id is provided but instance is not found, return an error
                    return self.response_info(status=False, status_code=404,message="Blog not found")
            else:
                # Create a new blog
                instance = models.Blog()
                instance.title = blog.title
                instance.content = blog.content
                db.add(instance)
                db.commit()
                db.refresh(instance)
                return self.response_info(status=True, status_code=201,message="Blog created successfully", data=instance)
            
        except SQLAlchemyError as e:
            db.rollback()
            # Handle specific database errors if necessary
            return self.response_info(status=False, status_code=500,message="Something went wrong", errors=str(e))
