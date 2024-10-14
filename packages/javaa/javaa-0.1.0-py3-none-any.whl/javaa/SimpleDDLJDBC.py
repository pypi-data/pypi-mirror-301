import java.sql.*;
import java.util.Scanner;

public class SimpleDDLJDBC {
    private static final String DB_URL = "jdbc:mysql://localhost:3306/kabil";
    private static final String USER = "root";
    private static final String PASS = "";

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Connection conn = null;
        Statement stmt = null;

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            conn = DriverManager.getConnection(DB_URL, USER, PASS);
            stmt = conn.createStatement();

            while (true) {
                System.out.println("\n1. Create Table");
                System.out.println("2. Alter Table");
                System.out.println("3. Rename Table");
                System.out.println("4. Drop Table");
                System.out.println("5. Retrieve Data");
                System.out.println("6. Exit");
                System.out.print("Choose an option: ");
                int option = scanner.nextInt();
                scanner.nextLine();

                switch (option) {
                    case 1:
                        createTable(stmt, scanner);
                        break;
                    case 2:
                        alterTable(stmt, scanner);
                        break;
                    case 3:
                        renameTable(stmt, scanner);
                        break;
                    case 4:
                        dropTable(stmt, scanner);
                        break;
                    case 5:
                        retrieveData(stmt);
                        break;
                    case 6:
                        System.out.println("Exiting...");
                        return;
                    default:
                        System.out.println("Invalid option. Please choose a valid option.");
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }     }


    private static void createTable(Statement stmt, Scanner scanner) throws SQLException {
        System.out.print("Enter table name: ");
        String tableName = scanner.nextLine();
        System.out.print("Enter column names and types (e.g., id INT, name VARCHAR(50)): ");
        String columns = scanner.nextLine();
        String createTableSQL = "CREATE TABLE " + tableName + " (" + columns + ")";
        
        stmt.executeUpdate(createTableSQL);
        System.out.println("Table '" + tableName + "' created successfully...");
    }


    private static void alterTable(Statement stmt, Scanner scanner) throws SQLException {
        System.out.print("Enter table name: ");
        String tableName = scanner.nextLine();

        System.out.println("1. Add column");
        System.out.println("2. Modify column");
        System.out.println("3. Drop column");
        System.out.print("Choose an option: ");
        int option = scanner.nextInt();
        scanner.nextLine();

        switch (option) {
            case 1:
                System.out.print("Enter new column name: ");
                String columnName = scanner.nextLine();
                System.out.print("Enter column type (e.g., VARCHAR(50)): ");
                String columnType = scanner.nextLine();
                stmt.executeUpdate("ALTER TABLE " + tableName + " ADD " + columnName + " " + columnType);
                System.out.println("Column added successfully.");
                break;
            case 2:
                System.out.print("Enter column name to modify: ");
                String modifyColumn = scanner.nextLine();
                System.out.print("Enter new type (e.g., VARCHAR(100)): ");
                String modifyType = scanner.nextLine();
                stmt.executeUpdate("ALTER TABLE " + tableName + " MODIFY " + modifyColumn + " " + modifyType);
                System.out.println("Column modified successfully.");
                break;
            case 3:
                System.out.print("Enter column name to drop: ");
                String dropColumn = scanner.nextLine();
                stmt.executeUpdate("ALTER TABLE " + tableName + " DROP COLUMN " + dropColumn);
                System.out.println("Column dropped successfully.");
                break;
            default:
                System.out.println("Invalid option.");
                break;
        }
    }


    private static void renameTable(Statement stmt, Scanner scanner) throws SQLException {
        System.out.print("Enter the current table name: ");
        String currentTableName = scanner.nextLine();
        System.out.print("Enter the new table name: ");
        String newTableName = scanner.nextLine();
        stmt.executeUpdate("RENAME TABLE " + currentTableName + " TO " + newTableName);
        System.out.println("Table renamed successfully.");
    }


    private static void dropTable(Statement stmt, Scanner scanner) throws SQLException {
        System.out.print("Enter table name to drop: ");
        String tableName = scanner.nextLine();
        stmt.executeUpdate("DROP TABLE " + tableName);
        System.out.println("Table dropped successfully.");
    }


    private static void retrieveData(Statement stmt) throws SQLException {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter table name to retrieve data from: ");
        String tableName = scanner.nextLine();
        String selectSQL = "SELECT * FROM " + tableName;

        ResultSet rs = stmt.executeQuery(selectSQL);
        ResultSetMetaData rsmd = rs.getMetaData();
        int columnCount = rsmd.getColumnCount();


        for (int i = 1; i <= columnCount; i++) {
            System.out.print(rsmd.getColumnName(i) + "\t");
        }
        System.out.println("\n------------------------------------------");


        while (rs.next()) {
            for (int i = 1; i <= columnCount; i++) {
                System.out.print(rs.getString(i) + "\t");
            }
            System.out.println();
        }
        rs.close();
    }
}
