import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ConversionProgramSwing extends JFrame implements ItemListener, ActionListener {
	private JComboBox<String>conversionChoice,choice2;
	private JTextField inputField,resultField;
	private JButton convertButton;

	public ConversionProgramSwing() {
		setLayout(new FlowLayout());
		conversionChoice = new JComboBox<>();
		conversionChoice.addItem("Select Conversion");
		conversionChoice.addItem("Kilometers");
		conversionChoice.addItem("Kilograms");
		conversionChoice.addItem("Celsius");
		conversionChoice.addItem("Feet");
		conversionChoice.addItem("Liters");
		add(conversionChoice);

		choice2 = new JComboBox<>();
		add(choice2);

		inputField = new JTextField(10);
		add(inputField);

		convertButton = new JButton("Convert");
		add(convertButton);

		resultField = new JTextField(20);
		resultField.setEditable(false);
		add(resultField);

		conversionChoice.addItemListener(this);
		convertButton.addActionListener(this);

		setTitle("Metric Conversion");
		setSize(600,600);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setVisible(true);

	}
	public void itemStateChanged(ItemEvent ie){
		resultField.setText("");
		inputField.setText("");
		if(ie.getSource() == conversionChoice){
			String sitem = (String) conversionChoice.getSelectedItem();
			choice2.removeAllItems();
			if(sitem.equals("Kilometers")){
				choice2.addItem("Meter");
				choice2.addItem("Centimeter");
				choice2.addItem("Miles");
			}
			if(sitem.equals("Kilograms")){
				choice2.addItem("Grams");
			}
			if(sitem.equals("Celsius")){
				choice2.addItem("Fahrenheit");

			}
			if(sitem.equals("Feet")){
				choice2.addItem("Inches");
			}
			if(sitem.equals("Liters")){
				choice2.addItem("Milliliters");
			}
		}
	}
	public void actionPerformed(ActionEvent ae){
		try{
			String s1 = (String) conversionChoice.getSelectedItem();
			String s2 = (String) choice2.getSelectedItem();
			double inputValue = Double.parseDouble(inputField.getText());
			double result = 0;

			 if (s1 != null && s2 != null && s1.length() != 0 && s2.length() != 0) {
                if (s1.equals("Kilometers") && s2.equals("Meter")) {
                    result = inputValue * 1000;

					
			}
			if(s1.equals("Kilometers") && s2.equals("Centimeter")){
				result = inputValue * 100000;
			}
			if(s1.equals("Kilograms") && s2.equals("Grams")){
				result = inputValue * 1000;
			}
			if(s1.equals("Celsius") && s2.equals("Fahrenheit")){
				result = (inputValue * 9/5) + 32;
			}
			if(s1.equals("Kilometers") && s2.equals("Miles")){
				result = inputValue * 0.621371;
			}
			if(s1.equals("Feet") && s2.equals("Inches")){
				result = inputValue * 12;
			}
			if(s1.equals("Liters") && s2.equals("Milliliters")){
				result = inputValue * 1000;
			}
		} else {
			resultField.setText("Please select a valid Conversion");
			return;
		}
		resultField.setText(String.valueOf(result));
	} catch (NumberFormatException e){
		resultField.setText("Invalid input");
	}
}
public static void main(String[] args){
	new ConversionProgramSwing();
}
}