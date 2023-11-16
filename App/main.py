from fastapi import FastAPI, Depends, HTTPException, status
from . import models, schema
from .database import engine, get_db
from sqlalchemy.orm import Session
import csv

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/top-players', response_model=schema.GetPlayers)
async def get_players(db: Session = Depends(get_db)):
    usernames_tuples = (
        db.query(models.PlayerRatingHistory.username).all()
    )
    """
    The output you're seeing, containing tuples with single elements like ('Himanshu',), 
    is because SQLAlchemy's query().all() method returns 
    results as a list of tuples when querying for specific columns. Each tuple corresponds 
    to a row in the result, and in this case, each tuple 
    contains a single element - the value of the username column.
    To transform this list of tuples into a list of strings (where each string represents a username), 
    you can use list comprehension or other methods to extract the string value from each tuple.

    """
    usernames = [
        username_tuple[0]  # Extract the first (and only) element from each tuple
        for username_tuple in usernames_tuples
    ]
    print(usernames)
    return {"usernames": usernames}


@app.get('/player/{username}/rating-history')
async def get_player_history(username: str, db: Session = Depends(get_db)):
    rating_history = (db.query(models.PlayerRatingHistory.rating_history)
                      .filter(models.PlayerRatingHistory.username == username)).first()
    if not rating_history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the rating for player with username: {username} does not exist')
    print(rating_history)
    parsed_rating_history = rating_history[0] if rating_history[0] else {}
    return {"GetScore": parsed_rating_history}


@app.get('/players/rating-history-csv')
async def get_players_rating_history_csv(db: Session = Depends(get_db)):
    top_50_players = (
        db.query(models.PlayerRatingHistory.username, models.PlayerRatingHistory.rating_history)
        .order_by(models.PlayerRatingHistory.id)
        .limit(50)
        .all()
    )

    # Prepare CSV data
    csv_data = [["Username", "Rating History"]]  # Header row
    for username, rating_history in top_50_players:
        # Append a row for each player containing username and rating_history
        csv_data.append([username, rating_history])

    # Write data to a CSV file
    with open('player_ratings.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    # Return a response indicating success or the file URL if serving the file
    return {"message": "CSV file generated successfully"}
