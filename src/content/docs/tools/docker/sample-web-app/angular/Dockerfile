FROM node:14.15.0 as node

# RUN mkdir /app
WORKDIR /app

COPY package*.json .

RUN npm install

COPY . .

# Generate the build of the application
# RUN npm run build

# EXPOSE 4200
# CMD ["ng", "serve", "--host", "0.0.0.0"]
# CMD ["npm", "start"]