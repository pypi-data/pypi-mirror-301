import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.*;
import javax.servlet.http.*;

public class FirstServlet extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        String name = request.getParameter("userName");
        out.print("Welcome, " + name + "!");

        Cookie cookie = new Cookie("uname", name);
        response.addCookie(cookie);

        out.print("<form action='servlet2' method='post'>");
        out.print("<input type='submit' value='Go'>");
        out.print("</form>");

        out.close();
    }
}
