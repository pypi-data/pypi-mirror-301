package com.example;

import java.sql.*;
import java.io.*;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/MyServlet")
public class MyServlet extends HttpServlet{
	private static final long serailVersionUID = 1;
	
	protected void doPost(HttpServletRequest request,HttpServletResponse response)throws ServletException{
		int id = Integer.parseInt(request.getParameter("id"));
		String username = request.getParameter("username");
		String email = request.getParameter("email");

		Connection conn = null;
		PreparedStatement stmt= null;

		response.setContentType("text/html");
		try{
			Class.forName("com.mysql.cj.jdbc.Driver");
			conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/mydb","root","");
			String sql = "INSERT INTO servlet VALUES(?,?,?)";
			stmt = conn.prepareStatement(sql);
			stmt.setInt(1,id);
			stmt.setString(2,username);
			stmt.setString(3,email);
			int i = stmt.executeUpdate();
			PrintWriter out = response.getWriter();
			out.println("<html><body>");
			if(i>0){
				out.println("<h2>Data inserted in db successfully</h2>");
			}
			out.println("<h2>Form Data Submitted Successfully</h2>");
			out.println("<p>Id: "+id+"</p>");
			out.println("<p>Name: "+username+"</p>");
			out.println("<p>Email: "+email+"</p>");
			out.println("</body></html>");
			stmt.close();
			conn.close();
		}catch(Exception e){
			e.printStackTrace();
		}
		finally{
				
		}
	}
}