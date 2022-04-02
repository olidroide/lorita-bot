FROM --platform=$BUILDPLATFORM node:lts-buster-slim AS base
RUN apt-get update && apt-get install libssl-dev ca-certificates -y
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /lorita-bot/frontend

COPY ./frontend/package.json ./

FROM base as build
RUN export NODE_ENV=production
RUN yarn

COPY ./frontend .
RUN yarn build


FROM base as prod-build

RUN yarn install --production
RUN cp -R node_modules prod_node_modules

FROM base as prod

COPY --from=prod-build /lorita-bot/frontend/prod_node_modules /lorita-bot/frontend/node_modules
COPY --from=build  /lorita-bot/frontend/.next /lorita-bot/frontend/.next
COPY --from=build  /lorita-bot/frontend/public /lorita-bot/frontend/public

EXPOSE 3000
CMD ["yarn", "start"]