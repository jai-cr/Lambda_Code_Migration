```java
package pl.software2.awsblocks.passwordlessloginservice.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import pl.software2.awsblocks.lambda.model.Route;
import pl.software2.awsblocks.lambda.routes.RouteHandler;
import pl.software2.awsblocks.lambda.routes.content.ApiGatewayResponseProducer;
import pl.software2.awsblocks.service.jwt.LoadJWTTokenSecret;

import java.io.IOException;
import java.util.Set;

@Slf4j
@RestController
@RequestMapping("/api")
public class ApiController {

    private final LoadJWTTokenSecret loadJWTTokenSecret;
    private final ObjectMapper objectMapper;
    private final ApiGatewayResponseProducer responseProducer;
    private final Set<RouteHandler> routes;

    @Autowired
    public ApiController(LoadJWTTokenSecret loadJWTTokenSecret,
                         ObjectMapper objectMapper,
                         ApiGatewayResponseProducer responseProducer,
                         Set<RouteHandler> routes) {
        this.loadJWTTokenSecret = loadJWTTokenSecret;
        this.objectMapper = objectMapper;
        this.responseProducer = responseProducer;
        this.routes = routes;
    }

    @PostMapping("/event")
    public APIGatewayV2HTTPResponse handleRequest(@RequestBody String input) throws IOException {
        var event = objectMapper.readValue(input, APIGatewayV2HTTPEvent.class);
        log.info("Received APIGatewayV2HTTPEvent: {}", event);
        loadJWTTokenSecret.loadSecret();
        return routes.stream()
                .filter(route -> route.supports(Route.fromRequest(event)))
                .findFirst()
                .map(routeHandler -> {
                    log.info("Route handler: {}", routeHandler.getClass().getSimpleName());
                    return routeHandler.handle(event);
                })
                .orElse(responseProducer.notFound(event.getRawPath()));
    }
}
```