from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Enum, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Follower(db.Model):
    __tablename__ = "follower"
    user_from_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True)

    def __str__(self):
        return f"{self.user_from_id} → {self.user_to_id}"

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }

class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")
    media_items: Mapped[list["Media"]] = relationship(back_populates="post")

    def __str__(self):
        if self.user:
            return f"Post {self.id} by {self.user.username}"
        return f"Post {self.id}"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }


class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

    def __str__(self):
        author_name = self.author.username if self.author else self.author_id
        return f"Comment {self.id} by {author_name}"

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }


class Media(db.Model):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(
        Enum("image", "video", name="media_type"))
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    post: Mapped["Post"] = relationship(back_populates="media_items")

    def __str__(self):
        return f"{self.type} {self.id} for Post {self.post_id}"

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id,
        }
    
class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")
    followers: Mapped[list["Follower"]] = relationship(
        foreign_keys=[Follower.user_to_id], backref="followed"
    )
    following: Mapped[list["Follower"]] = relationship(
        foreign_keys=[Follower.user_from_id], backref="follower"
    )

    character_favorites: Mapped[list["UserCharacterFavorite"]] = relationship(back_populates="user")
    planet_favorites: Mapped[list["UserPlanetFavorite"]] = relationship(back_populates="user")

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }


class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(20), nullable=False)
    population: Mapped[str] = mapped_column(String(20), nullable=False)
    orbital_period: Mapped[str] = mapped_column(String(20), nullable=False)
    rotation_period: Mapped[str] = mapped_column(String(20), nullable=False)
    diameter: Mapped[str] = mapped_column(String(20), nullable=False)

    favorites: Mapped[list["UserPlanetFavorite"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter
        }
    
class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    height: Mapped[str] = mapped_column(String(20), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(20), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(20), nullable=False)

    favorites: Mapped[list["UserCharacterFavorite"]] = relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color
        }
    
class UserCharacterFavorite(db.Model):
    __tablename__ = "userCharacterFavorite"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))

    user: Mapped["User"] = relationship(back_populates="character_favorites")
    character: Mapped["Character"] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }

class UserPlanetFavorite(db.Model):
    __tablename__ = "userPlanetFavorite"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))

    user: Mapped["User"] = relationship(back_populates="planet_favorites")
    planet: Mapped["Planet"] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }