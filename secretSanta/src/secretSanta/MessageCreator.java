package secretSanta;

import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;

public class MessageCreator {
	Sender send;
	People peeps;
	
	
	MessageCreator(Sender sender,People peep){
		send = sender;
		peeps = peep;
	}
	
	void sendMessages() {
		for(Person peep : peeps.people) {
			String bodyText = "<h1>" + peep.name + ", Your Secret Santa Match is " + peep.match.name;
			if(peep.match.extras != null) {
				bodyText = bodyText + "<br><br>" + peep.match.name + " wanted to tell you: " + peep.match.extras;
			}
			bodyText += "<br><br>Merry ChristmaHanuKwanzaa!" + "</h1>";
			//bodyText = readFile("html1","ANSI");
			send.sendMessage(peep.address,"Your Secret Santa Match",bodyText);
			System.out.println("Sent a message");
		}
	}
	static String readFile(String path, Charset encoding) 
			  throws IOException 
			{
			  byte[] encoded = Files.readAllBytes(Paths.get(path));
			  return new String(encoded, encoding);
			}
}

