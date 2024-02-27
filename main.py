from fastapi import FastAPI
from apps.blogs.views import BlogView
from database import engine, Base


app = FastAPI(
    title="Blog Management",
    description="This is a fantastic project that exposes a blog API.",
    version="1.0.0",

)

Base.metadata.create_all(bind=engine)

blog_view = BlogView()
app.include_router(blog_view.router, prefix="/api/v1")
