# [Backstage](https://backstage.io)

To start the app, cd to the backstage directory and run:

```sh
yarn install
```
## Prerequisites
You will need environment variables:
```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
NODE_OPTIONS=--no-node-snapshot
```

`NODE_OPTIONS=--no-node-snapshot` is vital when running this application with node 20 or higher. Check your node version with `node --version`. You can use nvm (node version manager) to upgrade/downgrade.

Simply run a PostgreSQL docker container, with the default user ('postgres') for super user privileges. Password, host and port are configurable.

You will need a Github Token to let Backstage create new repositories in your account. To do that:
1. Go to 'Settings'
2. Scroll all the way down to 'Developer Settings'.
3. Go to 'Personal Access Tokens'.
4. Create a classic token with 'repo' privileges.
5. Save it, you will need it later. 

Finally, you need a way to run the start command with environmental variables. We recommend using `dotenv-cli`. Install it by running:
```sh
yarn global add dotenv-cli
```
Then start the application:
```sh
dotenv yarn start
```

## Creating a Keycloak template

Once the app is running:
1. Authenticate as Guest.
2. Navigate to 'Create' on the sidebar.
3. Follow the steps to create a Keycloak Authentication Block.
4. It is expected to fail the last stage 'Register in Backstage Catalog'. As long as the first two stages passed, you will find the new repo you created in your Github.