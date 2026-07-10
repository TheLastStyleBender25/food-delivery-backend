from app.db.session import SessionLocal


async def get_db():          # async function (non-blocking)
    async with SessionLocal() as db:   # opens a DB session
        yield db             # gives session to the route, then comes back to close it
        #Pauses the function and sends db to the route handler
        #After the route finishes, comes back here to clean up
