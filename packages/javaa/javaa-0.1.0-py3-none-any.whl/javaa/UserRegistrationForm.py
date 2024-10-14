import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class UserRegistrationForm extends JFrame implements ActionListener {
    JTabbedPane tabbedPane;
    JPanel personalPanel, academicPanel, finalPanel;
    JTextField firstNameField, lastNameField, ageField;
    JRadioButton maleButton, femaleButton, otherButton;
    JCheckBox javaCheckBox, pythonCheckBox, cppCheckBox;
    JComboBox<String> yearComboBox, degreeComboBox;
    JTextField collegeNameField, gpaField;
    JButton nextButton1, nextButton2, backButton, submitButton;
    JTextArea resultArea;
    ButtonGroup genderGroup;

    UserRegistrationForm() {
        setTitle("User Registration Form");
        setSize(500, 500);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        tabbedPane = new JTabbedPane();

        personalPanel = new JPanel(new GridLayout(8, 2));
        personalPanel.add(new JLabel("First Name:"));
        firstNameField = new JTextField();
        personalPanel.add(firstNameField);

        personalPanel.add(new JLabel("Last Name:"));
        lastNameField = new JTextField();
        personalPanel.add(lastNameField);

        personalPanel.add(new JLabel("Age:"));
        ageField = new JTextField();
        personalPanel.add(ageField);

        personalPanel.add(new JLabel("Gender:"));
        JPanel genderPanel = new JPanel();
        maleButton = new JRadioButton("Male");
        femaleButton = new JRadioButton("Female");
        otherButton = new JRadioButton("Other");
        genderGroup = new ButtonGroup();
        genderGroup.add(maleButton);
        genderGroup.add(femaleButton);
        genderGroup.add(otherButton);
        genderPanel.add(maleButton);
        genderPanel.add(femaleButton);
        genderPanel.add(otherButton);
        personalPanel.add(genderPanel);

        personalPanel.add(new JLabel("Skills:"));
        JPanel skillsPanel = new JPanel();
        javaCheckBox = new JCheckBox("Java");
        pythonCheckBox = new JCheckBox("Python");
        cppCheckBox = new JCheckBox("C++");
        skillsPanel.add(javaCheckBox);
        skillsPanel.add(pythonCheckBox);
        skillsPanel.add(cppCheckBox);
        personalPanel.add(skillsPanel);

        nextButton1 = new JButton("Next");
        nextButton1.addActionListener(this);
        personalPanel.add(nextButton1);

        tabbedPane.addTab("Personal Information", personalPanel);

        
        academicPanel = new JPanel(new GridLayout(6, 2));
        academicPanel.add(new JLabel("College Name:"));
        collegeNameField = new JTextField();
        academicPanel.add(collegeNameField);

        academicPanel.add(new JLabel("Degree:"));
        String[] degrees = {"BSc", "BA", "BCom", "BEng", "BTech", "MSc", "MA", "MCom", "MEng", "MTech"};
        degreeComboBox = new JComboBox<>(degrees);
        academicPanel.add(degreeComboBox);

        academicPanel.add(new JLabel("Graduation Year:"));
        String[] years = {"2019","2020","2021","2022","2023","2024"};
       
        yearComboBox = new JComboBox<>(years);
        academicPanel.add(yearComboBox);

        academicPanel.add(new JLabel("GPA:"));
        gpaField = new JTextField();
        academicPanel.add(gpaField);

        backButton = new JButton("Back");
        backButton.addActionListener(this);
        academicPanel.add(backButton);

        nextButton2 = new JButton("Next");
        nextButton2.addActionListener(this);
        academicPanel.add(nextButton2);

        tabbedPane.addTab("Academic Information", academicPanel);

        finalPanel = new JPanel(new BorderLayout());
        resultArea = new JTextArea();
        resultArea.setEditable(false);
        finalPanel.add(new JScrollPane(resultArea), BorderLayout.CENTER);

        submitButton = new JButton("Submit");
        submitButton.addActionListener(this);
        finalPanel.add(submitButton, BorderLayout.SOUTH);

        tabbedPane.addTab("Summary", finalPanel);

        add(tabbedPane);
        setVisible(true);
    }

    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == nextButton1) {
            tabbedPane.setSelectedIndex(1);
        } else if (e.getSource() == backButton) {
            tabbedPane.setSelectedIndex(0);
        } else if (e.getSource() == nextButton2) {
            tabbedPane.setSelectedIndex(2);
            displayDetails();
        } else if (e.getSource() == submitButton) {
            displayDetails();
            JOptionPane.showMessageDialog(this, "Registration Successful!");
        }
    }

    private void displayDetails() {
    StringBuilder personalInfo = new StringBuilder();
    personalInfo.append("Personal Information:\n")
            .append("First Name: ").append(firstNameField.getText()).append("\n")
            .append("Last Name: ").append(lastNameField.getText()).append("\n")
            .append("Age: ").append(ageField.getText()).append("\n")
            .append("Gender: ");
   
    if (maleButton.isSelected()) {
        personalInfo.append("Male\n");
    } else if (femaleButton.isSelected()) {
        personalInfo.append("Female\n");
    } else if (otherButton.isSelected()) {
        personalInfo.append("Other\n");
    } else {
        personalInfo.append("Not specified\n");
    }

    personalInfo.append("Skills: ");
    boolean skillsAppended = false;
    if (javaCheckBox.isSelected()) {
        personalInfo.append("Java");
        skillsAppended = true;
    }
    if (pythonCheckBox.isSelected()) {
        if (skillsAppended) {
            personalInfo.append(", ");
        }
        personalInfo.append("Python");
        skillsAppended = true;
    }
    if (cppCheckBox.isSelected()) {
        if (skillsAppended) {
            personalInfo.append(", ");
        }
        personalInfo.append("C++");
        skillsAppended = true;
    }
    personalInfo.append("\n");

    StringBuilder academicInfo = new StringBuilder();
    academicInfo.append("Academic Information:\n")
            .append("College Name: ").append(collegeNameField.getText()).append("\n")
            .append("Degree: ").append(degreeComboBox.getSelectedItem().toString()).append("\n")
            .append("Graduation Year: ").append(yearComboBox.getSelectedItem().toString()).append("\n")
            .append("GPA: ").append(gpaField.getText()).append("\n");

    resultArea.setText(personalInfo.toString() + academicInfo.toString());
}


    public static void main(String[] args) {
        new UserRegistrationForm();
    }
}
