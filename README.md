# Freelancer Backend API
Backend Application to offer account management, authentication, location tracking, location based search, peer to peer messaging, inbox notifications, job offer/acceptance workflow, and payment solution.

## Getting Started 
2.  Build docker image (or use pre-built image)
	- `docker build -t flask-sample-one:latest .`
3.  Run docker container using image
	- `docker run -d -p 5000:5000 flask-sample-one
4.  Make sure its running
	- `docker ps -a`
5.  Resources
	- http://containertutorials.com/docker-compose/flask-simple-app.html
	- https://docs.docker.com/machine/get-started/


## Routes
### Account Management Routes
- `POST /signup`  <- Creates user
- `POST /user`    <- Updates user by id
- `GET /user`     <- Gets the user by id
- `DELETE /user`  <- Deletes user by id
- `GET /users`    <- Gets list of users by query

### Authentication Routes
- `POST /authorize`    <- Returns access token upon valid authorize (email/password).  Logs active session in Redis Geospacial
- `POST /authorize`    <- Returns access token upon valid authorize (email/password).  Removes active session in Redis Geospacial


### Location Routes
- `POST /location`  <- Stores user by id and location and ttl into Redis geodata 
- `GET /search`   <- Gets all users by location and radius 

### Messenger Routes
- `GET /inbox`   <- Gets inbox for user id
- `POST /send`  <- Sends and stores message into inbox for user id

### Ledger Routes
- `POST /job`   <- Creates or Updates Job by id
- `GET /jobs`   <- Gets jobs for query
- `POST /job/:id/status` <- Updates job status by job id

### Payment - TBD

# Integrations
- MongoDB
- Redis
- Stripe Payment Solutions
- OAuth
- Bcrypt

# Database Collections
### Account
```
{
	"_id":<BSON::ObjectID>,
	"first_name":String,
	"last_name":String,
	"inbox_id":<BSON::ObjectID>,
	"ledger_id":<BSON::ObjectID>,
	"roles":Array(CLIENT,WORKER,ADMIN)
	"email":String,
	"salted_password":<BCRYPT>,
	"token":<OAUTH_TOKEN>
}
```
### Inbox
```
{
	"_id":<BSON::ObjectID>,
	"user_id"<BSON::ObjectID>,
	"messages":Array(<Message>)
}
```
### Message
```
{
	"text":String,
	"from":<BSON::ObjectID>,
	"timestamp":Date
}
```
### Ledger
```
{
	"_id":<BSON::ObjectID>,
	"title":String,
	"description":String,
	"logs":Array(<Entry>)
}
```
### Entry
```
{
	"status":String(REQUESTED,ACCEPTED,DECLINED,STARTED,COMPLETED,PENDING_PAYMENT,PAID),
	"description":String,
	"status_log":Array(<Status>)
}
```



# Cache Keys
### Location
`token : <GEOSPATIAL LAT/LONG COORDINATES>`

# Feature Adds (Not included in current scope)
- Administrative Privledges
	- Create Admin, Update Users, Delete Users
	- Create, Read, Update, and Delete Categories
- Notification System
	- SMS, Push Notification, Email
- Email Integration
	- Forgot Password
	- Email Confirmation on sign up
- Messenger Upgrades
	- Instant Messaging
	- Paginated Inbox Responses (reduce network io for large conversations) 
- Job Workflow Upgrades
	- Expiration on job offers
	- Job alerting
	- Location tracking
- Payment Upgrades
	- Funds Escrow
- Account Upgrades
	- Account Reviews


# Notes
1.  Each request should extend ttl on user access token
2.  User access token should have a 1-to-1 relationship with the user.  aka lookup from access token to user.  Each user should have their own access token on their account.
3.  POST Job Routes should send automated message to user's inbox to notify the change
	- REQUESTED,ACCEPTED,DECLINED each have separate messaging workflows
4.  Make sure user has picture before allowing ACCEPT.  Warn client about picture when REQUESTED
5.  Convert from Flask to Flastk/Gunicorn 
	- Check out http://matthewminer.com/2015/01/25/docker-dev-environment-for-web-app.html
6.  Add Oauth2
7.  `export DEBUG=true` to see logs


# Questions
1.  Are there UI Designs? UX Workflow? Product Specs? 
2.  What is the request/accept workflow?  Preferred? MVP? 
3.  Database Preference?  Why MySQL?
4.  Language Preference?  Why Javascritpt?
5.  Have the Android or iOS projects started yet? How does collaboration happen? Technical Lead?
6.  Web solution to start? 
7.  Which payment solutions did you have in mind? 
8.  Timeline?




