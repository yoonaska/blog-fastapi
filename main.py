from fastapi import FastAPI
from apps.blogs.views import CreateOrUpdateBlogView, DeleteBlogView, GetBlogsPaginatedView, GetBlogsApiView
from database import engine, Base


app = FastAPI(
    title="Blog Management",
    description="This is a fantastic project that exposes a blog API.",
    version="1.0.0",

)

Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(GetBlogsApiView().router, prefix="/get-blogs")
app.include_router(GetBlogsPaginatedView().router, prefix="/get-blogs")
app.include_router(CreateOrUpdateBlogView().router, prefix="/create-or-update-blog")
app.include_router(DeleteBlogView().router, prefix="/delete-blog")
