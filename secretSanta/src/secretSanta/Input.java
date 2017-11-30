package secretSanta;
import java.util.Scanner;

public class Input {
	Scanner sc;

	public Input() {
		sc = new Scanner(System.in);
		// TODO Auto-generated constructor stub
	}
	
	String getName() {
		boolean doned = false;
		String name = null;
		while(!doned) {
			System.out.println("Enter your name: ");
			name = sc.nextLine();
			System.out.println("Is \"" + name + "\" the correct name? (y/n)");
			doned = getYN();
		}
		return name;
	}
	
	String getEmail() {
		boolean doned = false;
		String email = null;
		while(!doned) {
			System.out.println("Enter your e-mail: ");
			email = sc.nextLine();
			System.out.println("Is \"" + email + "\" the correct email? (y/n)");
			doned = getYN();
		}
		return email;
	}
	
	String getExtras() {
		System.out.println("Would you like to tell whoever is getting you a gift anything? (y/n)");
		if(!getYN()) {
			return null;
		}
		boolean doned = false;
		String extra = null;
		while(!doned) {
			System.out.println("Enter any info you would like whoever is getting you a gift to know: ");
			extra = sc.nextLine();
			System.out.println("Is \"" + extra + "\" the correct info? (y/n)");
			doned = getYN();
		}
		return extra;
	}
	
	boolean done() {
		System.out.println("Enter another name? (y/n)");
		return getYN();
	}
	
	boolean getYN() {
		String resp = sc.nextLine().toLowerCase();
		if(resp.equals("y".toString())) {
			return true;
		}
		return false;
	}

}
