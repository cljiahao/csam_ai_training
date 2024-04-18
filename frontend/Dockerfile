FROM node:lts-alpine3.19 as base
WORKDIR /app
COPY ./package*.json ./

FROM base as prod
RUN npm ci
COPY ./ ./
COPY ./node_modules/react-scripts/config/webpack.config.js ./node_modules/react-scripts/config/webpack.config.js
RUN npm run build
CMD ["node", "index"]

# Development specific setup
FROM base as dev
RUN npm install -g nodemon && npm install
COPY ./ ./
CMD ["nodemon", "app"]