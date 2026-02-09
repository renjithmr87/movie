# API Documentation

This document describes the REST API endpoints for the Movie Database application.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

Currently, the API does not require authentication. For production, consider adding:
- Token-based authentication
- OAuth2
- JWT tokens

## Endpoints

### Movies

All movie-related operations.

#### List Movies

Retrieve a paginated list of all movies.

**Endpoint:** `GET /api/movies/`

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Results per page (default: 10)

**Response:** `200 OK`

```json
{
  "count": 25,
  "next": "http://localhost:8000/api/movies/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "The Shawshank Redemption",
      "director": "Frank Darabont",
      "genre": "Drama",
      "year": 1994,
      "description": "Two imprisoned men bond over a number of years...",
      "rating": "9.3",
      "duration": 142,
      "created_at": "2024-02-09T12:00:00Z",
      "updated_at": "2024-02-09T12:00:00Z"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/api/movies/
```

---

#### Create Movie

Create a new movie.

**Endpoint:** `POST /api/movies/`

**Request Body:**
```json
{
  "title": "Movie Title",
  "director": "Director Name",
  "genre": "Genre",
  "year": 2024,
  "description": "Movie description",
  "rating": 8.5,
  "duration": 120
}
```

**Required Fields:**
- `title` (string, max 200 characters)
- `director` (string, max 100 characters)
- `genre` (string, max 50 characters)
- `year` (integer)
- `rating` (decimal, 0-10)
- `duration` (integer, in minutes)

**Optional Fields:**
- `description` (text)

**Response:** `201 Created`

```json
{
  "id": 2,
  "title": "Movie Title",
  "director": "Director Name",
  "genre": "Genre",
  "year": 2024,
  "description": "Movie description",
  "rating": "8.5",
  "duration": 120,
  "created_at": "2024-02-09T13:00:00Z",
  "updated_at": "2024-02-09T13:00:00Z"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/movies/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Inception",
    "director": "Christopher Nolan",
    "genre": "Sci-Fi",
    "year": 2010,
    "rating": 8.8,
    "duration": 148,
    "description": "A thief who steals corporate secrets..."
  }'
```

---

#### Retrieve Movie

Get details of a specific movie.

**Endpoint:** `GET /api/movies/{id}/`

**Path Parameters:**
- `id` (integer): Movie ID

**Response:** `200 OK`

```json
{
  "id": 1,
  "title": "The Shawshank Redemption",
  "director": "Frank Darabont",
  "genre": "Drama",
  "year": 1994,
  "description": "Two imprisoned men bond over a number of years...",
  "rating": "9.3",
  "duration": 142,
  "created_at": "2024-02-09T12:00:00Z",
  "updated_at": "2024-02-09T12:00:00Z"
}
```

**Error Response:** `404 Not Found`

```json
{
  "detail": "Not found."
}
```

**Example:**
```bash
curl http://localhost:8000/api/movies/1/
```

---

#### Update Movie (Full)

Update all fields of a movie.

**Endpoint:** `PUT /api/movies/{id}/`

**Path Parameters:**
- `id` (integer): Movie ID

**Request Body:**
```json
{
  "title": "Updated Title",
  "director": "Updated Director",
  "genre": "Updated Genre",
  "year": 2024,
  "description": "Updated description",
  "rating": 9.0,
  "duration": 130
}
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "title": "Updated Title",
  "director": "Updated Director",
  "genre": "Updated Genre",
  "year": 2024,
  "description": "Updated description",
  "rating": "9.0",
  "duration": 130,
  "created_at": "2024-02-09T12:00:00Z",
  "updated_at": "2024-02-09T14:00:00Z"
}
```

**Example:**
```bash
curl -X PUT http://localhost:8000/api/movies/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Shawshank Redemption",
    "director": "Frank Darabont",
    "genre": "Drama",
    "year": 1994,
    "rating": 9.5,
    "duration": 142,
    "description": "Updated description"
  }'
```

---

#### Update Movie (Partial)

Update specific fields of a movie.

**Endpoint:** `PATCH /api/movies/{id}/`

**Path Parameters:**
- `id` (integer): Movie ID

**Request Body:** (only include fields to update)
```json
{
  "rating": 9.5,
  "description": "Updated description only"
}
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "title": "The Shawshank Redemption",
  "director": "Frank Darabont",
  "genre": "Drama",
  "year": 1994,
  "description": "Updated description only",
  "rating": "9.5",
  "duration": 142,
  "created_at": "2024-02-09T12:00:00Z",
  "updated_at": "2024-02-09T14:30:00Z"
}
```

