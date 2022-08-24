FROM cypress/included:10.6.0
COPY ./Townstreet /e2e
WORKDIR /e2e
RUN npm install -g cypress-file-upload
# dependencies will be installed only if the package files change
RUN npm link cypress-file-upload
