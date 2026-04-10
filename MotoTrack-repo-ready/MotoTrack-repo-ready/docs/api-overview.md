# MotoTrack API Overview

## Authentication

### POST `/api/auth/register`
Creates a new user account.

### POST `/api/auth/login`
Authenticates a user and returns a JWT.

## Motorcycles

### GET `/api/motorcycles`
Returns all motorcycles owned by the authenticated user.

### POST `/api/motorcycles`
Creates a motorcycle profile.

### GET `/api/motorcycles/<id>`
Returns one motorcycle owned by the authenticated user.

### PUT `/api/motorcycles/<id>`
Updates a motorcycle profile.

### DELETE `/api/motorcycles/<id>`
Deletes a motorcycle profile.

## Maintenance Logs

### GET `/api/maintenance/motorcycle/<motorcycle_id>`
Returns all maintenance logs for a motorcycle.

### POST `/api/maintenance`
Creates a maintenance log.

### PUT `/api/maintenance/<log_id>`
Updates a maintenance log.

### DELETE `/api/maintenance/<log_id>`
Deletes a maintenance log.

## Dashboard

### GET `/api/dashboard`
Returns dashboard data including recent logs and services currently due.
