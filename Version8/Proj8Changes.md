# Version 8 Changes
## User System
### Guest Functionality
The guest functionality is now functioning, as users can click the log-in as guest button on the sign in page and get recommendations instantly, no setup required. Also, guests are no longer allowed to leave reviews, and the option no longer displays on the home page. This is for security and anti-spam purposes.

### Search Filtering
Now users are able to search for movies by actor, director, genre, and title! Before, the only method to find a movie in our database was by its title, but now if you would like to search only for Christopher Nolan movies, you can do so!

Details on these additions can be found here: [Search Page](https://github.com/CSC-510-Group-5/BingeSuggest/blob/master/docs/frontend.md#search-page)

### Streaming Service Integration
Once you have your list of recommended movies, you'll want to get watching as soon as possible. Instead of having to google search around for where to watch your new movie, we provide that for you! For every recommendation, we provide all of the available streaming locations directly to you, so you can get watching immediately!

Details on these additions can be found here: [Search Page](https://github.com/CSC-510-Group-5/BingeSuggest/blob/master/docs/frontend.md#watchlistjs)

### Watch history
Users can view all of their previously watched movies and delete movies as required.

Details on these additions can be found here: [Search Page](https://github.com/ychen-207523/BingeSuggest/blob/master/docs/frontend.md#watched_historyjs)

### Dockerization
BingeSuggest has been containerized, so it is deployable to any platform and there is no need for development tools to be installed to run it! For both developers and users, this change makes BingeSuggest more accessible and error-free.


### Database
#### Startup Functionality
Users no longer have to manually download and initialize the massive movie database that BingeSuggest uses, this is done on startup! This feature saves time, energy, and frustration.

## Documentation
Documentation for installation has been updated, with the new API keys required and simplified setup steps.
