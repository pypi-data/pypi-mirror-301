import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.*;
import javax.servlet.http.*;

public class SecondServlet extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        Cookie[] cookies = request.getCookies();
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if ("uname".equals(cookie.getName())) {
                    out.print("Hello, " + cookie.getValue() + "!");
                    break;
                }
            }
        } else {
            out.print("No cookies found.");
        }

        out.close();
    }
}
