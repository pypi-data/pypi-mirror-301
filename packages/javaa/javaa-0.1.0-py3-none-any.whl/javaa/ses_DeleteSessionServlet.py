import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
public class DeleteSessionServlet extends HttpServlet {
 protected void doPost(HttpServletRequest request, HttpServletResponse response)
throws ServletException, IOException {
 HttpSession session = request.getSession(false);
 if (session != null) {
 session.invalidate();
 }
 response.setContentType("text/html");
 PrintWriter out = response.getWriter();
 out.println("<html><body>");
 out.println("<h2>Session deleted successfully.</h2>");
 out.println("<a href='index.html'>Go back to form</a>");
 out.println("</body></html>");
 }
}