**Example:**
```bash
curl -X PATCH http://localhost:8000/api/movies/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 9.5
  }'
```

---

#### Delete Movie

Delete a movie.

**Endpoint:** `DELETE /api/movies/{id}/`

**Path Parameters:**
- `id` (integer): Movie ID

**Response:** `204 No Content`

**Error Response:** `404 Not Found`

```json
{
  "detail": "Not found."
}
```

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/movies/1/
```

---

## Error Responses

### 400 Bad Request

Returned when the request data is invalid.

```json
{
  "title": ["This field is required."],
  "year": ["Ensure this value is greater than or equal to 1888."]
}
```

### 404 Not Found

Returned when the requested resource doesn't exist.

```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error

Returned when there's a server error.

```json
{
  "detail": "Internal server error."
}
```

## Data Models

### Movie

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | auto | Unique identifier |
| title | string | yes | Movie title (max 200 chars) |
| director | string | yes | Director name (max 100 chars) |
| genre | string | yes | Movie genre (max 50 chars) |
| year | integer | yes | Release year |
| description | text | no | Movie description |
| rating | decimal | yes | Rating (0.0-10.0) |
| duration | integer | yes | Duration in minutes |
| created_at | datetime | auto | Creation timestamp |
| updated_at | datetime | auto | Last update timestamp |

## Pagination

The API uses page number pagination:

**Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Results per page (default: 10, max: 100)

**Response Format:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/movies/?page=3",
  "previous": "http://localhost:8000/api/movies/?page=1",
  "results": [...]
}
```

**Example:**
```bash
curl "http://localhost:8000/api/movies/?page=2&page_size=20"
```

## Response Format

All successful responses return JSON with appropriate HTTP status codes:

- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Validation error
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Testing the API

### Using cURL

See examples above for each endpoint.

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000/api"

# List movies
response = requests.get(f"{BASE_URL}/movies/")
print(response.json())

# Create movie
movie_data = {
    "title": "Test Movie",
    "director": "Test Director",
    "genre": "Drama",
    "year": 2024,
    "rating": 8.0,
    "duration": 120
}
response = requests.post(f"{BASE_URL}/movies/", json=movie_data)
print(response.json())

# Get specific movie
movie_id = 1
response = requests.get(f"{BASE_URL}/movies/{movie_id}/")
print(response.json())

# Update movie
update_data = {"rating": 9.0}
response = requests.patch(f"{BASE_URL}/movies/{movie_id}/", json=update_data)
print(response.json())

# Delete movie
response = requests.delete(f"{BASE_URL}/movies/{movie_id}/")
print(response.status_code)  # 204
```

### Using JavaScript Fetch

```javascript
const BASE_URL = "http://localhost:8000/api";

// List movies
fetch(`${BASE_URL}/movies/`)
  .then(response => response.json())
  .then(data => console.log(data));

// Create movie
fetch(`${BASE_URL}/movies/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: "Test Movie",
    director: "Test Director",
    genre: "Drama",
    year: 2024,
    rating: 8.0,
    duration: 120
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Web Interface

In addition to the REST API, the application provides a web interface:

- **Home:** `http://localhost:8000/` - List all movies
- **Create:** `http://localhost:8000/create/` - Create new movie
- **Detail:** `http://localhost:8000/{id}/` - View movie details
- **Update:** `http://localhost:8000/{id}/update/` - Edit movie
- **Delete:** `http://localhost:8000/{id}/delete/` - Delete movie
- **Admin:** `http://localhost:8000/admin/` - Django admin panel

## API Browser

Django REST Framework provides a browsable API interface. Access it at:

```
http://localhost:8000/api/movies/
```

This interface allows you to:
- View and test all endpoints
- Make requests directly from the browser
- See request/response formats
- Test authentication (if enabled)

## Rate Limiting

Currently, there is no rate limiting. For production, consider implementing:
- Throttling rules
- API keys
- Per-user limits

## Future Enhancements

Planned improvements:
- Search and filtering
- Sorting options
- Authentication and authorization
- User-specific movie lists
- Movie ratings and reviews
- Image upload for movie posters
- Bulk operations
- Export to CSV/JSON
