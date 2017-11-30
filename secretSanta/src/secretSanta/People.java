package secretSanta;

import java.util.ArrayList;

public class People {
	ArrayList<Person> people = new ArrayList<Person>();

	void addPerson(String name,String address) {
		people.add(new Person(name,address));
	}
		
	void setMatch(Person matcher,Person matchee) {
		matcher.match = matchee;
		matchee.giver = matcher;
	}
}
