package secretSanta;
import java.util.ArrayList;
import java.util.Random;

public class Matcher {
	ArrayList<Person> unChosen;
	People peep;
	Random rand = new Random();
	
	Matcher(People peeps){
		peep = peeps;
		unChosen = new ArrayList<Person>(peep.people);
	}
	
	void match() {
		for(int i = 0;i < peep.people.size();i++) {
			while(1 == 1) {
				int matchInd = rand.nextInt(unChosen.size());
				//System.out.println(peep.people.get(i).name + ", " + unChosen.get(matchInd).name);
				if(!unChosen.get(matchInd).equals(peep.people.get(i))) {
					peep.setMatch(peep.people.get(i),unChosen.get(matchInd));
					unChosen.remove(matchInd);
					break;
				}else {
					if(unChosen.size() == 1) {
						unChosen = new ArrayList<Person>(peep.people);
						i = 0;
						System.out.println("The last person got themself, restarting");
					}else {
						System.out.println(unChosen.get(matchInd).name + " got themself");
					}
				}
			}
		}
	}
	
	void printMatches() {
		for(Person pers : peep.people) {
			System.out.println("Name: " + pers.name + ", Address: " + pers.address);
			System.out.println("Match Name: " + pers.match.name + ", Match Address: " + pers.match.address);
			System.out.println("Giver Name: " + pers.giver.name + ", Giver Address: " + pers.giver.address +
					"\n:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::");
			
		}
	}
}
