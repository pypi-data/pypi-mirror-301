
import java.sql.*;

public class CallableStatementExample {
    public static void main(String[] args) {
        String jdbcURL = "jdbc:mysql://localhost:3306/student";
        String dbUsername = "root";
        String dbPassword = "";

        try (Connection connection = DriverManager.getConnection(jdbcURL, dbUsername, dbPassword)) {
            
            String sql = "{call GetAllUserAndPassword ()}";
            try (CallableStatement callableStatement = connection.prepareCall(sql)) {
               
                ResultSet resultSet = callableStatement.executeQuery();
                
                
                System.out.println("Username\tPassword");
                while (resultSet.next()) {
                    String username = resultSet.getString("username");
                    String password = resultSet.getString("password");
                    System.out.println(username + "\t" + password);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}