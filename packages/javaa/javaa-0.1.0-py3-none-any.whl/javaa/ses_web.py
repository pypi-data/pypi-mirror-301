<?xml version="1.0" encoding="UTF-8"?>
<!--
  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                      http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
  version="3.1"
  metadata-complete="true">
 <servlet>
 <servlet-name>StoreSession</servlet-name>
 <servlet-class>StoreSessionServlet</servlet-class>
 </servlet>
 <servlet-mapping>
 <servlet-name>StoreSession</servlet-name>
 <url-pattern>/storeSession</url-pattern>
 </servlet-mapping>
 <servlet>
 <servlet-name>RetrieveSession</servlet-name>
 <servlet-class>RetrieveSessionServlet</servlet-class>
 </servlet>
 <servlet-mapping>
 <servlet-name>RetrieveSession</servlet-name>
 <url-pattern>/retrieveSession</url-pattern>
 </servlet-mapping>
 <servlet>
 <servlet-name>DeleteSession</servlet-name>
 <servlet-class>DeleteSessionServlet</servlet-class>
 </servlet>
 <servlet-mapping>
 <servlet-name>DeleteSession</servlet-name>
 <url-pattern>/deleteSession</url-pattern>
 </servlet-mapping>
</web-app>