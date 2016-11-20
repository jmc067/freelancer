# Freelancer Backend API
Backend Application to offer account management, authentication, location tracking, location based search, peer to peer messaging, inbox notifications, job offer/acceptance workflow, and payment solution.

## Getting Started 
1.  `cd freelancer`
2.  Build docker-compose
	- `docker-compose build .`
3.  Run docker-compose
	- `docker-compose up`
4.  Make sure its running
	- `docker ps -a`
5.  Resources
	- http://containertutorials.com/docker-compose/flask-simple-app.html
	- https://docs.docker.com/machine/get-started/


## Routes
### Account Management Routes
- `POST /user/signup`  <- Creates user
- `POST /user/:user_id`    <- Updates user by id
- `GET /user/:user_id`     <- Returns the user by id
- `DELETE /user/:user_id`  <- Deletes user by id
- `GET /users/search`    <- Returns list of users by query

### Category Management Routes
- `POST /category/new`  <- Creates a new category (or sub-category)
- `POST /category/:category_id`    <- Updates category by id
- `GET /category/:category_id`     <- Gets the category by id
- `DELETE /category/:category_id`  <- Deletes category by id and all subcategories associated with it
- `GET /category/search`    <- Gets list of categories by query

### Subcategory Management Routes
- `POST /subcategory/new`  <- Creates a new subcategory (or sub-subcategory)
- `POST /subcategory/:subcategory_id`    <- Updates subcategory by id
- `GET /subcategory/:subcategory_id`     <- Gets the subcategory by id
- `DELETE /subcategory/:subcategory_id`  <- Deletes subcategory by id
- `GET /subcategory/search`    <- Gets list of categories by query

### Authentication Routes
- `POST /login`    <- Returns scramble token upon valid authorize (email/password).  Stores active session in Redis
- `POST /logout`   <- Removes active session in Redis
- `POST /extend`   <- Extends TTL of redis session
- `check_authorization` <- Check session scramble before each route

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
	"role":Array(CLIENT,WORKER,ADMIN)
	"email":String,
	"salted_password":<BCRYPT>,
	"photo":<image>
}
```
### Category
```
{
	"_id":<BSON::ObjectID>,
	"name":String,
	"description":String
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
1.  Each request should extend ttl on user scramble token
2.  User scramble token should have a 1-to-1 relationship with the user.  aka lookup from scramble token to user.  Each user should have their own scramble token on their account.
3.  POST Job Routes should send automated message to user's inbox to notify the change
	- REQUESTED,ACCEPTED,DECLINED each have separate messaging workflows
4.  Make sure user has picture before allowing ACCEPT.  Warn client about picture when REQUESTED
5.  Convert from Flask to Flastk/Gunicorn 
	- Check out http://matthewminer.com/2015/01/25/docker-dev-environment-for-web-app.html
6.  Add Oauth2
7.  `export DEBUG=true` to see logs
8.  Refactor to use classes
9.  Refactor authorization/session out of user.py




