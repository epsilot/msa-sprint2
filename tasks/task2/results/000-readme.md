# task2

## Проблемы с перенаправлением запроса всех бронирований

Перенаправления запроса от монолита к соответсвующему микросервису не работает и генерирует ошибку,
при условии, что запрошен весь перечень бронирований. По этой причине тест всего списка бронирований отключён.
```shell
hotelio-monolith            | 2025-10-08T14:34:18.282Z ERROR 1 --- [nio-8080-exec-3] o.a.c.c.C.[.[.[/].[dispatcherServlet]    : Servlet.service() for servlet [dispatcherServlet] in context with path [] threw exception [Request processing failed: java.lang.NullPointerException] with root cause
hotelio-monolith            | 
hotelio-monolith            | java.lang.NullPointerException: null
hotelio-monolith            | 	at com.hotelio.proto.booking.BookingListRequest$Builder.setUserId(BookingListRequest.java:449) ~[p-o-y-1.0.0.jar!/:na]
hotelio-monolith            | 	at com.hotelio.GrpcBookingService.listAll(GrpcBookingService.java:26) ~[p-o-y-1.0.0.jar!/:na]
hotelio-monolith            | 	at com.hotelio.monolith.controller.BookingController.listBookings(BookingController.java:23) ~[!/:1.0.0]
hotelio-monolith            | 	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method) ~[na:na]
hotelio-monolith            | 	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77) ~[na:na]
hotelio-monolith            | 	at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43) ~[na:na]
hotelio-monolith            | 	at java.base/java.lang.reflect.Method.invoke(Method.java:568) ~[na:na]
hotelio-monolith            | 	at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:255) ~[spring-web-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:188) ~[spring-web-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:118) ~[spring-webmvc-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.java:926) ~[spring-webmvc-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.java:831) ~[spring-webmvc-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:87) ~[spring-webmvc-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1089) ~[spring-webmvc-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:979) ~[spring-webmvc-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1014) ~[spring-webmvc-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:903) ~[spring-webmvc-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at jakarta.servlet.http.HttpServlet.service(HttpServlet.java:564) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:885) ~[spring-webmvc-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at jakarta.servlet.http.HttpServlet.service(HttpServlet.java:658) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:206) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:150) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:51) ~[tomcat-embed-websocket-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:175) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:150) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.springframework.web.filter.RequestContextFilter.doFilterInternal(RequestContextFilter.java:100) ~[spring-web-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116) ~[spring-web-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:175) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:150) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.springframework.web.filter.FormContentFilter.doFilterInternal(FormContentFilter.java:93) ~[spring-web-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116) ~[spring-web-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:175) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:150) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:201) ~[spring-web-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116) ~[spring-web-6.1.6.jar!/:6.1.6]
hotelio-monolith            | 	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:175) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:150) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:167) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:90) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:482) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:115) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:93) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:74) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:344) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:391) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:63) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:896) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1736) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:52) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.tomcat.util.threads.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1191) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.tomcat.util.threads.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:659) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:63) ~[tomcat-embed-core-10.1.20.jar!/:na]
hotelio-monolith            | 	at java.base/java.lang.Thread.run(Thread.java:833) ~[na:na]
```


## Стратегия миграции данных

- Так как на текущем этапе точкой входа по-прежнему является монолит наиболее простым в реализации видится подход с
  полным дублированием запросов на создание бронирования в соответсвующий микросервис. Таким образом информация о новых
  бронированиях будет содержаться в базе монолита и базе микросервиса. Так как предполагается, что процесс миграции
  данных может быть завершён за разумный период времени такой подход позволит значительно минимизировать риск
  рассинхронизации данных. Также это позволит иметь полный и актуальный снимок данных о бронированиях в монолитной базе
  данных, что может быть важным в случае возникновения непредвиденных проблем в новом микросервисе, которые приведут к 
  порче данных.
- Отдельно следует продумать стратегию реагирования монолита на невозможность создать бронирование в микросервисе. Если
  будет признано, что новый микросервис достаточно стабилен для работы и серьёзных проблем на время миграции данных не
  ожидается, то в таком случае монолиту следует генерировать ошибку при невозможности создать бронирование в
  микросервисе и не генерировать (или удалять) данные о бронировании в базе монолита. Если же будут опасения в
  стабильности работы нового микросервиса, то монолит может игнорировать ошибки в создании бронирования в микросервисе,
  однако это потребует дополнительного этапа синхронизации данных после стабилизации работы микросервиса.
- Логику получения информации о бронировании на время миграции данных предлагается оставить на уровне монолита, так как
  в его базе будет содержаться полный список всех бронирований. Это позволит исключить необходимость отправки запросов в
  микросервис и последующего комбинирования данных о бронированиях из ответа микросервиса и базы монолита.
- Миграция данных из базы монолита в базу микросервиса будет производиться в асинхронном режиме через вспомогательное
  решение, которое будет читать данные из базы монолита и писать данные в базу нового микросервиса.
  