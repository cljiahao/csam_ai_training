FROM node:lts-alpine3.19 as base
WORKDIR /app
COPY ./package*.json ./
ARG REACT_APP_API
ENV REACT_APP_API $REACT_APP_API

FROM base as prod
RUN npm ci
COPY ./ ./
COPY ./webpack.config.js ./node_modules/react-scripts/config/webpack.config.js
RUN npm run build
ENTRYPOINT npx react-inject-env set && node index
CMD ["node", "index"]

# Development specific setup
FROM base as dev
RUN npm install -g nodemon && npm install
COPY ./ ./
CMD ["nodemon", "app"]