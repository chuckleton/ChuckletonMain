package secretSanta;

import java.util.ArrayList;

public class SecretSanta {
	
	static Sender sender;
	static People peeps;
	static Matcher match;
	static MessageCreator creator;
	static Input in;

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("Setting up Session");
		sender = new Sender();
		peeps = new People();
		in = new Input();
		boolean finished = false;
		while(!finished) {
			/*boolean done = true;
			while(done) {
				String name = in.getName();
				String email = in.getEmail();
				String extra = in.getExtras();
				peeps.addPerson(name, email);
				peeps.people.get(peeps.people.size() - 1).setExtra(extra);
				done = in.done();
			}*/
			peeps.addPerson("Dits/Gwent",		"adityasadhu15@gmail.com");
			peeps.addPerson("Jacob Pokryska",	"jacobpokryska@gmail.com");
			peeps.addPerson("Bryce",			"bryceknagy@gmail.com");
			peeps.addPerson("Josh Alpern",		"jpern1211@gmail.com");
			peeps.addPerson("Danny",			"dkolano2@gmail.com");
			peeps.addPerson("Jack Downey",		"jpidwaffle@gmail.com");
			peeps.addPerson("Evan Giordano",	"evangiordano8@gmail.com");
			peeps.addPerson("Isaac Pokryska",	"isaacpokryska@gmail.com");
			peeps.addPerson("Dyl",				"dylanmarkulec@gmail.com");
		
			for(Person person : peeps.people) {
				person.printPerson();
			}
		
			System.out.println("Are these the right people and emails? (y/n)");
			finished = in.getYN();
			if(!finished) {
				peeps.people = new ArrayList<Person>();
			}
		}
		
		match = new Matcher(peeps);
		
		match.match();
		//match.printMatches();
		
		creator = new MessageCreator(sender,peeps);
		
		creator.sendMessages();
		//System.out.println("Sending Message");
		//sender.sendMessage("dkolano2@gmail.com","LOKER","Suker");
		System.out.println("Messages sent");
	}

}
