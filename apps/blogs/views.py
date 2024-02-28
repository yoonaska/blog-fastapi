from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from apps.blogs import schemas, models
from apps.blogs.models import Blog
from helpers.response import ResponseHandler
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional


class BlogView(ResponseHandler):
    def __init__(self):
        super().__init__()  # Initialize the parent ResponseHandler class
        self.router = APIRouter()  # Create a router for this view

        # Add routes to the router
        self._register_routes()

    def _register_routes(self):
        """Private method to add API routes."""
        self.router.add_api_route("/blogs", self.read_blogs, methods=["GET"], tags=["Blogs"])
        self.router.add_api_route("/blogs-paginated-view", self.get_all_blogs, methods=["GET"], tags=["Blogs"])
        self.router.add_api_route("/create-or-update", self.create_or_update_blog, methods=["POST"], tags=["Blogs"])
        self.router.add_api_route("/delete-blogs/{blog_id}", self.delete_blog, methods=["DELETE"], tags=["Blogs"])  # Register the delete endpoint

    async def read_blogs(self, db: Session = Depends(get_db), blog_id: Optional[int] = None, title: Optional[str] = None):
        """Endpoint to retrieve all blogs or filter by id and/or title."""
        try:
            query = db.query(Blog)
            
            if blog_id is not None:
                query = query.filter(Blog.id == blog_id)
            
            if title is not None:
                query = query.filter(Blog.title.contains(title))
            
            blogs = query.all()
            return self.response_info(message="Blogs fetched successfully", data=blogs)
            
        except Exception as e:
            return self.response_info(status=False, status_code=500, message="An error occurred", errors=str(e))
        
        
    async def get_all_blogs(self, db: Session = Depends(get_db), page: Optional[int] = 1, page_size: Optional[int] = 10):
        """Endpoint to retrieve all blogs with pagination."""
        try:
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Fetch paginated blogs
            blogs_query = db.query(Blog).offset(offset).limit(page_size)
            blogs = blogs_query.all()

            # Optionally, calculate total number of records and total pages
            total_records = db.query(Blog).count()
            total_pages = (total_records // page_size) + (0 if total_records % page_size == 0 else 1)

            # Prepare the paginated response
            paginated_response = {
                "data": blogs,
                "total_records": total_records,
                "total_pages": total_pages,
                "current_page": page,
                "page_size": page_size
            }

            return self.response_info(message="Blogs fetched successfully", data=paginated_response)
        
        except Exception as e:
            return self.response_info(status=False, status_code=500, message="An error occurred", errors=str(e))

        
    async def create_or_update_blog(self,blog: schemas.BlogCreate, db: Session = Depends(get_db)):
        try:
            if blog.instance_id is not None:
                instance = db.query(Blog).filter(Blog.id == blog.instance_id).first()
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


    async def delete_blog(self, blog_id: int, db: Session = Depends(get_db)):
            """Endpoint to delete a blog by ID."""
            try:
                blog = db.query(Blog).filter(Blog.id == blog_id).first()
                
                if not blog:
                    return self.response_info(status=False, status_code=404, message="Blog not found")
                
                db.delete(blog)
                db.commit()
                return self.response_info(status=True, status_code=200, message="Blog deleted successfully")
            
            except SQLAlchemyError as e:
                db.rollback()
                return self.response_info(status=False, status_code=500, message="Something went wrong", errors=str(e))


