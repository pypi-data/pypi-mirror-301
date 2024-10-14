import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
public class RetrieveSessionServlet extends HttpServlet {
 protected void doGet(HttpServletRequest request, HttpServletResponse response)
throws ServletException, IOException {
 response.setContentType("text/html");
 PrintWriter out = response.getWriter();
 HttpSession session = request.getSession(false);
 if (session != null && session.getAttribute("username") != null &&
session.getAttribute("age") != null) {
 String username = (String) session.getAttribute("username");
 String age = (String) session.getAttribute("age");
 out.println("<html><body><center>");
 out.println("<h2>Session Data:</h2>");
 out.println("Name: " + username + "<br>");
 out.println("Age: " + age + "<br>");
 out.println("<form action='deleteSession' method='post'>");
 out.println("<input type='submit' value='Delete Session'>");
 out.println("</form>");
 out.println("</body></html>");
 } else {
 response.sendRedirect("index.html");
 }
 }
}
