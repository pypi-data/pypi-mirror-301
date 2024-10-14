import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class PreparedStatementCRUDExample {
    public static void main(String[] args) {
        String jdbcURL = "jdbc:mysql://localhost:3306/student";
        String username = "root";
        String password = "";

        try (Connection connection = DriverManager.getConnection(jdbcURL, username, password)) {

            String insertSQL = "INSERT INTO stud (username, password) VALUES (?, ?)";
            try (PreparedStatement preparedStatement = connection.prepareStatement(insertSQL)) {
                
                String[][] records = {
                    {"Anitha", "Anitha123"},
                    {"radha", "radha123"},
                    {"Seetha", "seetha123"},
                    {"ram", "ram123"}
                };

                for (String[] record : records) {
                    preparedStatement.setString(1, record[0]);
                    preparedStatement.setString(2, record[1]);
                    int insertResult = preparedStatement.executeUpdate();
                    System.out.println("INSERT Operation for " + record[0] + ": " + (insertResult > 0 ? "Success" : "Failed"));
                }
            }
           
            
            String selectSQL = "SELECT username, password FROM stud";
            try (PreparedStatement preparedStatement = connection.prepareStatement(selectSQL);
                 ResultSet resultSet = preparedStatement.executeQuery()) {
                System.out.println("\nSELECT Operation:");
                while (resultSet.next()) {
                    String selectedUsername = resultSet.getString("username");
                    String selectedPassword = resultSet.getString("password");
                    System.out.println("Username: " + selectedUsername + ", Password: " + selectedPassword);
                }
            }
 

          
            String updateSQL = "UPDATE stud SET password = ? WHERE username = ?";
            try (PreparedStatement preparedStatement = connection.prepareStatement(updateSQL)) {
                preparedStatement.setString(1, "radha@123");
                preparedStatement.setString(2, "radha");
                int updateResult = preparedStatement.executeUpdate();
                System.out.println("\nUPDATE Operation: " + (updateResult > 0 ? "Success" : "Failed"));
            }
            displayTable(connection);  

           
            String deleteSQL = "DELETE FROM stud WHERE username = ?";
            try (PreparedStatement preparedStatement = connection.prepareStatement(deleteSQL)) {
                preparedStatement.setString(1, "Anitha");
                int deleteResult = preparedStatement.executeUpdate();
                System.out.println("\nDELETE Operation: " + (deleteResult > 0 ? "Success" : "Failed"));
            }
            displayTable(connection);  

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

   
    private static void displayTable(Connection connection) {
        String selectSQL = "SELECT username, password FROM stud";
        try (PreparedStatement preparedStatement = connection.prepareStatement(selectSQL);
             ResultSet resultSet = preparedStatement.executeQuery()) {
            System.out.println("\nCurrent Table Status:");
            while (resultSet.next()) {
                String username = resultSet.getString("username");
                String password = resultSet.getString("password");
                System.out.println("Username: " + username + ", Password: " + password);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}