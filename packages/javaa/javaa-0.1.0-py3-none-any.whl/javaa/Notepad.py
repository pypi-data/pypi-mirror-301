import javax.swing.*;
import java.awt.*;
import java.io.*;

public class Notepad extends JFrame {
    private JTextArea textArea;
    private JFileChooser fileChooser;
    private File currentFile;

    public Notepad() {

        setTitle("Notepad");
        setSize(600, 400);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(EXIT_ON_CLOSE);


        textArea = new JTextArea();
        textArea.setLineWrap(true);
        textArea.setWrapStyleWord(true);
        JScrollPane scrollPane = new JScrollPane(textArea);
        add(scrollPane, BorderLayout.CENTER);


        fileChooser = new JFileChooser();


        JMenuBar menuBar = new JMenuBar();
        setJMenuBar(menuBar);


        JMenu fileMenu = new JMenu("File");
        menuBar.add(fileMenu);


        JMenuItem newItem = new JMenuItem("New");
        newItem.addActionListener(e -> newFile());
        fileMenu.add(newItem);


        JMenuItem openItem = new JMenuItem("Open");
        openItem.addActionListener(e -> openFile());
        fileMenu.add(openItem);


        JMenuItem saveItem = new JMenuItem("Save");
        saveItem.addActionListener(e -> saveFile());
        fileMenu.add(saveItem);


        JMenuItem saveAsItem = new JMenuItem("Save As");
        saveAsItem.addActionListener(e -> saveAsFile());
        fileMenu.add(saveAsItem);
        fileMenu.addSeparator();


        JMenuItem exitItem = new JMenuItem("Exit");
        exitItem.addActionListener(e -> exit());
        fileMenu.add(exitItem);


        JMenu editMenu = new JMenu("Edit");
        menuBar.add(editMenu);


        JMenuItem cutItem = new JMenuItem("Cut");
        cutItem.addActionListener(e -> textArea.cut());
        editMenu.add(cutItem);


        JMenuItem copyItem = new JMenuItem("Copy");
        copyItem.addActionListener(e -> textArea.copy());
        editMenu.add(copyItem);


        JMenuItem pasteItem = new JMenuItem("Paste");
        pasteItem.addActionListener(e -> textArea.paste());
        editMenu.add(pasteItem);
        editMenu.addSeparator();


        JMenuItem findItem = new JMenuItem("Find");
        findItem.addActionListener(e -> findText());
        editMenu.add(findItem);
    }


    private void newFile() {
        int option = JOptionPane.showConfirmDialog(this,
            "Are you sure you want to create a new file? Unsaved changes will be lost.",
            "New File", JOptionPane.YES_NO_OPTION);
        if (option == JOptionPane.YES_OPTION) {
            textArea.setText("");
            currentFile = null;
        }
    }


    private void openFile() {
        int result = fileChooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            File file = fileChooser.getSelectedFile();
            try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                textArea.read(reader, null);
                currentFile = file;
            } catch (IOException e) {
                JOptionPane.showMessageDialog(this,
                    "Could not open file.",
                    "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }


    private void saveFile() {
        if (currentFile == null) {
            saveAsFile();
        } else {
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(currentFile))) {
                textArea.write(writer);
            } catch (IOException e) {
                JOptionPane.showMessageDialog(this,
                    "Could not save file.",
                    "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }


    private void saveAsFile() {
        int result = fileChooser.showSaveDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            currentFile = fileChooser.getSelectedFile();
            saveFile();
        }
    }


    private void findText() {
        String searchTerm = JOptionPane.showInputDialog(this, "Enter text to find:");
        if (searchTerm != null && !searchTerm.isEmpty()) {
            String content = textArea.getText();
            int index = content.indexOf(searchTerm);
            if (index != -1) {
                textArea.setCaretPosition(index);
                textArea.select(index, index + searchTerm.length());
                textArea.requestFocus();
            } else {
                JOptionPane.showMessageDialog(this,
                    "Text not found.",
                    "Find", JOptionPane.INFORMATION_MESSAGE);
            }
        }
    }


    private void exit() {
        int option = JOptionPane.showConfirmDialog(this,
            "Are you sure you want to exit? Unsaved changes will be lost.",
            "Exit", JOptionPane.YES_NO_OPTION);
        if (option == JOptionPane.YES_OPTION) {
            System.exit(0);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Notepad().setVisible(true));
    }
}