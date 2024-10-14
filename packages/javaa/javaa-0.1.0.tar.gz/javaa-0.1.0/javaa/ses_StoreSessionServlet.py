import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import javax.servlet.annotation.*;

@WebServlet("/storeSession")
public class StoreSessionServlet extends HttpServlet {
 protected void doPost(HttpServletRequest request, HttpServletResponse response)
throws ServletException, IOException {
 String username = request.getParameter("username");
 String age = request.getParameter("age");
 HttpSession session = request.getSession();
 session.setAttribute("username", username);
 session.setAttribute("age", age);
 response.setContentType("text/html");
 PrintWriter out = response.getWriter();
 out.println("<html><body>");
 out.println("<h2>Session data stored</h2>");
 out.println("<a href='retrieveSession'>Go to Next Page</a>");
 out.println("</body></html>");
 }
}