FROM node:latest

WORKDIR /workspace/frontend

COPY --chown=node:node frontend/package*.json ./

RUN npm install

COPY --chown=node:node frontend/ /workspace/frontend/

USER node

EXPOSE 3000

CMD ["npm", "start"]
