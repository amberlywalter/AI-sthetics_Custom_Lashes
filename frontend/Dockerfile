# Stage 1: Build the Next.js app
FROM node:20-alpine AS builder

# Set working directory inside container
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy all frontend source code
COPY . .

# Build the production version of the app
RUN npm run build

# Stage 2: Run the built app with a lightweight image
FROM node:20-alpine AS runner
WORKDIR /app

# Copy only necessary build output from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./

# Expose port 3000 for Next.js
EXPOSE 3000

# Run the app
CMD ["npm", "start"]
