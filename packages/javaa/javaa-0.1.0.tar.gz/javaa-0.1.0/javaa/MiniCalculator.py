
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;

public class MiniCalculator extends JFrame implements ActionListener {
    private JTextField display;
    private JButton[] numButtons;
    private JButton[] opButtons;
    private JButton clearButton, equalsButton, backButton;
    private List<String> operations;
    private Font myFont = new Font("Times new roman", Font.BOLD, 25);

    public MiniCalculator() {
        setTitle("Calculator");
        setSize(420, 520);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());
       
        operations = new ArrayList<>();

        display = new JTextField(30);
        display.setEditable(false);
        display.setFont(new Font("Arial", Font.BOLD, 30));
        display.setHorizontalAlignment(JTextField.RIGHT);
        display.setBackground(Color.PINK);
        display.setForeground(Color.WHITE);
        display.setBorder(BorderFactory.createEmptyBorder(60, 10, 10, 30));
        add(display, BorderLayout.NORTH);

        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new GridLayout(6, 3, 5, 5));
        buttonPanel.setBackground(Color.PINK);

        numButtons = new JButton[10];
        for (int i = 9; i >= 0; i--) {
            numButtons[i] = new JButton(String.valueOf(i));
            numButtons[i].setFont(myFont);
            numButtons[i].addActionListener(this);
            buttonPanel.add(numButtons[i]);
        }

        opButtons = new JButton[5];
        String[] opSymbols = {"+", "-", "*", "/", "%"};
        for (int i = 0; i < 5; i++) {
            opButtons[i] = new JButton(opSymbols[i]);
            opButtons[i].setFont(myFont);
            opButtons[i].addActionListener(this);
            buttonPanel.add(opButtons[i]);
        }

        clearButton = new JButton("C");
        clearButton.setFont(myFont);
        clearButton.addActionListener(this);
        buttonPanel.add(clearButton);

        equalsButton = new JButton("=");
        equalsButton.setFont(myFont);
        equalsButton.addActionListener(this);
        buttonPanel.add(equalsButton);

        backButton = new JButton("<=");
        backButton.setFont(myFont);
        backButton.addActionListener(this);
        buttonPanel.add(backButton);

        add(buttonPanel, BorderLayout.CENTER);
        setVisible(true);
    }

    public void actionPerformed(ActionEvent e) {
        String command = e.getActionCommand();
        if (Character.isDigit(command.charAt(0))) {
            display.setText(display.getText() + command);
        } else if (command.equals("+") || command.equals("-") || command.equals("*") || command.equals("/")
                || command.equals("%")) {
            operations.add(display.getText());
            operations.add(command);
            display.setText("");
        } else if (command.equals("=")) {
            operations.add(display.getText());
            double result = calculateResult(operations);
            display.setText(String.valueOf(result));
            operations.clear();
        } else if (command.equals("C")) {
            display.setText("");
            operations.clear();
        } else if (command.equals("<=")) {
            String currentText = display.getText();
            if (!currentText.isEmpty()) {
                display.setText(currentText.substring(0, currentText.length() - 1));
            }
        }
    }

    private double calculateResult(List<String> operations) {
        double result = 0;
        char currentOp = '+';
        for (String item : operations) {
            if (item.equals("+") || item.equals("-") || item.equals("*") || item.equals("/") || item.equals("%")) {
                currentOp = item.charAt(0);
            } else {
                double num = Double.parseDouble(item);
                switch (currentOp) {
                    case '+':
                        result += num;
                        break;
                    case '-':
                        result -= num;
                        break;
                    case '*':
                        result *= num;
                        break;
                    case '/':
                        if (num == 0) {
                            JOptionPane.showMessageDialog(this, "Error: Division by zero");
                            return 0;
                        }
                        result /= num;
                        break;
                    case '%':
                        result %= num;
                        break;
                }
            }
        }
        return result;
    }

    public static void main(String[] args) {
        new MiniCalculator();
    }
}