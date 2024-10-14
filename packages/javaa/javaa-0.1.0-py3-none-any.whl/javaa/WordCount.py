import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class WordCount extends JFrame implements ActionListener
{
  JTextArea ta;
    JButton b1, b2;
JLabel l1;

    WordCount()
{
l1=new JLabel("WORDCOUNT");
l1.setBounds(170,10,100,50);
l1.setForeground(Color.RED);
            ta = new JTextArea();
        ta.setBounds(50, 50, 300, 200);

        b1 = new JButton("WORD");
        b1.setBounds(50, 300, 100, 30);

        b2 = new JButton("CHARACTER");
        b2.setBounds(180, 300, 100, 30);


        b1.addActionListener(this);
        b2.addActionListener(this);

        getContentPane().setBackground(Color.GREEN);

        add(b1);
        add(b2);
        add(ta);
add(l1);
        setSize(400, 400);
setTitle("WORDCOUNT");
        setLayout(null);
        setVisible(true);
    }
public void actionPerformed(ActionEvent e)
{
    String text = ta.getText().trim();

    if (e.getSource() == b1)
{
        if (text.isEmpty())
{
            JOptionPane.showMessageDialog(this, "Total Words: 0");
            return;
        }

       
        String[] words = text.split("\\s+");
        int count = words.length;
        JOptionPane.showMessageDialog(this, "Total Words: " + count, "Word Count", JOptionPane.INFORMATION_MESSAGE);
 
    }

    if (e.getSource() == b2)
{
        JOptionPane.showMessageDialog(this, "Total Characters with space: " + text.length(), "Character Count", JOptionPane.INFORMATION_MESSAGE);
    }
}


    public static void main(String[] args)
  {
        new WordCount();
    }
}
