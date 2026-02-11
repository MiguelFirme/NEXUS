# Build
FROM maven:3.9-eclipse-temurin-17-alpine AS build
WORKDIR /app

COPY pom.xml .
RUN mvn dependency:go-offline -B

COPY src src
RUN mvn package -DskipTests -B

# Run
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

RUN adduser -D -u 1000 appuser
RUN mkdir -p uploads && chown -R appuser:appuser uploads

COPY --from=build /app/target/*.jar app.jar
USER appuser

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
