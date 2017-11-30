package secretSanta;

import java.awt.Image;

import javax.swing.ImageIcon;

public class Person {
	String name = null;
	String address = null;
	String extras = null;
	Person match = null;
	Person giver = null;
	Image pic = null;
	
	Person(String newName,String newAddress){
		name = newName;
		address = newAddress;
	}
	
	void setImage(String path) {
		pic = new ImageIcon(path).getImage();
	}
	
	void setExtra(String ex) {
		extras = ex;
	}
	
	void printPerson() {
		System.out.print("Name: " + name + "\n Email: " + address + "\n Extras: " + extras);
		if(match != null) {
			System.out.println("\n Match: " + match.name + "\n Giver: " + giver.name);
		}
		System.out.println("\n***************************************************************\n");
	}
}
