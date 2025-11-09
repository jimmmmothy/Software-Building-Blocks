# [Backstage](https://backstage.io)

## Prerequisites
First, cd to the `backstage/` directory. All the following commands must be executed there.

### Environment variables
You will need environment variables. Place them in `backstage/` directory:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<your password>
POSTGRES_HOST=<your host (http://localhost)>
POSTGRES_PORT=<your port (5432)>
NODE_OPTIONS=--no-node-snapshot
GITHUB_TOKEN=<your GH token>
```
`NODE_OPTIONS=--no-node-snapshot` is vital when running this application with node 20 (recommended). Check your node version with `node --version`. You can use [nvm](https://github.com/nvm-sh/nvm?tab=readme-ov-file#intro) (node version manager) to upgrade/downgrade.

### Database
Run a PostgreSQL docker container, with the default user ('postgres') for super user privileges. Password, host and port are configurable. Suggestion ↓.
```sh
docker run --name backstage-postgres -e POSTGRES_PASSWORD=<your password> -p <your port>:5432 -v postgres_data:/var/lib/postgresql/data -d postgres
```

### GitHub Access Token
You will need a Github Token to let Backstage create new repositories in your account. To do that:
1. Go to your github and navigate to 'Settings' > 'Developer Settings' > 'Personal Access Tokens' or click [here](https://github.com/settings/tokens).
2. Generate a **classic** token with 'repo' privileges (it should look like `ghp_...`).
3. Save it in the .env file. 

## Run the application
Finally, you need a way to run the start command with environmental variables. We recommend using `dotenv-cli`. Install it by running:
```sh
npm install -g dotenv-cli
```
Then start the application:
```sh
yarn install
dotenv yarn start
```

## Creating a Keycloak template

Once the app is running:
1. Authenticate with your GitHub account.
2. Navigate to 'Create' on the sidebar.
3. Follow the steps to create a 'Keycloak Authentication Block'.
4. Once you finish, go back to the catalog page, refresh (maybe a few times, try switching 'Kind' filter back and forth to Component) you will find the new building block you created. If you press on it you can find a link to the new source repo.